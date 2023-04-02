function appendToChatLog(message) {
    // Check if the message contains a numbered list
    if (/\d+\./.test(message)) {
        // Replace the numbered list with new lines
        message = message.replace(/(\d+\.)\s?/g, '<br>$1 ');
    }

    // Append the formatted message to the chat log
    $('#chat_log').append('<div>' + message + '</div>');
    // Scroll to the bottom of the chat log
    $('#chat_log').scrollTop($('#chat_log')[0].scrollHeight);
}


function sendMessage() {
    let user_input = $('#input_box').val();
    if (!user_input) return;

    appendToChatLog('You: ' + user_input);

    $('#ellipsis').show(); // Show the ellipsis effect
	
    let api_endpoint = '/chatbot/api/';
    if (window.location.href === 'https://www.aiitsupport.net/') {
        api_endpoint = '/api/free_chatbot/';
    }
	
    $.ajax({
        url: api_endpoint,
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
        data: {
            'user_input': user_input,
        },
        success: function (data) {
            $('#ellipsis').hide(); // Hide the ellipsis effect
            appendToChatLog('Ruby: ' + data.response);
            $('#resolve_button').prop('disabled', !data.resolve_enabled);
            $('#new_problem_button').prop('disabled', !data.new_problem_enabled);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $('#ellipsis').hide(); // Hide the ellipsis effect
            if (jqXHR.status === 403) {
                appendToChatLog('Error: You must be logged in to use the chatbot.');
            } else {
                appendToChatLog('Error: An unexpected error occurred.');
            }
        }
    });

    $('#input_box').val('');
}

$('#send_button').on('click', sendMessage);
$('#input_box').on('keypress', function(e) {
    if (e.which === 13) {
        e.preventDefault();
        sendMessage();
    }
});


$('#resolve_button').on('click', function() {
    // Handle the "resolve" button click
});

$('#new_problem_button').on('click', function() {
    // Handle the "new problem" button click
});

appendToChatLog('Ruby: Hi, how may I help you today?');
