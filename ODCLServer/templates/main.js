let submissions = 0;
let submissionSet = new Set();

function refresh(){
	var images = document.getElementById("submissions").children
	for(var i = 0; i < images.length; i++){
//		console.log(images[i]);
		if(images[i].accepted == true || images[i].discarded == true){
			images[i].style.display = 'none'
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
//			if (data["id"] < submissions) {
//				return;
//			}
//			console.log(data.length);
			for(let i = 0; i < data.length; i++){
//				console.log("Looping")
//				console.log(i);
				let id = data[i]["id"]
//				console.log(id);
//				console.log(submissionSet.has(id));
				if(!submissionSet.has(id)){
					addSubmissionRequest(data[i])
					submissionSet.add(id)
				}
			}
		})
		.catch(function () {
//			console.log("Error occured with data request");
		});
};
setInterval(fetchSubmission, 500)











function addSubmissionRequest(data) {
//	console.log("ADDING")
//	console.log(data);
	if(data["submitted"] == false){
		submissions++;

		let parent = createSubmissionRequestBlock(data);

		// Add the parent div to the div containing the list of submission requests
		parent.classList.add("submission")
		document.getElementById("submissions").appendChild(parent)	

//		textContainer.appendChild(buttonContainer)
	}
	console.log("HI")
}

function createImageContainer(data){
	let image = document.createElement("img")
	image.src = `${/*path*/data.img_path}`
	return image;
}

function createTextContainer(data){
	let textContainer = document.createElement("div")
	textContainer.classList.add("textContainer")

	let captionContainer = document.createElement("div")
	let caption = document.createElement("figcaption")
	caption.textContent = `Submission Request ${submissions}`
	captionContainer.appendChild(caption)
	textContainer.appendChild(captionContainer)

	let infoContainer = document.createElement("div")
	infoContainer.classList.add("infoContainer")
	textContainer.appendChild(infoContainer)

	let shapeContainer = document.createElement("div")
	shapeContainer.classList.add("shapeContainer")
	let shapeLabel = document.createElement("h4")
	shapeLabel.textContent = `Shape Information: `
	shapeContainer.appendChild(shapeLabel)
	let shape = document.createElement("p")
	shape.textContent = `Shape: ${data.shape}`
	shapeContainer.appendChild(shape)
	let shape_color = document.createElement("p")
	shape_color.textContent = `Color: ${data.shapeColor}`
	shapeContainer.appendChild(shape_color)
	infoContainer.appendChild(shapeContainer)

	let letterContainer = document.createElement("div")
	letterContainer.classList.add("letterContainer")
	let letterLabel = document.createElement("h4")
	letterLabel.textContent = `Letter Information: `
	letterContainer.appendChild(letterLabel)
	let letter = document.createElement("p")
	letter.textContent = `Alphanumeric: ${data.alphanumeric}`
	letterContainer.appendChild(letter)
	let letter_color = document.createElement("p")
	letter_color.textContent = `Color: ${data.alphanumericColor}`
	letterContainer.appendChild(letter_color)
	infoContainer.appendChild(letterContainer)

	let positionContainer = document.createElement("div")
	positionContainer.classList.add("positionContainer")
	let positionLabel = document.createElement("h4")
	positionLabel.textContent = `Position Information: `
	positionContainer.appendChild(positionLabel)
	let latitude = document.createElement("p")
	latitude.textContent = `Latitude: ${data.latitude}`
	positionContainer.appendChild(latitude)
	let longitude = document.createElement("p")
	longitude.textContent = `Longitude: ${data.longitude}`
	positionContainer.appendChild(longitude)
	let heading = document.createElement("p")
	heading.textContent = `Heading: ${data.orientation}`
	positionContainer.appendChild(heading)
	infoContainer.appendChild(positionContainer)

	return textContainer;
}

function createSubmissionRequestButtons(parent){

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
			// submitSubmission(parent.id)
			// document.getElementById("submissions").style.display = 'none';
			// document.getElementById("submissions").style.display = 'block';
			alert('You have just submitted! (but not actually)')
		})

		discardButton.addEventListener('click', (e) => {
			data["discarded"] = true
			parent.discarded = true
			refresh()
			alert('You have just discarded!')
		})

		buttonContainer.appendChild(submitButton)
		buttonContainer.appendChild(discardButton)
		buttonContainer.classList.add("buttonContainer")

		return buttonContainer;
}

function createSubmissionRequestBlock(data){

	let parent = document.createElement("div")
	parent.id = "parent"

	let image = createImageContainer(data);
	parent.appendChild(image)

	let textContainer = createTextContainer(data);
	parent.appendChild(textContainer)

	let buttonContainer = createSubmissionRequestButtons(parent);
	textContainer.appendChild(buttonContainer);
	parent.appendChild(textContainer);

	return parent;
}

function createSubmissionBlock(data){
	let parent = document.createElement("div")
	parent.id = "parent"

	let image = createImageContainer(data);
	parent.appendChild(image)

	let textContainer = createTextContainer(data);
	parent.appendChild(textContainer)

	let buttonContainer = createSubmissionButtons(parent);
	textContainer.appendChild(buttonContainer);
	parent.appendChild(textContainer);

	return parent;
}