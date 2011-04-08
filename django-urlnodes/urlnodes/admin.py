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


from django.contrib import admin
from django import forms
from django.utils.translation import ugettext as _
from django.conf import settings
from django.forms.util import ValidationError
from urlnodes.models import URLNode

class URLNodeAdminForm(forms.ModelForm):
    class Meta:
        model = URLNode
    # urlconf = forms.ChoiceField(choices=TargetURLconfChoices(), required=False)
    
    def validate_unique(self):
        """Workaround the bug in validate_unique that does not allow column pairs that
        are unique both to be NULL.
        
        """
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            super(URLNodeAdminForm, self).validate_unique()
        except ValidationError, e:
            # XXX: This hack workaround can break stuff when the bug is fixed.
            # If there's just one error message and content_type and object_id are both None,
            # this this problably the bug we're trying to workaround
            if len(e.messages) == 1 and content_type is None and object_id is None:
                self.cleaned_data['content_type'] = content_type
                self.cleaned_data['object_id'] = object_id
            else:
                raise

class URLNodeAdmin(admin.ModelAdmin):
    list_display = ('path', 'title', 'node_type', 'target', )
    exclude = ['cached_path', 'cached_path_len', ]
    
    form = URLNodeAdminForm

admin.site.register(URLNode, URLNodeAdmin)
