// function doStuff(){
//   let preview = document.getElementById('preview');
//   let x = 50;
//   let y = 50;
//   let width = 50;
//   let height = 50;
//   crop(x,y,width,height,preview);
// }
//
// function crop(x,y,width,height,preview){
//   imageClipper('../assets/images/generictarget.jpg', function() {
//       this.crop(x, y, width, height)
//       .toDataURL(function(dataUrl) {
//           console.log('cropped!');
//           preview.src = dataUrl;
//       });
//   });
// }
//
// crop(50,50,50,50,document.getElementById('preview'));
// imageClipper('../assets/images/generictarget.jpg', function() {
//     this.crop(100, 100, 100, 100)
//     .toDataURL(function(dataUrl) {
//         console.log('cropped!');
//         preview.src = dataUrl;
//     });
// });
