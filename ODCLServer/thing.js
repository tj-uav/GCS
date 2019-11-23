var submissions = 0

var parent = document.createElement("div")
parent.classList.add("submission")
document.getElementById("submissions").appendChild(parent)

function addSubmission(image_path) {
	let image = document.createElement("img")
	image.src = `${image_path}`
	parent.appendChild(image)

	let caption = document.createElement("figcaption")
	caption.textContent = `Submission ${++submissions}`
	parent.appendChild(caption)
}

addSubmission("submit.jpg")