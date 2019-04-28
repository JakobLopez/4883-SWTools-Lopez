function getTextSelection() {

    //W3C or Mozilla Range Object
    //Supported on Chrome, Edge, Safari, IE 9 +
    //Table to supported browsers : https://developer.mozilla.org/en-US/docs/Web/API/Range
    if (window.getSelection) {

        //Get selection from window
        var selectionObj = window.getSelection();
        var sel = selectionObj.toString();
        /*

        //If browser supports getRangeAt
        if (selectionObj.getRangeAt)
            // Get range starting from index 0
            var range = selectionObj.getRangeAt(0);
        //For Safari, doesn't support getRangeAt    
        else {
            //Create new range object
            var range = document.createRange();

            //Set start and end of range
            range.setStart(selectionObjel.anchorNode, selectionObj.anchorOffset);
            range.setEnd(selectionObj.focusNode, selectionObj.focusOffset);
        }

        //Get text from selected range
        var text = range.cloneContents();
        var div = document.createElement('div');
        div.appendChild(text);*/

        /*
        if (!document.execCommand("copy", false)) {
            makeEditableAndHighlight('yellow');
        }*/

        return sel;
    }
    //For browsers that use Microsoft Text Range Objects
    else if (document.selection) {
        var sel = document.selection.createRange();

        var selectedText = userSelection;

        if (userSelection.text)
            selectedText = userSelection.text;
        return selectedText;
        //range.execCommand("BackColor", false, 'yellow');
    }

}

/**
 * Gets text currently in clipboard
 * @param none
 * @returns text in clipboard
 */
async function getClipboardText() {
    try {
        //Gets read permission
        var readResult = await navigator.permissions.query({
            name: "clipboard-read"
        });

        //If permission allowed
        if (readResult.state == "granted" || readResult.state == "prompt")
            //Return text in clipboard
            return await navigator.clipboard.readText();
    } catch (e) {
        alert('An error occured reading from the clipboard');
    }
}

/**
 * Writes text to clipboard
 * @param newClip the text to be written to clipboard
 * @returns nothing
 */
async function writeToClipboard(newClip) {
    try {
        //Gets write permission
        var writeResult = await navigator.permissions.query({
            name: "clipboard-write"
        });

        if (writeResult.state == "granted" || writeResult.state == "prompt")
            await navigator.clipboard.writeText(newClip);
    } catch (e) {
        alert('An error occured writing to the clipboard.');
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



document.addEventListener('mousedown', getTextSelection);
/**
 * Listens for a request from the button in the browser.
 * When it sees the getTextSelection request, it returns the selection HTML, as well as the URL and title of the tab.
 */
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {

    //If message from background.js is getTextSelection
    if (request.method == "getTextSelection") {
        //Get content from selection
        var selection = getTextSelection();

        //Get text already in the clipboard
        getClipboardText().then(text => {
            //Append currently selected text to what is already in clipboard
            writeToClipboard(text + selection);

            //Send response back to background.ts
            sendResponse({
                body: selection,
                url: window.location.href,
                subject: document.title
            });
        });

    } else
        //Send back a blank message to background.ts
        sendResponse({}); // snub them.

    //Makes listener asynchronous
    return true;
});