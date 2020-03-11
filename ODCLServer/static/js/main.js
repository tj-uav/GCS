let requests = 0;
let submissions = 0;
let requestSet = new Set();

var SHAPES = ['CIRCLE', 'SEMICIRCLE', 'QUARTER CIRCLE', 'TRIANGLE', 'SQUARE', 'RECTANGLE', 'TRAPEZOID', 'PENTAGON', 'HEXAGON', 'HEPTAGON', 'OCTAGON', 'STAR', 'CROSS'];
var COLORS = ['WHITE', 'BLACK', 'GRAY', 'RED', 'BLUE', 'GREEN', 'BROWN', 'ORANGE', 'YELLOW', 'PURPLE'];
var ALPHANUMERICS = [];
for(let i = 0; i < 26; i++){
	ALPHANUMERICS.push(String.fromCharCode(i+65));
}
for(let i = 0; i < 10; i++){
	ALPHANUMERICS.push(String.fromCharCode(i+48));
}

function refresh(){
	let accepted = $("#accepted");
	let requests = $("#requests");
	requests.children().each( function() {
		let parent = $(this);
		if(parent.prop("discarded")){
			console.log("Discarded");
			parent.remove();
		}
		else if(parent.prop("accepted") == true){
			console.log("Accepted");
			submissions++;
			parent.find("select").prop("disabled", true);
			submitRequest(parent);
			parent.remove();
			accepted.append(parent);
		}
	});
}


function addRequest(data) {
	requests++;
	let parent = createRequestBlock(data).addClass("submission");
	$("#requests").append(parent);
	$(".submission button").click(refresh);
}


function fetchRequests () {
	fetch("http://localhost:5000/post")
		.then(function (response) {
			return response.json();
		})
		.then(function (data) {
			for(let i = 0; i < data.length; i++){
				let id = data[i]["id"];
				if(!requestSet.has(id)){
					addRequest(data[i]);
					requestSet.add(id);
				}
			}
		})
		.catch(function (err) {
			console.log("Error occured with data request");
			console.log(err);
		});
}


function submitRequest(parent){
	// Extract data from dropdowns and whatnot
	let shape = parent.find("#shape_select").val();
	let shape_color = parent.find("#shape_color_select").val();
	let alpha = parent.find("#alpha_select").val();
	let alpha_color = parent.find("#alpha_color_select").val();
	let latitude = parent.data("data").latitude;
	let longitude = parent.data("data").longitude;
	let altitude = parent.data("data").altitude;

	let data = {"shape": shape, "shape_color": shape_color, "alpha": alpha, "alpha_color": alpha_color, "latitude": latitude, "longitude": longitude, "altitude": altitude};
	postData("/test/", data);
}

window.onload = function() {
	setInterval(fetchRequests, 500);
};