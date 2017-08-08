// Grab elements, create settings, etc.


var home = document.getElementById("vid_container");
var snap_txt  = document.getElementById("snap_txt");
var video = document.createElement('video');
var checkbox = document.createElement('checkbox');
var videoSelect = document.querySelector('select#videoSource');

video.id = "video";
video.width = "640";
video.height = "480";
video.autoplay = true;
// Elements for taking the snapshot
var canvas = document.createElement('canvas');
canvas.id = "canvas";
canvas.width = "640";
canvas.height = "480";


var context = canvas.getContext('2d');
var csrftoken = $.cookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

var errorCallback = function(e) {
    $('#snap_txt').text("Can't connect to media");
   console.log('Reeeejected!', e);
 };


 navigator.mediaDevices.enumerateDevices()
     .then(gotDevices).then(getStream).catch(handleError);

videoSelect.onchange = getStream;

 function gotDevices(deviceInfos) {
   for (var i = 0; i !== deviceInfos.length; ++i) {
     var deviceInfo = deviceInfos[i];
     var option = document.createElement('option');
   option.value = deviceInfo.deviceId;

     if (deviceInfo.kind === 'videoinput') {
       option.text = deviceInfo.label || 'camera ' +
       (videoSelect.length + 1);
       videoSelect.appendChild(option);

     } else {
       console.log('Found ome other kind of source/device: ', deviceInfo);
     }
   }
 }


 function getStream() {
   if (window.stream) {
     window.stream.getTracks().forEach(function(track) {
       track.stop();
     });
   }

   var constraints = {
     video: {
       optional: [{
         sourceId: videoSelect.value
       }]
     }
   };

   navigator.mediaDevices.getUserMedia(constraints).
       then(gotStream).catch(handleError);
 }

 function gotStream(stream) {
   window.stream = stream; // make stream available to console
   video.srcObject = stream;
   vide.play();
   home.appendChild(video);
   home.appendChild(canvas);
   setupSnapAndAjaxPost();
 }

 function handleError(error) {
   console.log('Error: ', error);
     $('#snap_txt').text("Camera not avaliable...");
 }


/*if (hasGetUserMedia()) {
  navigator.getUserMedia({video: true, audio: false}, function(localMediaStream) {
    home.appendChild(video);
    home.appendChild(canvas);
    video.src = window.URL.createObjectURL(localMediaStream);
    // Note: onloadedmetadata doesn't fire in Chrome when using it with getUserMedia.
    // See crbug.com/110938.
    video.onloadedmetadata = function(e) {
      setupSnapAndAjaxPost();
    };
  }, errorCallback);


} else {
  $('#snap_txt').text("getUserMedia() is not supported in your browser");
}

*/
function hasGetUserMedia() {
  return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

function setupSnapAndAjaxPost() {
  // Trigger photo take
  document.getElementById("video").addEventListener("click", function() {
  context.drawImage(video, 0, 0, 640, 480);
  //tutaj trzeba przekazac url do image file canvas.toDataURL()
  // trzeba to zrobic przez posta z url zdjecia i update form'a z nowym zdjeciem

    var img_data = {
              id: id,
              id_t: id_t,
              img_base64: canvas.toDataURL('image/png')
          };

    $('#snap_txt').text('Great! Sending snap...')

    $.ajax({
           type:"POST",
           url:"/inventory/"+ id + "/tree/"+id_t+"/snap/",
           dataType: "json",
           data: JSON.stringify(img_data),
           success: function(data) {

             if (data.redirect) {
                $('#snap_txt').text('Redirecting...');
                 window.location.replace(data['redirect']);
             }
           },
           error: function(xhr, textStatus, errorThrown){
             console.log(xhr.statusText);
              console.log(textStatus);
              console.log(errorThrown);
           }
    });
  });
}



/* Legacy code below: getUserMedia
else if(navigator.getUserMedia) { // Standard
    navigator.getUserMedia({ video: true }, function(stream) {
        video.src = stream;
        video.play();
    }, errBack);
} else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
    navigator.webkitGetUserMedia({ video: true }, function(stream){
        video.src = window.webkitURL.createObjectURL(stream);
        video.play();
    }, errBack);
} else if(navigator.mozGetUserMedia) { // Mozilla-prefixed
    navigator.mozGetUserMedia({ video: true }, function(stream){
        video.src = window.URL.createObjectURL(stream);
        video.play();
    }, errBack);
}
*/
