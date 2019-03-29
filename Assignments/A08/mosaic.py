import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import glob
from random import *
from dominant_color import get_dominant_colors
import json


def resize(img,width):
    """
    Resizes the img while maintining aspect ratio. Keep in 
    mind that not all images scale to ascii perfectly because of the
    large discrepancy between line height line width (characters are 
    closer together horizontally then vertically)
    Params:
        img - image to be resized
        width - specified width of resized image
    Returns:
        img - resized image
    """
    wpercent = float(width / float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((width ,hsize), Image.ANTIALIAS)

    return img

def process_folder_images(path_to_folder):
    """
    Creates a JSON file containing dominant color information for each image
    in folder
    Params:
        path_to_folder - path to a folder of image (ex. './emojis')
    Returns:
        none
    Requires:
        get_dominant_colors
    """
    data = {}

    files = glob.glob(path_to_folder + '/**/*.png', recursive=True)

    for file in files:  
        file_path = file.replace('\\','/')
        colors = get_dominant_colors(file_path)
        data[file_path] = colors

    with open('color_data.json','w') as f:
        f.write(json.dumps(data))
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
    """
    path = './emojis/100.png'
    original = './si.png'

    im = Image.open(original)

    width, height = im.size

    files = glob.glob('./emojis/**/*.png', recursive=True)

    bg = Image.new("RGBA", (width * 64, height * 64), "white")


    for y in range(height):
        y = y * 64
        for x in range(width):
            #Open random emoji
            emoji = Image.open(files[randint(0,876)]).convert("RGBA")

            #Paste emoji where pixel is in original image
            bg.paste(emoji, (x*64,y),emoji)

            emoji.close()
        
    bg.save('output.png')
    """
    process_folder_images('./emojis')

    #print(colors)