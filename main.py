from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from log_handler import Logging
import csv, glob, time, os, sys
import smtp
import env  # be sure to set variables in the env.py file before running this script.


class SeleniumChromeDriver:
    # start the virtual chrome driver
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": env.download_path}
    options.add_experimental_option("excludeSwitches", ["enable-logOutputToFile"])
    options.add_experimental_option("prefs", prefs)
    # chromeOptions = Options()
    # chromeOptions.headless = True

    # Below line to enable headless chrome client
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    # classwide variables
    blacklisted_emails = []
    path_to_logs = env.path_to_logs
    logger = Logging(path_to_logs=path_to_logs)
    email_sender = smtp.SendEmail(sender=env.email_username)

    def __init__(self):
        pass

    def navigateToStatusIOAndLogIn(self):
        try:
            expected_url = "https://app.status.io/statuspage/5d12c411b2ae2712fe35a742"
            self.driver.get("https://status.io/login")
            username = self.driver.find_element(By.ID, "email")
            passwd = self.driver.find_element(By.ID, "password")
            username.send_keys(env.status_io_username)
            passwd.send_keys(env.status_io_password, Keys.ENTER)
            WebDriverWait(self.driver, 10).until(EC.title_is("Status.io"))
        except Exception as e:
            self.logger.unableToNavigateToStatusIOAndLogIn(e)
            self.email_sender.scriptEarlyTerminationNotification()
            self.driver.quit()
            sys.exit("Failed at main.SeleniumChromeDriver.navigateToStatusIOAndLogIn")

    def downloadBlacklistedEmailsCSVFromNotificationsPage(self, url):
        try:
            self.url = url
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//*[@id="wrapper"]/section/div/div[2]/div[6]/article/div/section/a[1]',
                    )
                )
            )
            download_csv_button = SeleniumChromeDriver.driver.find_element(
                By.XPATH,
                '//*[@id="wrapper"]/section/div/div[2]/div[6]/article/div/section/a[1]',
            )
            download_csv_button.click()
            time.sleep(2)
        except TimeoutException:
            self.logger.noEmailsPresentOnBlacklist()
            self.email_sender.noEmailsToRemove()
            sys.exit(
                "Download Blacklisted Emails file element not present on the status io notifications page"
            )
        except Exception as e:
            self.logger.unableToDownloadBlacklistedEmailsCSV(e)
            self.email_sender.scriptEarlyTerminationNotification()
            self.driver.quit()
            sys.exit(
                "Failed at main.SeleniumChromeDriver.downloadBlacklistedEmailsCSVFromNotificationsPage"
            )

    def parseCSVForEmails(self):
        filename = glob.glob(env.download_path + "\\blacklist-*")[0]
        try:
            with open(filename, "r") as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                    email = row[0]
                    if email:
                        self.blacklisted_emails.append(email)
                    return self.blacklisted_emails
        except Exception as e:
            self.logger.unableToParseCSVForEmails(e)
            self.email_sender.scriptEarlyTerminationNotification()
            self.driver.quit()
            sys.exit("Failed at main.SeleniumChromeDriver.parseCSVForEmails")

    def fillOutBlacklistedEmailsForm(self):
        try:
            for i in range(len(self.blacklisted_emails)):
                blacklist_element = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="wrapper"]/section/div/div[2]/div[6]/article/div/section/a[2]',
                )
                blacklist_element.click()

                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="email_address"]'))
                )
                blacklisted_email_form = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="email_address"]',
                )
                blacklisted_email_form.send_keys(self.blacklisted_emails[i])

                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="read_statement"]'))
                )
                blacklist_box = self.driver.find_element(
                    By.XPATH, '//*[@id="read_statement"]'
                )
                blacklist_box.click()
                blacklist_submit = self.driver.find_element(
                    By.XPATH,
                    '//*[@id="blacklist_removal_modal"]/div/div/div[2]/form/div[3]/button',
                )
                blacklist_submit.click()
            time.sleep(1)
        except Exception as e:
            self.logger.unableToFillOutBlacklistedEmailsForm(e)
            self.email_sender.scriptEarlyTerminationNotification()
            self.driver.quit()
            sys.exit("Failed at main.SeleniumChromeDriver.fillOutBlacklistedEmailsForm")

    def deleteDownloadedCSV(self):
        try:
            filename = glob.glob(env.download_path + "\\blacklist-*")[0]
            os.remove(filename)
        except Exception as e:
            self.logger.unableToDeleteDownloadedCSV(e)
            self.email_sender.scriptEarlyTerminationNotification()
            self.driver.quit()
            sys.exit("Failed at main.SeleniumChromeDriver.deleteDownloadedCSV")

    def checkIfAllEmailsRemoved(self):
        while True:
            try:
                self.downloadBlacklistedEmailsCSVFromNotificationsPage("https://app.status.io/dashboard/5d12c411b2ae2712fe35a742/notifications/email")
                self.logger.programSuccessful()
                self.parseCSVForEmails()
                self.deleteDownloadedCSV()
                self.logger.unableToRemoveAllEmails()
                break
            except NoSuchElementException:
                break
            
    def ranSuccessfully(self):
        self.driver.quit()
        self.logger.programSuccessful()
        self.email_sender.blacklistSuccessfullyCleared()

    def main(self):
        self.navigateToStatusIOAndLogIn()
        self.downloadBlacklistedEmailsCSVFromNotificationsPage(
            "https://app.status.io/dashboard/5d12c411b2ae2712fe35a742/notifications/email"
        )
        self.parseCSVForEmails()
        self.fillOutBlacklistedEmailsForm()
        self.deleteDownloadedCSV()
        self.driver.quit()
        self.email_sender.blacklistSuccessfullyCleared()
        self.ranSuccessfully()

    # below methods used for testing

    def parseTestCSVForEmails(self):
        try:
            blacklisted_emails = self.blacklisted_emails
            with open(env.download_path + "\\use_me_to_test.csv") as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                    email = row[0]
                    if email:
                        blacklisted_emails.append(email)
                return blacklisted_emails
        except Exception as e:
            self.logger.testLoggingMethod(e)
            self.email_sender.scriptEarlyTerminationNotification()
            self.driver.quit()
            sys.exit("Failed at main.SeleniumChromeDriver.parseTestCSVForEmails")

    def test(self):
        self.navigateToStatusIOAndLogIn()
        self.downloadBlacklistedEmailsCSVFromNotificationsPage(
            "https://app.status.io/dashboard/5e348d87d8905e088e69e7d7/notifications/email"
        )
        self.parseTestCSVForEmails()
        self.fillOutBlacklistedEmailsForm()
        self.deleteDownloadedCSV()
        self.ranSuccessfully()
