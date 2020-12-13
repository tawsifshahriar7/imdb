let addmoviebox = document.getElementById("new_movie");
let addshowbox = document.getElementById("new_show");
let addceleb_box = document.getElementById("new_celeb");

let btn1 = document.getElementById("addmovie_btn");
let btn2 = document.getElementById("addshow_btn");
let btn3 = document.getElementById("addceleb_btn");

let span1 = document.getElementsByClassName("close")[0];
let span2 = document.getElementsByClassName("close")[1];
let span3 = document.getElementsByClassName("close")[2];

btn1.onclick = function() {
  addmoviebox.style.display = "block";
}

btn2.onclick = function() {
  addshowbox.style.display = "block";
}

btn3.onclick = function() {
  addceleb_box.style.display = "block";
}

span1.onclick = function() {
  addmoviebox.style.display = "none";
}

span2.onclick = function() {
  addshowbox.style.display = "none";
}

span3.onclick = function() {
  addceleb_box.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == addmoviebox) {
    addmoviebox.style.display = "none";
  }
}

window.onclick = function(event) {
  if (event.target == addshowbox) {
    addshowbox.style.display = "none";
  }
}

window.onclick = function(event) {
  if (event.target == addceleb_box) {
    addceleb_box.style.display = "none";
  }
}