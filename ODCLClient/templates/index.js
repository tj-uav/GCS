const IMG_FILENAME = '';
const IMG_EXTENSION = '.jpg';

var IMG, subCount, currNum, lowest, highest;

var IMG = document.getElementById('myImage');
IMG.onmousedown = startRubber;
IMG.onmouseup = stopRubber;
var subCount = 0;
var currNum = 0;
var lowest = 0;
var highest = 0;

const SHAPE_OPTIONS = ["Circle", "Semicircle", "Quarter_circle", "Triangle", "Square", "Rectangle", "Trapezoid", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Star", "Cross"];
const COLOR_OPTIONS = ["Black", "Gray", "White", "Red", "Blue", "Green", "Brown", "Orange", "Yellow", "Purple"];
var ALPHA_OPTIONS =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
resetDropdowns();
	

function previous() {
	currNum -= 1;
	setImageCurr();
}
function next() {
	currNum += 1;
	setImageCurr();
}
function setImageCurr() {
	img_filename = '../assets/img/' + IMG_FILENAME + currNum + IMG_EXTENSION;
	IMG.src = img_filename;
	document.getElementById("current_index").innerHTML = currNum + "";
}
function gotoImage(value) {
	currNum = parseInt(value);
	setImageCurr();
}

function openTab(evt, tabName) {
	// Get all elements with class="tabcontent" and hide them
	console.log(tabName);
	let tabcontent = document.getElementsByClassName("tabcontent");
	for (let i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}
	// Get all elements with class="tablinks" and remove the class "active"
	let tablinks = document.getElementsByClassName("tablinks");
	for (let i = 0; i < tablinks.length; i++) {
		tablinks[i].className = tablinks[i].className.replace(" active", "");
	}
	// Show the current tab, and add an "active" class to the button that opened the tab
	document.getElementById(tabName).style.display = "block";
	evt.currentTarget.className += " active";
}

function addToDropdown(select, option_text, option_value) {
	let option = document.createElement('option');
	option.appendChild(document.createTextNode(option_text));
	option.value = option_value;
	select.appendChild(option);
}

function resetDropdowns() {
	var shape_dropdown = document.getElementById("shape_dropdown");
	for (let i = 0; i < SHAPE_OPTIONS.length; i++) {
		addToDropdown(shape_dropdown, SHAPE_OPTIONS[i], SHAPE_OPTIONS[i].toUpperCase());
	}
	
	var alpha_dropdown = document.getElementById("alpha_dropdown");
	for (let i = 0; i < ALPHA_OPTIONS.length; i++) {
		addToDropdown(alpha_dropdown, ALPHA_OPTIONS[i], ALPHA_OPTIONS[i].toUpperCase());
	}
	var shape_color_dropdown = document.getElementById("shape_color_dropdown");
	var alpha_color_dropdown = document.getElementById("alpha_color_dropdown");
	for (let i = 0; i < COLOR_OPTIONS.length; i++) {
		addToDropdown(shape_color_dropdown, COLOR_OPTIONS[i], COLOR_OPTIONS[i].toUpperCase());
		addToDropdown(alpha_color_dropdown, COLOR_OPTIONS[i], COLOR_OPTIONS[i].toUpperCase());
	}
}

function getClosestOrientation(val) {
	let dirs = ["N", "NW", "W", "SW", "S", "E", "E", "NE"];
	let closestRotation = Infinity;
	let closestIndex = 0;
	for (let index = 0; index < dirs.length; index++) {
		let dist = Math.min(Math.abs(index * 45 - val), Math.abs(index * 45 + 360 - val));
		if (dist < closestRotation) {
			closestRotation = dist;
			closestIndex = index;
		}
	}
	return dirs[closestIndex];
}

function submit_standard() {
	let slide = document.getElementById("slide");
	let shape_dropdown = document.getElementById("shape_dropdown");
	let shape_color_dropdown = document.getElementById("shape_color_dropdown");
	let alpha_dropdown = document.getElementById("alpha_dropdown");
	let alpha_color_dropdown = document.getElementById("alpha_color_dropdown");
	let View = document.getElementById('cropView');
	console.log(View.src);
	
	let dict = {};
	dict['type'] = 'STANDARD';
	dict['latitude'] = 38.1443113;
	dict['longitude'] = -76.4257693;
	//  dict['orientation'] = getClosestOrientation(slide.value + gps["orientation"]);
	dict['orientation'] = getClosestOrientation(slide.value);
	dict['shape'] = shape_dropdown.value;
	dict['shapeColor'] = shape_color_dropdown.value;
	dict['alphanumeric'] = alpha_dropdown.value;
	dict['alphanumericColor'] = alpha_color_dropdown.value;
	dict['autonomous'] = false;
	
	add_submission(dict);
	let post_dict = {};
	post_dict['odcl'] = dict;
	post_dict['img_num'] = currNum;
	//  post_dict['img_url'] = View.src;
	
	let rb = document.getElementById("rubberBand");
	let crop_dict = {};
	let width_scale = 4208 / IMG.width;
	let height_scale = 3120 / IMG.height;
	
	console.log(parseInt(rb.style.left) / IMG.width);
	crop_dict['x'] = parseInt(rb.style.left) / IMG.width;
	crop_dict['y'] = parseInt(rb.style.top) / IMG.height;
	crop_dict['w'] = parseInt(rb.style.width) / IMG.width;
	crop_dict['h'] = parseInt(rb.style.height) / IMG.height;
	post_dict['img_crop'] = crop_dict;
	
	console.log(post_dict)
	server_post(post_dict)
}

function add_submission(dict, image) {
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
	fetch("http://localhost:5005/data")
	.then(function (response) {
		return response.json();
	})
	.then(function (data) {
		// Update the DOM
		console.log(data)
		highest = data['highest'];
		document.getElementById("highest_index").innerHTML = highest + "";
	})
	.catch(function () {
		console.log("Error occured with data request");
	});
};
setInterval(updateData, 500)

function server_post(post_dict) {
	$.ajax({
		url: 'receiver',
		type: 'POST',
		dataType: 'json',
		data: JSON.stringify(post_dict),
		contentType: "application/json; charset=UTF-8"
	})
	.done(function (data) {
		// do stuff here
		console.log("POSTED DATA");
		console.log(data);
	})
	.fail(function (err) {
		// do stuff here
	})
	.always(function (info) {
		// do stuff here
	});
}
