function createImageContainer(data){
    console.log("Image path:");
    console.log(data.img_path);
	let img = $("<img />", {src: "/static/images/requests/" + data.img_path, style: "width: 200px; height: 200px"});
	return img;
}

function createPositionContainer(data){
	let container = $("<div />", {class: "positionContainer"});
	let header = $("<h4 />", {text: "Position Information: "});
	let latitude = $("<p />", {text: "Latitude: " + data['latitude'], id: "latitude"});
	let longitude = $("<p />", {text: "Longitude: " + data['longitude'], id: "longitude"});
	let altitude = $("<p />", {text: "Altitude: " + data['altitude'], id: "altitude"});
	container.append(header, latitude, longitude, altitude);
	return container;
}


function createTextContainer(data, num){
	let textContainer = $("<div />", {class: "textContainer"});
	let caption = $("<figcaption />", {text: "Submission Request " + num});

	let infoContainer = $("<div />", {class: "infoContainer"});
	let shapeContainer = $("<div />");
	let shapeLabel = $("<h4 />", {text: "Shape Information "});

	let shape = createDropdown(SHAPES, 'shape_select').val(data.shape);
	let shape_color = createDropdown(COLORS, 'shape_color_select').val(data.shapeColor);

	shapeContainer.append(shapeLabel, shape, shape_color);

	let alphaContainer = $("<div />");
	let alphaLabel = $("<h4 />", {text: "Alphanumeric Information"});

	let alpha = createDropdown(ALPHANUMERICS, 'alpha_select').val(data.alphanumeric);
	let alpha_color = createDropdown(COLORS, 'alpha_color_select').val(data.alphanumericColor);

	alphaContainer.append(alphaLabel, alpha, alpha_color);

	let positionContainer = createPositionContainer(data);
	infoContainer.append(shapeContainer, alphaContainer, positionContainer);

	textContainer.append(caption, infoContainer);
	return textContainer;
}


function createRequestButtons(data, parent){

	// Create submit and discard buttons
	let buttonContainer = $("<div />", {class: "buttonContainer"});
	let submitButton = $("<button />", {text: "Submit"});
	let discardButton = $("<button />", {text: "Discard"});

	parent.prop("accepted", false);
	parent.prop("discarded", false);

	submitButton.click(function() {
		data["submitted"] = true;
		parent.prop("accepted", true);
	});

	discardButton.click(function() {
		data["discarded"] = true;
		parent.prop("discarded", true);
	});

	buttonContainer.append(submitButton, discardButton);
	return buttonContainer;
}


function createRequestBlock(data){
	let parent = $("<div />", {id: "parent"});
	let image = createImageContainer(data);
	let textContainer = createTextContainer(data, requests);
	let buttonContainer = createRequestButtons(data, parent);

	textContainer.append(buttonContainer);
	parent.append(image, textContainer);
	parent.data("data", data);
	return parent;
}


function createDropdown(list, id){
	let dropdown = $("<select />", {id: id});
	for(let val of list){
		$("<option />", {value: val, text: val}).appendTo(dropdown);
	}
	return dropdown;
}

function openTab(evt, tabName) {
	// Hide all tabs and make them active, then show the tab that was clicked on and declare it as active
	console.log("Opened: " + tabName);
	$(".tabcontent").css("display", "none");
	$(".tablinks").removeClass("active");
	$("#" + tabName).css("display", "block");
	$("#" + tabName + "_btn").addClass("active");
}

function postData(url, dict){
	$.ajax({
		url: url,
		type: 'POST',
		dataType: 'json',
		data: JSON.stringify(dict),
		contentType: "application/json; charset=UTF-8"
	})
	.done(function (data) {
		// do stuff here
//		console.log("Successfully posted data");
//		console.log(data);
	})
	.fail(function (err) {
//		console.log("Failed to post data");
//		console.log(err);
	})
	.always(function (info) {
		// Fill this out if we wanna always be doing something
	});
}
