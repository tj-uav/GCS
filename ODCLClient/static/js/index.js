const IMG_FILENAME = 'image';
const IMG_EXTENSION = '.jpg';

var subCount, currNum, highest;

const SHAPE_OPTIONS = ["Circle", "Semicircle", "Quarter_circle", "Triangle", "Square", "Rectangle", "Trapezoid", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Star", "Cross"];
const COLOR_OPTIONS = ["Black", "Gray", "White", "Red", "Blue", "Green", "Brown", "Orange", "Yellow", "Purple"];
const ALPHA_OPTIONS =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];


function previous() {
	if(currNum <= 1){
		return;
	}
	currNum -= 1;
	setImage(currNum);
}
function next() {
	if(currNum >= highest){
		return;
	}
	currNum += 1;
	setImage(currNum);
}
function gotoImage(value) {
	currNum = Math.min(Math.max(parseInt(value), 0), highest);
	setImage(currNum);
}

function submit_standard() {
	let post_dict = {};
	post_dict['img_num'] = currNum;

	let gps = gps_dict[currNum];

	let dict = {};
	dict['type'] = 'STANDARD';
	//38.1443113, -76.4257693
	dict['latitude'] = gps["latitude"];
	dict['longitude'] = gps["longitude"];
	dict['orientation'] = getClosestOrientation(slide.value + gps["yaw"]);
	dict['shape'] = document.getElementById("shape_dropdown").value;
	dict['shape_color'] = document.getElementById("shape_color_dropdown").value;
	dict['alphanumeric'] = document.getElementById("alpha_dropdown").value;
	dict['alphanumeric_color'] = document.getElementById("alpha_color_dropdown").value;
	dict['autonomous'] = false;
	
	post_dict['odcl'] = dict;
	
	let rb = document.getElementById("rubberBand");
	let crop_dict = {};
	let width_scale = 4208 / IMG.width;
	let height_scale = 3120 / IMG.height;
	
	crop_dict['x'] = parseInt(rb.style.left) / IMG.width;
	crop_dict['y'] = parseInt(rb.style.top) / IMG.height;
	crop_dict['w'] = parseInt(rb.style.width) / IMG.width;
	crop_dict['h'] = parseInt(rb.style.height) / IMG.height;
	post_dict['img_crop'] = crop_dict;
	
	server_post(post_dict);
	addSubmission(dict);
}

function addSubmission(dict, image) {
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

fetchData = function () {
	fetch("http://localhost:5000/data")
	.then(function (response) {
		return response.json();
	})
	.then(function (data) {
		// Update the DOM
		highest = data['highest'];
		$("#highest_index").text(highest + "");
	})
	.catch(function () {
		console.log("Error occured with data request");
	});
};

window.onload = () => {
	subCount = 0;
	currNum = 0;
	highest = 0;
	setInterval(fetchData, 500);
    $("#myImage").mousedown(startRubber);
    $("#myImage").mouseup(stopRubber);
	resetDropdowns();
};