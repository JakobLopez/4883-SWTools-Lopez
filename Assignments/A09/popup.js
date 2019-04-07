
function toggleActivation(){
  chrome.browserAction.setBadgeText({text: 'ON'});
  alert()
}

document.getElementById('toggle_button').addEventListener('click', toggleActivation);