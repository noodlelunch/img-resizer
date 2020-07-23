import argparse
import os
import sys
from PIL import Image

FILE_TYPES = ['.jpg', '.jpeg', '.png']

dirname_pattern = re.compile("^.+_resized_\d+x\d+$") # Used to skip directories called foo_resized_1080x1080

parser = argparse.ArgumentParser()
parser.add_argument('path_to_images', help='path to directory of images to resize')

parser.add_argument("-xy", "--xymax", help="Maximum X and Y dimensions of a box images will be scaled down to fit into.",
                    type=int,  default=1080)

parser.add_argument("-r", "--rename", help="Rename file(s) with file dimensions appended e.g. image.png -> image_100x200.png",
                    action="store_true", default=False)

# Extract args
args = parser.parse_args()
rename_files = args.rename
target_xy_max = args.xymax  # max height AND width of resized image in pixels (new image should fit in a target_xy_max x target_xy_max box)

# Start...
print(f'Resizing images to fit in {target_xy_max} x {target_xy_max} box')
print(f"Images will{'' if rename_files else ' not'} be renamed.")

source_image_path = args.path_to_images

file_list = []
print('Scanning files...')

for root, dirnames, filenames in os.walk(source_image_path):
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

        # Create the output directory if necessary
        resize_dir = f'{os.path.dirname(file)}_resized_{target_xy_max}x{target_xy_max}'
        if not os.path.exists(resize_dir):
            os.mkdir(resize_dir)

        # Save the resized file
        # First get the max(width, height) so we can scale the largest dimension
        orig_max_dimension = max(image.size)

        # Now calculate the scaling ratio (only scale image down- not up)
        sr = 1.0
        if orig_max_dimension > target_xy_max:
            sr = target_xy_max/orig_max_dimension

        # Resize and save it
        new_size = tuple(round(sr * x) for x in image.size)
        print(f'Using scaling ratio of {sr}, resized image: {new_size}')
        new_image = image.resize(new_size)

        # Grab filename from file and rename if requested
        resized_filename = os.path.basename(file)

        if rename_files:
            root_ext = os.path.splitext(resized_filename)
            resized_filename = f'{root_ext[0]}_{new_image.size[0]}x{new_image.size[1]}{root_ext[1]}'
            print('resized_filename: ', resized_filename)

        new_image.save(os.path.join(resize_dir, resized_filename))

    except IOError as ioe:
        print(f'Unable to open file: {file}')
        print(ioe)
