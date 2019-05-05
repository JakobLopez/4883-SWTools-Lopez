var active = true;

function toggleActivation() {
  if (!active) {
    chrome.browserAction.setBadgeText({
      text: 'ON'
    });
    active = true;
  } else {
    chrome.browserAction.setBadgeText({
      text: ''
    });
    active = false;
  }
}

function copySelectedText() {
  //Force popup window to close because it makes the clipboard error
  window.close();
  
  //Send message to copy selected text from window
  chrome.runtime.sendMessage({
    method: "getTextSelection"
  });

}
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById('copy').addEventListener('click', copySelectedText);
});
//document.getElementById('activate').addEventListener('click', toggleActivation);

//document.getElementById('toggle_button').addEventListener('click', toggleActivation);