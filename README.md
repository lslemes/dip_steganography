# Hiding and revealing information on images
This project was created for the Image Processing course in 2017 at the Institute of Mathematics and Computer Science (ICMC), University of São Paulo (USP).

## Briefing
Our project’s main objective is to hide text within colored images using a few similar approaches, generating a JPEG image, which is a method of lossy compression for digital images (so we expect to lose some of the text’s data), and a PNG (with lossless compression, thus no loss) image. Then we are going to compare both images and check how the text was affected by the compression, and calculate how different it is from the original one.

## Running the demo
The "in" folder contains all the input images, if you want to use a personalized image, please, put it there.

To run the demo version, make sure your text file containing the message to be hidden is located at the demo folder, then run the command:

python3 demo.py img msg quality redundancy showFlag

img - the filename of the image

msg - the filename of the message

quality - the quality of the JPEG compression, from 0 to 100

redundancy - 1 to use redundancy method, 0 to not use it

showFlag - 1 to print out additional information on the output, 0 to not print the additional information

python3 demo.py img1.jpg msg.txt 100 0 0

This will run the demo and hide msg.text on img1.jpg, using all of the bits available, with 100% of quality on JPEG compression, without using the redundancy technique and without printing additional information on output.txt, after about 10 seconds the program will show you some plots comparing the results. The output images will be generated at the "out" folder if you want to check. The output.txt contains the output of the program (we're writing it to a file because it's easier to manipulate large text files out of the terminal).

## Running the final
To run the final version, make sure your text file containing the message to be hidden is located at the final folder, then run the command:

python3 main.py img msg bit quality redundancy showFlag

img - the filename of the image

msg - the filename of the message

bit - bit used to hide (0 the least significant, 7 the most significant)

quality - the quality of the JPEG compression, from 0 to 100

redundancy - 1 to use redundancy method, 0 to not use it

showFlag - 1 to print out additional information on the output, 0 to not print the additional information

python3 main.py img1.jpg msg.txt 7 100 1 1

This will run the final version and hide msg.txt on img1.jpg, using the most significant bit, 100% quality of JPEG compression, using redundancy technique and printing additional information on output.txt, after a couple seconds (might take a while for lage messages) the program will end its execution. You can check output.txt to see the message recovered, the percentage of message loss and the RMSD between the input and output image. The output images will be generated on the "out" folder.

## Authors
Douglas Seiti Kodama - 9277131

Leonardo de Souza Lemes - 8941126
