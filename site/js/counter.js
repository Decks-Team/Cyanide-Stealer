function changeText(s, id) {
    document.getElementById(id).innerText = s;
}

document.addEventListener("DOMContentLoaded", () => {
        function counter(id, start, end, duration) {
        let obj = document.getElementById(id),
        current = start,
        range = end - start,
        increment = end > start ? 1 : -1,
        step = Math.abs(Math.floor(duration / range)),
        timer = setInterval(() => {
        current += increment;
        obj.textContent = current;
            if (current == end) {
                clearInterval(timer);
            }
        }, step);
    }

    const xhr = new XMLHttpRequest();

    const body = JSON.stringify({
    "token": localStorage.getItem("token"),
    "n": localStorage.getItem("random")
    });

    xhr.open("POST", "http://127.0.0.1:8080/count");
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(body);
    xhr.responseType = "json";
    xhr.onload = () => {
        let victims = xhr.response["victims"]
        let tokens = xhr.response["tokens"]
        let creds = xhr.response["creds"]
        counter("creds-text", 0, creds, 3000);
        
        if (parseInt(victims) < 10){
            changeText(victims, "victims-text")
            changeText(tokens, "tokens-text")
        }
        else{
            counter("tokens-text", 0, tokens, 3000);
            counter("victims-text", 0, victims, 3000);
        }
        
    }
    
});