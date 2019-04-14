//var prev = document.createElement('input');
function getTextSelection() {


    //W3C or Mozilla Range Object
    //Supported on Chrome, Edge, Safari, IE 9 +
    //Table to supported browsers : https://developer.mozilla.org/en-US/docs/Web/API/Range
    if (window.getSelection) {

        //Get selection from window
        var selectionObj = window.getSelection();
        var sel = selectionObj.toString();

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
        div.appendChild(text);
        /*
        //prev.innerText = prev.innerText + " " + selectionObj.toString();
        //selectionObj.deleteFromDocument();
        var input = document.createElement('input');
        
        navigator.clipboard.readText()
            .then(text => {
                
                var word = text + sel;
                input.innerText = word;
      
                alert(input.innerText)
                input.select();

                document.execCommand("copy");

            })
            .catch(err => {
                word = 'Failed to read clipboard contents: ' + err;
            });
*/

        //Read contents already in clipboard
        //let cliptext = await navigator.clipboard.readText();
        //var newContent = cliptext + sel;
        //alert(cliptext)
        //var copiedText = document.createTextNode(cliptext);

        //Append the selected text to the new text
        //div.appendChild(copiedText)
        //div.appendChild(text);

        /*navigator.clipboard.writeText(newContent).then( () =>{
            alert("success");
        },function(e){
            alert("something went wrong");
        });*/


        /*
        .then(clipboardText => {
            //Create text from clipboard as node
            var copiedText = document.createTextNode(clipboardText);

            //Append the selected text to the new text
            div.appendChild(copiedText)
            div.appendChild(text);

            var newContent = new String(div.innerHTML);
            alert(typeof(newContent));

            //Write all copied/selected text to clipboard
            navigator.clipboard.writeText(newContent).then(function () {
                alert('Async: Copying to clipboard was successful!');
            }, function (err) {
                alert('Async: Could not copy text: ', err);
            });

        });*/

        /*
        if (!document.execCommand("copy", false)) {
            makeEditableAndHighlight('yellow');
        }*/

        return div.innerText;
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

async function getClipboardText() {
    var readResult = await navigator.permissions.query({
        name: "clipboard-read"
    })

    if (readResult.state == "granted" || readResult.state == "prompt")
        return await navigator.clipboard.readText();


}

function writeToClipboard(newClip) {
    navigator.clipboard.writeText(newClip).then(function () {
        alert("good");
    }, function () {
        alert("bad");
    });
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



//document.addEventListener('mousedown', getTextSelection);
/**
 * Listens for a request from the button in the browser.
 * When it sees the getTextSelection request, it returns the selection HTML, as well as the URL and title of the tab.
 */
chrome.runtime.onMessage.addListener(async function (request, sender, sendResponse) {
    if (request.method == "getTextSelection") {
        var selection = getTextSelection();

        var text = await getClipboardText();
        alert(text);

        writeToClipboard(text + selection);




        sendResponse({
            body: selection,
            url: window.location.href,
            subject: document.title
        });
    } else
        sendResponse({}); // snub them.

    return true;

});