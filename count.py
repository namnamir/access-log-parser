
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
            for k,v in item.items():
                # skip the exempted keys
                if k in self.exceptions:
                    continue

                # change the empty (NULL) items to 'none'
                if not v:
                    v = '_UNKNOWN_'
                
                # add the key to the dictionary
                if not k in output:
                    output[k] = {}

                # count others
                if v in output[k]:
                    output[k][v] += 1
                else:
                    output[k][v] = 1
        return output

    # count total number of occurrences in each month
    def by_month(self):
        # initiate variables
        output = {}

        # iterate over log file
        for item in self.data:
            # iterate over each line of the log file formated in a dictionary
            for k,v in item.items():
                # skip the exempted keys
                if (k in self.exceptions) or (k == 'time_custom'):
                    continue

                # add the time_custom name to the dictionary
                if not item['time_custom'] in output:
                    output[item['time_custom']] = {}

                # add the key to the dictionary
                if not k in output[item['time_custom']]:
                    output[item['time_custom']][k] = {}
                
                # count others
                if v in output[item['time_custom']][k]:
                    output[item['time_custom']][k][v] += 1
                else:
                    output[item['time_custom']][k][v] = 1
        return output
    
    # sort dictionary ascendingly/descendingly
    def sort(self, data, sort_type, sort_value, max_no_data):
        # define if it needs to sort by keys or values
        sort_value = 0 if sort_value.lower() == 'key' else 1

        # sort data
        if sort_type.lower() in ['asc', 'ascending', 'ascendingly']:
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[sort_value], reverse=False)}
        elif sort_type.lower() in ['des', 'descending', 'descendingly']:
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[sort_value], reverse=True)}

        # return the requested number of sorted data, e.g. least 10, or top 10
        return dict(list(data.items())[:max_no_data])
