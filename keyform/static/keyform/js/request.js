$(document).ready(function() {
    $('#add').click(function() {
        $('#comments').toggleClass('add-comment', true);
    });

    $('#cancel').click(function() {
        $('#comments').toggleClass('add-comment', false);
    });

    $('#submit').click(function() {
        if(confirm("Are you sure you want to add this comment?")) {
            var message = $('#comment-text').val();
            var pk = $('#key-section').data('pk');
            $.post(COMMENT_URL, { message:message, pk:pk }, function() {
                location.reload();
            });
        }
    });
});
