"""
Course: cmps 4883
Assignemt: A05
Date: 3/05/19
Github username: JakobLopez
Repo url: https://github.com/JakobLopez/4883-SWTools-Lopez
Name: Jakob Lopez
Description: 
    This program converts an image into ascii art.
    Each pixel in the provided image is assigned to a unicode
    character depending on the pixel's greyscale value. The 
    lower the value, the darker the character. After the unicode 
    characters have been assigned each pixel, they are drawn onto a 
    white background in the same color as their corresponding pixel. 
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

"""
Name: img_to_ascii
Description: 
    Resizes image to a smaller version.
    Converts the image to grayscale.
    Assigns an ascii character to each pixel depending
    on the pixel's grayscale value. Each ascii character
    is added to list.
Params:
    **kwargs - contains width and image path
Returns:
    original - the resized original image
    imlist - the list of ascii characters that represent each pixel
    w - image width
    h - image height
"""
def img_to_ascii(**kwargs):
    """ 
    The ascii character set we use to replace pixels. 
    The grayscale pixel values are 0-255.
    0 - 25 = '#' (darkest character)
    250-255 = '.' (lightest character)
    """
    ascii_chars = [ str(2), str(1), 'T', 'S', 'W', 'L', 'J', 'I', 'D', 'E', 'K']
  
    width = kwargs.get('width',200)
    path = kwargs.get('path',None)

    #Open image
    im = Image.open(path)

    #Resize
    im = resize(im,width)
    #Copy of original resized image
    original = im

    #width and height
    w,h = im.size
    print(w,h)

    # convert to grayscale
    im = im.convert("L") 

    #Return grayscale values to list
    imlist = list(im.getdata())

    #Assign ascii character to grayscale ranges
    imlist[:] = [ascii_chars[val // 25] for val in imlist]
    """
    #Write ascii art to file
    f = open("demofile.txt", "w")
    i = 1
    for val in imlist:
        f.write(val)
        i += 1
        if i % width == 0:
            f.write("\n")
    f.close()
    """
    
    return original, imlist, w, h

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

"""
Name: ascii_img_to_color
Description: 
    Draws the original image onto a white background where 
    each ascii character represents a pixel. The ascii characters
    are drawn in the color of the pixel they represent.
Params:
    orig - the original resized image
    ascii_im - list of ascii characters for each pixel in orig
    w - width
    h - height
    font - font that the ascii characters will be written in
Returns:
    newImg - the drawn ascii image
"""
def ascii_img_to_color(orig, ascii_im, w, h,font):
    #Open a new image using 'RGBA' (a colored image with alpha channel for transparency)
    #              color_type      (w,h)     (r,g,b,a) 
    #                   \           /            /
    #                    \         /            /
    newImg = Image.new('RGBA', (w*5,h*5), (255,255,255,255))
    
    #Open a TTF file and specify the font size
    fnt = ImageFont.truetype(font, 12)

    #Get a drawing context for your new image
    drawOnMe = ImageDraw.Draw(newImg)

    #Convert original image to rgb
    rgb_im = orig.convert('RGB')

    i = 0
    for y in range(h):
        for x in range(w):
            #Ascii character from list
            c = ascii_im[i]
            #Increment
            i = i+1

            #Color of pixel in original img
            color = rgb_im.getpixel((x,y)) 

            #Add a character to some xy 
            #         location   character  ttf-font   color-tuple
            #            \         /        /            /
            #             \       /        /            /
            drawOnMe.text(((x*5)-1,(y*5)-1), c, font=fnt, fill=color)
            #Uncomment to overlap characters and output better image
            """drawOnMe.text(((x*5)-1,(y*5)+1), c, font=fnt, fill=color)
            drawOnMe.text(((x*5)+1,(y*5)-1), c, font=fnt, fill=color)
            drawOnMe.text(((x*5)+1,(y*5)+1), c, font=fnt, fill=color)"""
    return newImg



if __name__=='__main__':
    #Image 
    path = 'sp.jpg'
    #Convert image to ascii
    orig, ascii_im, w, h = img_to_ascii(path=path,width=150)

    #Downloaded font
    font_type = 'Aliencons TFB.ttf'
    #Redrawn ascii image
    img = ascii_img_to_color(orig,ascii_im,w,h, font_type)

    #Display your new image 
    img.show()

    #Save the image
    img.save('output.png')