function hightlightTextSelection() {

    //W3C or Mozilla Range Object
    //Supported on Chrome, Edge, Safari, IE 9 +
    //Table to supported browsers : https://developer.mozilla.org/en-US/docs/Web/API/Range
    if (window.getSelection) {
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
        if (!document.execCommand("HiliteColor", false, '#3297FD')) {
            document.execCommand("BackColor", false, '#3297FD');
        }

        //Change text color to white
        document.execCommand('foreColor', false, 'white');

        document.designMode = "off";
    }

}

function getTextSelection() {
    var fontList = document.getElementsByTagName('font');
    var fontContent = "";
    for (let font of fontList) {
        if (font.getAttribute('color') == '#ffffff')
            fontContent = fontContent + font.innerText + " ";
    }
    return fontContent;
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


document.addEventListener('mousedown', hightlightTextSelection);

/**
 * Listens for a request from the button in the browser.
 * When it sees the getTextSelection request, it returns the selection HTML, as well as the URL and title of the tab.
 */
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {

    //If message from background.js is getTextSelection
    if (request.method == "getTextSelection") {
        //Get content from selection
        var selection = getTextSelection();


        //Append currently selected text to what is already in clipboard
        writeToClipboard(selection).then(() => {
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