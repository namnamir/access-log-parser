# What Does it Do?
This python code is going to parse, analyze and visualize access.log file of Apache in Linux servers

# How to Install it?
- Make sure that you have Python 3.1 or above by typing `python --version` in the terminal.
- Download [the updated package](https://github.com/namnamir/access-log-parser/archive/main.zip).
- Install requirements by running this command in your terminal `pip install -r requirements.txt`. Maybe it is a good idea to install a virtual environment.
- Configure the `config.py` file.

# How to Use it?
Using this tool is so simple. You fist need to config the `config.py` in the way you like. It has been pre-configured but you can change it by your desire.

To see the help, just run `python main.py -h` or `python main.py -help`.
```Bash
usage: main.py [-h] -f [PATH_to_FILE] [-l [No_of_LINES]] -e [ELEMENT_NAME]
               [-ne [No_of_ELEMENTS]] [-nm [No_of_MONTH]] [-se [ASC|DES]] [-sm [ASC|DES]]

The Apache access.log file parser

optional arguments:
  -h, --help            show this help message and exit
  -f [PATH_to_FILE], --file [PATH_to_FILE]
                        [Required] Path to the Apache log file
  -l [No_of_LINES], --line [No_of_LINES]
                        [Optional] Set the number of the lines to be parsed from the
                        begining of the file.
  -e [ELEMENT_NAME], --element [ELEMENT_NAME]
                        [Required] Report based on the selected element.
  -ne [No_of_ELEMENTS], --number_element [No_of_ELEMENTS]
                        [Optional] Show the number of top elements. Default: 10
  -nm [No_of_MONTH], --number_month [No_of_MONTH]
                        [Optional] Show the number of top months. Zero (0) means not
                        categorization by month. Default: 3
  -se [ASC|DES], --sort_element [ASC|DES]
                        [Optional] Sort data ascendingly or desendingly. Default: des
  -sm [ASC|DES], --sort_month [ASC|DES]
                        [Optional] Sort monthly-based data (just months) ascendingly or
                        desendingly. Default: asc
``` 
As it can be seen, there are different arguments that can be used for parsing the `access.log` file.

## List of Gathering Data (Elements)
```
host_ip
host_country *
host_city *
host_province *
host_isp *
identity
user
time
size
referrer
user_agent_device
user_agent_os
user_agent_browser
```
Note: Marked elements depend on an API that can parse IPs.

## Examples
The following command will get the first **100** lines of `access.log` and parse them for the element `host_ip`. It will not categorize parsed logs in different months.
```bash
python main.py -f ./access.log -l 100 -nm 0 -e host_ip
```

This command will get all lines of the log file and show top 20 visitors' country in past 6 months (desendingly).
```bash
python main.py -f ./access.log -l 0 -nm 6 -e host_country -ne 20
```

# Rationale
A line of `access.log` is look like the following.
``` Bash
154.0.14.250 - - [06/Dec/2016:16:18:10 +0100] "POST /administrator/index.php HTTP/1.1" 200 4494 "http://almhuette-raith.at/administrator/index.php" "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0" "-"
```
It reveals that the pattern looks `%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"` where:
 - `%h` is the IP address of the client.
 - `%l` holds the user identity, if any. So, it can be none (aka `-`).
 - `%u` shows the username of the client if the request was authenticated, if any. So, it can be none (aka `-`).
 - `%t` shows the time that the request was received.
 - `\"%r\"` contains the the request line that includes the *HTTP method*, the *requested path*, and the *HTTP protocol*.
 - `%>s` shows the HTTP status code.
 - `%b` shows the size of the HTTP request.
 - `\"%{Referer}i\"` holds the referral URL, if any. So, it can be none (aka `-`).
 - `\"%{User-agent}i\"` contains the user agent (browser) details.

Read more about it [here](https://httpd.apache.org/docs/current/mod/mod_log_config.html).


# Change Log
## Version 1.0
- The initial script is released on 11 Oct 2020.

# To-Dos
- [ ] Add more charts
- [ ] Show the number of data
- [ ] Show the last element of data