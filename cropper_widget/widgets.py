# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.forms.utils import flatatt
from django.forms.widgets import *
from django.utils.html import mark_safe, conditional_escape


class ClearableImageInput(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: <img %(img_attrs)s src="%(initial_url)s"><br>'
        '%(clear_template)s<br>%(input_text)s: %(input)s'
    )

    def __init__(self, attrs=None, img_attrs=None):
        super(ClearableImageInput, self).__init__(attrs)
        if img_attrs:
            self.img_attrs = img_attrs.copy()
        else:
            self.img_attrs = {}

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            substitutions['img_attrs'] = flatatt(self.img_attrs)
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)


class ClearableImagePreviewInput(ClearableFileInput):
    class Media:
        js = ('js/image_input_preview.js',)

    template_with_initial = (
        '%(initial_text)s: <img %(img_attrs)s src="%(initial_url)s"><br>'
        '%(clear_template)s<br>%(input_text)s: %(input)s'
        '<img id="%(preview_id)s" src="" %(preview_attrs)s>'
    )

    def __init__(self, attrs=None, img_attrs={}, img_class='form-img-initial', preview_attrs={},
                 preview_class='form-img-preview'):
        super(ClearableImagePreviewInput, self).__init__(attrs)
        self.img_attrs = {'class': img_class}
        self.img_attrs.update(img_attrs)
        self.preview_attrs = {'class': preview_class}
        self.preview_attrs.update(preview_attrs)

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s<img id="%(preview_id)s" src="" %(preview_attrs)s>'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)
        substitutions['preview_id'] = 'preview-%s'%name
        self.preview_attrs['data-for'] = name
        substitutions['preview_attrs'] = flatatt(self.preview_attrs)

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            substitutions['img_attrs'] = flatatt(self.img_attrs)
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions
        return mark_safe(template % substitutions)


class ClearableImageCropInput(ClearableImagePreviewInput):
    def __init__(self, aspect=1, **kwargs):
        super(ClearableImageCropInput, self).__init__(**kwargs)
        self.preview_attrs['data-aspect'] = aspect

    class Media:
        js = ('js/cropper_widget.js', 'libs/cropper/cropper.min.js',)
        css = {'all': ('libs/cropper/cropper.min.css',)}

