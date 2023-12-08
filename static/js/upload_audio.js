const input = document.getElementById('file');
const link = document.getElementById('link');
let objectURL;

input.addEventListener('change', function () {
  if (objectURL) {
    // Revoke the old object URL to avoid using more memory than needed
    URL.revokeObjectURL(objectURL);
  }

  const file = this.files[0];

  // Check if the file is a .wav or .mp3
  if (file) {
    const fileName = file.name.toLowerCase();
    if (fileName.endsWith('.wav') || fileName.endsWith('.mp3')) {
      objectURL = URL.createObjectURL(file);

      link.href = objectURL;
      var today = new Date();
      link.download = file.name;
      link.style.display = "block"; // Show the download link
    } else {
      // Show an alert if the file is not a .wav or .mp3
      alert("Please select a .wav or .mp3 file.");
      // Reset the input field
      input.value = null;
    }
  }
});
