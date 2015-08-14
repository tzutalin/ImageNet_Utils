import os
import shutil

def _mkdir(path, filePath=False):
    if filePath:
        dirname = os.path.dirname(path)
    else:
        dirname = path

    if not os.path.exists(dirname):
        os.makedirs(dirname)

def _findWindsInAnnotationFolder(ids):
    return list(set([x.split('_')[0] for x in ids]))

def _saveImgIdList(outputFileName, ids):
    _mkdir(outputFileName, True)

    with open(outputFileName, 'w') as out:
        # Enumerate from 1 for matlab scripts
        for i, f in enumerate(ids, start=1):
            line = f + ' ' + str(i) + '\n'
            out.write(line)

def _saveMetaData(outputFileName, imagenetStructureFile, ids):
    import xml.etree.ElementTree as et
    import scipy.io as sio
    import numpy as np

    tree = et.parse(imagenetStructureFile)
    root = tree.getroot()

    dt = [('WNID', 'S10'), ('name', 'S100'), ('description', 'S1000')]
    arr = np.zeros((len(ids),), dtype=dt)
    for i, id in enumerate(ids):
        obj = root.find(".//*[@wnid='%s']" % id)
        if obj is None:
            continue

        arr[i][dt[0][0]] = id
        arr[i][dt[1][0]] = obj.attrib['words']
        arr[i][dt[2][0]] = obj.attrib['gloss']

    _mkdir(outputFileName, True)
    sio.savemat(outputFileName, {'synsets': arr})

def findWnidsInAnnotationFolder(annotationPath, imagePath):
    return _findWindsInAnnotationFolder(
        getMatchedIds(annotationPath, imagePath))

def copyAnnotations(annotationFiles, dstPath):
    _mkdir(dstPath)

    for f in annotationFiles:
        if os.path.isfile(f):
            shutil.copy(f, dstPath)

def copyImagesByAnnFiles(annotationFiles, imagePath, dstPath):
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)

    imageNames = []
    for e in annotationFiles:
        imageNames.append(os.path.basename(os.path.splitext(e)[0]) + '.JPEG')

    for root, dirs, files in os.walk(imagePath):
        for f in files:
            if f in imageNames:
                shutil.copy(os.path.join(root,f), dstPath)
                imageNames.remove(f)

def getMatchedIds(*paths):
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

def saveImgIdList(outputFileName, annotationPath, imagePath):
    _saveImgIdList( outputFileName,
                   sorted(getMatchedIds(annotationPath, imagePath)))

def saveMetaData(outputFileName, imagenetStructureFile, annotationPath, imagePath):
    _saveMetaData(outputFileName, imagenetStructureFile,
                  findWnidsInAnnotationFolder(annotationPath, imagePath))
