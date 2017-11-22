django-cropper-widget
=====================

Django app for `Cropper <https://github.com/fengyuanchen/cropper>`_ jQuery plugin integration.

Quickstart
----------

Install django-cropper-widget:

.. code-block::

    $ pip install git+git://github.com/Kudria/django-cropper-widget

Add django-cropper-widget to INSTALLED_APPS in settings.py for your project:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'cropper_widget',
    )


In your code:

.. code-block:: python


    from cropper_widget.widgetss import CropperWidget

    class MyForm(forms.Form):
        image = forms.ImageField(widget=CropperWidget(cropper_options={'aspectRatio': 1}))
