# Digital Image Processing Project
# Group 14
# Douglas Seiti Kodama - 9277131
# Leonardo de Souza Lemes - 8941126

# please note, we are assuming the most significant bit is bit 7, and the least significant bit is bit 0
# 0  0  0  0    0  0  0  0
# b7 b6 b5 b4   b3 b2 b1 b0

import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
import collections
import sys

# sets or resets the n-th bit of num depending on val
# example:
# num: 8 = 0000 1000
# th: 2
# val: 1
# returns num: 12 = 0000 1100
# basically it puts val (either 0 or 1) into the n-th bit of num
def set_bit(num, th, val):
	mask = 1 << th # mask to be used, the n-th bit is set
	num &= ~mask # perform an AND with the negation of the mask, resetting the n-th bit to 0 and not changing any other

	# if val is set, then set the n-th bit
	if val:
		num |= mask

	return num

# returns the value of the n-th bit of num
# example:
# num: 8 = 0000 1000
# val: 3
# returns 1
def get_bit(num, th):
	return (num >> th) & 1

# receives a string and returns a vector of ints with each character's ASCII code
def encode_message(msg):
	n = len(msg)
	res = np.zeros(n, np.uint8)

	for i in range(0, n):
		res[i] = ord(msg[i])

	return res

# receives a vector of ints and converts each number to its characters representation
# returns the string containing each value's character
def decode_message(res):
	n = len(res)
	msg = ""

	for i in range(0, n):
		msg += chr(res[i])

	return msg

# hides the msg into the img using the n-th bit
# returns the image with altered bits
def hide(img, msg, th):
	# gets a copy of the image and its dimensions
	res = img.copy()
	(h, w, tmp) = res.shape

	# gets the ASCII values of the message and its size
	n = len(msg)
	convertedMsg = encode_message(msg)

	# number of 8x8 regions on the image
	nHregions = math.floor(w / 8)
	nVregions = math.floor(h / 8)

	# index for the message
	index = 0

	for i in range(0, nVregions): # for each horizontal region
		for j in range(0, nHregions): # for each vertical region
			for channel in range(0, 3): # for each channel of the region
				for l in range(0, 8): # for each of the 8 lines of the 8x8 region (i, j)
					# converts the character to be put into this line to binary
					binChar = np.binary_repr(convertedMsg[index], 8)
					
					# index for the binChar
					# binChar is a string like "00001010"
					# so beware, here, binChar[0] is the most significant bit of the value
					# and binChar[7] is the least significant bit of the value
					count = 0
					
					for m in range(0, 8): # for each of the 8 columns of the line
						# alters the pixel value, setting or resetting the n-th bit of the pixel's intensity value with the bit of binChar[count]
						res.itemset((i * 8 + l, j * 8 + m, channel), set_bit(res.item(i * 8 + l, j * 8 + m, channel), th, int(binChar[count])))
						count += 1

					# finished hiding a character, increment index
					index += 1

					# finished hiding all characters, return the image
					if (index == n):
						return res

# recovers the message of size n, from an image img, with bits hidden on the n-th bit
# returns a string containing the message recovered
def recover(img, n, th):
	# gets the image dimensions
	(h, w, tmp) = img.shape

	# initializes the vector that will contain the recovered message's ASCII values
	res = np.zeros(n, np.uint8)

	# number of 8x8 regions on the image
	nHregions = math.floor(w / 8)
	nVregions = math.floor(h / 8)

	# index of the message
	index = 0

	for i in range(0, nVregions): # for each horizontal region
		for j in range(0, nHregions): # for each vertical region
			for channel in range(0, 3): # for each channel of the region
				for l in range(0, 8): # for each of the 8 lines of the 8x8 region (i, j)
					# b is a string that will contain the recovered bits of the character
					b = ""

					for m in range(0, 8): # for each of the 8 columns of the line
						# gets the value of the bit and appends it to b
						b += str(get_bit(img.item(i * 8 + l, j * 8 + m, channel), th))
					
					# finished getting all 8 bits of the ASCII value
					# converts this b string to an int value and stores it into the recovered message
					res[index] = int(b, 2)
					
					# recovered a single character, increment index
					index += 1

					# finished recovering all characters
					if (index == n):
						# returns the string of these ASCII values
						return decode_message(res)

# shows the pixel's intensity values in binary from 3 images, useful for debugging
# img1: original image
# img2: PNG image
# img3: JPEG image
# n: size of the message
def print_result(img1, img2, img3, n):
	# gets the image dimensions, all the 3 images have the same dimensions
	(h, w, tmp) = img1.shape

	# number of 8x8 regions on the image
	nHregions = math.floor(w / 8)
	nVregions = math.floor(h / 8)

	# index of the message
	index = 0

	for i in range(0, nVregions): # for each horizontal region
		for j in range(0, nHregions): # for each vertical region
			for channel in range(0, 3): # for each channel of the region
				print("i:", i, "- j:", j)
				print("\tchannel:", channel)
				print("\t\toriginal\tPNG\t\t\tJPG")
				for l in range(0, 8): # for each of the 8 lines of the 8x8 region (i, j)
					for m in range(0, 8): # for each of the 8 columns of the line
						# prints the binary representation for a single pixel of each of the 3 images
						print("\t\t", np.binary_repr(img1.item(i * 8 + l, j * 8 + m, channel), 8), "\t", np.binary_repr(img2.item(i * 8 + l, j * 8 + m, channel), 8), "\t", np.binary_repr(img3.item(i * 8 + l, j * 8 + m, channel), 8), sep = "")
					print()

					# finished printing all the pixels of a single character
					index += 1

					# finished printing all the pixels used to store the message
					if (index == n):
						return

# returns the RMSD of two images, f and g
def RMSD(f, g):
	# get the image dimensions, both must have the same dimensions
	(height, width, channels) = f.shape

	# compute the squared difference between f and g
	tmp = cv2.subtract(np.int64(f), np.int64(g))
	tmp = cv2.pow(tmp, 2)

	# compute the square root of the sum of the squared differences between f and g divided by height times width
	e = math.sqrt(np.sum(tmp) / (height * width))

	return e

# copies each character of the message 24 times and returns it
# example:
# msg: "a"
# returns "aaaaaaaaaaaaaaaaaaaaaaaa"
def enlarge_msg(msg):
	res = ""

	for i in range(0, len(msg)):
		for j in range(0, 24):
			res += msg[i]

	return res

# receives a message with redundancy and returns the message's most likely original state
# it basically analyses each block of 24 characters and selects the most frequent one
# to use as the character on the result message
# example:
# msg: "aaaaaaaabbaaaaaabbbbaaaa"
# returns "a"
def trim_msg(msg):
	res = ""

	for i in range(0, len(msg), 24): # for each block of 24 characters of the input message
		aux = ""
		for j in range(i, i + 24): # get all the 24 characters of the block
			aux += msg[j]
		res += collections.Counter(aux).most_common(1)[0][0] # get the most frequent one on the block

	return res

# since we are dealing with quite big outputs, we are writing the output to a text file named output.txt
sys.stdout = open("output.txt", "w")

imgFileName = "../in/" + str(sys.argv[1]) # filename for the image
msgFileName = str(sys.argv[2]) # filename for the message
bit = int(sys.argv[3]) # n-th bit to use
quality = int(sys.argv[4]) # quality to use in the JPEG compression, from 0 to 100
redundancyFlag = int(sys.argv[5]) # flag to use the redundancy method
showDebugFlag = int(sys.argv[6]) # flag to print additional debug data

# loads the input image
img = cv2.imread(imgFileName)

# loads the message
with open(msgFileName) as msgFile:
	msg = msgFile.read()

# hides the message in the image using the n-th bit
if (redundancyFlag):
	largeMsg = enlarge_msg(msg)
	stegoImg = hide(img, largeMsg, bit)
else:
	stegoImg = hide(img, msg, bit)

cv2.imwrite("./out/png/" + imgFileName[5:len(imgFileName) - 4] + ".png", stegoImg, (cv2.IMWRITE_PNG_COMPRESSION, 0)) # saves a PNG file with no compression
cv2.imwrite("./out/jpg/" + imgFileName[5:len(imgFileName) - 4] + ".jpg", stegoImg, (cv2.IMWRITE_JPEG_QUALITY, quality)) # saves a JPEG file with determined quality

# loads the PNG and JPEG image
resPNG = cv2.imread("./out/png/" + imgFileName[5:len(imgFileName) - 4] + ".png")
resJPG = cv2.imread("./out/jpg/" + imgFileName[5:len(imgFileName) - 4] + ".jpg")

# if flag is set to 1, shows additional debug data
if (showDebugFlag and redundancyFlag):
	print_result(img, resPNG, resJPG, len(largeMsg))
elif (showDebugFlag and (not redundancyFlag)):
	print_result(img, resPNG, resJPG, len(msg))

# recovers the message from the JPEG image
if (redundancyFlag):
	recoveredMsg = recover(resJPG, len(largeMsg), bit)
	recoveredMsg = trim_msg(recoveredMsg)
else:
	recoveredMsg = recover(resJPG, len(msg), bit)

# prints both messages
print(msg)
print(recoveredMsg)

# calculates the loss percentage of the message
matches = 0
for i in range(0, len(msg)):
	if (msg[i] == recoveredMsg[i]):
		matches += 1

lossRate = 100 - (100 * (matches / len(msg)))

# prints the loss rate of the message
print("%.2f%% lost" % lossRate)

#prints the RMSD between original image and JPEG image
print("RMSD: %.2f" % RMSD(img, resJPG))

sys.stdout.close()