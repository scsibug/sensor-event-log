#!/usr/bin/python
# Read smart data from a disk, and publish data to server
import sys, os, re, time, argparse
import hmac, hashlib
import json, decimal
import urllib2

from subprocess import check_output

# Before running, create monitors for each of the following:
#disk.SERIAL_NUMBER.read_errors  (count)
#disk.SERIAL_NUMBER.reallocated_sectors  (count)
#disk.SERIAL_NUMBER.power_on_time  (hours)
#disk.SERIAL_NUMBER.power_cycles  (count)
#disk.SERIAL_NUMBER.temperature  (celsius)
#disk.SERIAL_NUMBER.crc_errors  (count)

print "using "+os.environ['EVENT_SECRET_KEY']
parser = argparse.ArgumentParser(description='Write sensor value to remote server.')
parser.add_argument('--host', help='remote host to send updates to')
parser.add_argument('disk', help='disk to read SMART data from')

args = parser.parse_args()

def send_reading(monitor, value):
    data = json.dumps({"type": "float", "value": value, "monitor": monitor, "time": time.time()})
    authz = "HMAC "+hmac.new(os.environ['EVENT_SECRET_KEY'],data,hashlib.sha256).hexdigest()
    req = urllib2.Request(args.host, data, {'Content-Type': 'application/json', 'Authorization': authz})
    f = urllib2.urlopen(req)
    response = f.read()
    print response
    f.close()

# Run smartctl, with provided disk
smartctl_out = check_output(["smartctl", "-a", args.disk])
# if the return code is not 0, we'll exit with an exception.

# Find the serial number of the device
sn_matches = re.search(r"Serial Number:(.*)$", smartctl_out, re.MULTILINE)
serial_number = sn_matches.group(1).strip()
# TODO: check for valid serial number
monitor_prefix = "disk." + serial_number + "."
print "using monitor prefix: "+monitor_prefix
# Raw_Read_Error_Rate
read_error_matches = re.search(r"Raw_Read_Error_Rate.*\s(\d+)$", smartctl_out, re.MULTILINE)
read_error_count = read_error_matches.group(1).strip()
print "read error count: "+read_error_count
send_reading(monitor_prefix+"read_errors", read_error_count)
# Reallocated_Sector_Ct
realloc_sector_matches = re.search(r"Reallocated_Sector_Ct.*\s(\d+)$", smartctl_out, re.MULTILINE)
realloc_sector_count = realloc_sector_matches.group(1).strip()
print "reallocated sector count: "+realloc_sector_count
send_reading(monitor_prefix+"reallocated_sectors", realloc_sector_count)
# Power_On_Hours
poh_matches = re.search(r"Power_On_Hours.*\s(\d+)\s*$", smartctl_out, re.MULTILINE)
power_on_hours = poh_matches.group(1).strip()
print "power on hours: "+power_on_hours
send_reading(monitor_prefix+"power_on_time", power_on_hours)
# Power_Cycle_Count
power_cycle_count_matches = re.search(r"Power_Cycle_Count.*\s(\d+)$", smartctl_out, re.MULTILINE)
power_cycle_count = power_cycle_count_matches.group(1).strip()
print "power cycle count: "+power_cycle_count
send_reading(monitor_prefix+"power_cycles", power_cycle_count)
# Temperature_Celsius
temp_matches = re.search(r"Temperature_Celsius.*\s(\d+)\s*\(.*\)\s*$", smartctl_out, re.MULTILINE)
temp_celsius = temp_matches.group(1).strip()
print "temperature: "+temp_celsius
send_reading(monitor_prefix+"temperature", temp_celsius)
# UDMA_CRC_Error_Count
crc_error_count_matches = re.search(r"UDMA_CRC_Error_Count.*\s(\d+)$", smartctl_out, re.MULTILINE)
crc_error_count = crc_error_count_matches.group(1).strip()
print "CRC error count: "+crc_error_count
send_reading(monitor_prefix+"crc_errors", crc_error_count)
