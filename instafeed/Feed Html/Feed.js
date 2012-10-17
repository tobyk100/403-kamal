window.onload = function () {
    $('#post').bind('click', displayPostPopup);
    $('#submitPost').bind('click', submitAndResetPost)

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