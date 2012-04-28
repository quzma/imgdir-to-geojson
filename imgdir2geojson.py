from pexif import JpegFile
from pprint import pprint
import os
import sys
import argparse
import json

parser = argparse.ArgumentParser(description='Convert image directory into geojson.')
parser.add_argument('dirpath', metavar='D',
                   help='Path to image directory')
args = parser.parse_args()
dirpath = args.dirpath

print "-------------------------------"
print "This script will now create geojson file from images that have gps tags"
print "Locating directory ..."

if os.path.exists(dirpath) == 0:
	print >> sys.stderr, "Can't find folder:", dirpath, ", exiting."
	exit()

print "Directory found, processing images ..."
if dirpath[-1] != '/':
	dirpath += '/'

outfile = open(dirpath.split('/')[-2] + '.json', 'wb')

def get_image_coordinates(path):
	try:
		ef = JpegFile.fromFile(path)
		return ef.get_geo()
	except IOError:
		type, value, traceback = sys.exc_info()
		print "Skipping", path, "- reason: error opening file"
		return
	except JpegFile.NoSection:
		type, value, traceback = sys.exc_info()
		print "Skipping", path, "- reason: no GPS info"

		return
	except JpegFile.InvalidFile:
		type, value, traceback = sys.exc_info()
		print "Skipping", path, "- reason: error opening file"
		return

def process_image(file_name):
	
	lonlat = get_image_coordinates(dirpath+file_name)
	if lonlat == None:
		return

	nice_coords = '[' 
	nice_coords += "{0:.16f}".format(lonlat[0])
	nice_coords += ', ' 
	nice_coords += "{0:.16f}".format(lonlat[1])
	nice_coords += ']'
	
	geometry =	{'type'			: 'Point',
				 'coordinates'	: lonlat}
	properties = {'full_path' : dirpath+file_name,
				  'file_name' : file_name}

	return	{'type'			: 'Feature',
			 'geometry'		: geometry,
			 'properties'	: properties}


files = os.listdir(args.dirpath)
features = []

print "-------------------------------"
i = 1
for file in files:
	log = "(" + str(i) + "/" + str(len(files)) + ") "
	i += 1
	sys.stdout.write(log)

	feature = process_image(file)
	if feature:
		print "Inserting " + file
		features.append(feature)

geojson = json.dumps({'type':'FeatureCollection', 'features':features})
print>>outfile, geojson

print "-------------------------------"
print "Done! Inserted " + str(len(features)) + " images." + " Result written to: " + dirpath.split('/')[-2] + '.json'

