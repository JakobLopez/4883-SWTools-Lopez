## Required
  - pip install colormath
## How To Run
  - Command line ex. 
    - ```python mosaic.py input_file='./input_images/sp.jpg' input_folder='./emojis' size=24 output_folder='./output_images'```
  - If using emojis as subimages, downloading color_data.json will speed up execution
  - If not using emojis as subimages, uncomment 
  
## mosaic.py
  - Gets arguments from command line
    - input_file => path to image
    - input_folder => folder of images that will be subimages of the mosaic
    - size => size of subimages
    - output_folder => where mosaic will be stored
  - Preprocess subimages to find dominant colors
  - Loops through every pixel of given image
  - Finds the subimage with the closest dominant color in color_data.json
  - Replaces pixel with subimage on a new background
  - Saves image to given folder with format image_name + '_mosaic' + '.png'
  - In general, replaces each pixel in image with a subimage that is similar in color
