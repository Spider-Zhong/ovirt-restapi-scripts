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

# Example
ADDR     = "192.168.123.176"
API_PORT = "8443"
USER     = "rhevm@ad.rhev3.com"
PASSWD   = "T0pSecreT!"

if len(sys.argv) != 3:
        print "Usage: %s new_data_center_name new_description" %(sys.argv[0])
        sys.exit(1)

print "Renaming datacenter to %s" %(sys.argv[1])
print "Renaming description to: %s" %(sys.argv[2])

xml_request ="""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<data_center>
        <name>""" + sys.argv[1] + """</name>
        <description>""" + sys.argv[2] + """</description>
</data_center>
"""

# Setting URL
URL      = "https://" + ADDR + ":" + API_PORT + "/api/datacenters/dd073ccc-f8cb-43b3-86d5-c8fb045e50ba"

request = urllib2.Request(URL)
print "Connecting to: " + URL

base64string = base64.encodestring('%s:%s' % (USER, PASSWD)).strip()
request.add_header("Authorization", "Basic %s" % base64string)
request.add_header('Content-Type', 'application/xml')
request.get_method = lambda: 'PUT'

try:
        xmldata = urllib2.urlopen(request, xml_request)
except urllib2.URLError, e:
        print "Error: cannot connect to REST API: %s" % (e)
	print "Possible errors: "
        print "\t- Try to login using the same user/pass by the Admin Portal and check the error!"
        sys.exit(2)
