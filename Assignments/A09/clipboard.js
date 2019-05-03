var selections = [];

/**
 * Highlights a range of text
 * @param none
 * @returns nothing
 */
function hightlightTextSelection() {

    //W3C or Mozilla Range Object
    //Supported on Chrome, Edge, Safari, IE 9 +
    //Table to supported browsers : https://developer.mozilla.org/en-US/docs/Web/API/Range
    if (window.getSelection) {
        //Get selection from document
        var range, sel = window.getSelection();

        //If there is a selection, not just a mouse click
        if (sel.toString() != '') {
            selections.push(sel);
            console.log(selections)

            //If range is supported by browser
            if (sel.rangeCount && sel.getRangeAt)
                //Get range of selection starting from index 0
                range = sel.getRangeAt(0);

            //Allow edits to document
            document.designMode = "on";

            if (range) {
                //Remove current range from document
                sel.removeAllRanges();

                //Add range from selection
                sel.addRange(range);
            }

            // Use HiliteColor since some browsers apply BackColor to the whole block
            if (!document.execCommand("HiliteColor", false, '#3390ff'))
                document.execCommand("BackColor", false, '#3390ff');

            //Change text color to white
            document.execCommand('foreColor', false, 'white');
            
            //Remove window selection so there is no color clash
            window.getSelection().removeAllRanges();

            //Don't allow edits to document
            document.designMode = "off";
        }
    }
}

/**
 * Loops through document gets content of all selected items
 * @param none
 * @returns content of selected items
 */
function getTextSelection() {
    //List of all font tags
    var fontList = document.getElementsByTagName('font');

    //Initialize content to nothing
    var fontContent = "";

    //For every font tag
    for (let font of fontList) {
        //If color attribute is #ffffff
        if (font.getAttribute('color') == '#ffffff')
            //Add to content
            fontContent = fontContent + font.innerText + " ";
    }

    //Get current selection from document selection and convert to string
    //var sel = window.getSelection().toString();
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

document.addEventListener('mouseup', hightlightTextSelection);

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