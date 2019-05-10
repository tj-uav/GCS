//const COMMS_SOCKET = new WebSocket('ws://127.0.0.1:5000')
const IMG_FILENAME = 'image_';
const IMG_EXTENSION = '.PNG';
var IMG;
var currNum = 0;
var lowest = 0;
var highest = 0;

function init(){
  currNum = 0;
  lowest = 0;
  highest = 0;
  IMG = document.getElementById('myImage');
  document.getElementById("lowest_index").innerHTML = lowest + "";
  document.getElementById("current_index").innerHTML = currNum + "";
  document.getElementById("highest_index").innerHTML = highest + "";
//  IMG.src = 'assets/img/' + IMG_FILENAME + currNum + IMG_EXTENSION;
}

function previous(){
  if(currNum > lowest){
    currNum -= 1;
    img_filename = '../assets/img/' + IMG_FILENAME + currNum + IMG_EXTENSION;
    IMG.src = img_filename;
    document.getElementById("current_index").innerHTML = currNum + "";
  }
}

function send(){
  console.log('hi');
  sendData({"num":currNum});
}

function next(){
  console.log('hi')
  if(currNum < highest - 1){
    currNum += 1;
    img_filename = '../assets/img/' + IMG_FILENAME + currNum + IMG_EXTENSION;
    IMG.src = img_filename;
    document.getElementById("current_index").innerHTML = currNum + "";
  }
}

init();

var updateData = function() {
    fetch("http://localhost:5000/data")
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Update the DOM
            highest = data['highest'];
            document.getElementById("highest_index").innerHTML = highest + "";
        })
        .catch(function() {
            console.log("Error occured with data request");
        });
};

var doWork = function(){
  // ajax the JSON to the server
	$.post("receiver", data, function(){

	});
	// stop link reloading the page
 event.preventDefault();
}

setInterval(updateData, 1000);
//setInterval(sendData, 1000);
