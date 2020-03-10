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
		let shape = createDropdown(SHAPES, 'shape_select');
		shape.value = data.shape;
		shape.classList.add("shape");
		let shape_color = createDropdown(COLORS, 'shape_color_select');
		shape_color.value = data.shapeColor;
		shape_color.classList.add("shapeColor");
	}
	else{
		let shape = createParagraph(`Shape: ${data.shape}`);
		shape.classList.add("shape");
		let shape_color = createParagraph(`Color: ${data.shapeColor}`);
		shape_color.classList.add("shapeColor");
	}

	shapeContainer.append(shapeLabel, shape, shape_color);

	let alphaContainer = $("<div></div>").addClass("alphaContainer");
	let alphaLabel = $("<h4></h4>").text("Alphanumeric Information: ");

	let [alpha, alpha_color] = [undefined, undefined];
	if(editable){
		let alpha = createDropdown(ALPHANUMERICS, 'alpha_select');
		alpha.value = data.alphanumeric;
		alpha.classList.add("alpha");
		let alpha_color = createDropdown(COLORS, 'alpha_color_select');
		alpha_color.value = data.alphanumericColor;
		alpha_color.classList.add("alphaColor");
	}
	else{
		let alpha = createParagraph(`Alphanumeric: ${data.alphanumeric}`);
		alpha.classList.add("alpha");
		let alpha_color = createParagraph(`Color: ${data.alphanumericColor}`);
		alpha_color.classList.add("alphaColor");
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
//		refresh();
	});

	discardButton.click(function() {
		data["discarded"] = true;
		parent.prop("discarded", true);
//		refresh();
	});

	buttonContainer.append(submitButton, discardButton);
	return buttonContainer;
}


function createRequestBlock(data){

	console.log("Creating request block");

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

	let data = parent.data;

	let infoContainer = parent.getElementsByClassName('textContainer')[0].getElementsByClassName('infoContainer')[0];
	let shapeContainer = infoContainer.getElementsByClassName('shapeContainer')[0];
	let shape = shapeContainer.getElementsByClassName('shape')[0];
	let shape_color = shapeContainer.getElementsByClassName('shapeColor')[0];
	let alphaContainer = infoContainer.getElementsByClassName('alphaContainer')[0];
	let alpha = alphaContainer.getElementsByClassName('alpha')[0];
	let alpha_color = alphaContainer.getElementsByClassName('alphaColor')[0];

	data['shape'] = shape.value;
	data['shapeColor'] = shape_color.value;
	data['alphanumeric'] = alpha.value;
	data['alphanumericColor'] = alpha_color.value;

	let newparent = document.createElement("div");
	newparent.classList.add("submission");

	let image = createImageContainer(data);
	newparent.appendChild(image);

	let textContainer = createTextContainer(data, false, submissions);
	newparent.appendChild(textContainer);

	newparent.data = data;

	return newparent;
}


function createDropdown(list, id){
	let dropdown = document.createElement("select");
	dropdown.id = id;
	for(let i = 0; i < list.length; i++){
		let option = document.createElement("option");
		option.value = list[i];
		option.text = list[i];
		dropdown.appendChild(option);
	}
	return dropdown;
}
