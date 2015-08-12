# ImageNet_DownloadHelper
Utils to help download images by wnid, crop bounding box, etc.
### Usage
usage: main.py [-h] [--wnid WNID] [--downloadImages]
               [--downloadOriginalImages] [--downloadBoundingBox] [--verbose]

Help the user to download, crop, and handle bounding box and images from ImageNet

Download images from ImageNet:

	 usage: downloadutils.py [-h] [--wnid WNID] [--downloadImages]
	                        [--downloadOriginalImages] [--downloadBoundingBox]
	                        [--verbose]
	
	Help the user to download, crop, and handle images from ImageNet
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --wnid WNID           ImageNet Wnid. E.g. : n02710324
	  --downloadImages      Should download images
	  --downloadOriginalImages
	                        Should download original images
	  --downloadBoundingBox
	                        Should download bouding box annotation files
	  --verbose, -v         Enable verbose log


Assign labels:

	usage: labelcreator.py [-h] [--dir DIR] [--label LABEL]
	                       [--size_of_train SIZE_OF_TRAIN]
	                       [--size_of_val SIZE_OF_VAL]
	                       [--size_of_test SIZE_OF_TEST] [--file_train FILE_TRAIN]
	                       [--file_val FILE_VAL] [--file_test FILE_TEST]
	                       [--verbose]
	
	Create a label to train.txt, val.txt, or test.txt
	
	optional arguments:
	  -h, --help            show this help message and exit
	  --dir DIR, -d DIR     Image label that will be saved to train.txt or
	                        test.txt
	  --label LABEL, -l LABEL
	                        Image label that will be saved to train.txt or
	                        test.txt
	  --size_of_train SIZE_OF_TRAIN
	                        put how many image to train.txt
	  --size_of_val SIZE_OF_VAL
	                        put how many image to val.txt
	  --size_of_test SIZE_OF_TEST
	                        put how many image to text.txt
	  --file_train FILE_TRAIN
	                        The filename for train. By default, train.txt
	  --file_val FILE_VAL   The filename for validation. By default, val.txt
	  --file_test FILE_TEST
	                        The filename for test. By default, test.txt
	  --verbose, -v         Enable verbose log

### Sample:
Get the urls of wnid and download all of them

`$ python downloadutils.py --downloadImages --wnid n02710324`

Download the boundingbox xml of wnid

`$ python downloadutils.py --downloadBoundingBox --wnid n00007846`

Download all original images

`$ python downloadutils.py --downloadOriginalImages --wnid n00007846`

### Other utils
Utils to create train.txt and test.txt

Use the bellow cmd, and you can get image path and its label in train.txt and test.txt

`$ python labelcreator.py --size_of_train 1400 --size_of_test 200  --label 11 --dir car`

Auto assign a label to each folder containing images under the dir. Create train.txt, val.txt, and test.txt. Size is 1200, 300, and 300

`$ python labelcreator.py --size_of_train 1200 --size_of_val 300 --size_of_test 300`
