var modal = document.getElementById("Modal");
var span = document.getElementsByClassName("close")[0];
span.onclick = function() {
  modal.style.display = "none";
}
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


function resend(email){
document.getElementById("button").classList.add('button-clicked');
document.getElementById("button").classList.remove('button');
document.getElementById("button").disabled = true;
document.getElementById("button").innerHTML = "Resend verification link (45)";

fetch('/resend/' + email)
  .then((response) => response.json())

var counter = 45;
var int = setInterval(function() {
    counter--;
  document.getElementById("button").innerHTML = "Resend verification link ("+counter+")";
  if (counter == 0) {
				
        clearInterval(int);
        document.getElementById("button").classList.remove('button-clicked');
        document.getElementById("button").classList.add('button');
        document.getElementById("button").disabled = false;
        document.getElementById("button").innerHTML = "Resend verification link";
  }
}, 1000)
}


function disable(){
    document.getElementById("sign-up").disabled = true;
    document.getElementById("sign-up").style.cursor = 'default';
    document.getElementById("sign-up").style.backgroundColor = '10bc7c';
    document.getElementById("sign-up").style.opacity = '0.6';
    document.getElementById("sign-up").value = "Signing up...";
    var counter = 5;
    var int = setInterval(function() {
        counter--;
    
      if (counter == 0) {
                    
            clearInterval(int);
            document.getElementById("sign-up").disabled = false;
            document.getElementById("sign-up").value = "Sign up";
            document.getElementById("sign-up").style.cursor = 'pointer';
            document.getElementById("sign-up").style.backgroundColor = '20cd8d';
            document.getElementById("sign-up").style.opacity = '1';
    
    
      }
    }, 1000)
    }

