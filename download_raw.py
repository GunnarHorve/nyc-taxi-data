#!/usr/bin/env python

import os.path
import urllib2

def download(url, dest):
	file_name = url.split('/')[-1]

	if os.path.isfile(dest + file_name):
		print "already downloaded " + file_name
		return

	u = urllib2.urlopen(url)
	f = open(dest + file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,

	f.close()



# run 36 download operations
yellow_template = 'https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2015-%s.csv'
green_template = 'https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_2015-%s.csv'
fhv_template = 'https://s3.amazonaws.com/nyc-tlc/trip+data/fhv_tripdata_2015-%s.csv'


months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
for month in months:
	download(yellow_template % month, '/mnt/disks/storage/raw/')
	download(green_template % month, '/mnt/disks/storage/raw/')
	download(fhv_template % month, '/mnt/disks/storage/raw/')
