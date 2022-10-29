import smtplib, ssl
from email.message import EmailMessage
import env
import main


class SendEmail:
    msg = EmailMessage()
    ticket_email = "tooltix@databank.com"
    tools_team_email = "toolsteam@databank.com"

    def __init__(self, sender):
        self.sender = sender
        SendEmail.msg["From"] = self.sender

    def blacklistSuccessfullyCleared(self):
        blacklisted_emails_to_be_emailed = "\n".join(
            main.SeleniumChromeDriver.blacklisted_emails
        )
        self.subject = "Status.IO Blacklisted Emails Removed"
        self.content = f"Emails removed from the status io email blacklist:\n\n{blacklisted_emails_to_be_emailed}"
        self.msg["To"] = self.tools_team_email
        self.msg["Subject"] = self.subject
        self.msg.set_content(self.content)
        self.connectToServerAndSend()

    def scriptEarlyTerminationNotification(self):
        self.subject = "Status.IO Blacklisted Emails Script Error"
        self.content = "An error occured while running the status.io blacklisted emails remover. Check logs on the server for more information."
        self.msg["To"] = self.ticket_email
        self.msg["Subject"] = self.subject
        self.msg.set_content(self.content)
        self.connectToServerAndSend()

    def emailsNotRemoved(self):
        

    def noEmailsToRemove(self):
        self.subject = "Status.IO Blacklist No Emails to be Removed"
        self.content = "There were no blacklisted emails to be removed from the Status.IO email blacklist when the script ran."
        self.msg["To"] = self.ticket_email
        self.msg["Subject"] = self.subject
        self.msg.set_content(self.content)
        self.connectToServerAndSend()

    def connectToServerAndSend(self):
        context = ssl.create_default_context()
        with smtplib.SMTP("smtp.office365.com", port=587) as smtp:
            smtp.starttls(context=context)
            smtp.login(env.email_username, env.email_password)
            smtp.send_message(self.msg)
