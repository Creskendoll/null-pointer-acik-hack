function getSummary() {
  var xhttp = new XMLHttpRequest();
  const url = "https://turkcemetinozetleme.teaddict.net/ozetle/api/new";
  xhttp.open("POST", url, true);

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(xhttp.responseText);

      document.getElementById("textbox").innerHTML = JSON.parse(xhttp.response);
    }
  };
  xhttp.send(JSON.stringify({ "contextOfText": document.getElementById("textbox").value }));
}

function getParaphrase() {
  console.log("asduighk");

}

function getSuggestion() {
}

function appendFirstSuggestion() {
  const appendedText = `${document.getElementById("textbox").innerHTML} + ${document.getElementById("li1").innerText}`
  document.getElementById("textbox").innerHTML = appendedText;

}

function appendSecondSuggestion() {
  const appendedText = `${document.getElementById("textbox").innerHTML} + ${document.getElementById("li2").innerText}`
  document.getElementById("textbox").innerHTML = appendedText;

}

function appendThirdSuggestion() {
  const appendedText = `${document.getElementById("textbox").innerHTML} + ${document.getElementById("li3").innerText}`
  document.getElementById("textbox").innerHTML = appendedText;

}