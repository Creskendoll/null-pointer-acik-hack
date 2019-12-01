function getSummary() {
  var xhttp = new XMLHttpRequest();
  const url = "https://turkcemetinozetleme.teaddict.net/ozetle/api/new";
  xhttp.open("POST", url, true);

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(xhttp.responseText);
      document.getElementById("textbox").value = JSON.parse(xhttp.response).result;
    }
  };
  xhttp.send(JSON.stringify({ "contextOfText": document.getElementById("textbox").value }));
}

function getParaphrase() {
  var xhttp = new XMLHttpRequest();
  const body = document.getElementById("textbox").value;
  
  const url = 'http://192.168.1.114:5000/paraphrase'
  xhttp.open("POST", url, true);

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      const curVal = document.getElementById("textbox").value; 
      console.log(xhttp.responseText);
      document.getElementById("textbox").value = "`" + curVal + "` - " + JSON.parse(xhttp.response).paraphrase;
    }
  };
  xhttp.send(body);
}

function getSuggestion() {
    var xhttp = new XMLHttpRequest();
  const body = document.getElementById("textbox").value;
  
  const url = 'http://192.168.1.114:5000/suggest'
  // const url = 'https://acik-hack.appspot.com/suggest'
  xhttp.open("POST", url, true);

  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {      
      const div = document.getElementById("pop-up");
      div.style = "display: flex;justify-content: center;"

      const listItem = document.getElementById("li1");
      listItem.innerText = JSON.parse(xhttp.response).prediction.split(' ')[1];

      const listItem2 = document.getElementById("li2");
      listItem2.innerText = JSON.parse(xhttp.response).prediction.split(' ')[2];

      const listItem3 = document.getElementById("li3");
      listItem3.innerText = JSON.parse(xhttp.response).prediction.split(' ')[3];
    }
  };
  xhttp.setRequestHeader('Content-Type', 'utf-8');
  xhttp.send(body);
}

function appendFirstSuggestion() {
  const appendedText = `${document.getElementById("textbox").value} ${document.getElementById("li1").innerText}`
  document.getElementById("textbox").value = appendedText;
    getSuggestion();
}

function appendSecondSuggestion() {
  const appendedText = `${document.getElementById("textbox").value} ${document.getElementById("li2").innerText}`
  document.getElementById("textbox").value = appendedText;

  getSuggestion();
}

function appendThirdSuggestion() {
  const appendedText = `${document.getElementById("textbox").value} ${document.getElementById("li3").innerText}`
  document.getElementById("textbox").value = appendedText;

  getSuggestion();
}