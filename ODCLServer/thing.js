let submissions = 0

function addSubmission(image_path) {
	var parent = document.createElement("div")
	parent.classList.add("submission")
	document.getElementById("submissions").appendChild(parent)

	let image = document.createElement("img")
	image.src = `${image_path}`
	parent.appendChild(image)

	let caption = document.createElement("figcaption")
	caption.textContent = `Submission ${++submissions}`
	parent.appendChild(caption)
}

for (let i = 0; i < 5; i++) {
	addSubmission("submit.jpg")
}