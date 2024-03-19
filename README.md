# HevoData
Demo Project For HevoData

# Project Setup 
- Make sure, You have Chrome browser installed on your system
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