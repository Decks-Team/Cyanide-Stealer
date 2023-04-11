const form = document.querySelector("form");
const username = document.getElementById("username");
const password = document.getElementById("password");
const button = document.getElementById("submit");

function textLog(s) {
    document.getElementById("log").innerHTML = s;
    document.getElementById("log").classList.add("fadeIn");
    setTimeout(function() {
        document.getElementById("log").classList.remove("fadeIn");
    }, 1000);
}

function login(passwordHash) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8080/login");
    
    const body = JSON.stringify({
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

form.onsubmit = function (e) {
    e.preventDefault();

    let passwordhashed = CryptoJS.SHA256(password.value).toString();
    login(passwordhashed);
}

username.onkeyup = function (e){
    e.preventDefault();
    if (password.value.length <= 0 || username.value.length <= 0){
        document.getElementById("submit").disabled = true;
    }
    else{
        document.getElementById("submit").disabled = false;
    }
}

password.onkeyup = function (e){
    e.preventDefault();
    if (password.value.length <= 0 || username.value.length <= 0){
        document.getElementById("submit").disabled = true;
    }
    else{
        document.getElementById("submit").disabled = false;
    }
}

document.getElementById("submit").disabled = true;