window.onload = function () {
    alert(document.URL);
    var string = document.URL;
    var array = string.split("#");
    var token = array[1].split("&");
    alert(token[0]);
}