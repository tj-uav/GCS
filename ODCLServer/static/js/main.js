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
		if(parent.attr("discarded")){
			parent.remove();
		}
		else if(parent.attr("accepted")){
			submissions++;
			accepted.append(parent);
			parent.remove();
		}
	});
}

function openTab(evt, tabName) {
	// Hide all tabs and make them active, then show the tab that was clicked on and declare it as active
	console.log("Opened: " + tabName);
	$(".tabcontent").css("display", "none");
	$(".tablinks").removeClass("active");
	$("#" + tabName).css("display", "block");
	$("#" + tabName + "_btn").addClass("active");
}
  

var fetchSubmission = function () {
	fetch("http://localhost:5000/post")
		.then(function (response) {
			return response.json();
		})
		.then(function (data) {
			for(let i = 0; i < data.length; i++){
				let id = data[i]["id"]
				if(!requestSet.has(id)){
					addRequest(data[i])
					requestSet.add(id)
				}
			}
		})
		.catch(function (err) {
			console.log("Error occured with data request");
			console.log(err.message);
		});
};
setInterval(fetchSubmission, 2000)
console.log("HI");

function addRequest(data) {
	assert(data["submitted"] == false, "ERROR OCCURED W/ ASSERTION");
	requests++;
	let parent = createRequestBlock(data).addClass("submission");
	$("#requests").append(parent);
}