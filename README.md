# thameswater
Disclaimer: I have no connection to [Thames Water][thames] at all (other than a water supply and sewage pipe ;-) ) and this is a utility that I wrote because I was frustrated that I could not download this information directly from the website.

## What It Does
This is a Python utility that allows you to download your daily water usage, over the last 6 months, from the [Thames Water][thames] website and produce a comma separated values (CSV) file that you can import into a spreadsheet or use in whatever way you wish.

Under the covers the utility uses the [Chrome browser][chrome] to surf the [Thames Water][thames] website and download the information that you want.

## Installation
You will need both the [Chrome browser][chrome] and the [ChromeDriver – WebDriver for Chrome][chromedriver] .  The [ChromeDriver - WebDriver for Chrome][chromedriver] allows this Python application to drive the Chrome browser just as if you were sat their typing and clicking links – you can sit and watch this happen if you like by not running this script ‘headless’.

So install Chrome if you haven’t already and then copy the ChromeDriver to somewhere on your system before installing this utility.

It is recommended that you install the utility into either virtualenv or venv environment and you must use Python3 not Python2.  Once the environment is created, the following should install this utility:

```
$ pip install thameswater
```

The thameswater application can then be run to download your daily water usage data.

## Usage
```
usage: thameswater.py [-h] --login LOGIN --password PASSWORD --driver DRIVER
                      [--headless] --csv CSV

Read daily water usage data from the Thames Water website and write it out to
a CSV file.

optional arguments:
  -h, --help           show this help message and exit
  --login LOGIN        your Thames Water login e-mail address
  --password PASSWORD  your Thames Water login password
  --driver DRIVER      location of browser driver e.g. chromedriver
  --headless           use headless browser
  --csv CSV            Name of CSV file to be written
```
You probably want to create a batch/shell script to avoid having to type the longish command line each time.

## It Went Wrong!
Very occasionally it does, normally because the [Thames Water][thames] website has stopped responding in a timely manner; go make a cup of tea and try later because there’s nothing you or I can do about that!

## Under the Covers
The Python script uses [Selenium][selenium] to drive the [Chrome browser][chrome] via the [ChromeDriver WebDriver][chromedriver].  It then runs around the Thames Water website just as you would, including logging in using the e-mail address and password that you provided, until it reaches the ‘Daily Usage’ page.

It turns out that in order to show the daily bar charts, the [Thames Water][thames] website downloads the last 6 months of daily usage in a JSON encoded file, which this script gets hold of, tweaks the dates into a more sensible format and then writes out to the CSV file.  The JSON file is accessed via Chrome’s performance data, the data that Chrome uses to show network access if you watch your browsing with the Developer Tools open.

## Why Chrome?
* It’s the browser that I normally use; the code might well work with Firefox and the Firefox driver or perhaps even Edge or other browsers, providing a suitable Selenium driver is available.
* Chrome can be run in ‘headless’ mode which is nice if you don’t want a browser to launch onto your desktop just to download these figures.

## Debugging/Logging
Logging is turned off by default but can be enabled via the command-line options.  Logging is disabled because there is nothing interesting at present and there are lots of confusing warnings and complaints that do not affect the operation of the utility.

  [thames]: https://www.thameswater.co.uk
  [chrome]: https://www.google.com/chrome/
  [chromedriver]: https://sites.google.com/a/chromium.org/chromedriver/downloads
  [pypi]: https://pypi.org/thameswater
  [selenium]: http://selenium-python.readthedocs.io/
