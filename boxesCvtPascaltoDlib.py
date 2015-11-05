#!/usr/bin/env python
import xml.etree.ElementTree as et
import os
import argparse


def initRootOut():
    rootOut = et.Element('dataset')
    sub = et.SubElement(rootOut, 'name')
    sub.text = 'imglab dataset'
    sub = et.SubElement(rootOut, 'comment')
    sub.text = 'From Pascal VOC dataset'
    et.SubElement(rootOut, 'images')
    return rootOut


def addImg(imgs, xmlIn, imgPath):
    ele = xmlIn.find('filename')
    if ele is None:
        return False
    fileName = os.path.join(imgPath, ele.text)
    img = et.SubElement(imgs, 'image', attrib={'file': fileName})

    # add bounding boxes
    for obj in xmlIn.findall('object'):
        ele = obj.find('name')
        if ele is None:
            continue
        label = ele.text

        ele = obj.find('bndbox')
        if ele is None:
            continue

        pts = {}
        if ele.find('xmin') is None:
            continue
        left = float(ele.find('xmin').text)
        if ele.find('ymin') is None:
            continue
        top = float(ele.find('ymin').text)
        if ele.find('xmax') is None:
            continue
        right = float(ele.find('xmax').text)
        if ele.find('ymax') is None:
            continue
        down = float(ele.find('ymax').text)
        pts['left'] = str(int(round(left)))
        pts['top'] = str(int(round(top)))
        pts['width'] = str(int(round(right - left + 1)))
        pts['height'] = str(int(round(down - top + 1)))
        ele = et.SubElement(img, 'box', pts)
        ele = et.SubElement(ele, 'label')
        ele.text = label


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Convert Pascal format to Dlib format')
    p.add_argument('bboxes', help='Folder of bounding boxes files')
    p.add_argument('imgPath', help='Path of images')
    p.add_argument('--out', help='Output file', default='out.xml')
    args = p.parse_args()

    imgExt = '.jpg'
    rootOut = initRootOut()
    imgs = rootOut.find('images')

    for f in os.listdir(args.bboxes):
        if not f.endswith('.xml'):
            continue

        try:
            rootIn = et.parse(os.path.join(args.bboxes, f)).getroot()
        except:
            print('Fail to open ' + f + '!')
            continue

        addImg(imgs, rootIn, args.imgPath)

    tree = et.ElementTree(rootOut)
    tree.write(args.out)
