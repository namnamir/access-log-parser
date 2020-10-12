from datetime import datetime
from config import config


# draw charts
class DrawChart:
    def __init__(self, color, tick, no_row, no_col):
        self = self
        self.tick = tick
        self.no_row = no_row
        # format [style, fg_color, bg_color]
        self.color = color
        
        fg_color = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37}

        if (0 <= color[0] <= 7) and (color[1] in fg_color) and (color[2] in fg_color):
            self.color = '\033[{0};{1};{2}m'.format(color[0], fg_color[color[1]], fg_color[color[2]]+10)
        else:
            self.color = '\033[0;33;40m'
    
    # draw bar chart horizontally
    def bar(self, data, first_line):
        # get the maximum length of keys
        max_key_len = max(map(len,list(data.keys())))
        max_digit_len = max(len(str(max(list(data.values())))), len(first_line[2]))
        max_bar_len = self.no_row - (max_key_len + (2 if max_digit_len < 3 else max_digit_len) + 8)
        i = 1

        # print the first two lines
        print(first_line[0] + ' ' +
              (max(len(str(len(data))), len(first_line[0])) - len(first_line[0]) + 1) * ' ' +
              first_line[1] + ' ' +
              (max(max_key_len, len(first_line[1])) - len(first_line[1]) + 1) * ' ' +
              first_line[2] + ' ' +
              (2 if max_digit_len < 3 else max_digit_len - len(first_line[2]) + 1) * ' ' +
              first_line[3] + ' ' +
              (max(7, len(first_line[3])) - len(first_line[3]) + 1) * ' ' +
              first_line[4]
             )
        print(max(len(str(len(data))), len(first_line[0])) * '-' +
              '  ' +
              max(max_key_len, len(first_line[1])) * '-' +
              '  ' +
              max(max_digit_len, len(first_line[2])) * '-' +
              '  ' +
              max(7, len(first_line[3])) * '-' +
              '  ' +
              len(first_line[4]) * '-'
             )

        # print the bar chart
        for key, value in data.items():
            # get the max spaces and the bar size
            sum_values = sum(data.values())
            bar_size = round(int(value) * max_bar_len / sum_values)
            space_size_key = max_key_len - len(key) + 1
            space_size_digit = 4 if max_digit_len < 3 else max_digit_len - len(str(value)) + 1
            max_perc = round(int(value) / sum_values, 2)
            space_size_perc = max(7, max_perc) - len(str(max_perc))

            print(str(i) + ' ' +
                  (max(len(str(len(data))), len(str(i))) - len(str(i)) + 1) * ' ' +
                  key + ' ' +
                  space_size_key * ' ' + 
                  str(value) +
                  space_size_digit * ' ' + ' ' +
                  '{0}%'.format(max_perc) +
                  int(space_size_perc) * ' ' + 
                  self.color + bar_size * self.tick + ' \033[0;0;0m'
                 )
            
            i += 1

    # draw bar charts per month
    def bar_by_month(self, data, first_line):
        # iterate over months
        for key, value in data.items():
            # change the format of the date to the defined one in the config file
            key = datetime.strptime(key, '%Y %m').strftime(config['dateFormat']['bar_chart'])

            # print the title of the chart
            print('\n\033[0;30;41m' +
                  key +
                  (self.no_row - (len(key) + 1)) * ' ' +
                  ' \033[0;0;0m'
                 )

            # draw charts
            self.bar(value, first_line)
