imgdir-to-geojson
=================

.: Image directory to Geojson :.

Author	.: ivo.kuzmanovic@gmail.com

Date	.: April 27, 2012

=================

*	This script will go through files in directory, find files that are geotagged images, insert them to a geojson 
	encoded array, and dump that array to a file.

*	File can that can be used as a source for a vector layer

*	Besides coordinates, attribute properties added are:	
		full path to file (full_path) and file name (file_name)

*	Pyexif.py is courtesy of: http://code.google.com/p/pexif/ (with slight modifications)

*	Example usage: 
		$ python imgdir2geojson.py /home/ivok/Pictures/

*	IMPORTANT: make a backup of your files before processing them. nothing should go wrong, but anyway.
=================

Have a nice day! :.