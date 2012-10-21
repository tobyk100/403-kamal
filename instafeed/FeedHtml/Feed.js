window.onload = function () {
    $('#post').bind('click', displayPostPopup);
    $('#submitPost').bind('click', submitAndResetPost)
    $('#facebookRefresh').bind('click', loadFacebookFeed);
    $('#twitterRefresh').bind('click', loadTwitterFeed);
}

function displayPostPopup(){
    //alert($('#postMessage').css("display"));
    if ($('#postPopup').css("display") == 'none') {
        $('#postPopup').show();
    } else {
        $('#postPopup').hide();
    }
}

function submitAndResetPost() {
    $('#postText').val('');
    //AJAX REQUEST TO DJANGO
}

function loadFacebookFeed()
{
    createPostInFacebookFeed("Sample message", "3:59", "Brandon");    
}

function createPostInFacebookFeed(message, time, person){
    $('#facebookFeed').append('<div class ="FeedPost"><img src="FacebookLogo.jpg" class="logo" alt="Facebook"/><div class="NameTime">' + person + ' - ' + time + '</div><div class="Message">' + message + '</div></div>');
}

function loadTwitterFeed()
{
    createPostInTwitterFeed("stry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s", "3:59", "Brandon");    
} 

function createPostInTwitterFeed(message, time, person){
    $('#twitterFeed').append('<div class ="FeedPost"><img src="TwitterLogo.jpg" class="logo" alt="Facebook"/><div class="NameTime">' + person + ' - ' + time + '</div><div class="Message">' + message + '</div></div>');
} 