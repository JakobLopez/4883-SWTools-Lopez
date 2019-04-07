/*
//Executes script when icon is clicked
chrome.browserAction.onClicked.addListener(function (tabId, tab) {
            chrome.tabs.executeScript({
                    file: "clipboard.js"
                }, _ => {
                    //Catches error
                    let e = chrome.runtime.lastError;
                    if (e !== undefined) {
                        alert("Clipboard cannot be used on this page.");
                    }
                }
            )});*/
