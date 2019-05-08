var IMG;

function startRubber (evt) {
  console.log("Start");
  evt.preventDefault();
  var r = document.getElementById('rubberBand');
  r.style.width = 0;
  r.style.height = 0;
  r.style.left = evt.clientX + 'px';
  r.style.top = evt.clientY + 'px';
  r.style.visibility = 'visible';
  r.onmouseup = stopRubber;
  r.onmousemove = moveRubber;
  IMG.onmousemove = moveRubber;
}

function moveRubber (evt) {
  console.log("Move");
  var r = document.getElementById('rubberBand');
  let tempLeft = parseInt(r.style.left);
  let tempTop = parseInt(r.style.top);
  if(tempLeft > evt.clientX || tempTop > evt.clientY){
    if(tempLeft > evt.clientX){
      r.style.left = evt.clientX;
      r.style.width = tempLeft - parseInt(r.style.left);
    }
    if(tempTop > evt.clientY){
      r.style.top = evt.clientY;
      r.style.height = tempTop - parseInt(r.style.top);
    }
  }
  else{
    r.style.width = evt.clientX - tempLeft;
    r.style.height = evt.clientY - tempTop;
  }
}

function stopRubber (evt) {
  console.log("Stop");
  IMG.onmousemove = null;
  var r = document.getElementById('rubberBand');
  r.onmousemove = null;
  r.onmousedown = startRubber;
}

function cancelDragDrop()
{
  console.log("Cancel");
  window.event.returnValue = false;
}

function rotate(deg){
	var preview = document.getElementById('cropView');
  string = 'rotate(' + deg + 'deg)'
  preview.style.transform = string;
}

function cropCoords(x, y ,width, height, imageSrc, preview, previewW, previewH){
  console.log('Cropping coords');
  console.log(x);
  imageClipper(imageSrc, function() {
      let temp = this.crop(x, y, width, height);
      temp.toDataURL(function(dataUrl) {
          console.log('cropped!');
          preview.src = dataUrl;
          preview.width = previewW;
          preview.height = previewH;
          let padHeight = parseInt((230 - previewH)/2);
          let padWidth = parseInt(20 + Math.max(previewW, previewH)/2);
          preview.style.padding = padHeight + " " + padWidth + "px";
      });
  });
}

function crop(){
  console.log('Cropping');
  let rb = document.getElementById("rubberBand");
  let preview = document.getElementById("cropView");
  let image = document.getElementById("myImage");
  let bar = document.getElementById("slideGroup");
  bar.style.display = "block";
  let x = parseInt(rb.style.left);
  let y = parseInt(rb.style.top);
  let w = parseInt(rb.style.width);
  let h = parseInt(rb.style.height);
  let imageSrc = image.src;
  let oriX = parseInt(x * image.naturalWidth / image.width)
  let oriY = parseInt(y * image.naturalHeight / image.height)
  let oriW = parseInt(w * image.naturalWidth / image.width)
  let oriH = parseInt(h * image.naturalHeight / image.height)

  let larger = Math.max(w,h);
  let previewW = 230 * w / (1.5 * larger);
  let previewH = 230 * h / (1.5 * larger);

  console.log(previewW);
  cropCoords(oriX, oriY, oriW, oriH, imageSrc, preview, previewW, previewH);
  console.log('Done');
}

IMG = document.getElementById('myImage');
IMG.onmousedown = startRubber;
IMG.onmouseup = stopRubber;
