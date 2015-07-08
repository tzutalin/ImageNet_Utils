import sys
import bbox_helper
import imagedownloader

if __name__ == '__main__':
    downloader = imagedownloader.ImageNetDownloader()
    wnid = 'n02699494'
    list = downloader.getImageURLsOfWnid(wnid)
    downloader.downloadImagesByURLs(wnid, list)

    # Download andnotation files
    downloader.downloadBBox(wnid)
    # Get the list of image URLs of Wnid
    allAnnotationFiles = bbox_helper.scanAnnotationFolder(wnid)
    # Download original image, but need to set key and username
    username = None
    accessKey = None
    if username is None or accessKey is None:
        print 'need username and accessKey to download original images'
    else:
        downloader.downloadOriginalImages(wnid, username, accessKey)

    for andnotation_xml in allAnnotationFiles:
        bboxhelper = bbox_helper.BBoxHelper(andnotation_xml)
        # Get box list
        boxs = bboxhelper.get_BoudingBoxs()
        print boxs
        #bboxhelper.saveBoundBoxImage(savedTargetDir = str(wnid) + 'boudingboxImages')
