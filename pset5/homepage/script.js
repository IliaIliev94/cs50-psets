

var btn = document.querySelector('.button1');
var input = document.querySelector('input');
function validateForm(e){
    e.preventDefault();
    if(input.value === ''){
        window.alert("Invlaid e-mail");
        input.focus();
    } else{
        form.submit();
    }
}
var form = document.querySelector('form');
form.addEventListener('submit', validateForm);

var currentImage = document.querySelector("#big-image");
function changeImage(e){
    var source = e.target.getAttribute("src");
    currentImage.setAttribute("src", source);
}
var img = document.querySelector(".bottom-images");
img.addEventListener("click", changeImage);