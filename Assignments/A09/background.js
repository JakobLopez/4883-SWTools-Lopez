//Fires when there is a click on chrome extension icon in browser
//addListener => 
//              1. function sends message to current tab
//              2. callback function after tab sends response
chrome.browserAction.onClicked.addListener(function (tab) {
    chrome.tabs.sendMessage(tab.id, {
        method: "getTextSelection"
    }, function (response) {

        //Get response from content.js
        var url = response.url;
        var subject = response.subject;
        var body = response.body;

        alert(url + '\n' + subject + '\n' + body);
    });
});