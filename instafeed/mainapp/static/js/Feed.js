window.onload = function () {
    bindButtons();
}

//Binds all appropriate buttons with clicks
function bindButtons(){
    $('#postButton').bind('click', displayPostPopup);
    //$('#accountsButton').bind('click', directToAccounts); TODO This function doesn't exist yet
    $('#submitPostButton').bind('click', submitAndResetPost);
    $('#facebookRefreshButton').bind('click', loadFacebookFeed);
    $('#twitterRefreshButton').bind('click', loadTwitterFeed);
    $('#addFacebookButton').bind('click', displayLoginScreenFacebook);
    $('#addTwitterButton').bind('click', displayLoginScreenTwitter);
    $('#signinToTwitter').bind('click', signinToTwitter);
    $('#signinToFacebook').bind('click', signinToFacebook);
}

//Directs to backend to start process to login to Twitter
function signinToTwitter(){
       $.ajax({
        type: "POST",
        url: "/twitter_signin/",
        data: { title: "begin twitter signin process" },
        datatype: "json",
        error: function (data) { alert('Error:' + data); },
        success: function (data) {
            //alert('URL: ' + data);
            $(location).attr('href',data);
        }
    });
}

//Directs to backend to start process to login to Facebook
function signinToFacebook(){
       $.ajax({
        type: "POST",
        url: "/facebook_signin/",
        data: { title: "begin facebook signin process" },
        datatype: "json",
        error: function (data) { alert('Error:' + data); },
        success: function (data) {
           // alert('URL: ' + data);
            $(location).attr('href',data);
        }
    });
}


//Shows Twitter login screen if not already shown
function displayLoginScreenTwitter(){
    if ($('#addScreenTwitter').css("display") == 'none') {
        $('#addScreenTwitter').show();
        $('#addScreenFacebook').hide();
    }
}

//Shows Facebook login screen if not already shown
function displayLoginScreenFacebook(){
    if ($('#addScreenFacebook').css("display") == 'none') {
        $('#addScreenFacebook').show();
        $('#addScreenTwitter').hide();
    }
}


//Toggles display popup for user to type in post
function displayPostPopup(){
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
      console.log(data);
    }
  });
}

//Loads Facebook feeds from server
//Post request used to get list of posts
function loadFacebookFeed()
{
    $.ajax({
        type: "POST",
        url: "/facebook_request/",
        data: { title: "ajax call from facebook",
		type: "feedRequest"},
        datatype: "json",
        error: function (data) { alert('Error:' + data); },
        success: function (data) {
	    $('#facebookFeed').empty();
            for(var i = 0; i < data.updates.length; i++){
                createPostInFacebookFeed(data.updates[i][0], data.updates[i][2], data.updates[i][1]);
            }
        }
    });
}


//Creates a pop in the social media feed with the given parameters
function createPostInFacebookFeed(message, time, person){
    var date = new Date(time * 1000);
    var formattedDate = (date.toLocaleString().substring(0,3) + ' ' + 
			 date.toLocaleTimeString());
    
    $('#facebookFeed').append('<div class ="FeedPost">' +
                      '<img src="/static/img/FacebookLogo.jpg" class="logo" alt="Facebook"/>' +
                      '<div class="nameTime">' + person + ' - ' + formattedDate + '</div><div class="message">' + message + '</div></div>');
}

function loadTwitterFeed()
{
    $.ajax({
        type: "POST",
        url: "/twitter_request/",
        data: { type: "feedRequest" },
        datatype: "json",
        error: function (data) { alert('Error:' + data); },
        success: function (data) {
            $('#twitterFeed').empty();
	    var posts = JSON.parse(data);
            for(var i = 0; i < posts.tweets.length; i++){
                createPostInTwitterFeed(posts.tweets[i].text, posts.tweets[i].created_at , posts.tweets[i].user.name)
	    }
        }
    });
}

function createPostInTwitterFeed(message, time, person){
    $('#twitterFeed').append('<div class ="FeedPost">' +
                    '<img src="/static/img/TwitterLogo.jpg" class="logo" alt="Facebook"/>' +
                    '<div class="nameTime">' + person + ' - ' + time + '</div><div class="message">' + message + '</div></div>');
}
