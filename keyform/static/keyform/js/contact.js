$(document).ready(function() {
    $('.delete').click(function() {
        if(confirm("NOTE: This will delete the contact from EVERY building they are associated with.")) {
            var pk = $(this).closest('.contact').data('pk');
            $.post(window.location.href, { pk:pk }, function(data) {
                $('.contact[data-pk=' + pk + ']').remove();
                if (!data.success)
                    alert('You do not have permission to delete contacts!');
            })
            .fail(function() {
                alert('The server is not responding');
            });
        }
    });
});
