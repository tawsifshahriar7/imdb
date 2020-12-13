let ratebox = document.getElementById("rateForm");

let reviewbox = document.getElementById("reviewForm");

let btn = document.getElementById("ratebtn");

let btn2 = document.getElementById("reviewbtn");

let  span = document.getElementsByClassName("close")[0];
let span2 = document.getElementsByClassName("close")[1];

btn.onclick = function() {
  ratebox.style.display = "block";
}

btn2.onclick = function() {
  reviewbox.style.display = "block";
}

span.onclick = function() {
  ratebox.style.display = "none";
}

span2.onclick = function() {
  reviewbox.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == ratebox) {
    ratebox.style.display = "none";
  }
}

window.onclick = function(event) {
  if (event.target == reviewbox) {
    reviewbox.style.display = "none";
  }
}
$("textarea").keyup(function(e) {
if(e.keyCode == 13) //13 is the ASCII code for ENTER
    {
        var rowCount = $(this).attr("rows");
        $(this).attr({rows: rowCount + 5});
    }
});