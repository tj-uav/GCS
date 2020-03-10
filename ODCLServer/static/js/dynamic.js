function createImageContainer(data){
	let image = document.createElement("img");
	image.src = `${data.img_path}`;
	image.style.width = 200 + "px";
	image.style.height = 200 + "px";
	return image;
}


function createPositionContainer(data){
	let container = $("<div></div>").addClass("positionContainer");
	let header = $("<h4></h4>").text("Position Information: ");
	let latitude = $("<p></p>").text("Latitude: " + data['latitude']);
	let longitude = $("<p></p>").text("Longitude: " + data['longitude']);
	let altitude = $("<p></p>").text("Altitude: " + data['altitude']);
	container.append(header, latitude, longitude, altitude);
	return container;
}


function createTextContainer(data, editable, num){
	let textContainer = $("<div></div>").addClass("textContainer");
	let caption = $("<figcaption></figcaption>").text("Submission Request: " + num);

	let infoContainer = $("<div></div>").addClass("infoContainer");
	let shapeContainer = $("<div></div>").addClass("shapeContainer");
	let shapeLabel = $("<h4></h4>").text("Shape Information: ");

	let [shape, shape_color] = [undefined, undefined];
	if(editable){
		console.log(data.shape);
		shape = createDropdown(SHAPES, 'shape_select').val(data.shape);
		shape_color = createDropdown(COLORS, 'shape_color_select').val(data.shapeColor);
	}
	else{
		shape = $("<p></p>").text("Shape: " + data.shape);
		shape_color = $("<p></p>").text("Color: " + data.shape);
	}

	shapeContainer.append(shapeLabel, shape, shape_color);

	let alphaContainer = $("<div></div>").addClass("alphaContainer");
	let alphaLabel = $("<h4></h4>").text("Alphanumeric Information: ");

	let [alpha, alpha_color] = [undefined, undefined];
	if(editable){
		alpha = createDropdown(ALPHANUMERICS, 'alpha_select').val(data.alphanumeric);
		alpha_color = createDropdown(COLORS, 'alpha_color_select').val(data.alphanumericColor);
	}
	else{
		alpha = $("<p></p>").text("Alphanumeric: " + data.alphanumeric);
		alpha_color = $("<p></p>").text("Color: " + data.alphanumericColor);
	}

	alphaContainer.append(alphaLabel, alpha, alpha_color);

	let positionContainer = createPositionContainer(data);
	infoContainer.append(shapeContainer, alphaContainer, positionContainer);

	textContainer.append(caption, infoContainer);
	return textContainer;
}


function createRequestButtons(data, parent){

	// Create submit and discard buttons
	let buttonContainer = $("<div></div>").addClass("buttonContainer");
	let submitButton = $("<button></button>").text("Submit");
	let discardButton = $("<button></button>").text("Discard");

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
	let parent = $("<div></div>").attr("id", "parent");
	let image = createImageContainer(data);
	let textContainer = createTextContainer(data, true, requests);
	let buttonContainer = createRequestButtons(data, parent);

	textContainer.append(buttonContainer);
	parent.append(image, textContainer);
	parent.data = data;
	return parent;
}


function createSubmission(parent){
	parent.find("select").prop("disabled", true);
	return parent;
}


function createDropdown(list, id){
	let dropdown = $("<select />").attr("id", id);
	for(let val of list){
		$("<option />", {value: val, text: val}).appendTo(dropdown);
	}
	return dropdown;
}
