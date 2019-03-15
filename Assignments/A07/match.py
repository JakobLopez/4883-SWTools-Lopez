"""
Course: cmps 4883
Assignemt: A07
Date: 3/15/2019
Github username: JakobLopez
Repo url: https://github.com/JakobLopez/4883-SWTools-Lopez
Name: Jakob Lopez
Description: 
	Ex. of command line
		python match.py folder='path' image='path'
		folder => path to a folder of images
		image => path to an image you want to be compared
    This program finds the most similar image in the folder
	to the original image provided. Images are compared using 2
	different methods: mse and ssim. MSE is faster but less accurate,
	and ssim is slower but more accurate. The most similar image using
	both methods are displayed using matplotlib. If the original 
	image is in the folder, it won't be displayed as most similar.
"""
from skimage.measure import compare_ssim 
import matplotlib.pyplot as plt
import numpy as np
import cv2
import sys
import os

def mse(imageA, imageB):
	"""
	Calculates the Mean Squared Error between 2 images.
	Params:
		imageA - 1st image
		imageB - 2nd image
	Returns:
		The mse of the 2 images
	"""
	#Resize image
	imageA,imageB = resize(imageA,imageB)

	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def ssim(imageA, imageB):
	"""
	Calculates the Structural Similarity between 2 images
	Params:
		imageA - 1st image
		imageB - 2nd image
	Returns:
		The ssim of the 2 images
	"""
	imageA,imageB = resize(imageA,imageB)
	s = compare_ssim(imageA,imageB)
	#The closer the ssim is to 1, the more similar images are
	return s

def resize(a,b):
	"""
	Resizes the bigger image to the size of the smaller one
	Params:
		imageA - 1st image
		imageB - 2nd image
	Returns:
		The 2 resized images
	"""
	#Dimensions of image
	ah, aw= a.shape
	bh, bw = b.shape

	#If 2nd image is bigger
	if (ah*aw) < (bh*bw):
		#Resize to the size of the 1st image
		b = cv2.resize(b, (aw,ah))
	#If 1st image is bigger
	elif (ah*aw) > (bh*bw):
		#Resize to the size of the 2nd image
		a = cv2.resize(a, (bw,bh))

	return a,b

def get_arguments():
	"""
	Puts arguments from command line into dictionary.
	Assumes arguments are like: key1=val1 key2=val2 (with NO spaces between key equal val!)
	Params:
		None
	Returns:
		Dictionary with arugments
	"""
	args = {}
	#For every arg after 'python match.py'
	for arg in sys.argv[1:]:
		#Left side of '=' is key
		#Other side is key's value
		k,v = arg.split('=')
		args[k] = v
	return args

#Dictionary of arguments
args = get_arguments()

#Exit program if not enough arugments
if(len(args) < 2):
	print("Not enough arguments. Expected folder and image.")
	exit(1)

#Original image from arguments
original = cv2.imread(args['image'])
#Grayscale
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)

comparisons = {}
#Loop through directory
for dirname, dirnames, filenames in os.walk(args['folder']):
	#Loop through every file
	for filename in filenames:
		#Get path name and replace \ with /
		path = os.path.join(dirname, filename).replace("\\","/")
		
		#Image in file
		comparison = cv2.imread(path)
		#Grayscale
		comparison = cv2.cvtColor(comparison, cv2.COLOR_BGR2GRAY)
		
		#Get mse of original and current image
		m = mse(original,comparison)

		#Get ssim of original and current image 
		s = ssim(original,comparison)
		#If compared image is not the original
		if(s != 1 and m != 0):
			#Add results to dictionary
			comparisons[path] = {}
			comparisons[path]['image'] = comparison
			comparisons[path]['path'] = path
			comparisons[path]['mse'] = m
			comparisons[path]['ssim'] = s

#Get path to images closest to original according to mse and ssim
lowest_mse = min(comparisons, key=lambda x:comparisons[x]['mse'])
highest_ssim = max(comparisons, key=lambda x:comparisons[x]['ssim'])

#Closest images to original
mse_image = comparisons[lowest_mse]['image']
ssim_image = comparisons[highest_ssim]['image']

# initialize the figure
fig = plt.figure("Images")
plt.suptitle("Closest Images")

# show the image
ax = fig.add_subplot(131)
ax.set_title("Original")
plt.imshow(original, cmap = plt.cm.gray)
plt.axis("off")

# show the image
ax = fig.add_subplot(132)
ax.set_title("Lowest MSE: %.2f" % comparisons[lowest_mse]['mse'])
plt.imshow(mse_image, cmap = plt.cm.gray)
plt.axis("off")

# show the image
ax = fig.add_subplot(133)
ax.set_title("Highest ssim: %.2f" % comparisons[highest_ssim]['ssim'])
plt.imshow(ssim_image, cmap = plt.cm.gray)
plt.axis("off")
 
# show the figure
plt.show()