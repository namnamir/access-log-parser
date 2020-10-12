# What Does it Do?
This python code is going to parse, analyze and visualize access.log file of Apache in Linux servers

# How to Install it?


# How to Use it?


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
