$(document).ready(function() {
    $('.delete').click(function() {
        if(confirm("Are you sure you want to delete this contact?")) {    
            var pk = $(this).closest('.contact').data('pk')
            $.post(window.location.href, { pk:pk }, function() {
            });
            $(this).closest('.contact').remove()
        }
    });
});
