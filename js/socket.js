var app = require('express')();
var http = require('http').createServer(app);
var io = require('socket.io')(http);
var sizeof = require('object-sizeof');

app.get('/', function (req, res) {
  res.send('running');
})

io.on('connection', function (socket) {
  socket.on('name', (name) => {
    console.log(`connected ${name}`)

    if (name == "video") {
      socket.on('data1', function (data) {                     // listen on client emit 'data'
        const imgElem1 = document.getElementById("camera1")
        imgElem1.src = `data:image/jpeg;base64,${data}`
      })
      socket.on('data2', function (data) {                     // listen on client emit 'data'
        const imgElem2 = document.getElementById("camera2")
        imgElem2.src = `data:image/jpeg;base64,${data}`
      })
      socket.on('data3', function (data) {                     // listen on client emit 'data'
        const imgElem3 = document.getElementById("camera3")
        imgElem3.src = `data:image/jpeg;base64,${data}`
      })
    }
    if (name === "telemetry") {
      socket.on('data', (data) => {
        console.log(data)
      })
    }
  })
})



http.listen(3000, function () {
  console.log('listening on *:3000');
})