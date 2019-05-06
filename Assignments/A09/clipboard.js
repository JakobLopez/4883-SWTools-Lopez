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
            selections.push(sel.toString());

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

            //If browser supports HiliteColor
            if (!document.execCommand("HiliteColor", false, '#3390ff'))
                document.execCommand("BackColor", false, '#3390ff');

            //Change text color to white
            //document.execCommand('foreColor', false, 'white');

            //Remove window selection so there is no color clash
            window.getSelection().removeAllRanges();

            //Don't allow edits to document
            document.designMode = "off";
        }
    }
}

/**
 * Loops through document to get content of all selected items
 * @param none
 * @returns content of selected items
 */
async function getTextSelection() {

    //List of all font tags
    var fontList = document.getElementsByTagName('span');

    //Initialize content to nothing
    var fontContent = "";

    //For every font tag
    for (let font of fontList) {
        //If color attribute is #ffffff
        if (font.getAttribute('style') == 'background-color: rgb(51, 144, 255);')
            //Add to content
            fontContent = fontContent + font.innerText + " ";
    }

    return fontContent;
}

/**
 * Writes text to clipboard
 * @param newClip the text to be written to clipboard
 * @returns the copied text, or an error message
 */
async function writeToClipboard(newClip) {
    try {
        //Gets write permission
        var writeResult = await navigator.permissions.query({
            name: "clipboard-write"
        });

        if (writeResult.state == "granted" || writeResult.state == "prompt")
            await navigator.clipboard.writeText(newClip);

        return String(newClip);
    } catch (e) {
        return 'An error occured writing to the clipboard.';
    }
}

async function copy() {
    //Get content from selection         
    var selection = await getTextSelection();

    //Write content of selected text to clipboard    
    return await writeToClipboard(selection);
}

async function initialize() {
    chrome.storage.sync.get('state', function (data) {
        if (data.state == 'on')
            document.addEventListener('mouseup', hightlightTextSelection)
    });
}

initialize();

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {

    //If message from sender is getTextSelection     
    if (request.method == "getTextSelection") {
        copy().then(response => {
            //Send response back to background.ts  
            sendResponse({
                body: response,
                url: window.location.href,
                subject: document.title
            });
        });
    } else if (request.method == "disable")
        document.removeEventListener('mouseup', hightlightTextSelection)
    else if (request.method == "enable")
        document.addEventListener('mouseup', hightlightTextSelection)

    //Make sendResponse asynchronous
    return true;
});