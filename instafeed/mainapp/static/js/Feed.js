//Binds all appropriate buttons with clicks
$(document).on('ready', function() {
    loadFacebookFeed();
    loadTwitterFeed();
    loadGoogleFeed();
    $('#submitPostButton').on('click', submitPost);

    $('#facebookRefreshButton').bind('click', loadFacebookFeedRefresh);
    $('#twitterRefreshButton').bind('click', loadTwitterFeedRefresh);
    $('#googleRefreshButton').bind('click', loadGoogleFeedRefresh);
    $('#postText').bind('keyup keypress', countNewPostChars);
    var refreshId = setInterval(function(){
      loadFacebookFeed();
      loadTwitterFeed();
      loadGoogleFeed();
    }, 60000);
    $('#postBox').on('hide', resetPostBox);
});

function loadFacebookFeedRefresh()
{
  //clear out the old posts so the 'loading' message will be displayed when called
  $('#facebookFeedPosts').empty();
  loadFacebookFeed();
}


function loadTwitterFeedRefresh()
{
  //clear out the old posts so the 'loading' message will be displayed when called
  $('#twitterFeedPosts').empty();
  loadTwitterFeed();
}

function loadGoogleFeedRefresh()
{
  //clear out the old posts so the 'loading' message will be displayed when called
  $('#googleFeedPosts').empty();
  loadGoogleFeed();
}


function countNewPostChars() {
  if ($('#postOptionTwitter').is(':checked')) {
    var count = $(this).val().length,
        count_elem = $('#textCount');
    count_elem.text(count);
    if (count > 140) {
      count_elem.addClass('text-error');
    } else {
      count_elem.removeClass('text-error');
    }
  } else {
    $('#textCount').text('');
  }
}

// Submits a post using an ajax request.
function submitPost() {
    var message = $('#postText').val(),
    twitterchecked = $('#postOptionTwitter').is(':checked');
    if (!twitterchecked || message.length <= 140) {
	if ($("#facebookCommentFlag").is(':checked')){
	    //alert($("#facebookCommentFlag").val());
	    //call comment method and pass it id and message
	    submitFacebookComment(message, $("#facebookCommentFlag").val());
	} else {
	    if (message != '') {
		if ($('#postOptionFacebook').is(':checked')) {
		    submitPostHelper(message, '/facebook_request/');
		}
		if (twitterchecked && message.length <= 140) {
		    submitPostHelper(message, '/twitter_request/');
		}
	    }
	}
	$('#postBox').modal('hide');
    }
}

function submitFacebookComment(msg , id) {
    $.ajax({
        type: 'POST',
        url: '/facebook_request/',
        data: {
            message: msg,
            postId: id,
            type: 'comment'
        },
        datatype: 'json',
        error: function(data) {
            //$(location).attr('href',data);
          alert(data);
        }
    });
}

// Changed post box ui back to normal
function resetPostBox(){
    $("#myModalLabel").text("New Post");
    $("#postOptionTwitter").attr("checked", true);
    $("#postOptionFacebook").attr("checked", true);
    $("#postOptionTwitter").attr("disabled", false);
    $("#postOptionFacebook").attr("disabled", false);
    $("#postText").attr("placeholder", "Enter Post...").val('');
    $('#textCount').text('0').removeClass('text-error');
    $("#facebookCommentFlag").attr("checked", false);
    $("#submitPostButton").text("Submit Post");
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
            //$(location).attr('href',data);
          alert(data);
        }
    });
}

// A generic function to display signin notice.
// @param name The social media name, such as 'Facebook', 'Twitter', etc
// @param fn The function to be invoked after the signin button is clicked
// @return void
function displaysigninbutton(name, fn) {
  var colclass = '#' + name.toLowerCase() + 'FeedPosts',
      btnclass = '#signinTo' + name,
      btnid = 'signinTo' + name,
      fbcol = $(colclass).empty(),
      signin_title = '<h6>Please log in to ' + name + ' again</h6>',
      signin_button = '<button id="' + btnid
                      + '" class="btn">' + name + ' Login</button>',
      signin_notice = ['<div style="text-align: center">',
                      signin_title, signin_button, '</div>'].join('');
  fbcol.append(signin_notice);
  $(btnclass).bind('click', fn);
}

function loadFacebookFeed() {
  //if there are no posts currently displayed
  if($('#facebookFeedPosts').children().length == 0)
  {  
    var gif = $("<img>");
    gif.attr('src', 'http://www.henley-putnam.edu/Portals/_default/Skins/henley/images/loading.gif'); 
    gif.attr('alt', 'loading gif');
    $('#facebookFeedPosts').append(gif);
  }
  $.ajax({
    type: "POST",
    url: "/facebook_request/",
    data: {
      title: "ajax call from facebook",
      type: "feedRequest"
    },
    datatype: "json",
    error: function (data) {
      displaysigninbutton('Facebook', signinToFacebook);
    },
    success: function (data) {
      if (data.success == "false") {
        displaysigninbutton('Facebook', signinToFacebook);
      } else {
        $('#facebookFeedPosts').empty();
        for(var i = 0; i < data.updates.length; i++) {
          createPostInFacebookFeed(
            urlify(data.updates[i][0]),
            data.updates[i][2],
            data.updates[i][1],
            data.updates[i][3],
            data.updates[i][4]
          );
        }
      }
    }
  });
}

//Creates a pop in the social media feed with the given parameters
function createPostInFacebookFeed(message, time, person, img_src, id){
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
                  formattedDate + '</div><div class="message">' + message +
                  '<br> <a class="comment" id="likeid' + id + '" href="#" onclick="facebookLike(\'' + id +  '\')">Like   </a>' +
                  '<a class="comment" href="#" onclick="facebookComment(\'' + id + '\')">Comment</a></div></div>');
}

function loadTwitterFeed() {
  if($('#twitterFeedPosts').children().length == 0)
  {  
    var gif = $("<img>");
    gif.attr('src', 'http://www.henley-putnam.edu/Portals/_default/Skins/henley/images/loading.gif'); 
    gif.attr('alt', 'loading gif');
    $('#twitterFeedPosts').append(gif);
  }

    $.ajax({
	type: "POST",
	url: "/twitter_request/",
	data: {
	    type: "feedRequest"
	},
	datatype: "json",
	error: function (data) {
	    displaysigninbutton('Twitter', signinToTwitter);
	},
	success: function (data) {
	    if(!data.success) {
		displaysigninbutton('Twitter', signinToTwitter);
	    } else {
		$('#twitterFeedPosts').empty();
		var posts = data;
		for (var i = 0, length = posts.tweets.length; i < length; i++) {
		    var post = posts.tweets[i];
		    createPostInTwitterFeed(
			urlify(post.text),
			post.created_at ,
			post.user.name,
			post.user.profile_image_url,
			post.id_str
		    );
		}
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

function createPostInTwitterFeed(message, time, person, profilePicture, id) {
    $('#twitterFeedPosts').append('<div class ="FeedPost">' +
                 '<img src=\'' + profilePicture + '\' class="user_img" alt="User Avatar"/>' +
                 '<img src="/static/img/TwitterLogo.jpg" class="logo" alt="Facebook"/>' +
                 '<div class="nameTime">' + person + ' - ' + time +
                 '</div><div class="message">' + message +
                 '<br> <a class="comment" id="retweetid' + id + '"  href="#" onclick="twitterRetweet(\'' + id + '\')">Retweet   </a>' +
                 ' <a class="comment" href="#" onclick="twitterReply(\'' + person + '\')">Reply </a></div></div>'
    );
}

function loadGoogleFeed() {

  if($('#googleFeedPosts').children().length == 0)
  {  
    var gif = $("<img>");
    gif.attr('src', 'http://www.henley-putnam.edu/Portals/_default/Skins/henley/images/loading.gif'); 
    gif.attr('alt', 'loading gif');
    $('#googleFeedPosts').append(gif);
  }

  $.ajax({
    type: "POST",
    url: "/google_get_posts/",
    data: {
      title: "ajax call from google",
      type: "feedRequest"
    },
    datatype: "json",
    success: function (data) {
      if(!data.success) {
        displaysigninbutton('Google', signinToGooglePlus);
      } else {
        $('#googleFeedPosts').empty();
        var posts = data.posts;
        for(var i = 0; i < posts.length; i++) {
          createPostInGoogleFeed(
            urlify(posts[i].content),
            posts[i].published,
            posts[i].author_display_name,
            posts[i].author_image_url
          );
        }
      }
    }
  });
}

function createPostInGoogleFeed(message, time, person, profilePicture) {
    var date = new Date(time);
    var formattedDate = (
          date.toLocaleString().substring(0,3) +
          ' ' +
      date.toLocaleTimeString()
    );   

    $('#googleFeedPosts').append('<div class ="FeedPost">' +
                 '<img src=\'' + profilePicture + '\' class="user_img" alt="User Avatar"/>' +
                 '<img src="/static/img/GoogleLogo.jpg" class="logo" alt="Google"/>' +
                 '<div class="nameTime">' + person + ' - ' + formattedDate +
                             '</div><div class="message">' +
                             message + '</div></div>'
    );
}

function urlify(text) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    });
}

function facebookComment(id){
    //TODO
    //change post dialog to say comment
    //submit comment up like a normal post with the id
    //change post ui back to normal
    $("#myModalLabel").text("New Facebook Comment");
    $("#postOptionTwitter").attr("checked", false);
    $("#postOptionFacebook").attr("checked", true);
    $("#postOptionTwitter").attr("disabled", true);
    $("#postOptionFacebook").attr("disabled", true);
    $("#postText").attr("placeholder", "Enter Facebook Comment...");
    $("#submitPostButton").text("Submit Comment");
    $("#facebookCommentFlag").attr("checked", true);
    $("#facebookCommentFlag").val(id);
    $("#postButton").click();
}

function facebookLike(id){
    //call hampton's function taking an id of a post to like
    // alert(id);
    $.ajax({
        type: 'POST',
        url:"/facebook_request/" ,
        data: {
            postId: id,
            type: 'like'
        },
        datatype: 'json',
        success: function(data){
            var like_btn = $("#likeid" + id);
            like_btn.text("Liked ");
        },
        error: function(data) {
            alert(data);
        }
    });
}

function twitterRetweet(id){
    //call kevins function passing it an id to retweet for the user
    alert(id + "!");
    $.ajax({
        type: 'POST',
        url:"/twitter_request/" ,
        data: {
            postId: id,
            type: 'retweet'
        },
        datatype: 'json',
        success: function(data){
          alert(id);
          var retweet_btn = $("#retweetid" + id);
          retweet_btn.text("Retweeted ");
          
        },
        error: function(data) {
            alert(data);
        }
    });
}

function twitterReply(person){
    //Create normal post putting @person infront
    //TODO
    //Change our post dialog to look like a reply
    //fill in @person in text area and block off facebook check
    //submit it like you would a normal post
    //change post popup back to normal
    $("#myModalLabel").text("New Twitter Reply");
    $("#postOptionTwitter").attr("checked", true);
    $("#postOptionFacebook").attr("checked", false);
    $("#postOptionTwitter").attr("disabled", true);
    $("#postOptionFacebook").attr("disabled", true);
    $("#postText").text("@" + person);
    $("#submitPostButton").text("Submit Reply");
    $("#postButton").click();
}
