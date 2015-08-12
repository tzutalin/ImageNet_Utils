# ImageNet_DownloadHelper
Utils to help download images by wnid, crop bounding box, etc.

### Requirements
You should signup [ImageNet](http://www.image-net.org/)

### Usage - Download images:
Get the urls of wnid and download all of them

`$ python downloadutils.py --downloadImages --wnid n02710324`

Download the boundingbox xml of wnid

`$ python downloadutils.py --downloadBoundingBox --wnid n00007846`

Download all original images

`$ python downloadutils.py --downloadOriginalImages --wnid n00007846`

### Usage - Label images:
Utils to create train.txt, val.txt, and test.txt

Use the bellow cmd, and you can get image path and its label in train.txt and test.txt

`$ python labelcreator.py --size_of_train 1400 --size_of_test 200  --label 11 --dir car`

Auto assign a label to each folder containing images under the dir. Create train.txt, val.txt, and test.txt. Size is 1200, 300, and 300

`$ python labelcreator.py --size_of_train 1200 --size_of_val 300 --size_of_test 300`

### Usage - Process boudingbox xml:
Search the specificed image according to its boudingbox's xml
`$ python bbox_helper.py --bpath n00007846/Annotation/n00007846/n00007846_23985.xml`

Output:

	./n00007846/n00007846_original_images/n00007846_23985.JPEG

	[[227, 25, 323, 91]]
