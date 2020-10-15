from config import config


# counting calls
class Count:
    def __init__(self, data, exceptions):
        self.data = data
        self.exceptions = exceptions
    
    # count total number of occurrences 
    def total(self):
        # initiate variables
        output = {}

        # iterate over log file
        for item in self.data:
            # iterate over each line of the log file formated in a dictionary
            for key, value in item.items():
                # skip the exempted keys
                if key in self.exceptions:
                    continue

                # change the empty (NULL) items to 'none'
                if not value:
                    value = config['translation']['unknown']
                
                # add the key to the dictionary
                if not key in output:
                    output[key] = {}

                # count others
                if value in output[key]:
                    output[key][value] += 1
                else:
                    output[key][value] = 1
        return output

    # count total number of occurrences in each month
    def by_month(self):
        # initiate variables
        output = {}

        # iterate over log file
        for item in self.data:
            # iterate over each line of the log file formated in a dictionary
            for key, value in item.items():
                # skip the exempted keys
                # 'time_custom' is related to months
                if (key in self.exceptions) or (key == 'time_custom'):
                    continue

                # change the empty (NULL) items to 'none'
                if not value:
                    value = config['translation']['unknown']

                # add the time_custom name to the dictionary
                if not item['time_custom'] in output:
                    output[item['time_custom']] = {}

                # add the key to the dictionary
                if not key in output[item['time_custom']]:
                    output[item['time_custom']][key] = {}
                
                # count others
                if value in output[item['time_custom']][key]:
                    output[item['time_custom']][key][value] += 1
                else:
                    output[item['time_custom']][key][value] = 1
        
            # calculate total and unique number of visitors based on 'host_ip'
            output[item['time_custom']]['visitor'] = {}
            output[item['time_custom']]['visitor']['total'] = sum(output[item['time_custom']]['host_ip'].values())
            output[item['time_custom']]['visitor']['unique'] = len(output[item['time_custom']]['host_ip'])
        
        return output
    
    # sort dictionary ascendingly/descendingly
    def sort(self, data, sort_type, sort_value, max_no_data):
        # define if it needs to sort by keys or values
        sort_value = 0 if sort_value.lower() == 'key' else 1

        # sort data
        if sort_type.lower() in ['asc', 'ascending', 'ascendingly']:
            data = {key: value for key, value in sorted(data.items(), key=lambda item: item[sort_value], reverse=False)}
        elif sort_type.lower() in ['des', 'descending', 'descendingly']:
            data = {key: value for key, value in sorted(data.items(), key=lambda item: item[sort_value], reverse=True)}

        # return the requested number of sorted data, e.g. least 10, or top 10
        return dict(list(data.items())[:max_no_data])
