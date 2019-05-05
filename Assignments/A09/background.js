// Check whether new version is installed
chrome.runtime.onInstalled.addListener(function (details) {
    //If first time installed
    if (details.reason == "install")
        chrome.storage.sync.set({
            state: 'on'
        });

});


//Fires when message is sent to background
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {

    //If message from background.js is getTextSelection
    if (request.method == "getTextSelection") {

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
    } else{
        //Get current tab
        chrome.tabs.query({
            active: true,
            currentWindow: true
        }, function (tab) {

            //Send message to copy selected text from window
            chrome.tabs.sendMessage(tab[0].id, {
                method: request.method
            });
        });
    };
});

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