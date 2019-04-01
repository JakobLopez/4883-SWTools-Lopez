import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dominant_color import get_dominant_colors
import json
from process_files import openFileJson
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


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


def get_color_distance(pixel_color, subimage_color):
    #A result less than 2 is generally considered to be perceptually equivalent.
    
    color1_rgb = sRGBColor(pixel_color[0],pixel_color[1],pixel_color[2])

    color2_rgb = sRGBColor(subimage_color[0],subimage_color[1],subimage_color[2])

    # Convert from RGB to Lab Color Space
    color1_lab = convert_color(color1_rgb, LabColor)

    # Convert from RGB to Lab Color Space
    color2_lab = convert_color(color2_rgb, LabColor)

    # Find the color difference
    delta_e = delta_e_cie2000(color1_lab, color2_lab)

    return delta_e

def process_argv(args):
    """Takes arguments of type k=v and places them into 
    a dictionary. Arguments must ALL be k=v and not have
    any spaces.
    
    Example:
        python3 program.py key1=val1 key2=val2 key3=val3

        results in:

        {key1:val1,key2:val2,key3:val3}

    Arguments:
        argv   -- [list] sys.argv list of arguments
    Returns:
        dictionary
    """
    argd = {}
    for arg in args[1:]:
        k,v = arg.split('=')
        argd[k] = v
    return argd

if __name__=='__main__':
    #Get arguments
    args = process_argv(sys.argv)

    #Assign arguments
    image = args['input_file']
    folder = args['input_folder']
    size = int(args['size'])
    output = args['output_folder']

    #process_folder_images(folder)

    #Open given image
    im = Image.open(image)

    #Convert to RGBA
    im = im.convert('RGBA')

    #Get dimensions
    width, height = im.size
    if width > 1000:
        im = resize(im,width//8)
        width, height = im.size
    print(im.size)

    #Open json with player info
    data = openFileJson('./color_data.json')

    #Create new image to draw on
    bg = Image.new("RGBA", (width * size, height * size), "black")

    #No previous color because loop has not started
    prev_color = None

    #For every y in original image
    for y in range(height):

        #Update pixel for new image
        y2 = y * size

        #For every x in original image
        for x in range(width):
            #Color of pixel in original img
            color = im.getpixel((x,y)) 

            #If there is no previous color or color is not same as previous
            if not prev_color or get_color_distance(color,prev_color) >= 8:
                #Choose big closest value
                closest = 150

                #For ever subimage's dominant color
                for emoji_path,emoji_data in data.items():
                    #Get difference between current pixel and most dominant color in subimage
                    distance = get_color_distance(color,emoji_data[0]['rgb'])
                    #If difference is less than closest
                    if distance < closest:
                        #Update closest
                        closest = distance
                        closest_im = emoji_path

            #Open closest subimage            
            emoji = Image.open(closest_im).convert('RGBA')

            #Resize image
            emoji = emoji.resize((size,size))
            
            #Make a small background image the same color as pixel
            bg_color = Image.new('RGBA', (size,size), color)

            #Paste onto our canvas
            bg.paste(bg_color,(x * size, y2))

            #Paste closest subimage background and mask alpha channel for transparency
            bg.paste(emoji, (x * size, y2), emoji)

            #Update previous color
            prev_color = color
    
    #Split the image path on '/'
    image_parts = image.split('/')

    #Split file name on '.'
    name, ext = image_parts[-1].split('.')

    #Save image
    bg.save(output + '/' + name + '_mosaic.png')
  