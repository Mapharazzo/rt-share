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

function getInputSelection(el) {
    var start = 0, end = 0, normalizedValue, range,
        textInputRange, len, endRange;

    if (typeof el.selectionStart == "number" && typeof el.selectionEnd == "number") {
        start = el.selectionStart;
        end = el.selectionEnd;
    } else {
        range = document.selection.createRange();

        if (range && range.parentElement() == el) {
            len = el.value.length;
            normalizedValue = el.value.replace(/\r\n/g, "\n");

            // Create a working TextRange that lives only in the input
            textInputRange = el.createTextRange();
            textInputRange.moveToBookmark(range.getBookmark());

            // Check if the start and end of the selection are at the very end
            // of the input, since moveStart/moveEnd doesn't return what we want
            // in those cases
            endRange = el.createTextRange();
            endRange.collapse(false);

            if (textInputRange.compareEndPoints("StartToEnd", endRange) > -1) {
                start = end = len;
            } else {
                start = -textInputRange.moveStart("character", -len);
                start += normalizedValue.slice(0, start).split("\n").length - 1;

                if (textInputRange.compareEndPoints("EndToEnd", endRange) > -1) {
                    end = len;
                } else {
                    end = -textInputRange.moveEnd("character", -len);
                    end += normalizedValue.slice(0, end).split("\n").length - 1;
                }
            }
        }
    }

    return {
        start: start,
        end: end
    };
}

function offsetToRangeCharacterMove(el, offset) {
    return offset - (el.value.slice(0, offset).split("\r\n").length - 1);
}

function setInputSelection(el, startOffset, endOffset) {
    if (typeof el.selectionStart == "number" && typeof el.selectionEnd == "number") {
        el.selectionStart = startOffset;
        el.selectionEnd = endOffset;
    } else {
        var range = el.createTextRange();
        var startCharMove = offsetToRangeCharacterMove(el, startOffset);
        range.collapse(true);
        if (startOffset == endOffset) {
            range.move("character", startCharMove);
        } else {
            range.moveEnd("character", offsetToRangeCharacterMove(el, endOffset));
            range.moveStart("character", startCharMove);
        }
        range.select();
    }
}

$(document).ready(function(){
    new ClipboardJS('.btn');
    var namespace = $('#sess_id').text();;
    console.log(namespace);
    var urlElements = window.location.href.split('/')
    var url = urlElements.slice(0, urlElements.length - 1).join('/')
    console.log(url + '/' + namespace)
    var socket = io.connect(url + '/' + namespace);

    var txtarea = document.getElementById("shared-text");

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
        var sel = getInputSelection(txtarea);
        txtarea.value = msg.all_text;
        setInputSelection(txtarea, sel.start, sel.end);
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
