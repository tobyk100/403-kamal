//Binds all appropriate buttons with clicks
$(document).on('ready', function() {
    $('#submitPostButton').bind('click', submitAndResetPost);
    $('#facebookRefreshButton').bind('click', loadFacebookFeed());
    $('#twitterRefreshButton').bind('click', loadTwitterFeed());
    $('#googleRefreshButton').bind('click', loadGoogleFeed());
    var refreshId = setInterval(function(){
	loadFacebookFeed();
	loadTwitterFeed();
	loadGoogleFeed();
    }, 100000);
});


//Toggles display popup for user to type in post
function displayPostPopup() {
    if ($('#postPopup').css("display") == 'none') {
        $('#postPopup').show();
    } else {
        $('#postPopup').hide();
    }
}

//Submits a post using an ajax request.
//On callback return clears the text area so they can enter in another post
function submitAndResetPost() {
    var message = $('#postText').val();
    if (message != '') {
        post_ajax_call(message, '/facebook_request/');
        post_ajax_call(message, '/twitter_request/');
    }
}

function post_ajax_call(msg, url) {
    $.ajax({
	type: 'POST',
	url: url,
	data: {
	    message: msg,
	    type: 'upload'
	},
	datatype: 'json',
	error: function(data) {
	    $(location).attr('href',data);
	}
    });
}

//Loads Facebook feeds from server
//Post request used to get list of posts
function loadFacebookFeed() {
    //console.log('facebook');
    $('#facebookFeedPosts').empty();
    $.ajax({
        type: "POST",
        url: "/facebook_request/",
        data: {
            title: "ajax call from facebook",
	    type: "feedRequest"
        },
        datatype: "json",
        error: function (data) {
	    $(location).attr('href',data.responseText);
	},
        success: function (data) {
	    if(data.success == "false"){
		$('#facebookFeedPosts').append('No Facebook Account Found:<br>
<button id="signinToFacebook" class="btn">Facebook Login</button>');
		$('#signinToFacebook').bind('click', signinToFacebook);
	    }else {
		for(var i = 0; i < data.updates.length; i++){
                    createPostInFacebookFeed(urlify(
			data.updates[i][0]),
					     data.updates[i][2],
					     data.updates[i][1],
					     data.updates[i][3]);
		}
	    }
        }
    });
}

//Creates a pop in the social media feed with the given parameters
function createPostInFacebookFeed(message, time, person, img_src){
    var date = new Date(time * 1000);
    var formattedDate = (
          date.toLocaleString().substring(0,3) +
          ' ' +
	  date.toLocaleTimeString()
    );

    $('#facebookFeedPosts').append('<div class ="FeedPost">' +
			      '<img src="' + img_src + '" ' + 'class="user_img" alt="User Avatar"/>' +
			      '<img src="/static/img/FacebookLogo.jpg" class="logo" alt="Facebook"/>' +
			      '<div class="nameTime">' + person + ' - ' +
                              formattedDate + '</div><div class="message">' + message + '</div></div>');
}

function loadTwitterFeed() {
    $.ajax({
        type: "POST",
        url: "/twitter_request/",
        data: {
            type: "feedRequest"
        },
        datatype: "json",
        error: function (data) {
            console.log('Error:', data);
        },
        success: function (data) {
            $('#twitterFeedPosts').empty();
	    var posts = JSON.parse(data);
            for(var i = 0; i < posts.tweets.length; i++){
                createPostInTwitterFeed(urlify(
                    posts.tweets[i].text),
                    posts.tweets[i].created_at ,
                    posts.tweets[i].user.name,
                    posts.tweets[i].user.profile_image_url
                );
	    }
        }
    });
}

function createPostInTwitterFeed(message, time, person, profilePicture) {
    $('#twitterFeedPosts').append('<div class ="FeedPost">' +
			     '<img src=\'' + profilePicture + '\' class="user_img" alt="User Avatar"/>' +
			     '<img src="/static/img/TwitterLogo.jpg" class="logo" alt="Facebook"/>' +
			     '<div class="nameTime">' + person + ' - ' + time +
                             '</div><div class="message">' +
                             message + '</div></div>'
    );
}

function loadGoogleFeed() {
    console.log('load google feed');
    // TODO
}

function urlify(text) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    });
}

