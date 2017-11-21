/**
 * Use cropper plugin on form's image preview
 */
"use strict";
jQuery(function ($) {
    var previews = $('img.form-img-preview');
    previews.hide();
    previews.each(function (index, element) {
        var preview = $(element);
        var input_name = preview.data('for');
        var input = $('input[name=' + input_name + ']');
        input.on('change', function (changeEvent) {
            var input = changeEvent.delegateTarget;
            var $input = $(input);
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    preview.show();
                    preview.attr('src', e.target.result);
                    if (typeof $().cropper !== 'undefined') {
                        preview.cropper({
                            viewMode: 3,
                            aspectRatio: preview.data('aspect'),
                            movable: false,
                            scalable: false,
                            zoomable: false,

                        });
                        preview.cropper('replace', e.target.result);
                        var form = $input.parents('form');
                        form.submit(function (e) {
                            var croppedInput = $('<input>').attr('name', input_name + '-cropped').attr('type', 'text').hide();
                            form.append(croppedInput);
                            croppedInput.val(preview.cropper('getCroppedCanvas').toDataURL('image/jpeg'));
                        })
                    }
                }
                reader.readAsDataURL(input.files[0]);
            }
        });

    });
})