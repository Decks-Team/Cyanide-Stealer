Chart.defaults.global.defaultFontColor = "#fff";

var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let colors = [
  "rgba(132, 62, 148, 0.2)", "rgba(44, 168, 150, 0.2)", "rgba(214, 28, 28, 0.2)"
]
let borderColor = [
  "rgb(132, 62, 148)", "rgb(44, 168, 150)", "rgb(214, 28, 28)"
]

function bar() {
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
    let summaryData = xhr.response["summary"]

    new Chart("bar",{
      type: "bar",
      data: {
        labels: [ 'Passwords', 'Cookies', 'Histories'],
        datasets: [
          {
            data: [summaryData["passwords"], 62, 8],
            backgroundColor: colors,
            borderWidth: 3,
            borderColor: borderColor,
            borderWidth: 1
          }
        ]
      },
      options: {
        legend: {
            display: false,
          },
        scales: {
          xAxes: [{
              gridLines: {
                  color: "#404040"
              }
          }],
          yAxes: [{
              gridLines: {
                  color: "#404040"
              }   
          }]
        }
      }
    });
  } 
}


function line() {
  let yValue;
  const xhr = new XMLHttpRequest();

  const body = JSON.stringify({
    "token": localStorage.getItem("token"),
    "n": localStorage.getItem("random")
  });

  xhr.open("POST", "http://127.0.0.1:8080/date");
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(body);
  xhr.responseType = "json";

  xhr.onload = () => {
    yValue = xhr.response["dateCount"]
    yValue.push
    var lineData = {
      labels: months,
      datasets: [{
        borderColor: "#bae755",
        data: yValue,
        pointStyle: 'circle',
        pointRadius: 6,
        pointHoverRadius: 8
      }]
    }
    new Chart("lines", {
      type: "line",
      data: lineData,
      options: {
        responsive: true,
        legend: {
          display: false
        },
        scales: {
          xAxes: [{
              gridLines: {
                  color: "#404040"
              }
          }],
          yAxes: [{
              gridLines: {
                  color: "#404040"
              }   
          }]
        }
      }
    }); 
  }
}

line();
bar();