import sys
import os
import time
import tarfile

if sys.version_info >= (3,):
    import urllib.request as urllib2
    import urllib.parse as urlparse
else:
    import urllib2
    import urlparse
    import urllib

class ImageNetDownloader:
    def __init__(self):
        self.host = 'http://www.image-net.org'

    def download_file(self, url, desc=None, renamed_file=None):
        u = urllib2.urlopen(url)

        scheme, netloc, path, query, fragment = urlparse.urlsplit(url)
        filename = os.path.basename(path)
        if not filename:
            filename = 'downloaded.file'

        if not renamed_file is None:
            filename = renamed_file

        if desc:
            filename = os.path.join(desc, filename)

        with open(filename, 'wb') as f:
            meta = u.info()
            meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
            meta_length = meta_func("Content-Length")
            file_size = None
            if meta_length:
                file_size = int(meta_length[0])
            print("Downloading: {0} Bytes: {1}".format(url, file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)

                status = "{0:16}".format(file_size_dl)
                if file_size:
                    status += "   [{0:6.2f}%]".format(file_size_dl * 100 / file_size)
                status += chr(13)

        return filename

    def extractTarfile(self, filename):
        tar = tarfile.open(filename)
        tar.extractall()
        tar.close()

    def downloadBBox(self, wnid):
        filename = str(wnid) + '.tar.gz'
        url = self.host + '/downloads/bbox/bbox/' + filename
        try:
            filename = self.download_file(url, self.mkWnidDir(wnid))
            currentDir = os.getcwd()
            os.chdir(wnid)
            self.extractTarfile(filename)
            print 'Download bbbox annotation from ' + url + ' to ' + filename
            os.chdir(currentDir)
        except Exception, error:
            print 'Fail to download' + url

    def getImageURLsOfWnid(self, wnid):
        url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=' + str(wnid)
        f = urllib.urlopen(url)
        contents = f.read().split('\n')
        imageUrls = []

        for each_line in contents:
            # Remove unnecessary char
            each_line = each_line.replace('\r', '').strip()
            if each_line:
                imageUrls.append(each_line)

        return imageUrls

    def mkWnidDir(self, wnid):
        if not os.path.exists(wnid):
            os.mkdir(wnid)
        return os.path.abspath(wnid)

    def downloadImagesByURLs(self, wnid, imageUrls):
        # save to the dir e.g: n005555_urlimages/
        wnid_urlimages_dir = os.path.join(self.mkWnidDir(wnid), str(wnid) + '_urlimages')
        if not os.path.exists(wnid_urlimages_dir):
            os.mkdir(wnid_urlimages_dir)

        for url in imageUrls:
            try:
                self.download_file(url, wnid_urlimages_dir)
            except Exception, error:
                print 'Fail to download : ' + url
                print str(error)

    def downloadOriginalImages(self, wnid, username, accesskey):
        download_url = 'http://www.image-net.org/download/synset?wnid=%s&username=%s&accesskey=%s&release=latest&src=stanford' % (wnid, username, accesskey)
        try:
             download_file = self.download_file(download_url, self.mkWnidDir(wnid), wnid + '_original_images.tar')
        except Exception, erro:
            print 'Fail to download : ' + download_url

        currentDir = os.getcwd()
        extracted_folder = os.path.join(wnid, wnid + '_original_images')
        if not os.path.exists(extracted_folder):
            os.mkdir(extracted_folder)
        os.chdir(extracted_folder)
        self.extractTarfile(download_file)
        os.chdir(currentDir)
        print 'Extract images to ' + extracted_folder

