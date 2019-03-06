## How to Run Code
  - Command line arguments are in the form: ```python ascii_art.py path_to_image path_to_output path_to_font font_size```
  - EX:<br>
  ```python ascii_art.py './input_images/vans-logo.png' './output_images/vans_output.png' './Aliencons TFB.ttf' 12 ```
  - The extension of the output MUST be png. A jpg extension will cause an alpha channel error.
## ascii_art.py
  - Ran from the command line 
  - Resizes given image and maintains ratio
  - Converts image to grayscale
  - Appends every pixel as an ascii character to a list depending on the pixel's grayscale value
  - Draws every ascii character to a white background in the font specifed by command line
  - The drawn character is the same color as the pixel it represents in the original colored image
  - Characters spaced out to make each individual character visible
  - Drawn picture is saved to specified output path from command line


  

## input_images
  - Folder containing images to be converted to ascii art
  
## output_images
  - Folder containing converted images
  
## demofile.txt
  - Ascii representation of original resized image
  - This is NOT written in specified font
  
## Aliencons TFB.ttf
  - Downloaded alien font 
  - Used to changed ascii character to its corresponding alien font character
  - https://www.dafont.com/aliencons-tfb.font
