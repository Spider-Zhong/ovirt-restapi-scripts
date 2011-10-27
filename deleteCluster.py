#!/usr/bin/python
#
# Copyright (C) 2011
#
# Douglas Schilling Landgraf <dougsland@redhat.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import urllib2
import base64
import sys
from xml.etree import ElementTree

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

def getClusterId(cluster_name):
 
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/clusters"

	request = urllib2.Request(URL)

	print "Preparing to remove: %s" %(cluster_name)

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)

	try:
		xmldata = urllib2.urlopen(request).read()
	except urllib2.URLError, e:
		print "Error: cannot connect to REST API: %s" % (e)
		print "\tTry to login using the same user/pass by the Admin Portal and check the error!"
		sys.exit(2)

	tree = ElementTree.XML(xmldata)
	list = tree.findall("cluster")

	cluster_id = None
	for item in list:
		if cluster_name == item.find("name").text:
			cluster_id = item.attrib["id"]
			print "cluster id %s" % (cluster_id)
			break

	return cluster_id


def removeCluster(cluster_id):

	# Setting URL
	URL      = "https://" + ADDR + ":" + API_PORT + "/api/clusters/" + str(cluster_id)

	request = urllib2.Request(URL)
	print "connecting to: " + URL

	base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
	request.add_header("Authorization", "Basic %s" % base64string)

	request.get_method = lambda: 'DELETE'

	try:
        	xmldata = urllib2.urlopen(request).read()
	except urllib2.URLError, e:
        	print "Error: cannot connect to REST API: %s" % (e)
		print "Possible errors: "
	        print "\t- Are you trying to remove an non existing item?"
	        print "\t- Try to login using the same user/pass by the Admin Portal and check the error!"
        	sys.exit(2)

	return 0

if __name__ == "__main__":

	if len(sys.argv) != 2:
		print "Usage: %s my_cluster" %(sys.argv[0])
		sys.exit(1)

	id_ret = getClusterId(sys.argv[1])

	if id_ret == None:
		print "Cannot find Cluster"
		sys.exit(1)

	ret = removeCluster(id_ret)
	if ret == 0:
		print "Cluster removed"

