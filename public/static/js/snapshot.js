// Grab elements, create settings, etc.


var home = document.getElementById("vid_container");
var snap_txt  = document.getElementById("snap_txt");
var video = document.createElement('video');

var videoSelect = document.querySelector('select#videoSource');

video.id = "video";
video.autoplay = true;
// Elements for taking the snapshot
var canvas = document.createElement('canvas');
canvas.id = "canvas";



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



 if (hasGetUserMedia()) {

   navigator.mediaDevices.enumerateDevices()
       .then(gotDevices).then(getStream).catch(handleError);

  videoSelect.onchange = getStream;

  home.appendChild(video);

  setupSnapAndAjaxPost();

 } else {
   errorCallback
 }




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
       facingMode: { exact: "environment" },
       {minWidth: 320},
         {minWidth: 640},
         {minWidth: 1024},
         {minWidth: 1280},
         {minWidth: 1920},
         {minWidth: 2560},

     }
   };

   navigator.mediaDevices.getUserMedia(constraints).
       then(gotStream).catch(handleError);

 }

 function gotStream(stream) {
   window.stream = stream; // make stream available to console
   video.srcObject = stream;
   video.play();

 }

 function handleError(error) {
   console.log('Error: ', error);
     $('#snap_txt').text("Camera not avaliable...");
 }

 var errorCallback = function(e) {
     $('#snap_txt').text("Can't connect to media");
    console.log('Reeeejected!', e);
  };

function hasGetUserMedia() {
  return !!(navigator.getUserMedia || navigator.webkitGetUserMedia ||
            navigator.mozGetUserMedia || navigator.msGetUserMedia);
}

function setupSnapAndAjaxPost() {
  // Trigger photo take
  document.getElementById("video").addEventListener("click", function() {

  canvas.height = video.videoHeight;
  canvas.width = video.videoWidth;
   $(video).hide();
  console.log('Width ', video.videoWidth );

  home.appendChild(canvas);
  context.drawImage(video, 0, 0);
  //tutaj trzeba przekazac url do image file canvas.toDataURL()
  // trzeba to zrobic przez posta z url zdjecia i update form'a z nowym zdjeciem

    var img_data = {
              id: id,
              id_t: id_t,
              img_base64: canvas.toDataURL('image/jpeg')
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
            $('#snap_txt').text(errorThrown);
             console.log(xhr.statusText);
              console.log(textStatus);
              console.log(errorThrown);
           }
    });
  });
}
