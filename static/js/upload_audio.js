const input = document.getElementById('audio-upload');
let objectURL;

input.addEventListener('change', function () {
  const file = this.files[0];

  if (this.files.length > 1) {
    alert("Please upload only one file.");
    return;
  }

  if (file && (file.type === 'audio/mp3' || file.type === 'audio/wav' || file.type === 'audio/mpeg')) {
    if (objectURL) {
      URL.revokeObjectURL(objectURL);
    }
    
    objectURL = URL.createObjectURL(file);

    let audio = new Audio();
    audio.addEventListener('loadedmetadata', function() {

      if (audio.duration < 30) {
        alert("The file is too short. Please upload a file that is at least 30 seconds long.");
        URL.revokeObjectURL(objectURL);
      } else {
        // Create a download link instead of automatically downloading
        const downloadLink = document.createElement('a');
        downloadLink.href = objectURL;
        downloadLink.download = file.name;
        downloadLink.textContent = 'Download Audio';
        document.body.appendChild(downloadLink);
      }
    });

    audio.src = objectURL;
  } else {
    alert("Please upload a file in MP3 or WAV format.");
    input.value = "";
  }
});
