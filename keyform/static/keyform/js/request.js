$(document).ready(function() {
    $('#cancel').css("display", 'none');
    $('#submit').css("display", 'none')
    var div = document.getElementById('comments');
    $('#add').click(function() {
        $('#add').css("display", 'none');
        $('#cancel').css("display", 'inline-block');
        $('#submit').css("display", 'inline-block')
        div.innerHTML = '<p>Comment:</p><textarea id="comment-text" cols="40" rows="4"></textarea>';
    });

    $('#cancel').click(function() {
        $('#add').css("display", 'inline-block');
        $('#cancel').css("display", 'none');
        $('#submit').css("display", 'none');
        div.innerHTML = '';
    });

    $('#submit').click(function() {
        if(confirm("Are you sure you want to add this comment?")) {
            var message = $('#comment-text').val();
            var pk = $('#key-section').data('pk');
            console.log(message);
            $.post('/add-comment', { message:message, pk:pk }, function() {
                location.reload();
            });
        }
    });
});
