const token = localStorage.getItem("token");
const random = localStorage.getItem("random");


function checkAPI() {
    const xhttp = new XMLHttpRequest();

    xhttp.open("HEAD", "http://127.0.0.1:8080/endpoint", true);

    xhttp.onreadystatechange = function() {
    if (this.readyState === 4) {
        if (this.status === 200) {
        }
        else{
            window.location.replace("../offline.html");
        }
    };

    xhttp.onerror = function() {
        console.log("Errore nella chiamata API");
        window.location.replace("../offline.html");
        if (request.status == 0 && request.readyState == 4) {
          window.location.replace("../offline.html");
        }
      };}
    xhttp.send();   
}

function checkStorage() {
    if (token == null && random == null){
        window.location.replace("../login/index.html");
    }
}

function tokenLogin() {
    const xhr = new XMLHttpRequest();

    xhr.open("POST", "http://127.0.0.1:8080/token-login");
    const body = JSON.stringify({
        "token": token,
        "n": random
    });
    
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(body);
    xhr.responseType = "json";
    
    xhr.onload = () => {
        if (xhr.status == 401) {
            window.location.replace("../login/index.html");
        }else{
            document.getElementById("account").textContent = xhr.response["username"].charAt(0).toUpperCase() + xhr.response["username"].slice(1);
        }
    };
}

checkAPI();
checkStorage();
tokenLogin();
