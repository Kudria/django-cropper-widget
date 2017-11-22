/**
 * Use cropper plugin on form's rendered with CropperWidget
 */
jQuery(function ($) {
    var croppers = $('img.cropper');
    croppers.hide();
    croppers.each(function (index, element) {
        var cropper = $(element);
        var input_name = cropper.data('cropper-for');
        var $input = $('input[name=' + input_name + ']');
        $input.on('change', function (changeEvent) {
            var input = changeEvent.delegateTarget;
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    cropper.show();
                    cropper.attr('src', e.target.result);
                    var cropperOptions = cropper.data('cropper-conf');
                    cropper.cropper(cropperOptions);
                    cropper.cropper('replace', e.target.result);
                    var form = $input.parents('form');
                    var croppedInput = form.find('input[name=' + input_name + '-cropped-data]');
                    form.submit(function (e) {
                        croppedInput.val(cropper.cropper('getCroppedCanvas').toDataURL('image/jpeg'));
                    });
                };
                reader.readAsDataURL(input.files[0]);
            }
        });
    });
})