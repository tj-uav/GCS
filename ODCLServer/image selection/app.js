//  variable with rectangle information //
//  note: this defines the center of the rectangle stroke //
let rect = {}

let image = new Image()
let rectCanvas = document.createElement("canvas")
let rectContext = rectCanvas.getContext('2d')
rectCanvas.id = 'rectCanvas'
let clicks = []

importImage('../Unknown.jpg', 960, 640)

document.querySelector('body').appendChild(rectCanvas)
document.querySelector('body').appendChild(image)



//  handle mouse movement  //
window.addEventListener('mousemove', e => {
	handleMove({
		x: Math.min(e.clientX, rectCanvas.width),
		y: Math.min(e.clientY, rectCanvas.height)
	}, e)
})



//  handle click //
window.addEventListener('mousedown', e => {
	clicks.push({
		x: Math.min(e.clientX, rectCanvas.width),
		y: Math.min(e.clientY, rectCanvas.height)
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
function importImage(path, width, height) {
	rectCanvas.width = image.width = width
	rectCanvas.height = image.height = height
	image.src = path
}