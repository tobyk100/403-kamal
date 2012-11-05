window.onload = function () {
    alert(document.URL);
    var string = Document.URL;
    var array = string.split("#");
    var token = array[1].split("&");
    alert(token[0]);
}