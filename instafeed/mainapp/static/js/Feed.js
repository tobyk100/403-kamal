window.onload = function () {
    bindButtons();
}

//Binds all appropriate buttons with clicks
function bindButtons(){
    $('#postButton').bind('click', displayPostPopup);
    $('#accountsButton').bind('click', directToAccounts);
    $('#dashboardButton').bind('click', directToDashboard)
    $('#submitPostButton').bind('click', submitAndResetPost);
    $('#facebookRefreshButton').bind('click', loadFacebookFeed);
    $('#twitterRefreshButton').bind('click', loadTwitterFeed);
}
//Toggles display popup for user to type in post
function displayPostPopup(){
    if ($('#postPopup').css("display") == 'none') {
        $('#postPopup').show();
    } else {
        $('#postPopup').hide();
    }
}

//Directs the User to the Account Page
function directToAccounts() {
    var url = "/Accounts.html";    
    $(location).attr('href',url);
}

//Directs the User to the Account Page
function directToDashboard() {
    var url = "/Feed.html";    
    $(location).attr('href',url);
}

//Submits a post using an ajax request.
//On callback return clears the text area so they can enter in another post
function submitAndResetPost() {
    alert($('#postText').val());
    //AJAX REQUEST TO DJANGO
    //$.post('post', 
    //    { 
    //        message : $('#postText').val() 
    //    },
    //    function(data,status){
    //        alert("Data: " + data + "\nStatus: " + status);
    //        $('#postText').val('');
    //    });   
}

//Loads Facebook feeds from server
//Post request used to get list of posts
function loadFacebookFeed()
{
   $.post('facebook_request', 
       {
           message : "Get Facebook Feed"
       },
       function(data,status){
           alert("Data: " + data + "\nStatus: " + status);
           //parse data and call createPostInFacebookFeed
       });    
    //createPostInFacebookFeed("Sample message", "3:59", "Brandon");    
}


//Creates a pop in the social media feed with the given parameters
function createPostInFacebookFeed(message, time, person){
    $('#facebookFeed').append('<div class ="feedPost">' +
                      '<img src="FacebookLogo.jpg" class="logo" alt="Facebook"/>' +
                      '<div class="nameTime">' + person + ' - ' + time + '</div><div class="message">' + message + '</div></div>');
}

function loadTwitterFeed()
{
    createPostInTwitterFeed("stry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s", "3:59", "Brandon");    
} 

function createPostInTwitterFeed(message, time, person){
    $('#twitterFeed').append('<div class ="feedPost">' +
                    '<img src="TwitterLogo.jpg" class="logo" alt="Facebook"/>' +
                    '<div class="nameTime">' + person + ' - ' + time + '</div><div class="message">' + message + '</div></div>');
} 