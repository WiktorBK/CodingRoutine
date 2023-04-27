var modal = document.getElementById("Modal");
var span = document.getElementsByClassName("close")[0];
var btn = document.getElementById("button-cancel")
span.onclick = function() {modal.style.display = "none";}
btn.onclick = function() {modal.style.display = "none";}

function display(){modal.style.display = "block";}

window.onclick = function(event)
 {if (event.target == modal) {
    modal.style.display = "none";}}

function delete_message(message_id) {
    location.href = "http://localhost:8000/administration/messages/" + message_id + "/delete";
}