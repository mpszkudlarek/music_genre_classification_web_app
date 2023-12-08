document.getElementById("audio-upload")
document.addEventListener("change", changeHandler);

function changeHandler({
  target
}) {
  if (!target.files.length) return;


  const urlObj = URL.createObjectURL(target.files[0]);


  const audio = document.createElement("audio");


  audio.addEventListener("load", () => {
    URL.revokeObjectURL(urlObj);
  });


  var newItem = document.createElement("LI");
  newItem.appendChild(audio);

  var list = document.getElementById("myList");
  list.insertBefore(newItem, list.childNodes[0]);


  audio.controls = "true";


  audio.src = urlObj;
};