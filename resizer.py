import os
import sys
from PIL import Image

TARGET_XY_MAX = 1080 # desired max height AND width of resized image in pixels (new image should fit in a TARGET_XY_MAX x TARGET_XY_MAX box)
FILE_TYPES = ['.jpg', '.jpeg', '.png']

if len(sys.argv) != 2:
    print("Bro, try: 'python3 resizer.py <path-to-directory-of-images-to-resize>'")
    print('Try again.')
    sys.exit(-1) # sys.argv[0] is name of program

source_image_dir = sys.argv[1]

file_list = []
print('Scanning files...')

for root, dirnames, filenames in os.walk(source_image_dir):
    for file in filenames:
        fname, fext = os.path.splitext(file)
        if fext.lower() in FILE_TYPES:
            file_list.append(os.path.join(root, file))

print(f'Found {len(file_list)} file(s) with the file extensions of type: {FILE_TYPES}')

print('Resizing now...')

for file in file_list:
    try:
        image = Image.open(file)
        print(f'Opening file: {file}')
        print(f'Format: {image.format}')
        print(f'Size: {image.size}')

        # Grab filename from file
        resized_filename = os.path.basename(file)

        # Create the output directory if necessary
        resize_dir = os.path.dirname(file) + '_resized'
        if not os.path.exists(resize_dir):
            os.mkdir(resize_dir)

        # Save the resized file
        # First get the max(width, height) so we can scale the largest dimension
        orig_max_dimension = max(image.size)

        # Now calculate the scaling ratio (only scale image down- not up)
        sr = 1.0
        if orig_max_dimension > TARGET_XY_MAX:
            sr = TARGET_XY_MAX/orig_max_dimension

        # Resize and save it
        new_size = tuple(round(sr * x) for x in image.size)
        print(f'Using scaling ratio of {sr}, resized image: {new_size}')
        new_image = image.resize(new_size)
        new_image.save(os.path.join(resize_dir, resized_filename))

    except IOError as ioe:
        print(f'Unable to open file: {file}')
        print(ioe)
