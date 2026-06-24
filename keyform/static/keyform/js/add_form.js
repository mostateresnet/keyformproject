$(document).ready(function() {
    $('#form-set').on('click', '.generate_forms', function() {
        var form_idx = $('#id_keydata_set-TOTAL_FORMS').val();
        var new_form = $($('#empty_form').html().replace(/__prefix__/g, form_idx));
        new_form.find('input[id$=-room_number]').val(previous_room);
        $('#form-set').append(new_form);
        $('#id_keydata_set-TOTAL_FORMS').val(parseInt(form_idx) + 1);
    });

    $('#form-set').on('click', '.delete_button', function(){
        if ($('#form-set .keydata-form').length > 1){
            var form_idx = $('#id_keydata_set-TOTAL_FORMS').val();
            $(this).closest('.keydata-form').remove();
            $('#id_keydata_set-TOTAL_FORMS').val(parseInt(form_idx) - 1);
        }
    });

    function hide_keydata_field(){
        var key_type_selector = $(this);
        var pks_with_hide_core_number = key_type_selector.data('pks_with_hide_core_number');
        pks_with_hide_core_number = String(pks_with_hide_core_number).split(',');
        var current_key_type = key_type_selector.find('option:selected').attr('value');
        key_type_selector.closest('.keydata-form').find('[id$=-core_number]').closest('.row').toggle($.inArray(current_key_type, pks_with_hide_core_number) == -1)
    }

    $('#form-set').on('click change','.keydata-form select[data-pks_with_hide_core_number]', hide_keydata_field);

    function mode(arr) {
        return arr.sort(function(a,b){
            return arr.filter(function(v){ return v===a }).length
                 - arr.filter(function(v){ return v===b }).length
        }).pop();
    }

    var room_list = [];
    $(".keydata-form input[id$=-room_number]").each(function() {
        room_list.push($(this).val());
    });

    var global_room_number = $("[name=keydata_set-__prefix__-room_number]");
    var previous_room = mode(room_list);
    global_room_number.val(previous_room);

    function synchronize_room_number(){
        var current_val = global_room_number.val();
        $(".keydata-form input[id$=-room_number]").each(function() {
            if ($(this).val() == previous_room){
                $(this).val(current_val);
            }
        });
        previous_room = current_val;
    };

    global_room_number.on('keyup', synchronize_room_number);

    function calculate_charge_amount() {
        let sum = 0;
        $('[name^=charge_amount_]').each(function() {
            const price = parseFloat($(this).data('charge-amt'));
            const quantity = parseFloat($(this).val());
            if (!isNaN(price) && !isNaN(quantity)) {
                sum += quantity * price;
            }
        });
        $('#charge_amount_total').text('$' + sum.toFixed(2));
        if (sum === 0 && !CAN_CHARGE_ZERO) {
            $('#charge-error-msg').show();
        } else {
            $('#charge-error-msg').hide();
        }
        return sum;
    }

    $('#form-set').on('input change', '[name^=charge_amount_]', function () {
        const val = parseFloat(this.value);
        if (isNaN(val) || val < 0) {
            this.value = '';
        }
        calculate_charge_amount();
    });

    $('#form-set').on('keydown', '[name^=charge_amount_]', function (e) {
         if (e.key === '-' || e.key === 'Minus' || e.keyCode === 189) {
            e.preventDefault();
        }
    });

    $('#form-set').on('submit', function (e) {
    const total = calculate_charge_amount();
    if (total === 0 && !CAN_CHARGE_ZERO) {
        e.preventDefault();
        $('#charge-error-msg').show().text('Please enter at least one charge. Total cannot be $0.00.');
        }
    });

    $('[name^=charge_amount_]').on('click change keyup', calculate_charge_amount);
    calculate_charge_amount();
});
