// IMAGE HANDLER FUNCTIONS

function setImage(img_num) {
	$("#myImage").attr("src", "../static/images/original/" + IMG_FILENAME + img_num + IMG_EXTENSION);
	$("#current_index").text(img_num + "");
}

function startRubber (evt) {
    evt.preventDefault();
    console.log("Starting rubber");
    $("#rubberBand").css("width", 0).css("height", 0).css("left", evt.clientX + 'px').css("top", evt.clientY + 'px');
    $("#rubberBand").css("visibility", "visible");
    $("#rubberBand").mouseup(stopRubber);
    $("#myImage").mousemove(moveRubber);
}

function moveRubber (evt) {
    console.log("Moving rubber");
//    console.log(evt);
    let r = $("#rubberBand");
    let tempLeft = parseInt(r.css("left"));
    let tempTop = parseInt(r.css("top"));
    if(tempLeft > evt.clientX || tempTop > evt.clientY){
        if(tempLeft > evt.clientX){
            r.css("left", evt.clientX);
            r.css("width", tempLeft - parseInt(r.css("left")));
        }
        if(tempTop > evt.clientY){
            r.css("top", evt.clientY);
            r.css("height", tempTop - parseInt(r.css("top")));
        }
    }
    else{
        r.css("width", evt.clientX - tempLeft);
        r.css("height", evt.clientY - tempTop);
    }
}


function stopRubber (evt) {
    console.log("Stopping rubber");
    $("#myImage").off("mousemove").off("mouseup");
    $("#rubberBand").off("mousemove").off("mouseup");
}


function rotate(deg){
    let string = 'rotate(' + deg + 'deg)';
    $("#cropView").css("transform", string);
}

function cropCoords(x, y, width, height, imageSrc){
    imageClipper(imageSrc, function() {
        let temp = this.crop(x, y, width, height);
        temp.toDataURL(function(dataUrl) {
            console.log('cropped!');
            let preview = $("#cropView");
            preview.attr("src", dataUrl);
//            preview.src = dataUrl;
//            let padHeight = parseInt((230 - previewH)/2);
//            let padWidth = parseInt(20 + Math.max(previewW, previewH)/2);
//            preview.style.padding = padHeight + " " + padWidth + "px";
        });
    });
}

// OTHER FUNCTIONS

function toint (x) {
    return parseInt(x, 10);
}

function openTab(evt, tabName) {
	// Hide all tabs and make them active, then show the tab that was clicked on and declare it as active
	console.log("Opened: " + tabName);
	$(".tabcontent").css("display", "none");
	$(".tablinks").removeClass("active");
	$("#" + tabName).css("display", "block");
	$("#" + tabName + "_btn").addClass("active");
}


function postData(url, dict){
	$.ajax({
		url: url,
		type: 'POST',
		dataType: 'json',
		data: JSON.stringify(dict),
		contentType: "application/json; charset=UTF-8"
	})
	.done(function (data) {
		// do stuff here
//		console.log("Successfully posted data");
//		console.log(data);
	})
	.fail(function (err) {
//		console.log("Failed to post data");
//		console.log(err);
	})
	.always(function (info) {
		// Fill this out if we wanna always be doing something
	});
}
