# StatusIO Blacklisted Emails Remover

Before running this script you'll need to install required dependencies by running:
        
    $python -m pip install -r requirements.txt

You'll need to install google chrome and the chromium web driver

>download chromedriver: https://chromedriver.chromium.org/ <br />
>download google chrome: https://www.google.com/chrome/


Once you've got it downloaded, add chromedriver to your local PATH and restart your shell.

Next, you need to create a file within the directory of this program called .env and set some  variables in a .env file. In .env  you need to set the following variables: 
>*when adding a path to a directory instead of using '/' use ```'\\'``` example:*  ```'c:\\users\\user'```


    status_io_username = 'user_here'
    status_io_password = 'pass_here'
    download_path = 'desired_download_path'
    path_to_logs = 'desired_path_to_logs'
    email_username = 'email_user_here'
    email_password = 'email_pass_here'
    smtp_server = 'smtp_server_here'



>*Note: If you do not create a .env file within the /code directory and add the variables above, your code will not run. You do not need to edit env.py, only create and edit .env*

- status_io_username is the username that will be passed into the webdriver to log into status io
-  status_io_password is the password that will be passed into the webdrive to log into status io
    - note, there are StatusIO creds under epicor asset 'StatusIO'
-  download_path path is where you'd like the file to be stored for use in the script. The file is deleted after use. 
-  path_to_logs is where you want the log files store, '/var/log/statusio_bl_remover or './logs' are 2 suggestions. 
-  email_username is the email used to log in and send emails with smtp.py
-  email_password is the password for email_username
-  smtp_server is the smtp server we're connecting to to send mail



Finally, run the script with:

    $python runme.py



## Directory overview: 

- .env holds the environment variables accessed in env.py that are passed into the script
- env.py pulls from .env to pass environment variables into the program. 
- main.py is where the class SeleniumChromeDriver lives, this class is where the functions main() and test_main() are being called from in runme.py and test_runme.py respectively
- runme.py is for running the script
- smtp.py is a class for sending email notifications
- log_handler.py contains the class Logging which holds various methods to dump errors into a .txt file in the log folder
- test_runme.py is a script that uses the test page and pulls emails from "use_me_to_test.csv" for testing purposes
- __init__.py tells python the *.py files in this folder can be pulled in as packages to be used by other *.py files

**_fin._**


