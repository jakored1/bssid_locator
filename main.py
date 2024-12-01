#!/usr/bin/env python

# Based on these repos:
# https://github.com/dirk-makerhafen/apple-bssid
# https://github.com/darkosancanin/apple_bssid_locator
# https://github.com/zadewg/GS-LOC

# This script is a mess, I didn't invest any time in making it pretty or "proper coding"
# But, it works :)

import sys
import BSSIDApple_pb2
import pycurl
from io import BytesIO
import random
from contextlib import redirect_stdout
import os
import json
import re


def help():
  print("This script fetches the location of a given BSSID, and networks that are nearby the given BSSID, via Apples geo-location services")
  print("")
  print("usage: python3 ./client.py AA:BB:CC:DD:EE:FF")


def main():
  if len(sys.argv) > 1:
    if sys.argv[1] in ("-h", "--help"):
      help()
      return
    else:
      # Validating mac address
      if re.match(r'([0-9A-F]{2}[:]){5}[0-9A-F]{2}|([0-9A-F]{2}[-]){5}[0-9A-F]{2}', string=sys.argv[1], flags=re.IGNORECASE):
        bssid = sys.argv[1]
      else:
        print("Invalid BSSID\n")
        help()
        return
  else:
    print("Missing BSSID\n")
    help()
    return
    
  s1 = "%s%s%s%s%s*%scom.apple.Maps" % (chr(18), chr(19), chr(10), chr(17), bssid, chr(14))
  data = "\x00\x01\x00\x05"+"en_US"+"\x00\x00\x00\x09"+"5.1.9B176"+"\x00\x00\x00\x01\x00\x00\x00" + chr(len(s1)) + s1

  service_url = 'https://{}.apple.com/clls/wloc'
  service_shost = ['iphone-services', 'gs-loc']

  url = service_url.format(service_shost[random.choice([True, False])])

  c = pycurl.Curl()
  c.setopt(pycurl.URL, url)
  c.setopt(pycurl.USERAGENT, 'locationd/1756.1.15 CFNetwork/711.5.6 Darwin/14.0.0')
  b = BytesIO()
  c.setopt(c.WRITEFUNCTION, b.write)
  c.setopt(c.POSTFIELDS, data)
  c.perform()
  c.close()
  wifi_list = BSSIDApple_pb2.BlockBSSIDApple()
  wifi_list.ParseFromString(b.getvalue()[10:])

  tmp_file = '/tmp/wifi_list.tmp'
  with open(tmp_file, 'w') as f:
    with redirect_stdout(f):
      print(wifi_list)

  with open(tmp_file, 'r') as f:
    out = f.read().split("wifi ")

  networks = {}
  for network_info in out:
    if len(network_info) < 1:
      continue
    bssid = network_info.split(" ")[3].replace('"', "").strip().lower()
    
    location_info = network_info.split("location ")[1].split(" ")
    for i in range(len(location_info)):
      if location_info[i] == "latitude:":
        latitude = location_info[i+1].strip()[:2] + "." + location_info[i+1].strip()[2:]
      if location_info[i] == "longitude:":
        longitude = location_info[i+1].strip()[:2] + "." + location_info[i+1].strip()[2:]
      if location_info[i] == "valeur_inconnue3:":
        unknown_value3 = location_info[i+1].strip()
      if location_info[i] == "valeur_inconnue4:":
        unknown_value4 = location_info[i+1].strip()
      if location_info[i] == "valeur_inconnue5:":
        unknown_value5 = location_info[i+1].strip()
      if location_info[i] == "valeur_inconnue6:":
        unknown_value6 = location_info[i+1].strip()
      if location_info[i] == "valeur_inconnue11:":
        unknown_value11 = location_info[i+1].strip()
      if location_info[i] == "valeur_inconnue12:":
        unknown_value12 = location_info[i+1].strip()

    # If network was not found
    if latitude == "-1.8000000000" and longitude == "-1.8000000000":
      networks[bssid] = {
        "latitude": "unknown",
        "longitude": "unknown",
        "unknown_value3": unknown_value3,
        "unknown_value4": -1,
        "unknown_value5": unknown_value5,
        "unknown_value6": -1,
        "unknown_value11": -1,
        "unknown_value12": -1,
      }
    else:
      networks[bssid] = {
        "latitude": latitude,
        "longitude": longitude,
        "unknown_value3": unknown_value3,
        "unknown_value4": unknown_value4,
        "unknown_value5": unknown_value5,
        "unknown_value6": unknown_value6,
        "unknown_value11": unknown_value11,
        "unknown_value12": unknown_value12,
      }

  if os.path.exists(tmp_file):
    os.remove(tmp_file)

  print(json.dumps(networks, indent=4))


if __name__ == "__main__":
  main()
