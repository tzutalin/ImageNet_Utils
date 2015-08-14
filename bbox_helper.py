import os
import Image
import sys
import zipfile
import xml.etree.ElementTree as ET

def scanAnnotationFolder(annotationFolderPath):
	annotationFiles = []
	for root, dirs, files in os.walk(annotationFolderPath):
		for file in files:
			if file.endswith('.xml'):
				annotationFiles.append(os.path.join(root, file))
	return annotationFiles

class BBoxHelper:
	def __init__(self, annotation_file, image_path = None):
		self.annotation_file = annotation_file
		xmltree = ET.parse(annotation_file)
		filename = xmltree.find('filename').text
		wnid = filename.split('_')[0]
		image_id = filename.split('_')[1]
		# create a dict to save filename, wnid, image id, etc..
		self.annotation_filename = filename
		self.wnid = wnid
		self.image_id = image_id
		# find bouding box
		objects = xmltree.findall('object')
		self.rects = []
		for object_iter in objects:
			bndbox = object_iter.find("bndbox")
			self.rects.append([int(it.text) for it in bndbox])

		self.imgPath = image_path

	def saveBoundBoxImage(self, imgPath=None, savedTargetDir='bounding_box'):
		if imgPath == None:
			self.imgPath = self.findImagePath()

		if self.imgPath == None:
			return

		#annotation_file_dir = os.path.dirname(os.path.realpath(self.annotation_file))
		#outputFolder = os.path.join(annotation_file_dir, savedTargetDir)
		outputFolder = savedTargetDir
		if not os.path.exists(outputFolder):
			os.mkdir(outputFolder)

		# Get crop images
		bbs = []
		im = Image.open(self.imgPath)
		for box in self.rects:
			bbs.append(im.crop(box))
	    # Save them to target dir
		count = 0
		for box in bbs:
			count = count + 1
			outPath = str(os.path.join(outputFolder, self.annotation_filename + '_box'+ str(count) + '.JPEG'))
			box.save(outPath)
			print 'save to ' + outPath

	def get_BoudingBoxs(self):
		return self.rects

	def findImagePath(self, search_folder='.'):
		filename = self.annotation_filename + str('.JPEG')
		for root, dirs, files in os.walk(search_folder):
			for file in files:
				if filename == file:
					return os.path.join(root, file)
		print filename + ' not found'
		return None

import argparse
if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Help the user to download, crop, and handle images from ImageNet')
    p.add_argument('--bpath', help='Boudingbox xml path')
    args = p.parse_args()
    # Give bounding_box xml and show its JPEG path and bouding rects
    boudingbox_xml_path = args.bpath
    if not boudingbox_xml_path is None:
        bbhelper = BBoxHelper(boudingbox_xml_path)
        print bbhelper.findImagePath()
        print bbhelper.get_BoudingBoxs()
