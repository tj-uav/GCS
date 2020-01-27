let submissions = 0;
let submissionSet = new Set();

function addSubmission(data) {
	if(data["submitted"] == false){
		let parent = document.createElement("div")
		parent.id = "parent"
		parent.classList.add("submission")
		document.getElementById("submissions").appendChild(parent)

		let image = document.createElement("img")
		image.src = `${/*path*/data.img_path}`
		parent.appendChild(image)

		let textContainer = document.createElement("div")
		textContainer.classList.add("textContainer")
		parent.appendChild(textContainer)

		let captionContainer = document.createElement("div")
		let caption = document.createElement("figcaption")
		caption.textContent = `Submission ${++submissions}`
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

		let buttonContainer = document.createElement("div")
		buttonContainer.classList.add("buttonContainer")
		let submitButton = document.createElement("button")
		submitButton.classList.add("submitButton")
		submitButton.textContent = "Submit"

		let discardButton = document.createElement("button")
		discardButton.classList.add("discardButton")
		discardButton.textContent = "Discard"

		parent.accepted = false
//		parent.appendChild(accepted)
		submitButton.addEventListener('click', (e) => {
			data["submitted"] = true
			parent.accepted = true
			refresh()
			// submitSubmission(parent.id)
			// document.getElementById("submissions").style.display = 'none';
			// document.getElementById("submissions").style.display = 'block';
			alert(`You have just submitted! (but not actually)`)
		})
		buttonContainer.appendChild(submitButton)
		buttonContainer.appendChild(discardButton)
		textContainer.appendChild(buttonContainer)
	}
}

function submitSubmission(id) {
	var element = document.getElementById(id);
	element.parentNode.removeChild(element);
}

function refresh(){
	var images = document.getElementById("submissions").children
	for(var i = 0; i < images.length; i++){
		console.log(images[i]);
		if(images[i].accepted == true){
			images[i].style.display = 'none'
		}
	}
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
			console.log(data)
			for(let i = 0; i < data.length; i++){
				console.log(data[i]);
				let id = data[i]["id"]
				console.log(id);
				console.log(submissionSet.has(id));
				if(!submissionSet.has(id)){
					addSubmission(data[i])
					submissionSet.add(id)
				}
			}
		})
		.catch(function () {
			console.log("Error occured with data request");
		});
};
setInterval(fetchSubmission, 500)


/*
addSubmission("{{ url_for('static', filename='submit.jpg') }}", {
	shape: "circle",
	color: "orange"
}, {
	letter: "A",
	color: "blue"
}, {
	latitude: Math.round(Math.random() * 10000),
	longitude: Math.round(Math.random() * 10000),
	heading: Math.round(Math.random() * 360)
})
*/