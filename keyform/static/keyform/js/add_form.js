$(document).ready(function() {
    $('#form-set').on('click', '.generate_forms', function() {
        var form_idx = $('#id_keydata_set-TOTAL_FORMS').val();
        var new_form = $($('#empty_form').html().replace(/__prefix__/g, form_idx));
        new_form.find('input[id$=-room_number]').val(previous_val);
        $('#form-set').append(new_form);
        $('#id_keydata_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    $('#form-set').on('click', '.delete_button', function() {
        if ($('#form-set .keydata-form').length > 1){
            var form_idx = $('#id_keydata_set-TOTAL_FORMS').val();
            $(this).closest('.keydata-form').remove();
            $('#id_keydata_set-TOTAL_FORMS').val(parseInt(form_idx) - 1);
        }
    });

    function hide_keydata_field() {
        var key_type_selector = $(this);
        var pks_with_hide_core_number = key_type_selector.data('pks_with_hide_core_number');
        pks_with_hide_core_number = String(pks_with_hide_core_number).split(',');
        var current_key_type = key_type_selector.find('option:selected').attr('value');
        key_type_selector.closest('.keydata-form').find('[id$=-core_number]').closest('.row').toggle($.inArray(current_key_type, pks_with_hide_core_number) == -1)
    }

    $('#form-set').on('click change','.keydata-form select[data-pks_with_hide_core_number]', hide_keydata_field);

    var global_room_number = $("[name=keydata_set-__prefix__-room_number]");
    global_room_number.on('keyup', synchronize_room_number)

    var previous_val = global_room_number.val();
    function synchronize_room_number (){
        var current_val = global_room_number.val();
        $(".keydata-form input[id$=-room_number]").each(function() {
            if ($(this).val() == previous_val){
                $(this).val(current_val);
            }
        });
        previous_val = current_val;
    };
});
