function getTextSelection() {
    var sel;

    //W3C or Mozilla Range Object
    //Supported on Chrome, Edge, Safari, IE 9 +
    //Table to supported browsers : https://developer.mozilla.org/en-US/docs/Web/API/Range
    if (window.getSelection) {
        //Get selection from window
        sel = window.getSelection();

        //If browser supports getRangeAt
        if (sel.getRangeAt)
            // Get range starting from index 0
            var range = sel.getRangeAt(0);
        //For Safari, doesn't support getRangeAt    
        else {
            //Create new range object
            var range = document.createRange();

            //Set start and end of range
            range.setStart(sel.anchorNode, sel.anchorOffset);
            range.setEnd(sel.focusNode, sej.focusOffset);
        }

        //Get text from selected range
        var text = range.cloneContents();

        var div = document.createElement('div');
        div.appendChild(text);
        return div.innerHTML;
        /*
            if (!document.execCommand("BackColor", false, 'yellow')) {
                makeEditableAndHighlight('yellow');
            }
        } catch (ex) {
            makeEditableAndHighlight('yellow')
        }*/
    }
    //For browsers that use Microsoft Text Range Objects
    else if (document.selection) {
        sel = document.selection.createRange();
        var selectedText = userSelection;
        if (userSelection.text)
            selectedText = userSelection.text;
        //range.execCommand("BackColor", false, 'yellow');
    }
}

function makeEditableAndHighlight(colour) {
    var range, sel = window.getSelection();
    if (sel.rangeCount && sel.getRangeAt) {
        range = sel.getRangeAt(0);
    }
    document.designMode = "on";
    if (range) {
        sel.removeAllRanges();
        sel.addRange(range);
    }
    // Use HiliteColor since some browsers apply BackColor to the whole block
    if (!document.execCommand("HiliteColor", false, colour)) {
        document.execCommand("BackColor", false, colour);
    }
    document.designMode = "off";
}

//document.addEventListener('selectionchange', getTextSelection);
/**
 * Listens for a request from the button in the browser.
 * When it sees the getSelection request, it returns the selection HTML, as well as the URL and title of the tab.
 */
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.method == "getTextSelection") {
        var selection = window.getTextSelection();

        sendResponse({
            body: selection,
            url: window.location.href,
            subject: document.title
        });
    } else
        sendResponse({}); // snub them.

    return true;

});