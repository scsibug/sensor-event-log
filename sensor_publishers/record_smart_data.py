#!/usr/bin/python
# Read smart data from a disk, and publish data to server
import sys, os, re, time, argparse
import hmac, hashlib
import json, decimal
import urllib2

from subprocess import check_output

# Before running, create monitors for each of the following:
###disk.SERIAL_NUMBER.read_errors  (count)
###disk.SERIAL_NUMBER.reallocated_sectors  (count)
###disk.SERIAL_NUMBER.start_stops (count)
###disk.SERIAL_NUMBER.spin_retries (count)
###disk.SERIAL_NUMBER.runtime_bad_blocks (count)

#disk.SERIAL_NUMBER.high_fly_writes (count)
#disk.SERIAL_NUMBER.airflow_temperature (celsius)
#disk.SERIAL_NUMBER.load_unload_cycles (count)
#disk.SERIAL_NUMBER.internal_temperature (celsius)
#disk.SERIAL_NUMBER.total_lba_writes (count)
#disk.SERIAL_NUMBER.total_lba_reads (count)
#disk.SERIAL_NUMBER.power_on_time  (hours)
#disk.SERIAL_NUMBER.power_cycles  (count)
#disk.SERIAL_NUMBER.wear_leveling (count)
#disk.SERIAL_NUMBER.used_reserve_blocks (count)
#disk.SERIAL_NUMBER.program_failures (count)
#disk.SERIAL_NUMBER.erase_failures (count)
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

def simple_parse_and_send(smart_output, smart_attr_name, sensor_suffix):
    try:
        m = re.search(smart_attr_name+r".*\s(\d+)(\s*\(.*\)\s*)?$", smart_output, re.MULTILINE)
        r = m.group(1).strip()
        print sensor_suffix+": "+r
        send_reading(monitor_prefix+sensor_suffix, r)
    except:
        print "failed to record "+sensor_suffix

# Run smartctl, with provided disk
try:
    smartctl_out = check_output(["smartctl", "-a", args.disk])
except Exception e:
    smartctl_out = str(e.output)
# if the return code is not 0, we'll exit with an exception.

# Find the serial number of the device
sn_matches = re.search(r"Serial Number:(.*)$", smartctl_out, re.MULTILINE)
serial_number = sn_matches.group(1).strip()

# TODO: check for valid serial number
monitor_prefix = "disk." + serial_number + "."
print "using monitor prefix: "+monitor_prefix

simple_parse_and_send(smartctl_out, "1 Raw_Read_Error_Rate", "read_errors")
simple_parse_and_send(smartctl_out, "4 Start_Stop_Count", "start_stops")
simple_parse_and_send(smartctl_out, "5 Reallocated_Sector_Ct", "reallocated_sectors")
simple_parse_and_send(smartctl_out, "9 Power_On_Hours", "power_on_time")
simple_parse_and_send(smartctl_out, "10 Spin_Retry_Count", "spin_retries")
simple_parse_and_send(smartctl_out, "12 Power_Cycle_Count", "power_cycles")
simple_parse_and_send(smartctl_out, "177 Wear_Leveling_Count", "wear_leveling")
simple_parse_and_send(smartctl_out, "179 Used_Rsvd_Blk_Cnt_Tot", "used_reserve_blocks")
simple_parse_and_send(smartctl_out, "181 Program_Fail_Cnt_Total", "program_failures")
simple_parse_and_send(smartctl_out, "182 Erase_Fail_Count_Total", "erase_failures")
simple_parse_and_send(smartctl_out, "183 Runtime_Bad_Block", "runtime_bad_blocks")
simple_parse_and_send(smartctl_out, "189 High_Fly_Writes", "high_fly_writes")
simple_parse_and_send(smartctl_out, "190 Airflow_Temperature_Cel", "airflow_temperature")
simple_parse_and_send(smartctl_out, "193 Load_Cycle_Count", "load_unload_cycles")
simple_parse_and_send(smartctl_out, "194 Temperature_Celsius", "internal_temperature")
simple_parse_and_send(smartctl_out, "199 UDMA_CRC_Error_Count", "crc_errors")
simple_parse_and_send(smartctl_out, "241 Total_LBAs_Written", "total_lba_writes")
simple_parse_and_send(smartctl_out, "242 Total_LBAs_Read", "total_lba_reads")



