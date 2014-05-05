$(document).ready(function() {
	$('#post-submit').click(function(event) {
		event.preventDefault();
		var topic_id = $(this).siblings('#post-submit-topic').val();

		var form_data = $(this).parent().serialize();
		$.ajax({
			type : 'POST',
			url : '/board/topic/' + topic_id + '/addpost',
			data : form_data,
			success: function (data) {
				$(data).appendTo($('#posts')).slideDown('fast');
			}
		});
	});
	$('#pin-button').click(function(event) {
		$('#pin-button').prop('disabled', true);
		event.preventDefault();
		var topic_id = $(this).val();

		$.ajax({
			type : 'POST',
			url : topic_id + '/pin',
			success: function (data) {
				$('#pin-button').text(data);
				$('#pin-button').prop('disabled', false);
			}
		});
	});
    $(document).on('click', '.post-edit', function(event) {
        event.preventDefault();
        var $post_content = $(event.target).parent().siblings('.post-text');
        var content = $($post_content).text();
        $($post_content).css('font-size', '0');

        $($post_content).append('<form method="post" action=""><textarea name="post-new-content">'
                + content
                + '</textarea><br>'
                + '<input class="post-edit-submit" type="submit" value="Save">'
                + '<input class="post-edit-cancel" type="submit" value="Cancel">'
                + '</form>');
    });
    $(document).on('click', '.post-edit-submit', function(event) {
        event.preventDefault();
        var new_content = $(event.target).siblings('textarea').val();
        var form_data = $(event.target).parent().serialize();
        var post = $(event.target).parents('.post');
        var post_id = $(post).attr('id');
        $(event.target).parent().parent('.post-text').css('font-size', '12');
        //$(event.target).parent().parent('.post-text').text(new_content);

        $.ajax({
            type : 'POST',
            url : '/board/post/' + post_id + '/edit',
            data : form_data,
            success: function (data) {
                $(post).html(data);
            }
        });
        //$(event.target).parent().remove();
    });
    $(document).on('click', '.post-edit-cancel', function(event) {
        event.preventDefault();
        $(event.target).parents('.post-text').css('font-size', '12');
        $(event.target).parent().remove();
    });
});


/*
 * Django requires CSRF tokens on all POST requests. The following functions
 * ensure that CSRF tokens are sent with those requests even when not included
 * in the html, for the purpose of allowing AJAX requests.
 * @src		https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/#csrf-ajax
 */
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});