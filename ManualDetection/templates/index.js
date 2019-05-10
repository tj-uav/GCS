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
    if(currNum > 20 && currNum - 20 > lowest){
      lowest = currNum - 20;
      document.getElementById("lowest_index").innerHTML = lowest + "";
      server_post({"lowest":lowest});
    }
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

/*
var server_post = function(post_dict){
  // ajax the JSON to the server
	$.post("receiver", post_dict, function(){

	});
	// stop link reloading the page
 event.preventDefault();
}
*/

function server_post(post_dict){
  $.ajax({
      url: 'receiver',
      type: 'POST',
      dataType: 'json',
      data: JSON.stringify(post_dict),
      contentType:"application/json; charset=UTF-8"
  })
  .done(function(data) {
      // do stuff here
      console.log("POSTED DATA");
      console.log(data);
  })
  .fail(function(err) {
      // do stuff here
  })
  .always(function(info) {
      // do stuff here
  });
}

setInterval(updateData, 1000);
//setInterval(sendData, 1000);
