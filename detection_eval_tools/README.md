### Usage - Prepare ground truth for detection:
Help users to prepare ground truth for ILSVC detection results evaluation.

Create results for [ImageNet Large Scale Visual Recognition Challenge development kits](http://image-net.org/challenges/LSVRC/2014/index)

`$ ./gt_det.py dst_dir -p ann_dir img_dir labelMap.txt structure.xml`

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
