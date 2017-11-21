from django.conf import settings


CROPPER_JS_URL = getattr(settings, 'CROPPER_JS_URL', 'cropper/cropper.min.js')
CROPPER_CSS_URL = getattr(settings, 'CROPPER_CSS_URL', 'cropper/cropper.min.css')