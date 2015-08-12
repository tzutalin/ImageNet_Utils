import argparse
import sys
import os
import bbox_helper
import imagedownloader
import pref_utils

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Help the user to download, crop, and handle images from ImageNet')
    p.add_argument('--wnid', help='ImageNet Wnid. E.g. : n02710324')
    p.add_argument('--downloadImages', help='Should download images', action='store_true', default=False)
    p.add_argument('--downloadOriginalImages', help='Should download original images', action='store_true', default=False)
    p.add_argument('--downloadBoundingBox', help='Should download bouding box annotation files', action='store_true', default=False)
    #p.add_argument('--jobs', '-j', type=int, default=1, help='Number of parallel threads to download')
    #p.add_argument('--timeout', '-t', type=int, default=10, help='Timeout per image in seconds')
    #p.add_argument('--retry', '-r', type=int, default=10, help='Max count of retry for each image')
    p.add_argument('--verbose', '-v', action='store_true', help='Enable verbose log')
    args = p.parse_args()
    if args.wnid is None:
        print 'No wnid'
        sys.exit()

    wnid = str(args.wnid)
    downloader = imagedownloader.ImageNetDownloader()
    allAnnotationFiles = None
    username = None
    accessKey = None
    userInfo = pref_utils.readUserInfo()
    if not userInfo is None:
        username = userInfo[0]
        accessKey = userInfo[1]

    if args.downloadImages is True:
        list = downloader.getImageURLsOfWnid(wnid)
        downloader.downloadImagesByURLs(wnid, list)

    if args.downloadBoundingBox is True:
        # Download andnotation files
        downloader.downloadBBox(wnid)
        # Get the list of image URLs of Wnid
        allAnnotationFiles = bbox_helper.scanAnnotationFolder(wnid)
        for file in allAnnotationFiles:
            print 'Download: ' + file

    if args.downloadOriginalImages is True:
    # Download original image, but need to set key and username
        if username is None or accessKey is None:
            username = raw_input('Enter your username : ')
            accessKey = raw_input('Enter your accessKey : ')
            if username and accessKey:
                pref_utils.saveUserInfo(username, accessKey)

        if username is None or accessKey is None:
            print 'need username and accessKey to download original images'
        else:
            downloader.downloadOriginalImages(wnid, username, accessKey)

        # Read annotation files and crop the original image
        if not allAnnotationFiles is None:
            for andnotation_xml in allAnnotationFiles:
                bboxhelper = bbox_helper.BBoxHelper(andnotation_xml)
                # Get box list
                boxs = bboxhelper.get_BoudingBoxs()
                print boxs
                # Save to wnid_boudingboxImages dir
                crop_images_dir = os.path.join(wnid, str(wnid) + '_boudingboxImages')
                bboxhelper.saveBoundBoxImage(savedTargetDir = crop_images_dir)
