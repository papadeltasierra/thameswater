##!/bin.python
"""
Read daily water data from the Thames Water website and write it out to a
CSV file for easy import into something like Excel.
"""
import json
import csv
import argparse
import re
import time
from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# The CSV we create will contain these fields; the last three are from the
# downloaded JSON but the first we create from less useful date fields.
DAILY_FIELD_NAMES = [
    "Date", "Consumption", "CumulativeConsumption", "MeterRead"]

# These fields exist into the JSON data, Day as '12-Sep' and Month as '09'.
DAY = 'Day'
MONTH = 'Month'

# We prefer to write out standard dates such as 2017/09/12
DATE = 'Date'


class ThamesWater:
    """ A class for reading daily usage information from the thames Water
        website. """

    THAMES_WATER_LOGIN = 'https://www.thameswater.co.uk/login'
    # We cannot search for the Log In' text because of ::before and
    # ::after markers.
    INPUT_EMAIL = """//div[@class="fieldset"]/input"""
    INPUT_PASSWORD = """//input[@placeholder="Enter password here"]"""

    # Yes, there really are 12 leading spaces!
    NEXT_BUTTON = """//a[@class="btn btn-tw-secondary"]"""
    LOGIN_BUTTON = """//input[@value='Log in']"""
    VIEW_ACCOUNT = """//input[@title='View account']"""
    MY_USAGE = """//a[contains(., 'My usage')]"""
    DAILY_USAGE = """//a[contains(., 'View your daily usage here')]"""

    DEBUG_BODY = """//body"""

    TIMING_NAME = 'name'
    DAILYDATA = 'dailydata'

    def __init__(self, browser_driver, headless):

        print('Initializing browser...')
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument("--log-level=3")  # fatal

        self.web_driver = webdriver.Chrome(
            browser_driver, chrome_options=options)
        if not self.web_driver:
            raise Exception("Unable to launch Chrome driver")

    def login(self, username, password):
        """ Bring up the log-in screen and log us in. """

        # Start at the home page.
        self.web_driver.get(self.THAMES_WATER_LOGIN)
        wait = WebDriverWait(self.web_driver, 30)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, self.DEBUG_BODY)))
        wait.until(EC.presence_of_element_located(
            (By.XPATH, self.INPUT_EMAIL)))

        self.web_driver.find_element_by_xpath(self.INPUT_EMAIL).send_keys(
            username)
        self.web_driver.find_element_by_xpath(self.NEXT_BUTTON).click()

        wait = WebDriverWait(self.web_driver, 30)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, self.INPUT_PASSWORD)))

        self.web_driver.find_element_by_xpath(self.INPUT_PASSWORD).send_keys(
            password)
        self.web_driver.find_element_by_xpath(self.LOGIN_BUTTON).click()

    def read(self):
        """ Read the daily usage data. """

        print('Traversing website to get to daily usage data...')

        # Click the 'View account' button.
        self.web_driver.find_element_by_xpath(self.VIEW_ACCOUNT).click()

        # Click the 'My usage' href.
        self.web_driver.find_element_by_xpath(self.MY_USAGE).click()

        # Click the 'View your daily usage here' href
        # Search for href with text == 'View your daily usage here'
        self.web_driver.find_element_by_xpath(self.DAILY_USAGE).click()

        # We want the 'daily' file so we need to wait for it to have been
        # downloaded.  Give it 20s.
        wait_interval = 20
        data_filename = None
        rgx_daily = re.compile('.*Daily.xml')

        print("Waiting for daily usage data.", end='', flush=True)
        while wait_interval:
            wait_interval = wait_interval - 1

            # Access the performance data, which just happens to contain the
            # names of all http requested files downloaded as part of this
            # downloading this page.
            timings = self.web_driver.execute_script(
                "return window.performance.getEntries();")

            for timing in timings:
                if rgx_daily.match(timing[self.TIMING_NAME]):
                    data_filename = timing[self.TIMING_NAME]
                    break

            if data_filename:
                break

            time.sleep(1)
            print('.', end='', flush=True)

        if not data_filename:
            print('')
            raise Exception("Daily data not found")

        print('found')

        # Now that we have go here, we can download the daily usage figures as
        # a JSON file (confusingly called an XML file!).
        print('Downloading daily data file: \'%s\'...' % data_filename)
        self.web_driver.get(data_filename)

        # Hurrah - the body is the daily data encoded as JSON.
        daily_data = json.loads(
            self.web_driver.find_element_by_tag_name("body").text)
        return daily_data[self.DAILYDATA]

    def quit(self):
        """ Close down the Webself.web_driver. """
        self.web_driver.quit()


def write_csv(filename, json_data):
    """ Convert the received JSON daily usage data into a CSV file and write
        it out. """

    print('Writing daily usage data to CSV file...')

    # Convert the dates into sensible format.  Assumptions are:
    #
    # - We have < 12 months of data
    # - A month less than this month is the same year
    # - A month greater than this month must be the end of last year.
    today_month = date.today().month
    today_year = date.today().year

    for daily in json_data:
        this_date = datetime.strptime(daily["Day"], "%d-%b").date()
        this_month = this_date.month
        this_day = this_date.day
        if this_month <= today_month:
            # This year.
            this_date = datetime(today_year, this_month, this_day).date()
        else:
            # Last year.
            this_date = datetime(today_year-1, this_month, this_day).date()
        daily[DATE] = this_date.strftime("%Y/%m/%d")
        del daily[MONTH]
        del daily[DAY]

    with open(filename, 'w', newline='') as target:
        fieldnames = DAILY_FIELD_NAMES
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for daily in json_data:
            writer.writerow(daily)


def parser():
    """ Create a command line arguments parser. """

    arg_parser = argparse.ArgumentParser(description=(
        'Read daily water usage data from the Thames Water website and '
        'write it out to a CSV file.'))
    arg_parser.add_argument('--login', required=True,
                            help='your Thames Water login e-mail address')
    arg_parser.add_argument('--password', required=True,
                            help='your Thames Water login password')
    arg_parser.add_argument('--driver', required=True,
                            help='location of chromedriver')
    arg_parser.add_argument('--headless', action='store_true',
                            help='use headless browser')
    arg_parser.add_argument('--csv', required=True,
                            help='Name of CSV file to be written')
    return arg_parser


def main():
    """ Read daily water usage data from the Thames Water website and write
        is as a CSV file. """
    # Parse command line arguments
    args = parser().parse_args()

    # if True:
    try:
        # Create the browser object
        thames = ThamesWater(args.driver, args.headless)

        # if True:
        try:
            # Login to the Thames Water website
            thames.login(args.login, args.password)

            # Read the daily data as a JSON string.
            daily_data = thames.read()

            # Convert the data to CSV and write out the file.
            write_csv(args.csv, daily_data)

            # All done!
            print('Completed!')

        except Exception as exception:
            raise exception

        finally:
            # Close down the website.
            thames.quit()

    # Deliberately catching and ignoring the exception because we're about to
    # exit.
    except Exception as exception:    # pylint: disable=broad-except
        print("Failed with exception: %s" % str(exception))


if __name__ == '__main__':
    main()
