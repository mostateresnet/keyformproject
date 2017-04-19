$(document).ready(function() {
    $('#generate_forms').click(function() {
        var form_idx = $('#id_keydata_set-TOTAL_FORMS').val();
        $('#form-set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
        $('#id_keydata_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });
});
