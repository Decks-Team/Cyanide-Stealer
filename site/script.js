const form = document.querySelector("form");
const username = document.getElementById("username");
const password = document.getElementById("password");

form.onsubmit = function (e) {
    e.preventDefault();

    password = CryptoJS.SHA256(password).toString();

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "http://127.0.0.1:8080/login");
    const body = JSON.stringify({
        "username": username.value,
        "password": password.value,
      });
    
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.send(body);
    xhr.responseType = "json";
    
    xhr.onload = () => {
        let responseData = xhr.response;
        if (xhr.status == 401) {
            document.getElementById("log").innerHTML = responseData["error"];
        } else {
            
        }
    };

}