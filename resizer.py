import argparse
import os
import re
import sys
from PIL import Image

FILE_TYPES = ['.jpg', '.jpeg', '.png']
DEFAULT_RESAMPLE_FILTER = Image.LANCZOS
resample_filter = DEFAULT_RESAMPLE_FILTER
DEFAULT_QUALITY = 75 # 'quality' property used when saving jpegs. I assume this is ignored when saving pngs.
quality = DEFAULT_QUALITY

dirname_pattern = re.compile("^.+_resized_\d+x\d+$") # Used to skip directories called foo_resized_1080x1080

parser = argparse.ArgumentParser()
parser.add_argument('path_to_images', help='path to directory of images to resize')

parser.add_argument("-xy", "--xymax", help="Maximum X and Y dimensions of a box images will be scaled down to fit into.",
                    type=int,  default=1080)

parser.add_argument("-r", "--rename", help="Rename file(s) with file dimensions appended e.g. image.png -> image_100x200.png",
                    action="store_true", default=False)

parser.add_argument("-b", "--use-bicubic", help="By default, for best quality we resize using a Lanczos (aka anti-alias) filter. You can try this if you run into issues.",
                    action="store_true", default=False)

parser.add_argument("-q", "--max-quality", help="Default jpeg compression is 75. Using this flag sets it to 95, resulting in larger files, but slightly higher quality.",
                    action="store_true", default=False)

# Extract args
args = parser.parse_args()

target_xy_max = args.xymax  # max height AND width of resized image in pixels (new image should fit in a target_xy_max x target_xy_max box)

rename_files = args.rename

if args.use_bicubic:
    resample_filter = Image.BICUBIC

if args.max_quality:
    quality = 95

# Start...
print(f'\nResizing images to fit in {target_xy_max} x {target_xy_max} box')
print(f"Images will{'' if rename_files else ' not'} be renamed.")
print(f"Downsampling using: {'bicubic' if args.use_bicubic else 'Lanczos'} filter")
print(f"Saving jpegs using {'maximum quality (minimal compression)' if args.max_quality else 'standard quality'}")

source_image_path = args.path_to_images

file_list = []
print('\nScanning files...\n')

for root, dirnames, filenames in os.walk(source_image_path):
    # Ignore directories we (probably) created so we don't re-resize images
    if dirname_pattern.match(root):
        dirnames[:] = []
        filenames[:] = []

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
        resize_dir = f"{os.path.dirname(file)}{'_bicubic' if args.use_bicubic else ''}{'_max-quality' if args.max_quality else ''}_resized_{target_xy_max}x{target_xy_max}"
        if not os.path.exists(resize_dir):
            os.mkdir(resize_dir)

        # Save the resized file
        # First get the max(width, height) so we can scale the largest dimension
        orig_max_dimension = max(image.size)

        # TODO: I think most of the resizing code can be replaced with .thumbnail()
        # but I just learned about its existence and don't really feel like spending
        # more time on this. Assuming it does what I think it does, it definitely
        # seems like a reasonable change to make.

        # Now calculate the scaling ratio (only scale image down- not up)
        sr = 1.0
        if orig_max_dimension > target_xy_max:
            sr = target_xy_max/orig_max_dimension

        # Resize and save it
        new_size = tuple(round(sr * x) for x in image.size)
        print(f'Using scaling ratio of {sr}, resized image: {new_size}')
        new_image = image.resize(new_size, resample_filter)

        # Grab filename from file and rename if requested
        resized_filename = os.path.basename(file)

        if rename_files:
            root_ext = os.path.splitext(resized_filename)
            resized_filename = f'{root_ext[0]}_{new_image.size[0]}x{new_image.size[1]}{root_ext[1]}'
            print('resized_filename: ', resized_filename)

        new_image.save(os.path.join(resize_dir, resized_filename), quality=quality)

    except IOError as ioe:
        print(f'Unable to open file: {file}')
        print(ioe)
