// Grab elements, create settings, etc.


var home = document.getElementById("vid_container");
var snap_txt  = document.getElementById("snap_txt");
var video = document.createElement('video');
video.id = "video";
video.width = "640";
video.height = "480";
// Elements for taking the snapshot
var canvas = document.createElement('canvas');
canvas.id = "canvas";
canvas.width = "640";
canvas.height = "480";


var context = canvas.getContext('2d');
var para = document.createElement("p");
var node = document.createTextNode("Can't access camera.");
para.appendChild(node);

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

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        home.appendChild(video);
        home.appendChild(canvas);
        // Trigger photo take
        document.getElementById("video").addEventListener("click", function() {
        context.drawImage(video, 0, 0, 640, 480);
        //tutaj trzeba przekazac url do image file canvas.toDataURL()
        // trzeba to zrobic przez posta z url zdjecia i update form'a z nowym zdjeciem

        video.width = "0";
        video.height = "0";

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
        video.src = window.URL.createObjectURL(stream);
        video.play();
    }).catch(function(err) {
        node.nodeValue= err.name;
        home.appendChild(para);
    });
} else {
    node.nodeValue= "Can't connect to meadi";
    home.appendChild(para);
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
