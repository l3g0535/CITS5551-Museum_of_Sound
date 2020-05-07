URL = window.URL || window.webkitURL;
var gumstream; //stream from getUserMedia()
var record; // recorder.js object
var input;
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audio_context = new AudioContext();

var record_button = document.getElementById("record_button");
var stop_button = document.getElementById("stop_button");
var upload_button = document.getElementById("upload_button");

var recording = 0;

record_button.addEventListener("click", start_recording);
stop_button.addEventListener("click", stop_recording);
upload_button.addEventListener("click", upload_recording);

var minutes_label = document.getElementById("minutes");
var seconds_label = document.getElementById("seconds");
var count = 0;

function counting() {
  count++;
  if (count % 60 < 10 && count < 181) {
    minutes = parseInt(count / 60);
    seconds = "0" + (count % 60);
    minutes_label.innerHTML = minutes;
    seconds_label.innerHTML = seconds;
  } else if (count % 60 >= 10 && count < 181) {
    minutes = parseInt(count / 60);
    seconds = count % 60;
    minutes_label.innerHTML = minutes;
    seconds_label.innerHTML = seconds;
  } else {
    console.log("time out!");
    stop_recording();
  }
}

function start_recording() {
  console.log("Record button is clicked!");
  recording += 1;
  if (recording == 1) {
    var constraint = { audio: true, video: false }; //record audio
    navigator.mediaDevices
      .getUserMedia(constraint)
      .then(function (stream) {
        console.log(
          "getUserMedia() Success, stream created, intialising Recorder.js"
        );
        window.streamReference = stream;
        gumstream = stream;
        input = audio_context.createMediaStreamSource(stream);
        record = new Recorder(input, {
          numChannels: 1,
        });
        record.record();
        console.log("Recording.....");
        clear = setInterval(counting, 1000);
      })
      .catch(function (err) {
        console.log(err.name, err.message);
      });
    record_button.innerText = "Pause";
    stop_button.disabled = true;
    upload_button.disabled = true;
  }
  if (recording > 1) {
    pause_recording();
  }
}

function pause_recording() {
  if (recording % 2 == 0) {
    //pause
    clearInterval(clear);
    console.log("Pause");
    record.stop();
    stop_button.disabled = false;
    record_button.innerHTML = "Pause";
    record_button.innerText = "Resume";
  } else {
    clear = setInterval(counting, 1000);
    //resume
    console.log("Resume");
    stop_button.disabled = true;
    record.record();
    record_button.innerHTML = "Resume";
    record_button.innerText = "Pause";
  }
}

function upload_recording() {
  console.log("Pause button is clicked, rec.recording=", record.recording);
}

function stop_stream() {
  if (!window.streamReference) return;
  window.streamReference.getAudioTracks().forEach(function (track) {
    track.stop();
  });
  window.streamReference = NULL;
}

function stop_recording() {
  minutes_label.innerHTML = "0";
  seconds_label.innerHTML = "00";
  count = 0;
  recording = 0;
  clearInterval(clear);
  console.log("Stop button is clicked");
  record_button.innerText = "Record";
  stop_button.disabled = true;
  record_button.disabled = false;
  upload_button.disabled = false;
  //pause_button.innerHTML = "Pause";
  record.stop();
  gumstream.getAudioTracks()[0].stop();
  record.exportWAV(createDownloadLink);
  stop_stream();
}

function createDownloadLink(blob) {
  var url = URL.createObjectURL(blob);
  var aud = document.createElement("audio");
  var list = document.createElement("list");
  var link = document.createElement("link");
  aud.controls = true;
  aud.src = url;
  link.href = url;
  link.download = new Date().toISOString() + ".wav";
  link.innerHTML = link.download;
  list.appendChild(aud);
  recordingList.appendChild(list);
}
