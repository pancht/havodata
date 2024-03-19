# havodata
Project For HavoData

# Project setup details

- `pip install mysql-connector-python`
- `pip install Faker`
- `pip install sshtunnel`
- `pip install pymysql`

# Project Setup 
- Create a project dir
  - `mkdir HevoData`
- CD into project dir
  - `cd HevoData`
- Clone repo
  - `git clone git@github.com:pancht/havodata.git`
- CD into havodata dir (Sorry for the incorrect name _/\_)
  - `cd havodata`
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
- Install nRoBo Test Automation Framework
  - `pip install nrobo --require-virtualenv`
- Run the test 
  - `nrobo`