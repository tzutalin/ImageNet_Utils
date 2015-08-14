import os
import shutil

def findWnidsInAnnotationFolder(annotationPath, imagePath):
    ids = getMatchedIds(annotationPath, imagePath)

    return list(set([x.split('_')[0] for x in ids]))

def copyAnnotations(annotationFiles, dstPath):
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)

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
    dirname = os.path.dirname(outputFileName)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    ids = sorted(getMatchedIds(annotationPath, imagePath))

    with open(outputFileName, 'w') as out:
        # Enumerate from 1 for matlab scripts
        for i, f in enumerate(ids, start=1):
            line = f + ' ' + str(i) + '\n'
            out.write(line)

