const IMG_FILENAME = 'image';
const IMG_EXTENSION = '.jpg';

var subCount, imgNum, highest;

const SHAPE_OPTIONS = ["Circle", "Semicircle", "Quarter_circle", "Triangle", "Square", "Rectangle", "Trapezoid", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Star", "Cross"];
const COLOR_OPTIONS = ["Black", "Gray", "White", "Red", "Blue", "Green", "Brown", "Orange", "Yellow", "Purple"];
const ALPHA_OPTIONS =['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];

function previous() {
	if(imgNum <= 1){
		return;
	}
	imgNum -= 1;
	setImage(imgNum);
}
function next() {
	if(imgNum >= highest){
		return;
	}
	imgNum += 1;
	setImage(imgNum);
}
function gotoImage(value) {
	imgNum = Math.min(Math.max(parseInt(value), 0), highest);
	setImage(imgNum);
}

// Python side should handle getting gps data for the image, this only returns img filename and crop coords
function send() {
	let img = $("#myImage");
	let rb = $("#rubberBand");
	let [width, height] = [img.attr("width"), img.attr("height")].map(toint);

	let dict = {};
	dict['img_num'] = imgNum;
	dict['x'] = parseInt(rb.css("left")) / width;
	dict['y'] = parseInt(rb.css("top")) / width;
	dict['w'] = parseInt(rb.css("width")) / width;
	dict['h'] = parseInt(rb.css("height")) / width;
	server_post('/receiver/', dict);
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
	imgNum = 0;
	highest = 0;
	setInterval(fetchData, 500);
    $("#myImage").mousedown(startRubber);
    $("#myImage").mouseup(stopRubber);
};