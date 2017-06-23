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
            $.post(COMMENT_URL, { message:message, pk:pk }, function(data) {
                var comment_element = $(COMMENT_HTML);
                comment_element.find('.author').text(data.author);
                comment_element.find('.timestamp').text(data.timestamp);
                comment_element.find('.message').html(data.message.replace(/\n/g, '<br />'));

                $('#comment-list').append(comment_element);

            })
            .fail(function() {
                alert('Oops we were unable to save your comment, the error has been logged and we are looking into it!');
            });
        }
    });
});
