import env, main
from datetime import datetime
import traceback
import os


class Logging:
    date = datetime.now().strftime("%Y-%m-%d--%H-%M-%S")

    def __init__(self, path_to_logs):
        self.path_to_logs = path_to_logs

    def unableToNavigateToStatusIOAndLogIn(self, exception):
        while True:
            try:
                self.exception = exception
                filename = f"{self.path_to_logs}\\log_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        str(exception)
                        + f"\n\nThis error likely means that the program is either unable to navigate to status.io/login, or the credentials are set incorrectly in env.py\n\n{traceback.format_exc()}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def noEmailsPresentOnBlacklist(self):
        while True:
            try:
                filename = f"{self.path_to_logs}\\log_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        str(
                            "No Emails were downloaded from https://app.status.io/dashboard/5d12c411b2ae2712fe35a742/notifications/email, likely because there were none to be removed at the time of the script running."
                        )
                        + f"\n\npy\n\n{traceback.format_exc()}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def unableToDownloadBlacklistedEmailsCSV(self, exception):
        while True:
            try:
                self.exception = exception
                filename = f"{self.path_to_logs}\\log_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        str(exception)
                        + f"\n\nThis error likely means there are no emails to remove on the blacklist\n\n{traceback.format_exc()}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def unableToParseCSVForEmails(self, exception):
        while True:
            try:
                self.exception = exception
                filename = f"{self.path_to_logs}\\log_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        str(exception)
                        + f"\n\nThis likely means the program was unable to parse the CSV downloaded to {env.download_path} for the blacklisted emails\n\n{traceback.format_exc()}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def unableToFillOutBlacklistedEmailsForm(self, exception):
        while True:
            try:
                self.exception = exception
                filename = f"{self.path_to_logs}\\log_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        str(exception)
                        + f"\n\nThis likely means that the program was unable to fill out the form to remove the emails from the blacklist\n\n{traceback.format_exc()}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def unableToDeleteDownloadedCSV(self, exception):
        while True:
            try:
                self.exception = exception
                filename = f"{self.path_to_logs}\\log_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        str(exception)
                        + f"\n\nThis likely means the program was unable to delete the downloaded CSV from {env.download_path}\n\n{traceback.format_exc()}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def unableToRemoveAllEmails(self):
        while True:
            try:
                blacklisted_emails_not_removed = "\n".join(
                    main.SeleniumChromeDriver.blacklisted_emails
                )
                filename = f"{self.path_to_logs}\\emails_not_removed_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        f"Emails that could not be removed from the blacklist:\n\n{blacklisted_emails_not_removed}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def programSuccessful(self):
        while True:
            try:
                blacklisted_emails_successfully_removed = "\n".join(
                    main.SeleniumChromeDriver.blacklisted_emails
                )
                filename = f"{self.path_to_logs}\\emails_removed_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        f"Emails removed from the blacklist:\n\n{blacklisted_emails_successfully_removed}",
                        file=f,
                    )
                    break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)

    def testLoggingMethod(self, exception):
        while True:
            try:
                self.exception = exception
                filename = f"{self.path_to_logs}\\test_log_{self.date}.txt"
                with open(filename, "x") as f:
                    print(
                        str(exception) + "\n\nThis is a logging test message",
                        file=f,
                    )
                break
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)


    def testingtestingtesting(self):
        while True:
            try: 
                self.exception = exception
            except FileNotFoundError:
                os.mkdir(path=env.path_to_logs)
