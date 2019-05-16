// websocket scripts
// console.log(window.location)

var loc = window.location;
var formData = $("#form");
var msgInput = $("#id_message");
var chatHolder = $("#chat-items");
var me = $("#myUsername").val();

var wsStart = "ws://";

if (loc.protocol == "https:") {
  wsStart = "wss://";
}
var endpoint = wsStart + loc.host + loc.pathname;
var socket = new ReconnectingWebSocket(endpoint);

socket.onmessage = function(e) {
  // console.log("message", e)
  // console.log(e.data)
  var chatDataMsg = JSON.parse(e.data);
  chatHolder.append(
    "<li>" + chatDataMsg.message + " via " + chatDataMsg.username + "</li>"
  );
};
socket.onopen = function(e) {
  // console.log("open", e)
  formData.submit(function(event) {
    event.preventDefault();
    var msgText = msgInput.val();
    // chatHolder.append("<li>" + msgText + " via " + me + "</li>")
    // var formDataSerialized = formData.serialize()
    var finalData = {
      message: msgText
    };

    socket.send(JSON.stringify(finalData));
    // msgInput.val('')
    formData[0].reset();
  });
};
socket.onerror = function(e) {
  // console.log("error", e)
};
socket.onclose = function(e) {
  // console.log("close", e)
};
