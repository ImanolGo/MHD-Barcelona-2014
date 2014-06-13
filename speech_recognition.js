var recognizing;
var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
reset();
recognition.onend = reset;

recognition.onresult = function (event) {
  var final = "";
  var interim = "";
  for (var i = 0; i < event.results.length; ++i) {
    if (event.results[i].final) {
      final += event.results[i][0].transcript;
    } else {
      interim += event.results[i][0].transcript;
      //console.log(event.results[i][0].confidence);
    }
  }
  final_span.innerHTML = final;
  interim_span.innerHTML = interim;
  kati = interim.split(" ");
  console.log(kati);
}

function reset() {
  recognizing = false;
  button.innerHTML = "Click to Speak";
}

function toggleStartStop() {
  if (recognizing) {
    recognition.stop();
    reset();
  } else {
    recognition.start();
    recognizing = true;
    button.innerHTML = "Click to Stop";
    final_span.innerHTML = "";
    interim_span.innerHTML = "";
  }
}