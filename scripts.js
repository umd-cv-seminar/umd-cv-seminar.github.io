/* https://www.w3schools.com/howto/howto_js_collapsible.asp */

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
      this.innerHTML = "Click to expand abstract";
    } else {
      content.style.display = "block";
      this.innerHTML = "Click to collapse abstract";
    }
  });
} 