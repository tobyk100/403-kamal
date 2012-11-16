//Binds all appropriate buttons with clicks
$(document).on('ready', function() {
    $('#submitPostButton').on('click', submitPost);
    $('#facebookRefreshButton').bind('click', loadFacebookFeed);
    $('#twitterRefreshButton').bind('click', loadTwitterFeed);
    $('#googleRefreshButton').bind('click', loadGoogleFeed);
    /*var refreshId = setInterval(function(){
	loadFacebookFeed();
	loadTwitterFeed();
	loadGoogleFeed();
    }, 60000);
    */
});

// Submits a post using an ajax request.
function submitPost() {
    var message = $('#postText').val();
    if (message != '') {
        if ($('#postOptionFacebook').is(':checked')) {
            submitPostHelper(message, '/facebook_request/');
        }
        if ($('#postOptionTwitter').is(':checked')) {
            submitPostHelper(message, '/twitter_request/');
        }
        if ($('#postOptionGooglePlus').is(':checked')) {
        }
    }
}

function submitPostHelper(msg, url) {
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
		$('#facebookFeedPosts').append('No Facebook Account Found:<br><button id="signinToFacebook" class="btn">Facebook Login</button>');
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
	    if(data.success == "false") {
		$('#twitterFeedPosts')
                    .append('No Twitter Account Found:<br><button id="signinToTwitter" class="btn">Twitter Login</button>');
		$('#signinToTwitter').bind('click', signinToTwitter);
	    } else {
		var posts = JSON.parse(data);
		for (var i = 0, length = posts.tweets.length; i < length; i++) {
                    var post = posts.tweets[i];
                    createPostInTwitterFeed(
                        urlify(post.text),
                        post.created_at ,
                        post.user.name,
                        post.user.profile_image_url
                    );
		}
                // $('#twitterFeedPosts').append(feed_html);
	    }
        }
    });
}

/*
 <div class ="FeedPost">
     <img src='...' class="user_img" alt="User Avatar"/>
     <img src="/static/img/TwitterLogo.jpg" class="logo" alt="Facebook"/>
     <div class="nameTime"> person - time </div>
     <div class="message"> message </div>
 </div>

 TODO: could be rendered more efficiently with http://api.jquery.com/jQuery.template/
       But first modify the returned data,
       it doesn't make sense to return data we don't need since network transaction is expensive.

 */

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

