var IMG;
var subCount;
const IMG_FILENAME = '';
const IMG_EXTENSION = '.PNG';
var IMG;
var currNum = 0;
var lowest = 0;
var highest = 100;

function init(){
  currNum = 0;
  lowest = 0;
  highest = 0;
  document.getElementById("lowest_index").innerHTML = lowest + "";
  document.getElementById("current_index").innerHTML = currNum + "";
  document.getElementById("highest_index").innerHTML = highest + "";

  subCount = 0;
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

function previous(){
  if(currNum > lowest + 1){
    currNum -= 1;
    setImageCurr();
  }
}

function next(){
  console.log('hi')
  if(currNum < highest){
    currNum += 1;
    setImageCurr();
  }
}

function setImageCurr(){
  img_filename = '../assets/img/' + IMG_FILENAME + currNum + IMG_EXTENSION;
  IMG.src = img_filename;
  document.getElementById("current_index").innerHTML = currNum + "";
}

function gotoBoundary(inp){
  let val = parseInt(inp.value);
  val = Math.max(lowest, val);
  val = Math.min(highest,val);
}

function gotoImage(value){
  let val = parseInt(value);
  currNum = val;
  setImageCurr();
}

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

function getClosestOrientation(val){
  let dirs = ["n", "ne", "e", "se", "s", "sw", "w", "nw"];
  let closestRotation = Infinity;
  let closestIndex = 0;
  for(let index = 0; index < dirs.length; index++){
    let dir = dirs[index];
    let dist = Math.min(Math.abs(index * 45 - val), Math.abs(index * 45 + 360 - val));
    if(dist < closestRotation){
      closestRotation = dist;
      closestIndex = index;
    }
  }
  return dirs[closestIndex];
}

function submit_standard(){
  console.log("yee")
  let slide = document.getElementById("slide");
  let shape_dropdown = document.getElementById("shape_dropdown");
  let shape_color_dropdown = document.getElementById("shape_color_dropdown");
  let alpha_dropdown = document.getElementById("alpha_dropdown");
  let alpha_color_dropdown = document.getElementById("alpha_color_dropdown");
  let View = document.getElementById('cropView');
  let dict = {};
  dict['type'] = 'STANDARD';
  dict['latitude'] = 0;
  dict['longitude'] = 0;
//  dict['orientation'] = getClosestOrientation(slide.value + gps["orientation"]);
  dict['orientation'] = getClosestOrientation(slide.value);
  dict['shape'] = shape_dropdown.value;
  dict['shapeColor'] = shape_color_dropdown.value;
  dict['alphanumeric'] = alpha_dropdown.value;
  dict['alphanumericColor'] = alpha_color_dropdown.value;
  dict['autonomous'] = false;
  add_submission(dict);
  server_post({})
  console.log("haw")
}

function add_submission(dict, image){
  let div = document.createElement("div");
  div.id = "subDiv" + subCount;
  div.style.padding = "10 10px";

  let subHeader = document.createElement("header");
  subHeader.textContent = 'Submission #' + subCount;

  let subImg = document.createElement("img");
  subImg.src = document.getElementById("cropView").src;
  subImg.width = 100;
  subImg.height = 100;
  subImg.style.float = "left";

  let textDiv = document.createElement("div");
  textDiv.classList.add("submissionRow");

  let shapeDiv = document.createElement("div");
  shapeDiv.classList.add("column");
  shapeDiv.style.backgroundColor = "aaa";
  shapeDiv.id = "shapeDiv";

  let classHeader = document.createElement("h3");
  classHeader.textContent = "Classification:";

  let classText = document.createElement("p");
  classText.setAttribute('style', 'white-space: pre;');
  classText.textContent = 'Shape: ' + dict['shape'] + '\r\n';
  classText.textContent += 'Color: ' + dict['shapeColor'] + '\r\n';
  classText.textContent += 'Alphanumeric: ' + dict['alphanumeric'] + '\r\n';
  classText.textContent += 'Alphanumeric Color: ' + dict['alphanumericColor'] + '\r\n';
  classText.textContent += 'Orientation: ' + dict['orientation'];

  let alphaDiv = document.createElement("div");
  alphaDiv.classList.add("column");
  alphaDiv.style.backgroundColor = "bbb";

  shapeDiv.appendChild(classHeader);
  shapeDiv.appendChild(classText);

  textDiv.appendChild(shapeDiv);

  div.appendChild(subHeader);
  div.appendChild(subImg);
  div.appendChild(textDiv);
  document.getElementById("Submissions").appendChild(div);
  subCount++;
}

var updateData = function () {
  fetch("http://localhost:5000/data")
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      // Update the DOM
      highest = data['highest'];
      document.getElementById("highest_index").innerHTML = highest + "";
      document.getElementById('image_slide').max = highest;
    })
    .catch(function () {
      console.log("Error occured with data request");
    });
};
setInterval(updateData, 500)

function server_post(post_dict){
  $.ajax({
      url: 'receiver',
      type: 'POST',
      dataType: 'json',
      data: JSON.stringify(post_dict),
      contentType:"application/json; charset=UTF-8"
  })
  .done(function(data) {
      // do stuff here
      console.log("POSTED DATA");
      console.log(data);
  })
  .fail(function(err) {
      // do stuff here
  })
  .always(function(info) {
      // do stuff here
  });
}