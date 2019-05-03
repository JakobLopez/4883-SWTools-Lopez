chrome.browserAction.onClicked.addListener(function (tab) {
    chrome.tabs.sendMessage(tab.id, {
        method: "getTextSelection"
    }, function (response) {

        var url = response.url;
        var subject = response.subject;
        var body = response.body;
        alert(url + '\n' + subject + '\n' + body);

        if (body == '') {
            body = "No text selected";
            //You may choose to pop up a text box allowing the user to enter in a message instead.
        }

    });
});