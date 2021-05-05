##	LogBeast 
##	Initial Release - Genesis Release
##	Version 1.0
##	Supported features:
##		-User Agent Detection: Extraction of Device Type, Operation System and Browser with its version
##		-Parsing Microsoft IIS log files
##		-Using ipinfo API: Get ISP, Country and City.
##		-Generate the output to a CSV File

from user_agents import parse
import os
import requests
import unicodedata
import ipinfo
import sys
import ipaddress

reload(sys)
sys.setdefaultencoding('utf8')
files = os.listdir('.')
access_token = 'b2ba9e0db7fe5f'
handler = ipinfo.getHandler(access_token)

for i in range(0,len(files)):
	if files[i] == 'LogBeast.py' or files[i] == 'LogBeast.csv':
		continue
	line_count = 0
	f = open(files[i],'r')
	for line in f:
		if line_count == 0 or line_count == 1 or line_count == 2 or line_count == 3:
			line_count +=1
			continue
		if line[0] == "#":
			continue
		date = line.split(' ')[0] + '-' + line.split(' ')[1]
		ip = line.split(' ')[8]
		ip = unicode(ip,"utf-8")
		if ipaddress.ip_address(ip).is_private == True:
			continue
		details = handler.getDetails(ip)
		ua_string = line.split(' ')[9]
		url = line.split(' ')[4]
		if ip == '-':
			continue
		user_agent = parse(ua_string)
		isp = details.org
		if isp == None:
			continue
		if ',' in isp:
			isp = isp.replace(",", ".")

		country = details.country_name
		if ',' in country:
			country = country.replace(',','.')
		region = details.region
		if ',' in region:
			region = region.replace(',','.')
		g = open('LogBeast.csv','a+')
		isp = unicodedata.normalize('NFKD', isp).encode('ascii', 'ignore')
		print repr(isp)
		g.write(date + ',' + ip + ',' + str(user_agent) + ',' + isp + ',' + country + ',' + region + '\n')
		g.close()	
f.close() 