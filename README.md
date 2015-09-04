# ImageNet-Utils
Utils to help download images by wnid, crop bounding box, etc.

### Requirements
If you would like to download the original images, you should signup [ImageNet](http://www.image-net.org/)

### Usage - Download images:
Get the urls of wnid and download all of them. E.g., download [Dog images from ImageNet](http://www.image-net.org/synset?wnid=n02084071) and save images to ./n02084071/url_images/*.jpg

`$ python downloadutils.py --downloadImages --wnid n02084071`

Download all original images. E.g., download the original images about [person](http://www.image-net.org/synset?wnid=n00007846) and save to ./n00007846/n00007846_original_images/*.JPEG

`$ python downloadutils.py --downloadOriginalImages --wnid n00007846`

Download the boundingbox xml of wnid. E.g., download  bounding boxes of original images about [person](http://www.image-net.org/synset?wnid=n00007846)

`$ python downloadutils.py --downloadBoundingBox --wnid n00007846`

### Usage - Label images:
Utils to create train.txt, val.txt, and test.txt

Use the bellow cmd, and you can get image path and its label in train.txt and test.txt

`$ python labelcreator.py --size_of_train 1400 --size_of_test 200  --label 11 --dir car`

Auto assign a label to each folder containing images under the dir. Create train.txt, val.txt, and test.txt. Size is 1200, 300, and 300

`$ python labelcreator.py --size_of_train 1200 --size_of_val 300 --size_of_test 300`

### Usage - Process boundingbox xml:
Search the specificed image according to its boudingbox's xml. If found, it will crop and save as ./boundingbox/*.JPEG

`$ python bbox_helper.py --bxmlpath n00007846/Annotation/n00007846/n00007846_23985.xml --save_boundingbox`

Output:

	./n00007846/n00007846_original_images/n00007846_23985.JPEG

	[[227, 25, 323, 91]]
	save to n00007846/bounding_box_imgs/n00007846_23985_box1.JPEG

`$ python bbox_helper.py --bxmldir n00007846/ --save_boundingbox`

Output:

	./n00007846/n00007846_original_images/n00007846_35737.JPEG
	[[46, 99, 165, 290]]
	save to n00007846/bounding_box_imgs/n00007846_35737_box1.JPEG
	./n00007846/n00007846_original_images/n00007846_132010.JPEG
	[[101, 57, 330, 497]]
	save to n00007846/bounding_box_imgs/n00007846_132010_box1.JPEG
	./n00007846/n00007846_original_images/n00007846_158081.JPEG
	[[55, 85, 249, 498]]
	.....

### Usage - Prepare ground truth for detection:
Help users to prepare ground truth for ILSVC detection results evaluation.

Create results for (ImageNet Large Scale Visual Recognition Challenge development kits)[http://image-net.org/challenges/LSVRC/2014/index]

`$ python gt_det.py dst_dir -p ann_dir img_dir labelMap.txt structure.xml`

The above command will search `ann_dir` and `img_dir` recursively and copies annotation files and images to `dst_dir`. It also generates image ID list and meta data in `dst_dir`. `-p ann_dir img_dir labelMap.txt structure.xml` can be omitted if the same settings are used.

`labelMap.txt` maps the integer label to the name in annotations. For instance,

	20 n03781787
	15 n00007846
	9 n03002096

or

	20 tvmonitor
	15 person
	9 chair

`structure.xml` is the ImageNet structure file http://www.image-net.org/api/xml/structure_released.xml, which is optional.

### Usage - Reorder the meta data:
Reorder the meta data to match the labels of given dataset.

`$ python reorder_meta.py src.mat order.txt dst.mat`

`order.txt` list the WNIDs in the desired order. For example,

	n03781787
	n00007846
	n03002096

Add `--padding` to pad empty item if WNID is not found in `src.mat`.
