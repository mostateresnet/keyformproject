$(document).ready(function() {
    $('#form-set').on('click', '.generate_forms', function() {
        var form_idx = $('#id_keydata_set-TOTAL_FORMS').val();
        $('#form-set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_keydata_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    $('#form-set').on('click', '.delete_button', function() {
        if ($('#form-set .keydata-form').length > 1){
            var form_idx = $('#id_keydata_set-TOTAL_FORMS').val();
            $(this).closest('.keydata-form').remove();
            $('#id_keydata_set-TOTAL_FORMS').val(parseInt(form_idx) - 1);
        }
    });
});
