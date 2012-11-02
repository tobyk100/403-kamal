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
            alert('URL: ' + data);
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
            alert('URL: ' + data);
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
    alert($('#postText').val());
    //AJAX REQUEST TO DJANGO
    $.ajax({
	   	type:"POST",
		url:"/facebook_request/",
		data:{ message: $('#postText').val(),
                type: "upload" },
        datatype:"json",
        error:function(data){alert('Error:'+data);},
        success:function(data){
                    alert('Message Posted!');
                    $('#postText').val("");
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
        data: { title: "ajax call from facebook" },
        datatype: "json",
        error: function (data) { alert('Error:' + data); },
        success: function (data) {
            alert('OK! ' + data);
	    //TODO loop through json and call function with data
            createPostInFacebookFeed("Sample message", "3:59", "Brandon");
        }
    });
}


//Creates a pop in the social media feed with the given parameters
function createPostInFacebookFeed(message, time, person){
    $('#facebookFeed').append('<div class ="FeedPost">' +
                      '<img src="/static/img/FacebookLogo.jpg" class="logo" alt="Facebook"/>' +
                      '<div class="nameTime">' + person + ' - ' + time + '</div><div class="message">' + message + '</div></div>');
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
            alert('OK! ' + data);
	    //loop through json
	    //extrax message, time, author and pass to function
            createPostInTwitterFeed("Sample message", "3:59", "Brandon");
        }
    });
}

function createPostInTwitterFeed(message, time, person){
    $('#twitterFeed').append('<div class ="FeedPost">' +
                    '<img src="/static/img/TwitterLogo.jpg" class="logo" alt="Facebook"/>' +
                    '<div class="nameTime">' + person + ' - ' + time + '</div><div class="message">' + message + '</div></div>');
}

