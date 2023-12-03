### Run locally

! On UNIX like platforms `unixodbc` should be installed. !
[Refer to this page](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=ubuntu18-install,alpine17-install,debian8-install,redhat7-13-install,rhel7-offline)

1. Create Python 3.10 virtual environment
For example:
```bash
pyenv install 3.10
python -m venv env
source env/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. For better dev experience install dev dependencies
```bash
pip install -r requirements.dev.txt
```
