let {PythonShell} = require('python-shell')
var path = require("path")

function get_query(cmd) {

  var query = document.getElementById("query-input").value
  
  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : [query, cmd]
  }

  let pyshell = new PythonShell('main.py', options);

  pyshell.on('message', function(message) {
    var object = document.getElementById("query-result")
    object.value = message;
    object.style.height = object.scrollHeight + 'px';
    console.log(message)
  })
  document.getElementById("query-input").value = "";
}

function copy_from_sample(query) {
  document.getElementById("query-input").value = query;
}
