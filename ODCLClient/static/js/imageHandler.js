var IMG;

function toint (x) {
    return parseInt(x, 10);
}

function startRubber (evt) {
    evt.preventDefault();
    $("#rubberBand").width(0).height(0).left(evt.clientX + 'px').top(evt.clientY + 'px');
    $("#rubberBand").visibility('visible');
    $("#rubberBand").mouseup(stopRubber);
    $("#rubberBand").mouseup(moveRubber);
    IMG.onmousemove = moveRubber;
}

function moveRubber (evt) {
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
    IMG.onmousemove = null;
    var r = document.getElementById('rubberBand');
    r.onmousemove = null;
    r.onmousedown = startRubber;
}

function rotate(deg){
    var preview = document.getElementById('cropView');
    string = 'rotate(' + deg + 'deg)';
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
    let rb = $("#rubberBand");
    let preview = $("#cropView");
    let image = $("#myImage");
    let bar = $("#sliderGroup");
    bar.style("display", "block");
    let [x, y, w, h] = [rb.style.left, rb.style.top, rb.style.width, rb.style.height].map(toint);
    let imageSrc = image.src();
    let [scaleX, scaleY] = [image.naturalWidth / image.width, image.naturalHeight / image.height];
    let [oriX, oriY, oriW, oriH] = [x*scaleX, y*scaleY, w*scaleX, h*scaleY].map(toint);

    let larger = Math.max(w,h);
    let previewW = 230 * w / (1.5 * larger);
    let previewH = 230 * h / (1.5 * larger);

    cropCoords(oriX, oriY, oriW, oriH, imageSrc, preview, previewW, previewH);
}

window.onload = () => {
    IMG = document.getElementById('myImage');
    IMG.onmousedown = startRubber;
    IMG.onmouseup = stopRubber;
};