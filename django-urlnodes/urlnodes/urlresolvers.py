# Copyright (c) 2008 Erik Allik
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


import re

from django.conf.urls.defaults import *
from django.core.urlresolvers import RegexURLResolver, resolve, clear_url_caches
from django.conf import settings

from urlnodes.models import URLNode
from urlnodes import get_overridden_url

class URLNodesURLConf:
    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns


class URLNodesURLResolver(RegexURLResolver):
    @classmethod
    def _register(cls, resolver):
        if not hasattr(cls, '_resolvers'):
            cls._resolvers = []
        cls._resolvers.append(resolver)
        return resolver
    
    def __init__(self, regex, default_kwargs=None):
        super(URLNodesURLResolver, self).__init__(
            regex, urlconf_name='<dynamic>', default_kwargs=default_kwargs)
        URLNodesURLResolver._register(self)
    
    def _clear_cache(self):
        if hasattr(self, '_urlconf_module'):
            del self._urlconf_module
        self._reverse_dict = {}
    
    def _get_urlconf_module(self):
        """Builds a urlpatterns array using dynamic URLconf information retrieved from the databse.
        
        This method uses a trick to enable overriding of URLs for model objects. The trick is as follows:
        
        (Django needs to be patched so that any get_absolute_url overrides defined by the 
        ABSOLUTE_URL_OVERRIDES settings will result in the original get_absolute_url method being aliased
        as old_get_absolute_url so we can still call the original one.)
        
        For any model object (content) assigned to a URLNode, we compute the URLconf module name for the app
        that this model belongs to. We then temporarily override the ROOT_URLCONF setting, clear the URL
        caches so the ROOT_URLCONF override can take effect. We then retrieve the original get_absolute_url
        for the model object (we're not interested in the URL itself but the view it resolves to)
        and resolve it to a (view, args, kwargs) tuple that we store in our generated urlpatterns array.
        Finally we restore the ROOT_URLCONF setting to its original value (for each content node).
        
        """
        if not hasattr(self, '_urlconf_module'):
            original_root_urlconf = settings.ROOT_URLCONF
            pats = []
            for node in URLNode.objects.enabled():
                if node.urlconf:
                    pats.append((r'^%s/' % node.path, include(node.urlconf)))
                elif node.view:
                    url_kwargs = {}
                    if node.url_name:
                        url_kwargs['name'] = node.url_name
                    pats.append(url(r'^%s/$' % node.path, node.view, kwargs=node.kwargs, **url_kwargs))
                elif node.content:
                    # XXX: This is the greatest of all hacks.
                    # We swap out the ROOT_URLCONF setting to the URLconf of the app that
                    # the model object belongs to, then get the URL of the object, resolve that
                    # and store the results in our dynamically generated URLconf.
                    # We cannot simply call get_absolute_url without doing the swapping
                    # because that would result in an infinite loop: get_absolute_url
                    # would call reverse which would eventually call this method again because
                    # nothing has been cached yet (before this method completes execution).
                    # Have to test performance just in case, but shouldn't be anything terrible.
                    settings.ROOT_URLCONF = '%s.urls' % node.content._meta.app_label
                    clear_url_caches()
                    
                    content = node.content
                    # If ABSOLUTE_URL_OVERRIDES is in effect and the overridden function is the one
                    # provided by the urlnodes app, use the original get_absolute_url instead.
                    model_name = '%s.%s' % (content._meta.app_label, content._meta.module_name)
                    override = settings.ABSOLUTE_URL_OVERRIDES.get(model_name, None)
                    if override is not None and override == get_overridden_url:
                        content_url = content.old_get_absolute_url()
                    else:
                        content_url = content.get_absolute_url()
                    view, args, kwargs = resolve(content_url)
                    
                    # We need to do this EACH time we oveerride ROOT_URLCONF, otherwise things
                    # break (investigate why?).
                    settings.ROOT_URLCONF = original_root_urlconf
                    clear_url_caches()
                    
                    if kwargs:
                        pats.append(url(r'^%s/$' % node.path, view, kwargs))
                    else:
                        pats.append(url(r'^%s/$' % node.path, view, args))
            
            # We create a named pattern so that URLNode.get_absolute_url can call reverse('urlnodes_url')
            # to find the proper prefix to use. We override the pattern's resolve method to always return
            # None so this pattern never actually matches any URLs because otherwise it would match anything.
            ct_root = url(r'^(?P<path>.*)$', lambda: None, name='urlnodes_url')
            ct_root.resolve = lambda path: None
            pats.append(ct_root)
            
            self._urlconf_module = URLNodesURLConf(patterns('', *pats))
        return self._urlconf_module
    urlconf_module = property(_get_urlconf_module)
