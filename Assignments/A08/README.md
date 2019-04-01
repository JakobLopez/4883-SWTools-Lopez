## Required
  - pip install colormath
## How To Run
  - Command line ex. 
    - ```python mosaic.py input_file='./input_images/sp.jpg' input_folder='./emojis' size=24 output_folder='./output_images' resize=1```
  - If using emojis as subimages, downloading color_data.json will speed up execution
  - If not using emojis as subimages, uncomment 
  
## mosaic.py
  - Gets arguments from command line
    - input_file => path to image
    - input_folder => folder of images that will be subimages of the mosaic
    - size => size of subimages
    - output_folder => where mosaic will be stored
    - resize => float number to change original image by
      - ex. resize=1 means image is the same size; resize=.5 means image is half size; resize=.25 means image is quarter of size
      - if image is large, a resize will help speed up execution
  - Preprocess subimages to find dominant colors and writes to color_data.json
  - Loops through every pixel of given image
  - Finds the subimage with the closest dominant color in color_data.json
  - Replaces pixel with subimage on a new background
  - Saves image to given folder with format image_name + '_mosaic' + '.png'
  - New image dimension will be original_width * size by original_height * size
  - In general, replaces each pixel in image with a subimage that is similar in color
## dominant_color.py
  - https://github.com/rugbyprof/4883-Software-Tools/blob/master/Assignments/A08/DominantColors/main.py
  - Finds the 3 dominant colors in an image
  - Assumes background is black, so the color is ignored
## process_files.py
  - opens json file
  - verifies file is json
  - used to open color_data.json
## color_data.json
  - Each key is the path to a subimage
  - Value is a list of at most 3 items(dictionaries)
  - Each item contains dominant color information
  - Used to compare pixel to an image with similar color
## emojis
  - Folder containing emoji images
  - Used as subimages
## input_images
  - Some images to run mosaic on
  - Would not recommend running sp.jpg without a resize (took about 11 hours without resize)
## output_images
  - An example output folder containing images created from input_images
## image_dividing
  - NOT USED IN MOSAIC CODE
  - Previous code for subimage before easier solution but still wanted to keep
  - Contains divide_image.py and google_images_download.py
