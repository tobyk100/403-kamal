window.onload = function () {
    var string = document.URL;
    var array = string.split("#");
    var token = array[1].split("&");
    var accessToken = token[0].split("=");

    $.ajax({
        type: "POST",
        url: "/facebook_access/",
        data: { token: accessToken[1] },
        datatype: "json",
        error: function (data) {
            console.log('Error:', data);
        },
        success: function (data) {
	    $(location).attr('href', window.location.href + "accounts/");
        }
    });
}
