var IMG;

function init(){
  SHAPE_OPTIONS = ["Circle", "Semicircle", "Quarter_circle", "Triangle", "Square", "Rectangle", "Trapezoid", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Star", "Cross"]
  COLOR_OPTIONS = ["Black", "Gray", "White", "Red", "Blue", "Green", "Brown", "Orange", "Yellow", "Purple"]
  ALPHA_OPTIONS = []
  for(let i = 0; i < 26; i++){
    ALPHA_OPTIONS.push(String.fromCharCode(i+65));
  }
  for(let i = 0; i < 10; i++){
    ALPHA_OPTIONS.push(String.fromCharCode(i+48));
  }
  resetDropdowns();

  IMG = document.getElementById('myImage');
  IMG.onmousedown = startRubber;
  IMG.onmouseup = stopRubber;
}

init();

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;
  // Get all elements with class="tabcontent" and hide them
  console.log(tabName);
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

function addToDropdown(select, option_text, option_value){
  let option = document.createElement('option');
  option.appendChild(document.createTextNode(option_text));
  option.value = option_value;
  select.appendChild(option);
}

function resetDropdowns(){
  var shape_dropdown = document.getElementById("shape_dropdown");
  for(let i = 0; i < SHAPE_OPTIONS.length; i++){
    addToDropdown(shape_dropdown, SHAPE_OPTIONS[i], SHAPE_OPTIONS[i].toUpperCase());
  }

  var alpha_dropdown = document.getElementById("alpha_dropdown");
  for(let i = 0; i < ALPHA_OPTIONS.length; i++){
    addToDropdown(alpha_dropdown, ALPHA_OPTIONS[i], ALPHA_OPTIONS[i].toUpperCase());
  }
  var shape_color_dropdown = document.getElementById("shape_color_dropdown");
  var alpha_color_dropdown = document.getElementById("alpha_color_dropdown");
  for(let i = 0; i < COLOR_OPTIONS.length; i++){
    addToDropdown(shape_color_dropdown, COLOR_OPTIONS[i], COLOR_OPTIONS[i].toUpperCase());
    addToDropdown(alpha_color_dropdown, COLOR_OPTIONS[i], COLOR_OPTIONS[i].toUpperCase());
  }
}




















/*
var updateData = function() {
    fetch("http://localhost:5000/data")
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Update the DOM

        })
        .catch(function() {
            console.log("Error occured with data request");
        });
};
*/
//setInterval(updateData, 5);
