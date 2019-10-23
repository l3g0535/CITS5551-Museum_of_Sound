// This example uses MediaRecorder to record from a live audio stream,
// and uses the resulting blob as a source for an audio element.
//
// The relevant functions in use are:
//
// navigator.mediaDevices.getUserMedia -> to get audio stream from microphone
// MediaRecorder (constructor) -> create MediaRecorder instance for a stream
// MediaRecorder.ondataavailable -> event to listen to when the recording is ready
// MediaRecorder.start -> start recording
// MediaRecorder.stop -> stop recording (this will generate a blob of data)
// URL.createObjectURL -> to create a URL from a blob, which we can use as audio src

// from feathers browser database API



var recordButton, stopButton, recorder, sendButton;
var interval = undefined;
var startTimeInt = 10;
var currentTimeInt = startTimeInt;

window.onload = function () {
  recordButton = document.getElementById('record');
  stopButton = document.getElementById('stop');
  sendButton = document.getElementById('send');
  sendButton.disabled = true;

  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    recordButton.disabled = false;

    // recordButton.addEventListener('click', startRecording);
    // stopButton.addEventListener('click', stopRecording);

    recordButton.addEventListener('click', function() {
      startRecording();
      startRecordingLabel();
    });
    stopButton.addEventListener('click', function() {
      stopRecording();
      endRecordingLabel();
    });


    recorder = new MediaRecorder(stream);

    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available
    recorder.addEventListener('dataavailable', onRecordingReady);
  });
};

function startRecording() {
  recordButton.disabled = true;
  stopButton.disabled = false;
  sendButton.disabled = true;

  recorder.start();
}

function stopRecording() {
  recordButton.disabled = false;
  stopButton.disabled = true;
  sendButton.disabled = false;
  // Stopping the recorder will eventually trigger the `dataavailable` event and we can complete the recording process
  recorder.stop();



  // var soundURL = document.getElementById('audio').currentSrc;
  // document.getElementById('recordingURL').innerHTML = soundURL;
}

function onRecordingReady(e) {
  var audio = document.getElementById('audio');
  // e.data contains a blob representing the recording
  audio.src = URL.createObjectURL(e.data);
  audio.play();

  var sound_name = audio.src.slice(10);
  sendButton.addEventListener('click', function() {
    var descrip = document.getElementById("desc").value;
    console.log(descrip);
    sendToDatabase(sound_name);
    afterSending();
  });

  document.getElementById('recordingURL').innerHTML = sound_name;
}

function startRecordingLabel() {
  document.getElementById('recording').innerHTML = "Recording audio..."
}

function endRecordingLabel() {
  document.getElementById('recording').innerHTML = "";
}

function afterSending() {
  recordButton.disabled = false;
  stopButton.disabled = false;
  sendButton.disabled = true;
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendToDatabase(sound_file_name, description) {
  var csrftoken = getCookie('csrftoken');
   $.ajax({
    type: 'POST',
    url: '/user_upload/',
    data: {
      filename: sound_file_name,
      description: 'description',
      csrfmiddlewaretoken: csrftoken
    },
    success: function(responseData, textStatus, jqXHR) {
        var value = responseData.someKey;
    },
    error: function (responseData, textStatus, errorThrown) {
        alert('POST failed.');
    }
});
 }
