check_softlayer_bandwidth
=========================

This is an Icinga/Nagios compliant script that checks for bandwidth overages for a virtual rack at SoftLayer.
It has been updated to work with SoftLayer API 3.x+

```
Usage: check_softlayer_bandwidth.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -u User, --api_username=User
                        SoftLayer Username
  -a API Key, --api_key=API Key
                        api_username's SoftLayer API Key
  -r Rack ID, --rack_id=Rack ID
                        Virtual Rack ID
  -p, --use-projections
                        Warns if projected > allocated
```

Icinga / Nagios Configuration Examples

Add something like this to wherever you keep your commands, such as commands.cfg

```
define command {
       command_name    check_softlayer_bandwidth
       command_line    /usr/lib/nagios/plugins/contrib/check_softlayer_bandwidth.py $ARG1$
}
```

Add this to your services. I added this to a softlayer.cfg file
```
define service {
       check_command                  check_softlayer_bandwidth!-u user -a apikey -r rackid -p
       host_name                      localhost
       service_description            YouVersion Virtual Rack SoftLayer Bandwidth Overage
       use                            generic-service
}
```
