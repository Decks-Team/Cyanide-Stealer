const form = document.querySelector("form");
const username = document.getElementById("username");
const password = document.getElementById("password");
const productkey = document.getElementById("key");
const progress = document.getElementById("progress_bar");
const button = document.getElementById("submit")

function textLog(s) {
  document.getElementById("log").innerHTML = s;
  document.getElementById("log").classList.add("fadeIn");
  setTimeout(function() {
      document.getElementById("log").classList.remove("fadeIn");
  }, 1000);
}


function signup (passwordHash) {
  const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8080/signup");
    
    const body = JSON.stringify({
        "key": key.value,
        "username": username.value,
        "password": passwordHash
      });
    
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(body);
    xhr.responseType = "json";
    
    xhr.onload = () => {
        let responseData = xhr.response;
        if (xhr.status == 401) {
            textLog(responseData["error"])
        } else {
          localStorage.setItem("token", responseData["token"]);
          localStorage.setItem("random", responseData["n"]);
            window.location.replace("../panel/index.html");
        }
    };
    
    xhr.onerror = function(e){
        textLog("Connection refused by APIs");
    };
}

function changeMeter(s, color) {
    textMeter.innerHTML = s;
    textMeter.style.color = color;
}

function changeProgress(w, color) {
  progress.style.width = w;
  progress.style.backgroundColor = color;
}

function checkPasswordStrength() {
    const weaknesses = [];
  
    if (password.value.length < 11) {
      weaknesses.push("low chars");
    }
  
    if (!/[a-z]/.test(password.value)) {
      weaknesses.push("lower");
    }
  
    if (!/[A-Z]/.test(password.value)) {
      weaknesses.push("upper");
    }
  
    if (!/[0-9]/.test(password.value)) {
      weaknesses.push("numbers");
    }
  
    if (!/[^0-9a-zA-Z]/.test(password.value)) {
      weaknesses.push("special chars");
    }
  
    switch (weaknesses.length) {
      case 0:
        changeProgress("100%", "#1b9bb5")
        button.disabled = false;
        break;
      case 1:
        changeProgress("60%", "orange")
        changeMeter("Weakness: "+weaknesses[0], "orange")
        button.disabled = false;
        break;
      case 2:
        changeProgress("60%", "orange")
        button.disabled = false;
        break;
      default:
        changeProgress("20%", "#d11d1d")
        button.disabled = true;
        break;
    }
  }

password.onkeyup = function (e) {
    e.preventDefault();
    checkPasswordStrength();
}

form.onsubmit = function (e) {
  console.log(password.value)
  e.preventDefault();

  if (password.value.length <= 0 || username.value.length <= 0){
      textLog("One of the fields is empty");
  }
  else{
      let passwordhashed = CryptoJS.SHA256(password.value).toString();
      signup(passwordhashed)
  }
}

button.disabled = true;
changeProgress("20%", "#d11d1d")