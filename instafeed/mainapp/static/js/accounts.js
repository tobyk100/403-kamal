$('#signinToTwitter').bind('click', signinToTwitter);
$('#signinToFacebook').bind('click', signinToFacebook);

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
            $(location).attr('href',data);
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

