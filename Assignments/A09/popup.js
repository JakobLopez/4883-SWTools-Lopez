function toggleActivation() {
  chrome.storage.sync.get('state', function (data) {
    document.getElementById('activate').innerHTML = data.state;

    if (data.state === 'on') {
      chrome.storage.sync.set({
        state: 'off'
      });
      document.getElementById('activate').innerHTML = 'off';
      chrome.runtime.sendMessage({
        method: "disable"
      });

    } else {
      chrome.storage.sync.set({
        state: 'on'
      });
      document.getElementById('activate').innerHTML = 'on';
      chrome.runtime.sendMessage({
        method: "enable"
      });
    }
  });
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
  chrome.storage.sync.get('state', function (data) {
    document.getElementById('activate').innerHTML = data.state;
    /*if (data.state === 'on') {
      chrome.storage.sync.set({state: 'off'});
      //do something, removing the script or whatever
    } else {
      chrome.storage.sync.set({state: 'on'});
      //inject your script
    }*/
  });
  document.getElementById('activate').addEventListener('click', toggleActivation);
  document.getElementById('copy').addEventListener('click', copySelectedText);
});
//document.getElementById('activate').addEventListener('click', toggleActivation);

//document.getElementById('toggle_button').addEventListener('click', toggleActivation);