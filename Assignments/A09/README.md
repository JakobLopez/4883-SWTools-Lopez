## What is Clipboard
  - Chrome extension
  - Allows user to copy multiple, non-contiguous lines on web browser 
## How to use it
  - version 1
    - Extension is always enabled
    - Select text you wish to copy
    - Clicking on the icon will copy selected text to your clipboard(Concatenated)
    - After clicking icon, all highlights of selected texts will vanish
  - version 2
    - Enable or disable extension via popup
    - While enabled, select all text you wish to copy
    - Copy by clicking on the icon and selecting "Copy" in the popup
  - Version 2.1
    - Choose how you want to copy in the popup
## Requirements
  - Be accessbile via toolbar
  - Include a popup.html to disable and enable the extension
  - While enabled, multiple text selection will be enabled
  - Extension will display a badge when enabled so the user can know if it's on or not just by a quick look at the icon
  - Inject a background script into every website visited
  - Selected text will remain highlighted
  - Need a way to remove unwanted selections
  - Copy multiple items
  - Highlights get removed after copy
  - Have user choose how information is copied (concatenated or put into array)
  - Allow user to select which copied item to paste
  - Saves a history of copies made to the clipboard
## References
  - Ranges: https://www.quirksmode.org/dom/range_intro.html
  - Document.execCommand(): https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand
  - Clipboard access:https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/Interact_with_the_clipboard
