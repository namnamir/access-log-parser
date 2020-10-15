import argparse
import shutil

from config import config
from parse import data_parser
from count import Count
from draw_chart import DrawChart


def main():
    # get the size of the terminal (number of rows and columns)
    row, col = shutil.get_terminal_size()
    
    # the exception list of counting keys in the log 
    exception_list = config['exception_elements']
    
    # format [style, fg_color, bg_color]
    color = [config['chart']['bar']['text_style'],
             config['chart']['bar']['fg_color'],
             config['chart']['bar']['bg_color']
            ]

    # argument parser
    parser = argparse.ArgumentParser(description='The Apache access.log file parser')
    parser.add_argument('-f', '--file',
                        metavar='[PATH_to_FILE]',
                        required=True,
                        help='[Required] Path to the Apache log file'
                       )
    parser.add_argument('-l', '--line',
                        metavar='[No_of_LINES]',
                        type=int,
                        help='[Optional] Set the number of the lines to be parsed from the begining of the file.'
                       )
    parser.add_argument('-e', '--element',
                        metavar='[ELEMENT_NAME]',
                        required=True,
                        help='[Required] Report based on the selected element. Separate multiple elements with comma (",") and no space.'
                       )
    parser.add_argument('-c', '--chart',
                        metavar='[YES|NO]',
                        default='yes',
                        help='[Optional] Draw charts or just show the statistics.'
                       )
    parser.add_argument('-ne', '--number_element',
                        metavar='[No_of_ELEMENTS]',
                        type=int,
                        default=10,
                        help='[Optional] Show the number of top elements. Default: 10'
                       )
    parser.add_argument('-nm', '--number_month',
                        metavar='[No_of_MONTH]',
                        type=int,
                        default=3,
                        help='[Optional] Show the number of top months. Any minus number means not categorization by month. Default: 3'
                       )
    parser.add_argument('-se', '--sort_element',
                        metavar='[ASC|DES]',
                        default='des',
                        help='[Optional] Sort data ascendingly or desendingly. Default: des'
                       )
    parser.add_argument('-sm', '--sort_month',
                        metavar='[ASC|DES]',
                        default='asc',
                        help='[Optional] Sort monthly-based data (just months) ascendingly or desendingly. Default: asc'
                       )
    # # initiate variables
    args = parser.parse_args()
    print('\n{0}\n'.format(args))

    if not args.file:
        print("Please set the file path; the app won't work without it.")

    # set the maximum line of the file
    if args.line:
        max_line = args.line
    elif int(config['lines_to_parse']) > 0:
        max_line = int(config['lines_to_parse'])
    else:
        # max_line = sum(1 for line in open(args.file))
        max_line = -1

    # parse the log file
    log = data_parser(args, max_line, exception_list)

    # set a variable for the Count and DrawChart classes
    count = Count(log, exception_list)
    chart = DrawChart(color, config['chart']['bar']['tick'], args.chart, row, col)

    # iterate over elements defined by the user
    for element in args.element.split(','):
        # draw charts for the top defined number of months
        # or ignore categorizing by months
        if args.number_month > 0:
            # count log items
            counted_data = count.by_month()

            # sort counted data based on months
            sorted_data = count.sort(counted_data,
                                    args.sort_month,
                                    'key',
                                    args.number_month
                                    )

            # if it is going to give data related to visitors (total and unique)
            if element in ['visitor']:
                # # draw the chart
                chart.bar_visitor(counted_data, element)
            
            else:
                sorted_data_element = {}
                # sort inner data based on selected element
                for month in sorted_data.keys():
                    sorted_data_element[month] = count.sort(counted_data[month][element],
                                                        args.sort_element,
                                                        'value',
                                                        args.number_element
                                                        )

                # draw the chart
                print('\n\n\033[0;30;43m Statistics of "{0}" (Unique: {1} ({2}%) | All: {3}) \033[0;0;0m'.format(element,
                                                                                                                len(counted_data[month][element].keys()),
                                                                                                                round(len(counted_data[month][element].keys())*100/sum(counted_data[month][element].values()), 2),
                                                                                                                sum(counted_data[month][element].values())
                                                                                                        )
                )
                chart.bar_by_month(sorted_data_element, element)
        else:
            # shows the error if there is inconsistency
            if (args.number_month <= 0) and (element == 'hits'):
                print('Number of hits will be shown only in the monthly format. So, the value of "-mn" or "--number_month" should be higher than 0.')
                continue

            # count log items
            counted_data = count.total()

            # sort inner data based on selected element
            sorted_data = count.sort(counted_data[element],
                                    args.sort_element,
                                    'value',
                                    args.number_element
                                    )
            
            # draw the chart
            print('\n\n\033[0;30;43m Statistics of "{0}" (Unique: {1} ({2}%) | All: {3}) \033[0;0;0m'.format(element,
                                                                                                             len(counted_data[element].keys()),
                                                                                                             round(len(counted_data[element].keys())*100/sum(counted_data[element].values()), 2),
                                                                                                             sum(counted_data[element].values())
                                                                                                      )
            )
            chart.bar(sorted_data, element)
    
    # print some lines to make some space
    print('\n\n\n')

if __name__ == "__main__":
    main()
