from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import env  # be sure to set variables in the env.py file before running this script.
import smtp
import csv, glob, time, os
from datetime import datetime


# setting up the chrome driver for selenium to use
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": env.download_path}
options.add_experimental_option("excludeSwitches", ["enable-logOutputToFile"])
options.add_experimental_option("prefs", prefs)
### Below line to enable headless chrome client
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
blacklisted_emails = []
date = datetime.now().strftime("%Y%m%d-%H%M%S%p")


##Open browser and login as user
def startDriverAndAuthenticateStatusIO():
    driver.get("https://status.io/login")
    username = driver.find_element(By.ID, "email")
    passwd = driver.find_element(By.ID, "password")
    username.send_keys(env.status_io_username)
    passwd.send_keys(env.status_io_password, Keys.ENTER)


# Download the CSV that contains the list of blacklisted emails
def downloadBlacklistedEmailFile():
    # Navigate to notifications page
    driver.get(
        "https://app.status.io/dashboard/5d12c411b2ae2712fe35a742/notifications/email"
    )
    # Try to click on the find download blacklist button
    try:
        download_csv_button = driver.find_element(
            By.XPATH,
            '//*[@id="wrapper"]/section/div/div[2]/div[6]/article/div/section/a[1]',
        )
        download_csv_button.click()
        time.sleep(2)
    except Exception as e:
        filename = f"{env.download_path}\\logging\\log_{date}.txt"
        with open(filename, "x") as f:
            print(
                str(e)
                + "\n\nThis traceback likely means there are no emails to remove on the blacklist",
                file=f,
            )


##use the blacklist removal tool
def parseFileForEmails():
    filename = glob.glob(env.download_path + "\\blacklist-*")[0]
    print(filename)
    with open(filename, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            email = row[0]
            if email:
                blacklisted_emails.append(email)
        print(blacklisted_emails)
        return blacklisted_emails


def fillOutBlacklistedEmailsForm():
    # iterate through the list of emails an use the blacklist removal tool
    for i in range(len(blacklisted_emails)):
        blacklist_element = driver.find_element(
            By.XPATH,
            '//*[@id="wrapper"]/section/div/div[2]/div[6]/article/div/section/a[2]',
        )
        blacklist_element.click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="email_address"]'))
        )
        blacklisted_email_form = driver.find_element(
            By.XPATH,
            '//*[@id="email_address"]',
        )
        blacklisted_email_form.send_keys(blacklisted_emails[i])

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="read_statement"]'))
        )
        blacklist_box = driver.find_element(By.XPATH, '//*[@id="read_statement"]')
        blacklist_box.click()
        blacklist_submit = driver.find_element(
            By.XPATH,
            '//*[@id="blacklist_removal_modal"]/div/div/div[2]/form/div[3]/button',
        )
        blacklist_submit.click()
    time.sleep(1)


# function for testing
def testingtesting123():
    startDriverAndAuthenticateStatusIO()
    driver.get(
        "https://app.status.io/dashboard/5e348d87d8905e088e69e7d7/notifications/email"
    )
    with open(env.download_path + "\\use_me_to_test.csv") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            email = row[0]
            if email:
                blacklisted_emails.append(email)
        print(blacklisted_emails)
        fillOutBlacklistedEmailsForm()
        logOutputToFile()
        sending = smtp.SendEmail(
            sender=env.email_username, send_to="bwoodbury@databank.com"
        )
        sending.blacklistSuccessfullyCleared()


def deleteFile():
    try:
        filename = glob.glob(env.download_path + "\\blacklist-*")[0]
        os.remove(filename)
    except Exception as e:
        filename = f"{env.download_path}\\logging\\log_{date}.txt"
        with open(filename, "x") as f:
            print(
                str(e)
                + "\n\n This likely means the csv containing the blacklisted emails was not deleted ",
                file=f,
            )


def logOutputToFile():
    filename = f"{env.download_path}\\logging\log_{date}.txt"
    with open(filename, "x") as f:
        print(f"Emails removed: {blacklisted_emails}", file=f)


def main():
    startDriverAndAuthenticateStatusIO()
    downloadBlacklistedEmailFile()
    parseFileForEmails()
    fillOutBlacklistedEmailsForm()
    deleteFile()
    logOutputToFile()
