$(document).ready(function() {
    $('.delete').click(function() {
        if(confirm("Are you sure you want to delete this contact?")) {
            var pk = $(this).closest('.contact').data('pk');
            $.post(window.location.href, { pk:pk }, function(data) {
                $('.contact[data-pk=' + pk + ']').remove();
                if (!data.success)
                    alert('You do not have permission to delete a contact!');
            })
            .fail(function() {
                alert('The server is not responding');
            });
        }
    });
});
