## Example command line
  - ```python match.py folder=images image=jp_gates_original.png```
  - Folder and image can also be a path 
## match.py
  - Ran from command line
  - Command line needs 2 arguments: folder and image
  - Compares every image in folder to the image provided to find the most similar
  - Similarity comparison methods: Mean Squared Error and Structural Similarity
  - MSE = faster but less accurate
  - SSIM = slower but more accurate
  - Displays closest image for each method
  - Closest image cannot be the original image provided
 
## jp_gates_original.png
  - Original example image
  
## images
  - Example folder with images
  
