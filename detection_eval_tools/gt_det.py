#!/usr/bin/env python
import sys
sys.path.insert(0, '../')
import bbox_helper
import argparse
import os
import shutil
import scipy.io as sio
import numpy as np

def _mkdir(path, filePath=False):
    if filePath:
        dirname = os.path.dirname(path)
    else:
        dirname = path

    if not os.path.exists(dirname):
        os.makedirs(dirname)

def _findWnidsInAnnotationFolder(ids):
    return list(set([x.split('_')[0] for x in ids]))

def _saveImgIdList(outputFileName, ids):
    _mkdir(outputFileName, True)

    with open(outputFileName, 'w') as out:
        # Enumerate from 1 for matlab scripts
        for i, f in enumerate(ids, start=1):
            line = f + ' ' + str(i) + '\n'
            out.write(line)

def _matlabArr(count):
    dt = [('WNID', 'S10'), ('name', 'S100'), ('description', 'S1000')]
    return np.zeros(count, dtype=dt)

def _saveArr(outputFileName, arr):
    _mkdir(outputFileName, True)
    sio.savemat(outputFileName, {'synsets': arr})

def _toLabelAndName(labelNameMap):
    f = open(labelNameMap, 'rb')
    for line in f:
        label, name = line.strip().split(' ')
        yield int(label), name
    f.close()

def _findMaxLable(labelNameMap):
    maxLabel = -1
    for i, _ in _toLabelAndName(labelNameMap):
        if int(i) > maxLabel:
            maxLabel = int(i)

    if maxLabel > 0:
        return maxLabel
    else:
        return 1

def _saveMetaData(outputFileName, imagenetStructureFile, labelNameMap):
    import xml.etree.ElementTree as et

    tree = et.parse(imagenetStructureFile)
    root = tree.getroot()

    arr = _matlabArr(_findMaxLable(labelNameMap))
    for i, id in _toLabelAndName(labelNameMap):
        obj = root.find(".//*[@wnid='%s']" % id)
        if obj is None:
            continue

        i = i - 1
        arr[i]['WNID'] = id
        arr[i]['name'] = obj.attrib['words']
        arr[i]['description'] = obj.attrib['gloss']
    _saveArr(outputFileName, arr)

def _getMatchedIds(*paths):
    if len(paths) == 0:
        return []

    results = set([])
    for p in paths:
        ids = os.listdir(p)
        ids = [os.path.splitext(i)[0] for i in ids]
        if len(results) == 0:
            results = set(ids)
        else:
            results = results.intersection(ids)
            if len(results) == 0:
                break

    return list(results)

def _procPath(args):
    import pickle
    SAVED_PATH = '.pdet'
    if args is None:
        try:
            with open(SAVED_PATH, 'rb') as output:
                return pickle.load(output)
        except:
            print('Please specify paths.')
            exit()
    else:
        with open(SAVED_PATH, 'wb') as output:
            pickle.dump(args, output, pickle.HIGHEST_PROTOCOL)
        return args

def findWnidsInAnnotationFolder(annotationPath, imagePath):
    return _findWnidsInAnnotationFolder(
        _getMatchedIds(annotationPath, imagePath))

def copyAnnotations(annotationFiles, dstPath):
    _mkdir(dstPath)

    for f in annotationFiles:
        if os.path.isfile(f):
            shutil.copy(f, dstPath)

def copyImagesByAnnFiles(annotationFiles, imagePath, dstPath):
    _mkdir(dstPath)

    imageNames = []
    for e in annotationFiles:
        imageNames.append(os.path.basename(os.path.splitext(e)[0]) + '.JPEG')

    for root, dirs, files in os.walk(imagePath):
        for f in files:
            if f in imageNames:
                shutil.copy(os.path.join(root,f), dstPath)
                imageNames.remove(f)

def saveImgIdList(outputFileName, annotationPath, imagePath):
    _saveImgIdList( outputFileName,
                   sorted(_getMatchedIds(annotationPath, imagePath)))

def saveMetaData(outputFileName, imagenetStructureFile, labelNameMap):
    _saveMetaData(outputFileName, imagenetStructureFile, labelNameMap)

def saveMetaData(outputFileName, labelNameMap):
    arr = _matlabArr(_findMaxLable(labelNameMap))
    for i, c in _toLabelAndName(labelNameMap):
        i = i - 1
        arr[i]['WNID'] = c
        arr[i]['name'] = c
        arr[i]['description'] = ''
    _saveArr(outputFileName, arr)

if '__main__' == __name__:
    p = argparse.ArgumentParser(description='Help users to prepare ground truth \
                                for ILSVC detection results evaluation')
    p.add_argument('dst', type=str, help='Output folder')
    p.add_argument('-p', dest='path', nargs='+', type=str, help='Four paths \
                   should be specified: Path to search annotation files, path \
                   to search images, label to class name map, ImageNet structure \
                   file (optional). If not set, use saved paths')
    args = p.parse_args()
    paths = _procPath(args.path)

    OUT_ANN_DIR = os.path.join(args.dst, 'annotations')
    OUT_IMG_DIR = os.path.join(args.dst, 'images')
    OUT_ID_LIST = os.path.join(args.dst, 'ids.txt')
    OUT_META_DATA = os.path.join(args.dst, 'meta.mat')
    anns = bbox_helper.scanAnnotationFolder(paths[0])
    copyAnnotations(anns, OUT_ANN_DIR)
    copyImagesByAnnFiles(anns, paths[1], OUT_IMG_DIR)
    ids = _getMatchedIds(OUT_ANN_DIR, OUT_IMG_DIR)
    _saveImgIdList(OUT_ID_LIST, sorted(ids))
    if len(paths) == 3:
        saveMetaData(OUT_META_DATA, paths[2])
    elif len(paths) == 4:
        _saveMetaData(OUT_META_DATA, paths[3], paths[2])
