//Fires when there is a click on chrome extension icon in browser
//addListener => 
//              1. function sends message to current tab
//              2. callback function after tab sends response
/*chrome.browserAction.onClicked.addListener(function (tab) {
    chrome.tabs.sendMessage(tab.id, {
        method: "getTextSelection"
    }, function (response) {

        //Get response from content.js
        var url = response.url;
        var subject = response.subject;
        var body = response.body;

        alert(url + '\n' + subject + '\n' + body);
    });
});*/

//Listen for a keyboard shortcut
chrome.commands.onCommand.addListener(function (command) {
    //If Ctrl+Shift+5
    if (command == 'copy-selected-text') {
        //Get current tab
        chrome.tabs.query({
            active: true,
            currentWindow: true
        }, function (tab) {

            //Send message to copy selected text from window
            chrome.tabs.sendMessage(tab[0].id, {
                    method: "getTextSelection"
                },
                //Callback function to alert selected text and other information about window
                function (response) {

                    //Get response from content.js
                    var url = response.url;
                    var subject = response.subject;
                    var body = response.body;

                    alert(url + '\n' + subject + '\n' + body);
                });
        });
    }
});