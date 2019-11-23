let submissions = 0

function addSubmission(path, shape_info, letter_info, position_info) {
	let parent = document.createElement("div")
	parent.classList.add("submission")
	document.getElementById("submissions").appendChild(parent)

	let image = document.createElement("img")
	image.src = `${path}`
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
	shape.textContent = `Shape: ${shape_info.shape}`
	shapeContainer.appendChild(shape)
	let shape_color = document.createElement("p")
	shape_color.textContent = `Color: ${shape_info.color}`
	shapeContainer.appendChild(shape_color)
	infoContainer.appendChild(shapeContainer)

	let letterContainer = document.createElement("div")
	letterContainer.classList.add("letterContainer")
	let letterLabel = document.createElement("h4")
	letterLabel.textContent = `Letter Information: `
	letterContainer.appendChild(letterLabel)
	let letter = document.createElement("p")
	letter.textContent = `Alphanumeric: ${letter_info.letter}`
	letterContainer.appendChild(letter)
	let letter_color = document.createElement("p")
	letter_color.textContent = `Color: ${letter_info.color}`
	letterContainer.appendChild(letter_color)
	infoContainer.appendChild(letterContainer)

	let positionContainer = document.createElement("div")
	positionContainer.classList.add("positionContainer")
	let positionLabel = document.createElement("h4")
	positionLabel.textContent = `Position Information: `
	positionContainer.appendChild(positionLabel)
	let latitude = document.createElement("p")
	latitude.textContent = `Latitude: ${position_info.latitude}`
	positionContainer.appendChild(latitude)
	let longitude = document.createElement("p")
	longitude.textContent = `Longitude: ${position_info.longitude}`
	positionContainer.appendChild(longitude)
	let heading = document.createElement("p")
	heading.textContent = `Heading: ${position_info.heading}`
	positionContainer.appendChild(heading)
	infoContainer.appendChild(positionContainer)

	let submitContainer = document.createElement("div")
	submitContainer.classList.add("submitContainer")
	let submitButton = document.createElement("button")
	submitButton.classList.add("submitButton")
	submitButton.textContent = "Submit"
	submitButton.addEventListener('click', (e) => {
		alert(`You have just submitted! (but not actually)`)
	})
	submitContainer.appendChild(submitButton)
	textContainer.appendChild(submitContainer)
}

for (let i = 0; i < 5; i++) {
	addSubmission("submit.jpg", {
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
}