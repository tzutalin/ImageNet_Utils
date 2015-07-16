import argparse
import sys
import os
import Image

def isImageValid(imagePath):
    im = Image.open(imagePath)
    width, height = im.size
    minSize = 100
    if width <= minSize or height <= minSize:
        print 'error:' + imagePath
        return False
    return True

def scanAllImages(folderPath):
    extensions = {'.jpeg','.jpg', '.png', '.JPEG', 'JPG', 'png'}
    images = []
    for root, dirs, files in os.walk(folderPath):
        for file in files:
            if file.endswith(tuple(extensions)):
                relatviePath = os.path.join(root, file)
                if isImageValid(relatviePath) == True:
                    images.append(os.path.abspath(relatviePath))
    return images

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Create a label to train.txt or test.txt')
    p.add_argument('--dir', '-d', help='Image label that will be saved to train.txt or test.txt')
    p.add_argument('--label', '-l', type=int, help='Image label that will be saved to train.txt or test.txt')
    p.add_argument('--size_of_train', type=int, default=1000, help='put how many image to train.txt')
    p.add_argument('--size_of_test', type=int, default=1000, help='put how many image to text.txt')
    p.add_argument('--verbose', '-v', action='store_true', help='Enable verbose log')
    args = p.parse_args()
    if args.label is None or args.dir is None:
        print 'No label or dir'
        sys.exit()

    label = str(args.label)
    folderPath = str(args.dir)
    size_of_train = args.size_of_train
    size_of_test = args.size_of_test
    # scan all images's abspath
    images = scanAllImages(folderPath)
    countOfTrainImg = 0
    countOfTestImg = 0
    train_file = open('train.txt', 'a')
    test_file = open('test.txt', 'a')
    for imagePath in images:
        if countOfTrainImg < size_of_train:
            train_file.write(imagePath + ' ' + label + '\n')
            countOfTrainImg += 1
        elif countOfTestImg < size_of_test:
            test_file.write(imagePath + ' ' + label + '\n')
            countOfTestImg += 1

    train_file.close()
    test_file.close()
