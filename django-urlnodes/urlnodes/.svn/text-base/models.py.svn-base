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


from logging import debug

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch, clear_url_caches
from django.utils import simplejson


class URLNodeManager(models.Manager):
    def get_matching_for_path(self, path):
        from django.db import connection, backend
        cursor = connection.cursor()
        query = 'SELECT n.id FROM urlnodes_urlnode n ' \
                'WHERE (n.urlconf != \'\' AND %s LIKE (n.cached_path || \'%%\')) ' \
                'OR (n.urlconf = \'\' AND n.cached_path = %s) ' \
                'ORDER BY cached_path_len DESC LIMIT 1'
        cursor.execute(query, (path, path))
        rows = cursor.fetchall()
        if rows:
            node_id = rows[0][0]
        else:
            return None
        return self.enabled().get(id=node_id)
    
    def enabled(self):
        return self.get_query_set().filter(enabled=True)
    
    def for_content(self, content_obj):
        content_type = ContentType.objects.get_for_model(content_obj)
        return self.get_query_set().get(content_type=content_type, object_id=content_obj.pk)

class URLconfChoices():
    def __init__(self):
        self._i = 0
        self._urlconf_modules = []
        for app in settings.INSTALLED_APPS:
            urlconf_module_name = '%s.urls' % app
            try:
                __import__(urlconf_module_name, {}, {}, [''])
            except ImportError:
                pass
            else:
                self._urlconf_modules.append(urlconf_module_name)
    
    def next(self):
        if self._i + 1 > len(self._urlconf_modules):
            # self.__init__()
            raise StopIteration
        else:
            urlconf_module_name = self._urlconf_modules[self._i]
            self._i += 1
            if urlconf_module_name is None:
                return (None, '')
            else:
                return (urlconf_module_name, urlconf_module_name)
    
    def __getitem__(self, i):
        return self._urlconf_modules[i]
    
    def __iter__(self):
        return self


class URLNode(models.Model):
    """
    >>> root_node = URLNode(slug='en')
    >>> child_node = URLNode(slug='contact', parent=root_node)
    >>> child_node.get_absolute_url()
    'en/contact/'
    """
    
    slug = models.SlugField(_('slug'))
    name = models.CharField(_('name'), max_length=30, unique=True, blank=True, null=True)
    title = models.CharField(_('title'), max_length=100, blank=True)
    
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    order = models.PositiveSmallIntegerField(_('order'))
    
    enabled = models.BooleanField(_('enabled'), default=True)
    
    urlconf = models.CharField(_('URLconf module name'), max_length=100, blank=True, choices=URLconfChoices(),
        help_text=_('The name of the URLconf module that contains the URL patterns for this node'))
    
    object_id = models.IntegerField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    content = generic.GenericForeignKey()
    
    view = models.CharField(_('view'), max_length=100, blank=True,
        help_text=_('The Django view to map to this node'))
    url_name = models.CharField(_('URL name'), max_length=50, blank=True,
        help_text=_('The name of the URL pattern'))
    serialized_kwargs = models.CharField(_('kwargs'), max_length=255, blank=True,
        help_text=_('Keyword arguments to pass to the view in JSON format'))
    
    cached_path = models.CharField(_('cached path'), max_length=255, blank=True, default='')
    cached_path_len = models.PositiveSmallIntegerField(_('cached path length'), null=True)
    
    objects = URLNodeManager()
    
    class Meta:
        verbose_name = _('URL node')
        verbose_name_plural = _('URL nodes')
        
        ordering = ('cached_path', )
        unique_together = (
            ('parent', 'order'),
            ('object_id', 'content_type'),)
    
    def get_child_content(self, content_type):
        return self.get_descendant_content(content_type, children_only=True)
    
    def get_descendant_content(self, content_type, children_only=False):
        if not isinstance(content_type, ContentType):
            # Assume it's a string or unicode
            try:
                app_label, model_name = content_type.split('.')
            except ValueError:
                raise AttributeError, 'Invalid content type name format, must be app_label.model_name'
            content_type = ContentType.objects.get(app_label=app_label, model=model_name)
        
        if self.is_leaf_node():
            return content_type.model_class().objects.none()
        
        model = content_type.model_class()
        
        # Get all the child nodes of the given node for the given content type,
        # then select all objects of that content type whose ID is in the object_id
        # list of these nodes. (This will be a single SQL query.)
        if children_only:
            nodes = self.get_children()
        else:
            nodes = self.get_descendants()
        nodes = nodes.filter(content_type=content_type)
        object_ids = nodes.values('object_id').query
        return model.objects.filter(pk__in=object_ids)
    
    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return unicode(self.path)
    
    def save(self, **kwargs):
        if self.name == '':
            self.name = None
        if self.order is None:
            self.order = 1
        
        path = self._get_path()
        if self.cached_path != path:
            self.cached_path = path
            self.cached_path_len = len(path)
        
        super(URLNode, self).save(**kwargs)
        
        self._clear_url_caches()
    
    def delete(self):
        super(URLNode, self).delete()
        self._clear_url_caches()
    
    def _clear_url_caches(self):
        from urlnodes.urls import URLNodesURLResolver
        for ct_resolver in URLNodesURLResolver._resolvers:
            ct_resolver._clear_cache()
        clear_url_caches()
    
    def _get_path(self):
        if self.parent:
            return '%s/%s' % (self.parent.path, self.slug)
        else:
            return self.slug
    
    path = property(lambda self: self.cached_path)
    
    def _get_kwargs(self):
        kwargs = {'node': self}
        if self.serialized_kwargs.strip() != '':
            stored_kwargs = simplejson.loads(self.serialized_kwargs)
            kwargs.update(stored_kwargs)
        return kwargs
    def _set_kwargs(self, kwargs):
        self.serialized_kwargs = simplejson.dumps(kwargs)
    kwargs = property(_get_kwargs, _set_kwargs)
    
    def get_absolute_url(self):
        """An abstract node must have a title and URL"""
        try:
            # from urlnodes.urls import URLNodesURLResolver
            # URLNodesURLResolver._resolvers[0].regex
            return reverse('urlnodes_url', kwargs={'path': self.path + '/'})
        except NoReverseMatch:
            return '/%s/' % self.path
    
    def get_name(self):
        return self.name or ''
    get_name.short_description = _('name')
    
    def _node_type(self):
        if self.urlconf:
            return 'urlconf'
        elif self.content:
            return 'content'
        elif self.view:
            return 'view'
        else:
            return 'container'
    node_type = property(_node_type)
    
    def _target(self):
        if self.urlconf:
            return self.urlconf
        elif self.content:
            return '%s (%s.%s)' % (self.content, self.content._meta.app_label, self.content._meta.module_name)
        elif self.view:
            if self.serialized_kwargs.strip():
                return '%s with kwargs %s' % (self.view, self.serialized_kwargs or '{}')
            else:
                return self.view
        else:
            return ''
    target = property(_target)

import mptt
mptt.register(URLNode, order_insertion_by=['order'])

# XXX: Monkeypatch because django-mptt does not respect order_insertion_by
URLNode.old_get_children = URLNode.get_children
def get_children(self):
    # XXX: Need to do this because django-mptt does not respect order_insertion_by
    return self.old_get_children().order_by('order')
URLNode.get_children = get_children
