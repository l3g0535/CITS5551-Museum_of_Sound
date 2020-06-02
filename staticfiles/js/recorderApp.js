//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;

var gumStream; //stream from getUserMedia()
var rec; //Recorder.js object
var input; //MediaStreamAudioSourceNode we'll be recording
var send_blob;

var timer;
var three_min_timer;
var minutes, seconds;

var recording = 0;

// shim for AudioContext when it's not avb.
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var sendButton = document.getElementById("sendButton");

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
sendButton.addEventListener("click", sendRecording);

recordButton.disabled = false;
stopButton.disabled = true;
sendButton.disabled = true;

var countdown = document.getElementById("countdown");
var isRecording = document.getElementById("Recording");

function timeLimit() {
  if (recording == 1) {
    console.log("timed out");
    clearInterval(three_min_timer);
    stopRecording();
  }
}

function threeMinDisplay() {
  if (recording == 1) {
    var target_date = new Date().getTime() + 3 * 60000;

    // update the tag with id "countdown" every 1 second
    three_min_timer = setInterval(() => {
      // find the amount of "seconds" between now and target
      var current_date = new Date().getTime();
      var seconds_left = (target_date - current_date) / 1000;

      minutes = parseInt(seconds_left / 60);
      seconds = parseInt(seconds_left % 60);
      // format countdown string + set tag value

      countdown.innerHTML = `<br>Time Remaining<br><span class="minutes"> ${minutes} <b>Minutes</b></span> <span class="seconds"> ${seconds} <b>Seconds</b></span></div>`;
    }, 1000);
  }
}

function startRecording() {
  isRecording.innerHTML = "Recording<br>";
  recording = 1;
  console.log("recordButton clicked");

  /*
    Simple constraints object, for more advanced audio features see
    https://addpipe.com/blog/audio-constraints-getusermedia/
  */

  var constraints = { audio: true, video: false };

  /*
      Disable the record button until we get a success or fail from getUserMedia()
  */

  recordButton.disabled = true;
  stopButton.disabled = false;
  sendButton.disabled = true;

  /*
      We're using the standard promise based getUserMedia()
      https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
  */

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then(function (stream) {
      console.log(
        "getUserMedia() success, stream created, initializing Recorder.js ..."
      );

      /*
      create an audio context after getUserMedia is called
      sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
      the sampleRate defaults to the one set in your OS for your playback device
    */
      audioContext = new AudioContext();
      console.log("audioContext");

      /*  assign to gumStream for later use  */
      gumStream = stream;
      console.log("gumstream");
      /* use the stream */
      input = audioContext.createMediaStreamSource(stream);
      console.log("input");
      /*
      Create the Recorder object and configure to record mono sound (1 channel)
      Recording 2 channels  will double the file size
    */
      rec = new Recorder(input, { numChannels: 1 });
      console.log("init rec");

      //start the recording process

      rec.record();
      threeMinDisplay();
      timer = setTimeout(timeLimit, 180000);
    })
    .catch(function (err) {
      //enable the record button if getUserMedia() fails
      console.log("recording failed");
      console.log(err);
    });
}

function stopRecording() {
  isRecording.innerHTML = "";
  recording = 0;
  clearInterval(three_min_timer);
  console.log("stopButton clicked");

  //disable the stop button, enable the record too allow for new recordings
  recordButton.disabled = false;
  stopButton.disabled = true;
  sendButton.disabled = false;

  //tell the recorder to stop the recording
  rec.stop();

  //stop microphone access
  gumStream.getAudioTracks()[0].stop();

  //create the wav blob and pass it on to createDownloadLink
  rec.exportWAV(createDownloadLink);
}

function afterSending() {
  isRecording.innerHTML = "Recording Received";
  document.getElementById("needs").innerHTML = "";
  recordButton.disabled = false;
  stopButton.disabled = true;
  sendButton.disabled = true;
}

function sendRecording() {
  console.log("sendButton clicked");
  var descrip = document.getElementById("desc").value;
  var location = document.getElementById("location").value;
  var title = document.getElementById("title").value;
  var tags = multi.value();
  // var tags = document.getElementById("tag").value;

  if (descrip == "") {
    console.log("need description");
    document.getElementById("needs").innerHTML = "Please enter a description";
    sendButton.disabled = false;
  } else if (location == "") {
    console.log("need location");
    document.getElementById("needs").innerHTML = "Please enter a location";
    sendButton.disabled = false;
  } else {
    console.log(descrip);
    console.log(location);
    console.log(send_blob);
    var csrftoken = Cookies.get("csrftoken");
    console.log(Cookies.get("csrftoken"));
    var fd = new FormData();
    fd.append("csrfmiddlewaretoken", csrftoken);
    fd.append("descrip", descrip);
    fd.append("location", location);
    fd.append("tags", tags);
    fd.append("sound", send_blob);
    fd.append("title", title);
    $.ajax({
      type: "POST",
      url: "/sound/record",
      data: fd,
      processData: false,
      contentType: false,
    }).done(function (data) {
      console.log(data);
    });
    afterSending();
  }
}

function createDownloadLink(blob) {
  send_blob = blob;
  var a = new FileReader();
  a.readAsDataURL(blob);
  a.onloadend = function () {
    var dataurl = a.result;
    var sound = document.getElementById("audio-player");
    if (sound == null) {
      sound = document.createElement("audio");
      sound.id = "audio-player";
      sound.controls = "controls";
      sound.src = dataurl;
      sound.type = "audio/mpeg";
      sound.preload = "auto";
      document.getElementById("userrecord").appendChild(sound);
      sound.load();
    } else {
      sound.src = dataurl;
      sound.type = "audio/mpeg";
      sound.preload = "auto";
      sound.load();
    }
    countdown.innerHTML = "<p><br>Your recording is below.<br></p>";
  };
}
