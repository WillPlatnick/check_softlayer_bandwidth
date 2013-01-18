#!/usr/bin/env python
'''
Project     :       Icinga/Nagios SoftLayer Virtual Rack Bandwidth Check
Version     :       0.1
Author      :       Will Platnick <wplatnick@gmail.com>
Summary     :       This program is an icinga/nagios plugin that queries the SoftLayer API for Virtual Rack Bandwidth Overages
Dependency  :       Linux/nagios/Python-2.6

Usage :
```````
shell> python check_softlayer_bandwidth.py
'''

# Needs SoftLayer Python API Client at https://github.com/softlayer/softlayer-api-python-client
import SoftLayer.API
import sys
from optparse import OptionParser

################# OPTIONAL VARIABLES #####################
# Feel free to use these variables if you don't want to pass username or API key every time you call the script
# Softlayer API Username
api_username = ''
# Softlayer API Key
api_key = ''

# Command Line Parsing Arguements
cmd_parser = OptionParser(version = "0.1")
cmd_parser.add_option("-u", "--api_username", type="string", action = "store", dest = "api_username", help = "SoftLayer Username", default = api_username, metavar = "User")
cmd_parser.add_option("-a", "--api_key", type="string", action = "store", dest = "api_key", help = "api_username's SoftLayer API Key", default = api_key, metavar = "API Key")
cmd_parser.add_option("-r", "--rack_id", type="string", action = "store", dest = "rack_id", help = "Virtual Rack ID", metavar = "Rack ID")
cmd_parser.add_option("-p", "--use-projections", action = "store_true", dest = "use_projections", help = "Warns if projected > allocated", default = False)
(cmd_options, cmd_args) = cmd_parser.parse_args()

# Check the Command syntax
if not (cmd_options.api_username and cmd_options.api_key and cmd_options.rack_id):
    cmd_parser.print_help()
    sys.exit(3)

client = SoftLayer.API.Client('SoftLayer_Network_Bandwidth_Version1_Allotment', cmd_options.rack_id, cmd_options.api_username, cmd_options.api_key)

allocated = int(client.getTotalBandwidthAllocated())
usage = int(float(client.getOutboundPublicBandwidthUsage()))
projected = int(client.getProjectedPublicBandwidthUsage())

if allocated > usage and ((cmd_options.use_projections == False) or (allocated > projected and cmd_options.use_projections == True)):
    print "OK: Allocated: " + str(allocated) + ", Usage: " + str(usage) + ", Projected: " + str(projected)
    exit(0)
elif allocated > usage and ((cmd_options.use_projections == False) or (allocated < projected and cmd_options.use_projections == True)):
    print "WARNING: Allocated: " + str(allocated) + ", Usage: " + str(usage) + ", Projected: " + str(projected)
    exit(1)
elif allocated < usage:
    print "CRITICAL: Allocated: " + str(allocated) + ", Usage: " + str(usage) + ", Projected: " + str(projected)
    exit(2)
else:
    print "UNKNOWN: SOMETHING'S WRONG!"
    exit(3)