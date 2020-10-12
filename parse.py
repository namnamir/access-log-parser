
import re
import sys
import argparse
import json
import urllib.request
from user_agents import parse
from datetime import datetime
from config import config


# parse the log file
def data_parser(args, max_line, exceptions):
    # Regex for the common Apache log format
    elements = [
        r'(?P<host_ip>\S+)',      # %h -> host
        r'(?P<identity>\S+)',  # %l -> identity
        r'(?P<user>\S+)',      # %u -> user
        r'\[(?P<time>.+)\]',   # %t -> time
        r'"(?P<request>.*)"',  # \"%r\" -> HTTP request
        r'(?P<status>[0-9]+)', # %>s -> HTTP status
        r'(?P<size>\S+)',      # %b -> size in byte
        r'"(?P<referrer>.*)"', # \"%{Referer}i\" -> referral page
        r'"(?P<user_agent>.*)"',    # \"%{User-agent}i\" -> user agent
        r'"(?P<other>\S+)"',   # %l -> identity
    ]
    pattern = re.compile(r'\s+'.join(elements)+r'\s*\Z')

    # initiate variables
    items = []
    i = 1 # to count the number of lines
    j = 0 # to count the number of parsed lines
    api_flag = True # to stop unnecessary AIP requests

    # open the log file
    with open(args.file) as file:
        # iterate over the lines of the log file
        for line in file:
            # parse just number of lines mentioned by the user
            # if it is not mentioned, parse all lines
            if (max_line == -1) or (i < max_line):
                try:
                    # get the item based on the defined pattern
                    item = pattern.match(line).groupdict()

                    # remove exceptions
                    for element in exceptions:
                        item.pop(element)

                    # remove '-' from the unset items
                    # make hyphen (-) as NULL
                    for k,v in item.items():
                        if v == '-' or v == '"-"':
                            item[k] = ''
                        
                    # parse requests and categorize them into different HTTP methods
                    r = item['request'].split(' ')
                    item.pop('request')
                    item['request_' + r[0]] = r[1]

                    # resolve host IPs to country, city, province, and ISP if it is requested
                    if config['resolve_ip']['status'] and api_flag:
                        try:
                            # get the api result
                            with urllib.request.urlopen(config['resolve_ip']['api'].replace('__IP__',item['host_ip'])) as api:
                                # load json
                                h = json.loads(api.read().decode())
                                item['host_country'] = h[config['resolve_ip']['json_key_country']]
                                item['host_province'] = h[config['resolve_ip']['json_key_province']]
                                item['host_city'] = h[config['resolve_ip']['json_key_city']]
                                item['host_isp'] = h[config['resolve_ip']['json_key_isp']]
                        # if there is any error, do not send more API requests
                        except Exception as e:
                            print("There is an error in API request: {0}".format(e))
                            api_flag = False

                    # parse user agents
                    ua = str(parse(item['user_agent'])).split(' / ')
                    item.pop('user_agent')
                    item['user_agent_device'] = ua[0]
                    item['user_agent_os'] = ua[1]
                    item['user_agent_browser'] = ua[2]

                    # add month to the item
                    item['time_custom'] = datetime.strptime(item['time'], '%d/%b/%Y:%H:%M:%S %z').strftime('%Y %m')

                    # add the assembled log (in a dictionary format) to an array
                    items.append(item)

                    # count the number of parsed lines
                    j += 1
                except Exception as e:
                    print("line {0} from the '{1}' file can't be parsed. Error message: {2}".format(i, args.file, e))
                    i += 1
                    continue
            else:
                break
            
            i += 1
    
    print("{0} (out of {1}) lines are parsed from the file '{2}'.".format(j, max_line, args.file))
    return items
