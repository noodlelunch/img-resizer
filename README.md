# img-resizer
img-resizer is a batch image resizer, written in Python.

### The Story
I wrote this little tool when a friend called, asking me what he should use to resize a bunch of images for some volunteer work he was doing. I suggested a few things, then ended our conversation by pointing out that as an experienced developer, he could write one himself pretty quickly.


Having been laid off during the coronavirus pandemic, it had been a while since I'd written any code, so I decided to write one for my friend. Of course I didn't tell him what I was doing, so I was racing against the clock before he found one of the bazillions of free resizers that I assured him must exist. I knew I had no use for this tool, but I also knew my friend is lazy, so I had that working for me (just kidding, S!).

The problem was I had no idea what types of files my friend needed to resize, nor what file structure he would receive them in. I could safely assume they would be used for web purposes. So with flexibility in mind, I spent the following morning writing a little app/script that would do the following:

> Supplied with a path to a directory of images, proportionally scale down all png or jpeg images it finds. Place these images in a directory named the same as the source directory, with "\_resized" appended to the name. Create this target directory at the same level as the source directory. Descend into any subdirectories and do the same thing. Images that are smaller than _xymax_ pixels don't get resized, but just get copied. In other words, we only scale down.

_xymax_ is a single integer that represents the sides of a square into which your resized image will fit. In other words, if the image is portrait orientation, the resized image will be _xymax_ pixels tall. If it's landscape orientation, it will be _xymax_ pixels wide. Default value is 1080.

So that was it. Probably less than 40 lines of actual code. It worked with my test directory of images and I sent it off to my friend, who, it turned out, still had yet to receive any images to resize.

A few days later he tried it out (it apparently worked) and he emailed me with some image sizing specifications for WordPress and Facebook.

So now I had a dilemma on my hands. I still didn't really know what he was starting with, or what he was being asked to end up with. Seems I was more motivated to resize his files than he was. He could easily just change the value of _xymax_ in the code and run it once or twice, renaming the output directories.

Or I could let my unemployed, product-minded brain take over and further develop this tool that I have no use for (I have a Photoshop license, and I'm pretty sure it can do this as well. In fact, it was one of the things I offered to do for my friend, originally.) - just because.

First I added command line options for specifying a custom _xymax_ and renaming the images with the dimensions appended. (That also meant I had to make sure it didn't descend into directories it had created, or it would re-resize files if you wanted to run it multiple times with different _xymax_ values).

Then today I looked to see whether it was really optimizing quality when scaling down and found there's a better way to resample. I also looked into how it was compressing jpegs and added a flag to optionally reduce compression/increase quality. Finally, I added those flag settings to the output directory names to make it easier to compare file sizes.

So I'm finally about to send off this github URL to my friend, so he can try it. I don't *really* even know if it will work for him. Oh, but first it had an empty README.md. So that's what this is.


### Requirements
python3 (I wrote it with 3.8.4) with Pillow installed (I installed Pillow 7.2.0)

### Usage
python3 resizer.py path-to-directory-of-images-to-resize

More options:

```
(img-resizer-env) (Ted) ~/Documents/code/pie/img-resizer ]python resizer.py --help
usage: resizer.py [-h] [-xy XYMAX] [-r] [-b] [-q] path_to_images

positional arguments:
  path_to_images        path to directory of images to resize

optional arguments:
  -h, --help            show this help message and exit
  -xy XYMAX, --xymax XYMAX
                        Maximum X and Y dimensions of a box images will be scaled down to fit into.
  -r, --rename          Rename file(s) with file dimensions appended e.g. image.png -> image_100x200.png
  -b, --use-bicubic     By default, for best quality we resize using a Lanczos (aka anti-alias) filter. You can try this if you run into issues.
  -q, --max-quality     Default jpeg compression is 75. Using this flag sets it to 95, resulting in larger files, but slightly higher quality.
```

### Final Notes
I have no idea if this is of any use to anyone. Hopefully it will be to my friend. If he finds that it doesn't work, I'll fix it so it does. I have a note in the code that after writing the initial version, I learned there is a thumbnail() method that should remove a good chunk of code if used instead of resize(). I still haven't bothered to do that, mostly because I haven't wanted to invest the time to check the output. But I do believe it would be the right thing to do.
