// websocket scripts
// console.log(window.location)

$(document).ready(function () {
    var div = $("#chat-items");
    div.scrollTop(div.prop('scrollHeight'));
});

function truncateText(text) {
    var truncatedText = text;
    if (truncatedText.length > 19) {
        var truncatedText = (text.substring(0, 19) + "...");
    }
    return truncatedText;
}

// $("#chat_btn").click(function(event){
//     var dNow = new Date();
//     var localdate= (dNow.getMonth()+1) + '_' + dNow.getDate() + '_' + dNow.getFullYear() + '__' + dNow.getHours() + '_' + dNow.getMinutes() + '_' + dNow.getSeconds();
//     $(".direct-chat-text").removeAttr("id");
//     $(".direct-chat-text").attr('id', localdate);
// });

var loc = window.location;
var formData = $("#form");
var msgInput = $("#id_message");
var chatHolder = $("#chat-items");
var me = $("#myUsername").val();
var myDynamicName = $("#myDynamicName").val();
var client = $("#clientUsername").val();
var clientDynamicName = $("#clientDynamicName").val();
var div = $("#chat-items");
var msgDiv = $("#socket_messages")
var chatNotificationDiv = $('#chat-message-holder');
var linkInstance = $("a[href='" + loc.host + loc.pathname + "']");
var unseenCount = parseInt($('#unseen-count-holder').text());
var chatInput = $("#chat_box_input");
var chatBtn = $("#chat_btn");
var inputValHolder = msgInput.val();
var FireFox = !(window.mozInnerScreenX == null);

var wsStart = "ws://";

if (loc.protocol == "https:") {
    wsStart = "wss://";
}
var endpoint = wsStart + loc.host + loc.pathname;
var socket = new ReconnectingWebSocket(endpoint);

socket.onmessage = function (e) {
    // console.log("message", e)
    // console.log(e.data)

    var chatDataMsg = JSON.parse(e.data);
    var message = chatDataMsg.message;
    if (chatDataMsg.username == me) {
        var img = $("#my_image").html();
        var clientImg = $("#client_image").html();
        var html = ("<div class='direct-chat-msg right'>\
                <div class='direct-chat-info clearfix'>\
                    <span class='direct-chat-name pull-right'>\
                        You\
                    </span>\
                </div>\
                " + img + "\
                <div class='direct-chat-text' id='message_holder'>\
                    " + message + "\
                </div>\
            </div>\
            ");
        var chatNotificationHTML = ("<a class='hover text-deco-none b-b' href='/chat/" + client + "/'>\
                <input type='hidden' name='unseen_input' value='1' id='unseen_counter'>\
                <div class='notif-img'>\
                    " + clientImg + "\
                </div>\
                <div class='notif-content'>\
                    <span class='subject'>\
                        " + clientDynamicName + "\
                    </span>\
                    <span class='block truncate'>\
                        " + message + "\
                    </span>\
                </div>\
            </a>");
        var unseenFinalCounter = unseenCount;
    } else {
        var img = $("#client_image").html();
        var html = ("<div class='direct-chat-msg'>\
                <div class='direct-chat-info clearfix'>\
                    <span class='direct-chat-name pull-left'>\
                        " + clientDynamicName + "\
                    </span>\
                </div>\
                " + img + "\
                <div class='direct-chat-text' id='message_holder'>\
                    " + message + "\
                </div>\
            </div>\
        ");
        var chatNotificationHTML = ("<a class='bg-c-ash hover text-deco-none b-b' href='/chat/" + client + "/'>\
            <input type='hidden' name='unseen_input' value='1' id='unseen_counter'>\
            <div class='notif-img'>\
                " + $("#client_image").html() + "\
            </div>\
            <div class='notif-content'>\
                <span class='subject'>\
                    " + clientDynamicName + "\
                </span>\
                <span class='block truncate'>\
                    " + message + "\
                </span>\
            </div>\
        </a>");
        var unseenFinalCounter = unseenCount + 1;
    }
    chatHolder.append(
        // "<li>" + chatDataMsg.message + " via " + chatDataMsg.username + "</li>"
        html
    );
    $("a[href='/chat/" + client + "/']").each(function () {
        $(this).addClass("hidden");
    });
    chatNotificationDiv.append(
        chatNotificationHTML
    );
    $('#unseen-count-holder').html(unseenFinalCounter).css('color', '#070135').css('font-weight', '700');
    div.scrollTop(div.prop('scrollHeight'));
};

socket.onopen = function (e) {
    // console.log("open", e);
    
    $('div[data-notify="container"]').hide();

    chatBtn.click(function(){
        var rawValue = $("div.emojionearea-editor").html();
        inputValHolder = rawValue;
        $("#empty_message").hide();
    });

    formData.submit(function (event) {
        var rawValue = $("div.emojionearea-editor").html();
        event.preventDefault();
        if(rawValue == ""){
            chatBtn.attr("disabled", true);
            $("#chat_error").removeClass('hidden');
            $("#chat_error").html("Please type your message...");
            $(".form").addClass('border-danger-2');
        } else {
            var msgText = inputValHolder;
            // chatHolder.append("<li>" + msgText + " via " + me + "</li>")
            // var formDataSerialized = formData.serialize()
            var finalData = {
                message: msgText
            };

            socket.send(JSON.stringify(finalData));
            // msgInput.val('')
            formData[0].reset();
            $("div.emojionearea-editor").html("");
        }
    });
};

socket.onerror = function (e) {
    // console.log("error", e);
};

socket.onclose = function (e) {
    // console.log("close", e)
    var placementFrom = 'top';
    var placementAlign = 'center';
    var state = 'warning';
    var style = 'withicon';
    var content = {};

    content.message = 'Failed to establish connection!';
    content.title = 'No Connection';
    if (style == "withicon") {
      content.icon = 'fa fa-bell';
    } else {
      content.icon = 'none';
    }
    // content.url = '/';
    // content.target = '_blank';

    if(FireFox) {
        // $("#socket_messages").html(content.message).css('color', 'red');
        console.log("Browsing from firefox...");
    } else { 
        $.notify(content,{
            newest_on_top: true,
            type: state,
            placement: {
                from: placementFrom,
                align: placementAlign
            },
            time: 1000,
            delay: 0,
        });
    }
};

$(".form").click(function(e) {  
    $("#chat_error").addClass('hidden');
    chatBtn.attr("disabled", false);
    $(".form").removeClass('border-danger-2');
});