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

    function mailbox_field() {
        var key_type_selector = $(this);
        var pks_with_hide_core_number = key_type_selector.data('pks_with_hide_core_number');
        pks_with_hide_core_number = String(pks_with_hide_core_number).split(',');
        var current_key_type = key_type_selector.find('option:selected').attr('value');
        key_type_selector.closest('.keydata-form').find('[id$=-core_number]').closest('.row').toggle($.inArray(current_key_type, pks_with_hide_core_number) == -1)
    }

    $('.keydata-form select[data-pks_with_hide_core_number]').on('click change', mailbox_field);
});

