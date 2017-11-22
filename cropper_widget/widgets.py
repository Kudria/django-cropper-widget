# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.core.files.base import ContentFile
from django.forms.utils import flatatt
from django.forms import widgets
import base64
from django.utils.html import mark_safe, conditional_escape

from .settings import CROPPER_DEFAULT_OPTIONS, CROPPER_CSS_URL, CROPPER_JS_URL


class CropperWidget(widgets.ClearableFileInput):
    """ Widget renders <img class="cropper" ... /> after <input> and additional hidden input
     (<input name='{name} + -cropped-data' ... >) for cropped image data (in base64)."""

    template_with_initial = (
        '%(initial_text)s: <img %(img_attrs)s src="%(initial_url)s"><br>'
        '%(clear_template)s<br>%(input_text)s: %(input)s'
        '<img id="%(cropper_id)s" src="" %(cropper_attrs)s>'
        '<input type="hidden" %(cropped_data_attrs)s/>'
    )
    template_with_clear = ('%(input)s<img id="%(cropper_id)s" src="" %(cropper_attrs)s>'
                           '<input type="hidden" %(cropped_data_attrs)s/>')

    def __init__(self, attrs=None, cropper_options=None, img_attrs=None):

        super(CropperWidget, self).__init__(attrs)
        self.img_attrs = img_attrs or {}
        self.img_attrs.update(img_attrs)
        # cropper options
        cropper_options = cropper_options or {}
        self.cropperOptions = CROPPER_DEFAULT_OPTIONS.copy()
        self.cropperOptions.update(cropper_options)
        self.cropper_attrs = {
            'data-cropper-conf': json.dumps(self.cropperOptions),
            'class': 'cropper'
        }

    def render(self, name, value, attrs=None, renderer=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        substitutions['input'] = super(widgets.ClearableFileInput, self).render(name, value, attrs)
        substitutions['cropper_id'] = '%s-cropper' % name
        self.cropper_attrs['data-cropper-for'] = name
        substitutions['cropper_attrs'] = flatatt(self.cropper_attrs)
        substitutions['cropped_data_attrs'] = flatatt({'name': '%s-cropped-data' % name})
        template = self.template_with_clear

        if self.is_initial(value):
            template = self.template_with_initial
            substitutions.update(self.get_template_substitution_values(value))
            substitutions['img_attrs'] = flatatt(self.img_attrs)
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = widgets.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions
        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        img_file = files.get(name)
        cropped_image = data.get('%s-cropped-data' % name)
        if cropped_image:
            image_ct, image_data = cropped_image.split('base64,')
            image_decoded = base64.b64decode(image_data)
            # image = BytesIO(image_decoded)
            file = ContentFile(image_decoded, name=img_file.name)
            return file


    class Media:
        js = ('js/cropper_widget/cropper_widget.js', CROPPER_JS_URL,)
        css = {'all': (CROPPER_CSS_URL,)}
