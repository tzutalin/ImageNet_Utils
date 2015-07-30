# ImageNet_DownloadHelper
Utils to help download images by wnid, crop bounding box, etc.
# Usage
usage: main.py [-h] [--wnid WNID] [--downloadImages]
               [--downloadOriginalImages] [--downloadBoundingBox] [--verbose]

Help the user to download, crop, and handle images from ImageNet

optional arguments

  -h, --help            show this help message and exit

  --wnid WNID           ImageNet Wnid. E.g. : n02710324

  --downloadImages      Should download images

  --downloadOriginalImages
                        Should download original images

  --downloadBoundingBox
                        Should download bouding box annotation files

  --verbose, -v         Enable verbose log

# Sample:
Get the urls of wnid and download all of them

$ python main.py --downloadImages --wnid n02710324

Download the boundingbox xml of wnid

$ python main.py --downloadBoundingBox --wnid n00007846

Download all original images

$ python main.py --downloadOriginalImages --wnid n00007846

# Other utils
Utils to create train.txt and test.txt

Use the bellow cmd, and you can get image path and its label in train.txt and test.txt

$ python labelcreator.py --size_of_train 1400 --size_of_test 200  --label 11 --dir car

Auto assign a label to each folder containing images under the dir

$ python labelcreator.py --size_of_train 1400 --size_of_test 200
