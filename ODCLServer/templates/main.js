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
	let requests = document.getElementById("requests");
	let accepted = document.getElementById("accepted");
	let images = requests.children;
	console.log(images.length);
	for(let i = 0; i < images.length; i++){
		if(images[i].discarded == true){
			requests.removeChild(images[i]);
			i--;
		}
		else if(images[i].accepted == true){
			submissions++;
			let submission = createSubmission(images[i]);
			accepted.appendChild(submission);
			requests.removeChild(images[i]);
			i--;
		}
	}
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
		.catch(function () {
			console.log("Error occured with data request");
		});
};
setInterval(fetchSubmission, 500)











function addRequest(data) {
//	console.log("ADDING")
//	console.log(data);
	if(data["submitted"] == false){
		requests++;

		let parent = createRequestBlock(data);

		// Add the parent div to the div containing the list of submission requests
		parent.classList.add("submission")
		document.getElementById("requests").appendChild(parent)	

//		textContainer.appendChild(buttonContainer)
	}
	console.log("HI")
}

function createImageContainer(data){
	let image = document.createElement("img")
	image.src = `${/*path*/data.img_path}`
	image.style.width = 200 + "px";
	image.style.height = 200 + "px";
	return image;
}

function createPositionContainer(data){
	let positionContainer = document.createElement("div");
	positionContainer.classList.add("positionContainer");

	let positionLabel = createHeader(`Position Information: `);
	positionContainer.appendChild(positionLabel);

	let latitude = createParagraph(`Longitude: ${data.latitude}`);
	positionContainer.appendChild(latitude);

	let longitude = createParagraph(`Longitude: ${data.longitude}`);
	positionContainer.appendChild(longitude);

	let heading = createParagraph(`Heading: ${data.orientation}`);
	positionContainer.appendChild(heading);

	return positionContainer;
}

function createTextContainer(data, editable, num){
	let textContainer = document.createElement("div")
	textContainer.classList.add("textContainer")

	let caption = document.createElement("figcaption")
	caption.textContent = `Submission Request ${num}`

	let captionContainer = document.createElement("div")
	captionContainer.appendChild(caption)
	textContainer.appendChild(captionContainer)

	let infoContainer = document.createElement("div")
	infoContainer.classList.add("infoContainer")
	textContainer.appendChild(infoContainer)

	let shapeContainer = document.createElement("div")
	shapeContainer.classList.add("shapeContainer")

	let shapeLabel = createHeader(`Shape Information: `);
	shapeContainer.appendChild(shapeLabel)

	if(editable){
		let shape = createDropdown(SHAPES, 'shape_select');
		shape.value = data.shape;
		shape.classList.add("shape");
		let shape_color = createDropdown(COLORS, 'shape_color_select');
		shape_color.value = data.shapeColor;
		shape_color.classList.add("shapeColor");
		shapeContainer.appendChild(shape);
		shapeContainer.appendChild(shape_color);
	}
	else{
		let shape = createParagraph(`Shape: ${data.shape}`);
		shape.classList.add("shape");
		let shape_color = createParagraph(`Color: ${data.shapeColor}`);
		shape_color.classList.add("shapeColor");
		shapeContainer.appendChild(shape);
		shapeContainer.appendChild(shape_color);
	}

	infoContainer.appendChild(shapeContainer)

	let alphaContainer = document.createElement("div")
	alphaContainer.classList.add("alphaContainer")

	let alphaLabel = createHeader(`Alphanumeric Information: `);
	alphaContainer.appendChild(alphaLabel)

	if(editable){
		let alpha = createDropdown(ALPHANUMERICS, 'alpha_select');
		alpha.value = data.alphanumeric;
		alpha.classList.add("alpha");
		let alpha_color = createDropdown(COLORS, 'alpha_color_select');	
		alpha_color.value = data.alphanumericColor;
		alpha_color.classList.add("alphaColor");
		alphaContainer.appendChild(alpha);
		alphaContainer.appendChild(alpha_color);
	}
	else{
		let alpha = createParagraph(`Alphanumeric: ${data.alphanumeric}`);
		alpha.classList.add("alpha");
		let alpha_color = createParagraph(`Color: ${data.alphanumericColor}`);
		alpha_color.classList.add("alphaColor");
		alphaContainer.appendChild(alpha);
		alphaContainer.appendChild(alpha_color);
	}

	infoContainer.appendChild(alphaContainer)

	let positionContainer = createPositionContainer(data);
	infoContainer.appendChild(positionContainer)

	return textContainer;
}

function createRequestButtons(data, parent){

	// Create submit and discard buttons
	let buttonContainer = document.createElement("div")
	buttonContainer.classList.add("buttonContainer")
	let submitButton = document.createElement("button")
	submitButton.textContent = "Submit"

	let discardButton = document.createElement("button")
	discardButton.textContent = "Discard"

	parent.accepted = false
	parent.discarded = false

	submitButton.addEventListener('click', (e) => {
		data["submitted"] = true
		parent.accepted = true
		refresh()
		// submitRequest(parent.id)
		// document.getElementById("requests").style.display = 'none';
		// document.getElementById("requests").style.display = 'block';
		alert('Are you sure you want to submit this?')
	})

	discardButton.addEventListener('click', (e) => {
		data["discarded"] = true
		parent.discarded = true
		refresh()
		alert('Are you sure you want to discard this?')
	})

	buttonContainer.appendChild(submitButton)
	buttonContainer.appendChild(discardButton)
	buttonContainer.classList.add("buttonContainer")

	return buttonContainer;
}

function createRequestBlock(data){

	let parent = document.createElement("div")
	parent.id = "parent"

	let image = createImageContainer(data);
	parent.appendChild(image)

	let textContainer = createTextContainer(data, true, requests);
	parent.appendChild(textContainer)

	let buttonContainer = createRequestButtons(data, parent);
	textContainer.appendChild(buttonContainer);
	parent.appendChild(textContainer);

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

function createTextElement(elementType, text){
	let elem = document.createElement(elementType);
	elem.textContent = text;
	return elem;
}

function createParagraph(text){	return createTextElement("p", text); }
function createHeader(text){ return createTextElement("h4", text); }