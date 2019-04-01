import cv2
from PIL import Image, ImageDraw
import image_slicer


def thick_line(img,coords,fill,thickness=1,xy='x'):
    x1,y1,x2,y2 = coords

    dx=0
    dy=0
    for i in range(thickness):
        coord = x1+dx,y1+dy,x2+dx,y2+dy
        img.line(coord, fill=fill)
        if 'x' in xy:
            dx += 1
        else:
            dy += 1
    return img



if __name__=='__main__':
    #Path to picture
    path = 'vans-logo.png'

    #Split picture into slices
    #                  picture      # of slices     Don't automatic save
    #                         \        /            /
    #                          \      /            /                       
    tiles = image_slicer.slice(path, 4, save=False)
    
    #Output folder
    output = 'sliced_images/'

    #Saves split image chunks to folder
    #                    image slices     folder
    #                         \             /
    image_slicer.save_tiles(tiles, prefix=output)


    """
    image_name,ext = path.split('.')

    im = Image.open(path)

    if im.mode == 'P':
        im = im.convert('RGB')

    draw = ImageDraw.Draw(im)

    size = 16

    space = 0
    w,h = im.size
    fill = (0,0,0)

    while space < w:
        # tuples for line coords
        yline = (space,0,space,h)
        xline = (0,space,w,space)
        
        # draw the lines in the up and down and left and right
        draw = thick_line(draw,yline,fill,2,'x')
        draw = thick_line(draw,xline,fill,2,'y')

        # move lines over and down
        space += size

        

    # draw lines on bottom and far left
    draw = thick_line(draw,(w-2,0,w-2,h),fill,2,'x')
    draw = thick_line(draw,(0,h-2,w,h-2),fill,2,'y')
    im.show()


    out_name = image_name+'_'+str(size)+'.'+ext
    print(out_name)
    im.save(out_name, "PNG")
    """
   