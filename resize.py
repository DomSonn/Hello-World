'''
Script to resize all images in a selected directory and save copies in the same folder

Run the script from the same folder your images are in

Change the 'new_dimensions' variable as desired
'''

from PIL import Image
import os
import sys

directory = sys.argv[1]

for file_name in os.listdir(directory):
  print("Processing %s" % file_name)
  image = Image.open(os.path.join(directory, file_name))

  new_dimensions = (224, 224)
  output = image.resize(new_dimensions, Image.ANTIALIAS)

  output_file_name = os.path.join(directory, "resize_" + file_name)
  output.save(output_file_name, "JPEG", quality = 95)

print("All done")