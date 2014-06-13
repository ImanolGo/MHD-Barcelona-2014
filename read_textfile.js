document.getElementById('fileinput').addEventListener('change', readSingleFile, false);

function readSingleFile(evt) {
  //Retrieve the first (and only!) File from the FileList object
  var f = evt.target.files[0]; 

  if (f) {
    var r = new FileReader();
    r.onload = function(e) { 
      var contents = e.target.result;
      fairy_tale.innerHTML = contents;
    }
    r.readAsText(f);
  } else { 
    alert("Failed to load file");
  }
}