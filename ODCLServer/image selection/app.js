//  variable with rectangle information //
//  note: this defines the center of the rectangle stroke //
let rect = {}
let clicks = []

let image = new Image()

let rectCanvas = document.createElement("canvas")
let rectContext = rectCanvas.getContext('2d')
rectCanvas.style.position = 'absolute'
rectCanvas.style.zIndex = image.style.zIndex + 1
rectCanvas.id = 'rectCanvas'

importImage('Unknown.jpg', 960, 640)

document.querySelector('body').appendChild(rectCanvas)
document.querySelector('body').appendChild(image)

let imageBorder = image.getBoundingClientRect()
console.log(imageBorder)

rectCanvas.style.top = imageBorder.top + 'px'
rectCanvas.style.left = imageBorder.left + 'px'

//  handle mouse movement  //
window.addEventListener('mousemove', e => {
	handleMove({
		x: clamp(0, e.clientX - imageBorder.left, rectCanvas.width),
		y: clamp(0, e.clientY - imageBorder.top, rectCanvas.height)
	}, e)
})



//  handle click //
window.addEventListener('mousedown', e => {
	clicks.push({
		x: clamp(0, e.clientX - imageBorder.left, rectCanvas.width),
		y: clamp(0, e.clientY - imageBorder.top, rectCanvas.height)
	})
})



//  clear on esc  //
window.addEventListener('keydown', e => {
	var key = e.which || e.keyCode
	if (key === 27) //if its escape
		rectContext.clearRect(0, 0, window.innerWidth, window.innerHeight)
	if (key === 13) //if its enter
		alert(`x: ${rect.x}\ny: ${rect.y}\nwidth: ${rect.width}\nheight: ${rect.height}`)
})


//  runs whenever mouse moves; draws preview rect  //
var handleMove = (mouse, e) => {
	if (clicks.length % 2 !== 0) {
		clear(e)
		let last = clicks.length - 1
		rect = {
			x: clicks[last].x,
			y: clicks[last].y,
			width: mouse.x - clicks[last].x,
			height: mouse.y - clicks[last].y
		}
		rectContext.strokeStyle = 'red'
		rectContext.lineWidth = 3
		rectContext.strokeRect(rect.x, rect.y, rect.width, rect.height)
		while (clicks.length >= 2)
			clicks.shift()
	}
}



//  clear the entire rect canvas  //
var clear = () => {
	rectContext.clearRect(0, 0, window.innerWidth, window.innerHeight)
}



//  import image  //
var importImage = (path, width, height) => {
	rectCanvas.width = image.width = width
	rectCanvas.height = image.height = height
	image.src = path
}


//  helper method  //
var clamp = (min, num, max) => {
	num = Math.min(num, max)
	num = Math.max(num, min)
	return num
}