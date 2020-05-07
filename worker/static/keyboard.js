var $ = jQuery;

(function($) {
    $.fn.getCursorPosition = function() {
        var input = this.get(0);
        if (!input) return; // No (input) element found
        if ('selectionStart' in input) {
            // Standard-compliant browsers
            return input.selectionStart;
        } else if (document.selection) {
            // IE
            input.focus();
            var sel = document.selection.createRange();
            var selLen = document.selection.createRange().text.length;
            sel.moveStart('character', -input.value.length);
            return sel.text.length - selLen;
        }
    }
})(jQuery);

$(document).ready(function(){
    new ClipboardJS('.btn');
    // document.getElementById("hidden_url").style.display = "none";
    var namespace = $('#sess_id').text();;
    console.log(namespace);
    var urlElements = window.location.href.split('/')
    var url = urlElements.slice(0, urlElements.length - 1).join('/')
    console.log(url + '/' + namespace)
    var socket = io.connect(url + '/' + namespace);

    socket.on('on_connect', function() {
        $('#log').append('<br>Connected');
    });
    socket.on('on_disconnect', function() {
        $('#log').append('<br>Disconnected');
    });
    socket.on('my_response', function(msg) {
        $('#log').append('<br>Received: ' + msg.data);
        console.log(msg);
    });
    socket.on('text_polling', function(msg) {
        $('#shared-text').val(msg.all_text);
        console.log(msg);
    });
    $('#shared-text').on('input', function (e) {
        console.log(e);
        console.log(e.originalEvent.data);
        console.log(e.keyCode);
        console.log($(this).getCursorPosition())
        var type = e.originalEvent.inputType;
        var keyCode = e.originalEvent.data;
        if (!type) {
            type = e.originalEvent.type;
            keyCode = e.originalEvent.keyCode;
        }
        socket.emit('input', {type: type, keyCode: keyCode, pos: $(this).getCursorPosition()})
    });    
});
