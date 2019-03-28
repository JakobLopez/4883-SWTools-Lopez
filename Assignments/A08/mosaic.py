import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import glob
from random import *

"""
Name: resize
Description: 
    This resizes the img while maintining aspect ratio. Keep in 
    mind that not all images scale to ascii perfectly because of the
    large discrepancy between line height line width (characters are 
    closer together horizontally then vertically)
Params:
    img - image to be resized
    width - specified width of resized image
Returns:
    img - resized image
"""
def resize(img,width):

    wpercent = float(width / float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((width ,hsize), Image.ANTIALIAS)

    return img
if __name__=='__main__':
    """
    #Path to image (./input_images/picture.jpg) 
    input_path = sys.argv[1]
    #Path to output (./output_images/output.png)
    output_path = sys.argv[2]
    #Path to font type (./path_to_file/fonttype.ttf)
    font_type = sys.argv[3]
    #Size of font
    font_size = sys.argv[4]
    """

    path = './emojis/100.png'
    original = './si.png'

    im = Image.open(original)

    width, height = im.size

    files = glob.glob('./emojis/**/*.png', recursive=True)

    bg = Image.new("RGBA", (width * 64, height * 64), "white")
    print(len(files))


    for y in range(height):
        y = y * 64
        for x in range(width):
            #Open random emoji
            emoji = Image.open(files[randint(0,876)]).convert("RGBA")

            bg.paste(emoji, (x*64,y),emoji)

            emoji.close()
        
    bg.save('output.png')