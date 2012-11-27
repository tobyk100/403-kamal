$(document).ready(onload);

function onload(){
    $('#signinToTwitter').bind('click', signinToTwitter);
    $('#signinToFacebook').bind('click', signinToFacebook);
    $('#signinToGooglePlus').bind('click', signinToGooglePlus);
}

function signinToTwitter() {
   $.ajax({
        type: "POST",
        url: "/twitter_signin/",
        data: {
            title: "begin twitter signin process"
        },
        datatype: "json",
        error: function (data) {
            console.log('Error:', data);
        },
        success: function (data) {
            if (data.success) {
              $(location).attr('href', data);
            }
        }
    });
}

function signinToFacebook() {
   $.ajax({
        type: "POST",
        url: "/facebook_signin/",
        data: {
            title: "begin facebook signin process"
        },
        datatype: "json",
        error: function (data) {
            console.log('Error:', data);
        },
        success: function (data) {
            $(location).attr('href',data);
        }
    });
}

function signinToGooglePlus() {
   $.ajax({
        type: "POST",
        url: "/google_signin/",
        data: {
            title: "begin google signin process"
        },
        datatype: "json",
        error: function (data) {
            alert(JSON.parse(data.responseText).message)
            console.log('Error:', data);
        },
        success: function (data) {
            $(location).attr('href', data);
        }
    });
}
