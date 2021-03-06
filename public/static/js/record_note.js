var langs = ['Polski',['pl-PL']]


var notes = $("textarea#id_notes");


showInfo('info_start');

var create_email = false;
var final_transcript = '';
var recognizing = false;
var ignore_onend;
var start_timestamp;
if (!('webkitSpeechRecognition' in window)) {
  upgrade();
} else {
  start_button.style.display = 'inline-block';
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;
  recognition.onstart = function() {
    recognizing = true;
    showInfo('info_speak_now');
    document.getElementById("start_button").className = "btn btn-block btn-danger btn-lg";

  };

  recognition.onerror = function(event) {
    if (event.error == 'no-speech') {
      document.getElementById("start_button").className = "btn btn-block btn-success btn-lg";
      showInfo('info_no_speech');
      ignore_onend = true;
    }
    if (event.error == 'audio-capture') {
      document.getElementById("start_button").className = "btn btn-block btn-success btn-lg";
      showInfo('info_no_microphone');
      ignore_onend = true;
    }
    if (event.error == 'not-allowed') {
      if (event.timeStamp - start_timestamp < 100) {
        showInfo('info_blocked');
      } else {
        showInfo('info_denied');
      }
      ignore_onend = true;
    }
  };

  recognition.onend = function() {
    recognizing = false;
    if(final_transcript != "")
      notes.val( notes.val() + final_transcript + ". " );
    if (ignore_onend) {
      return;
    }
    document.getElementById("start_button").className = "btn btn-block btn-success btn-lg";
    if (!final_transcript) {
      showInfo('info_start');
      return;
    }
    showInfo('info_start');
    if (window.getSelection) {
      window.getSelection().removeAllRanges();
      var range = document.createRange();
      range.selectNode(document.getElementById('final_span'));
      window.getSelection().addRange(range);
    }
    if (create_email) {
      create_email = false;
      createEmail();
    }
  };

  recognition.onresult = function(event) {
    var interim_transcript = '';
    if (typeof(event.results) == 'undefined') {
      recognition.onend = null;
      recognition.stop();
      upgrade();
      return;
    }
    for (var i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    final_transcript = capitalize(final_transcript);
    final_span.innerHTML = linebreak(final_transcript);
    interim_span.innerHTML = linebreak(interim_transcript);

  };
}

function upgrade() {
  start_button.style.visibility = 'hidden';
  showInfo('info_upgrade');
}

var two_line = /\n\n/g;
var one_line = /\n/g;
function linebreak(s) {
  return s.replace(two_line, '<p></p>').replace(one_line, '<br>');
}

var first_char = /\S/;
function capitalize(s) {
  return s.replace(first_char, function(m) { return m.toUpperCase(); });
}

function createEmail() {
  var n = final_transcript.indexOf('\n');
  if (n < 0 || n >= 80) {
    n = 40 + final_transcript.substring(40).indexOf(' ');
  }
  var subject = encodeURI(final_transcript.substring(0, n));
  var body = encodeURI(final_transcript.substring(n + 1));
  window.location.href = 'mailto:?subject=' + subject + '&body=' + body;
}

function startButton(event) {
  if (recognizing) {
    recognition.stop();
    return;
  }
  final_transcript = '';
  recognition.lang = "pl-PL";
  recognition.start();
  ignore_onend = false;
  final_span.innerHTML = '';
  interim_span.innerHTML = '';
  start_button.val = '/intl/en/chrome/assets/common/images/content/mic-slash.gif';
  showInfo('info_allow');

  start_timestamp = event.timeStamp;
}

function showInfo(s) {
  if (s) {
    for (var child = info.firstChild; child; child = child.nextSibling) {
      if (child.style) {
        child.style.display = child.id == s ? 'block' : 'none';
      }
    }
    info.style.visibility = 'visible';
  } else {
    info.style.visibility = 'hidden';
  }
}
