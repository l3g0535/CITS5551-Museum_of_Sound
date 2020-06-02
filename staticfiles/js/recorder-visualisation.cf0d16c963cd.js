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

var recordButton, stopButton, rec, analyser, dataArray, canvasCtx, bufferLength, canvas;
var interval = undefined;
var startTimeInt = 10;
var currentTimeInt = startTimeInt;


window.onload = function () {
  recordButton = document.getElementById('record');
  stopButton = document.getElementById('stop');

  // get audio stream from user's mic
  navigator.mediaDevices.getUserMedia({
    audio: true
  })
  .then(function (stream) {
    console.log("getUserMedia() success");

    // create audio context to be passed to recorder.js
    audioContext = new AudioContext();
    console.log("AudioContext() success")

    analyser = audioContext.createAnalyser();
    console.log("Analyser created")

    recordButton.disabled = false;

    audioInput = audioContext.createMediaStreamSource(stream);
    console.log("StreamSource initialised")

    audioInput.connect(analyser);
    console.log("analyser connected")

    rec = new Recorder(audioInput);
    console.log("recorder initialised")

    canvas = document.getElementById("myCanvas");
    canvasCtx = canvas.getContext("2d");


    analyser.fftSize = 2048;
    bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);
    console.log("some fft stuff")


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

    //recorder = new MediaRecorder(stream);

    // listen to dataavailable, which gets triggered whenever we have
    // an audio blob available
    //recorder.addEventListener('dataavailable', onRecordingReady);
  });
};



function visualize() {
  WIDTH = canvas.width;
  HEIGHT = canvas.height;

    analyser.fftSize = 2048;
    var bufferLength = analyser.fftSize;
    console.log(bufferLength);
    var dataArray = new Uint8Array(bufferLength);

    canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

    var draw = function() {

      drawVisual = requestAnimationFrame(draw);

      analyser.getByteTimeDomainData(dataArray);

      canvasCtx.fillStyle = 'rgb(200, 200, 200)';
      canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

      canvasCtx.lineWidth = 2;
      canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

      canvasCtx.beginPath();

      var sliceWidth = WIDTH * 1.0 / bufferLength;
      var x = 0;

      for(var i = 0; i < bufferLength; i++) {

        var v = dataArray[i] / 128.0;
        var y = v * HEIGHT/2;

        if(i === 0) {
          canvasCtx.moveTo(x, y);
        } else {
          canvasCtx.lineTo(x, y);
        }

        x += sliceWidth;
      }

      canvasCtx.lineTo(canvas.width, canvas.height/2);
      canvasCtx.stroke();
    };

    draw();

  } 


function startRecording() {
  recordButton.disabled = true;
  stopButton.disabled = false;

  rec.record();
  console.log("recording")

  visualize()

}

function stopRecording() {
  recordButton.disabled = false;
  stopButton.disabled = true;
  // Stopping the recorder will eventually trigger the `dataavailable` event and we can complete the recording process
  rec.stop();
  console.log("stopped recording")
  rec.getBuffer(getBufferCallback);
  console.log("audio playing buffer for audio")
  // var soundURL = document.getElementById('audio').currentSrc;
  // document.getElementById('recordingURL').innerHTML = soundURL;
}

function getBufferCallback( buffers ) {
    var newSource = audioContext.createBufferSource();
    var newBuffer = audioContext.createBuffer( 2, buffers[0].length, audioContext.sampleRate );
    newBuffer.getChannelData(0).set(buffers[0]);
    newBuffer.getChannelData(1).set(buffers[1]);
    newSource.buffer = newBuffer;
    console.log("buffer 0:" + buffers[0].length + "  buffer 1:" + buffers[1].length)


    newSource.connect( audioContext.destination );
    newSource.start(0);
}

function onRecordingReady(e) {
  var audio = document.getElementById('audio');
  // e.data contains a blob representing the recording
  audio.src = URL.createObjectURL(e.data);
  audio.play();

  document.getElementById('recordingURL').innerHTML = audio.src;
}

function startRecordingLabel() {
  document.getElementById('recording').innerHTML = "Recording audio..."
}

function endRecordingLabel() {
  document.getElementById('recording').innerHTML = "";
}

