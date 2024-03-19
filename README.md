# HevoData
Demo Project For HevoData

NOTES:
  - Script do not cover sign in with Gmail method.
  - Make sure, You have Chrome browser installed on your system
  - Script covers only 1st test. and Not the 2nd test, altering row in source database, run pipeline and verify destination database.
  - Script is tested on macOS. However, it will work on Windows too!
  - Delete any pipeline and destinations if exists!!! Script will fail for sure in this case as it assumes that there are no pipelines and destinations exists in give HevoData account.

# Project Setup
- Create a project dir of your choice
  - `mkdir HevoData`
- CD into project dir
  - `cd HevoData`
- Clone repo
  - `git clone git@github.com:pancht/havodata.git`
- CD into havodata dir (Sorry for the incorrect name _/\_)
  - `cd havodata`
- Rename file cred-sample.yaml => cred.yaml
  - Add necessary details and remove all comments
- Create virtual environment
  - Install virtualenv module if not installed
    - `pip install virtualenv`
  - Install virtualenv
    - `virtualenv .venv`
- Activate virtualenv
  - Unix/Mac/Linux
    - `source .venv/bin/activate`
  - Windows
    - `.\\.venv\\Scripts\\activate`
- Install Python MySql connector module
  - `pip install mysql-connector-python`
- Install Faker module
  - `pip install Faker`
- Install sshtunnel module
  - `pip install sshtunnel`
- Install pymysql module
  - `pip install pymysql`
- Install nRoBo Test Automation Framework
  - `pip install nrobo --require-virtualenv`
- Run the test 
  - `nrobo`

Thanks!

Have a nice time.