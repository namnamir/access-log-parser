config = {
    # define the number of lines from the file that should be parsed
    # possible options: any positive digit.
    #                   minus numbers or 0 = all
    'lines_to_parse': 100,
    # list the elements should not be parsed and shown
    # list of all items:
    #       host_ip
    #     * host_country
    #     * host_city
    #     * host_province
    #     * host_isp
    #       identity
    #       user
    #     * time
    #       size
    #       referrer
    #       user_agent_device
    #       user_agent_os
    #       user_agent_browser
    #       other
    # * if time is not parsed, the monthly report can't be generated
    # $ host-related elements need API, check 'resolve_ip'
    'exception_elements': ['identity', 'other', 'size'],
    # it may need payment but in general it slows down the process
    'resolve_ip': {
        # turn on or of suing API
        # possible choices: True, False
        'status': True,
        # user __IP__ to determine where IP should be placed
        # it should be an API formats results in JSON
        'api': 'http://ip-api.com/json/__IP__',
        # define json keys
        'json_key_country': 'country',
        'json_key_city': 'city',
        'json_key_province': 'regionName', # state, province, region
        'json_key_isp': 'isp'
    },
    # date format based on the python parameters.
    # read more: https://strftime.org/
    'dateFormat' : {
        'bar_chart' : '%B %Y'
    },
    'chart': {
        'bar': {
            'tick': '▇',
            # foreground colors: red, blue, white, yellow, black, green, purple, cyan
            'fg_color': 'green',
            # background colors: red, blue, white, yellow, black, green, purple, cyan
            'bg_color': 'black',
            # Regular: 0, Bold: 1, Underline: 2, Reverse: 7
            'text_style': 0
        }
    },
    'translation': {
        'host_ip': ['#', 'IP Address', 'No. of Visitors', '%', 'Bar Chart'],
        'host_country': ['#', 'Country', 'No. of Visitors', '%', 'Bar Chart'],
        'host_city': ['#', 'City', 'No. of Visitors', '%', 'Bar Chart'],
        'host_province': ['#', 'Province', 'No. of Visitors', '%', 'Bar Chart'],
        'host_isp': ['#', 'ISP Name', 'No. of Visitors', '%', 'Bar Chart'],
        'identity': ['#', 'User Identity', 'No. of Visitors', '%', 'Bar Chart'],
        'user': ['#', 'User', 'No. of Visitors', '%', 'Bar Chart'],
        'time': ['#', 'Time', 'No. of Visitors', '%', 'Bar Chart'],
        'size': ['#', 'Request Size (B)', 'No. of Visitors', '%', 'Bar Chart'],
        'referrer': ['#', 'Referrer URL', 'No. of Visitors', '%', 'Bar Chart'],
        'user_agent_device': ['#', 'User Device', 'No. of Visitors', '%', 'Bar Chart'],
        'user_agent_os': ['#', 'User OS', 'No. of Visitors', '%', 'Bar Chart'],
        'user_agent_browser': ['#', 'User Browser', 'No. of Visitors', '%', 'Bar Chart']
    }
}
