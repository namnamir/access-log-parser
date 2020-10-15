from datetime import datetime
from config import config


# draw charts
class DrawChart:
    def __init__(self, color, tick, chart_flag, no_row, no_col):
        self.tick = tick
        self.no_row = no_row
        self.chart_flag = True if chart_flag in config['translation']['boolean_true'] else False
        # format [style, fg_color, bg_color]
        self.color = color
        
        # define the terminal colors
        fg_color = {'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'purple': 35, 'cyan': 36, 'white': 37}

        # set the color based on the user selection
        if (0 <= color[0] <= 7) and (color[1] in fg_color) and (color[2] in fg_color):
            self.color = '\033[{0};{1};{2}m'.format(color[0], fg_color[color[1]], fg_color[color[2]]+10)
        else:
            self.color = '\033[0;33;40m'
    

    # draw bar chart horizontally
    def bar(self, data, element):
        first_line = config['translation'][element]

        # get the maximum length of keys
        max_key_len = max(map(len, list(data.keys())))
        max_digit_len = max(len(str(max(list(data.values())))), len(first_line[2]))
        max_bar_len = self.no_row - (max_key_len + (2 if max_digit_len < 3 else max_digit_len) + max(7, len(first_line[3])) + 9)
        i = 1

        # print the first line; assemble each element
        # ignore chart drawing if it is asked
        print(first_line[0] + ' ' +
              (max(len(str(len(data))), len(first_line[0])) - len(first_line[0]) + 1) * ' ', end=''
        )
        print(first_line[1] + ' ' +
              (max(max_key_len, len(first_line[1])) - len(first_line[1]) + 1) * ' ', end=''
        )
        print(first_line[2] + ' ' +
              (2 if max_digit_len < 3 else max_digit_len - len(first_line[2]) + 1) * ' ', end=''
        )
        print(first_line[3] + ' ' +
              (max(7, len(first_line[3])) - len(first_line[3]) + 1) * ' ', end=''
        )
        print(first_line[4]) if self.chart_flag else print('')

        # print the second line; assemble each element
        # ignore chart drawing if it is asked
        print(max(len(str(len(data))), len(first_line[0])) * '-' + '  ', end='')
        print(max(max_key_len, len(first_line[1])) * '-' + '  ', end='')
        print(max(max_digit_len, len(first_line[2])) * '-' + '  ', end='')
        print(max(7, len(first_line[3])) * '-' + '  ', end='')
        print(len(first_line[4]) * '-') if self.chart_flag else print('')

        # print the bar chart
        for key, value in data.items():
            # get the max spaces and the bar size
            sum_values = sum(data.values())
            bar_size = round(int(value) * max_bar_len / sum_values)
            space_size_key = max_key_len - len(key) + 1
            space_size_digit = 4 if max_digit_len < 3 else max_digit_len - len(str(value)) + 1
            max_pct = round(int(value) * 100 / sum_values, 2)
            space_size_pct = max(7, len(str(max_pct))) - len(str(max_pct)) + 1

            print(str(i) + ' ' +
                  (max(len(str(len(data))), len(str(i))) - len(str(i)) + 1) * ' ', end=''
            )
            print(key + ' ' + space_size_key * ' ', end='')
            print(str(value) + space_size_digit * ' ' + ' ', end='')
            print('{0}%'.format(max_pct) + int(space_size_pct) * ' ', end='')
            print(self.color + bar_size * self.tick + ' \033[0;0;0m') if self.chart_flag else print('')
            
            i += 1


    # draw bar charts per month
    def bar_by_month(self, data, element):
        # iterate over months
        for key, value in data.items():
            # change the format of the date to the defined one in the config file
            new_key = datetime.strptime(key, '%Y %m').strftime(config['dateFormat']['bar_chart'])

            # print the title of the chart
            # print('\n\033[0;30;41m' + key + (self.no_row - (len(key) + 1)) * ' ' + ' \033[0;0;0m')
            print('\033[0;30;41m {0} (Unique: {1} | All: {2}) \033[0;0;0m'.format(new_key, len(data[key]), sum(value.values())))

            # draw charts
            self.bar(value, element)


    # draw bar chart of unique and total visitors
    def bar_visitor(self, data, element):
        # initiate some variables
        first_line = config['translation'][element]
        temp = {}
        total_visitor, unique_visitor = 0,0
        
        # iterate over data to remove unused ones and calculate
        # the total number of visitors regardless the month
        for key, value in data.items():
            key = datetime.strptime(key, '%Y %m').strftime(config['dateFormat']['bar_chart'])
            temp[key] = value['visitor']
            total_visitor += value['visitor']['total']
            unique_visitor += value['visitor']['unique']
        data = temp
        
        # print the first line
        print('\n\n\033[0;30;43m Statistics of "visitors" (Unique: {0} ({1}%) | All: {2}) \033[0;0;0m'.format(unique_visitor, round(unique_visitor/total_visitor, 2), total_visitor))

        max_key_len = max(map(len, list(data.keys())))

        # print the first line; assemble each element
        # ignore chart drawing if it is asked
        print(first_line[0] + ' ' +
            (max(max_key_len, len(first_line[0])) - len(first_line[0]) + 1) * ' ', end=''
        )
        print(first_line[1] + ' ' +
            (max(len(first_line[0]), len(first_line[1])) - len(first_line[1]) + 1) * ' ', end=''
        )
        print(first_line[2] + ' ' +
            (max(7, len(first_line[2])) - len(first_line[2]) + 1) * ' ', end=''
        )
        print(first_line[3] + ' ' +
            (max(len(first_line[2]), len(first_line[3])) - len(first_line[3]) + 1) * ' ', end=''
        )
        print(first_line[4] + ' ' +
            (max(7, len(first_line[4])) - len(first_line[4]) + 1) * ' '
        )

        # print the second line; assemble each element
        # ignore chart drawing if it is asked
        print(max(max_key_len, len(first_line[0])) * '-' + '  ', end='')
        print(max(10, len(first_line[1])) * '-' + '  ', end='')
        print(max(7, len(first_line[2])) * '-' + '  ', end='')
        print(max(10, len(first_line[3])) * '-' + '  ', end='')
        print(max(7, len(first_line[4])) * '-' + '  ')

        # print the bar chart
        for month, value in data.items():
            print(month + '  ' + (max_key_len - len(month)) * ' ', end='')
            print(str(value['total']) + '  ' + (max(len(str(value['total'])), len(first_line[1])) - len(str(value['total']))) * ' ', end='')
            pct = str(round(value['total'] * 100 / total_visitor, 2))
            print(pct + '% ' + (max(7, len(first_line[2])) - len(pct)) * ' ', end='')
            print(str(value['unique']) + '  ' + (max(len(str(value['unique'])), len(first_line[3])) - len(str(value['unique']))) * ' ', end='')
            pct = str(round(value['unique'] * 100 / total_visitor, 2))
            print(pct + '%  ')

            # for key, value in data[month].items():
                # get the max spaces and the bar size
                # sum_values = sum(data.values())
                # space_size_key = len(first_line[0]) - len(key) + 1
                # space_size_digit = 4 if max_digit_len1 < 3 else max_digit_len1 - len(str(value)) + 1
                # max_pct = round(int(value) * 100 / sum_values, 2)
                # space_size_pct = max(7, len(str(max_pct))) - len(str(max_pct)) + 1

                # print(month + ' ' + (max_key_len - len(month)) * ' ', end='')
                # print(str(value) + space_size_digit * ' ' + ' ', end='')
                # print('{0}%'.format(max_pct) + int(space_size_pct) * ' ', end='')
            
