<img src="https://img.shields.io/badge/Python-v3.8-blue">

# Deltalake Database Projects
Python deployment of SQL DB project files held by object for better management of databases using an IDE Visual Studio Code and Git.


## Parameters
There are 3 parameters defined using click:

```python
@click.command()
@click.option("--db_project", type=str)
@click.option("--config_dir", default="./db_projects", type=str)
@click.option("--config_file", default="config.yml", type=str)
```

- db_project: The project collection of databases you want to build in the config
- config_dir: The home folder of the project files & configuration
- config_file: The projection configuration of environments and projects

Configuration settings are held in a config.json file by default.

```yaml
environments: 
    development:
        storage: adl:blahblah
        location: "{{ storage }}/databricks/{{ database_home }}/{{ database_folder_name }}/{{ table_name }}"

    production:
        storage: adl:lalalala
        location: "{{ storage }}/databricks/{{ database_home }}/{{ database_folder_name }}/{{ table_name }}"

projects : 
    TestDB: 
        TestDBSql1 :
            database_folder_name: testdb
            database_home: delta
            format: delta
            table_type: UNMANAGED
        TestDBSql2:
            database_folder_name: testdb
            database_home: delta
            format: delta
            table_type: UNMANAGED
```



## Required Database Project Structure
Databases scripts must be 1 for each object and the files must have the same name as the object. Each SQL DML file must have the .sql extention.
Example project structure is as follows

Databases -> contains folders for database project

&nbsp;&nbsp;TestDB -> holds all the SQL Scripts for test DB

&nbsp;&nbsp;&nbsp;&nbsp;TestDB.sql -> script that creates the database if not exists

&nbsp;&nbsp;&nbsp;&nbsp;Tables -> holds the scripts for the tables

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TestTable1.sql -> table creation script for TestTable1

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TestTable2.sql -> table creation script for TestTable2

&nbsp;&nbsp;&nbsp;&nbsp;Views -> holds the scripts for the views - assumes create or replace

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TestView1.sql -> table creation script for TestView1

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;TestView2.sql -> table creation script for TestView2 

Deploy

&nbsp;&nbsp;deploy.py -> reads the scripts and executes them on your remote cluster using databricks-connect.

# Development Setup

Create virual environment and install dependencies for local development:

```
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install --editable .
```

# Run

```
python -m deltalake_dp --db_project TestDB --config_dir ./db_projects --config_file config.yml
```

# Build

Build python wheel:
```
python setup.py sdist bdist_wheel
```

There is a CI build configured for this repo that builds on main origin and publishes to PyPi.

# Test

Dependencies for testing:
```
pip install --editable .
```

Run tests:
```
pytest
```

Test Coverage:
```
pytest --cov=autobricks --cov-report=html
```

View the report in a browser:
```
./htmlcov/index.html
```


