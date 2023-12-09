const input = document.getElementById('file');
const link = document.getElementById('link');
let objectURL;

input.addEventListener('change', function () {
  if (objectURL) {
    URL.revokeObjectURL(objectURL);
  }

  const file = this.files[0];


  if (file) {
    const fileName = file.name.toLowerCase();
    if (fileName.endsWith('.wav') || fileName.endsWith('.mp3')) {
      objectURL = URL.createObjectURL(file);

      const audio = new Audio(objectURL);
      audio.addEventListener('loadedmetadata', function() {
        if(audio.duration >= 30) {
          link.href = objectURL;
          var today = new Date();
          link.download = file.name;
          link.style.display = "block"; 
        } else {
          alert("Please select an audio file that is at least 30 seconds long.");
          input.value = null;
        }
      });
    } else {
      alert("Please select a .wav or .mp3 file.");
      input.value = null;
    }
  }
});
