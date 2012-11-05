window.onload = function () {
    alert(document.URL);
    var string = document.URL;
    var array = string.split("#");
    var token = array[1].split("&");
    alert(token[0]);
    var accessToken = token[0].split("=");
    
    $.ajax({
        type: "POST",
        url: "/facebook_access/",
        data: { token: accessToken[1] },
        datatype: "json",
        error: function (data) { alert('Error:' + data); },
        success: function (data) {
	    $(location).attr('href',"http://dry-peak-6840.herokuapp.com/accounts/");
        }
    }); 
}