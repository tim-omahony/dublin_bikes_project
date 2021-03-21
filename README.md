# dublin_bikes_project
## Running the app
### Locally
 ```bash
FLASK_ENV=development FLASK_APP=app.py python -m flask run
````
### In production
 ```bash
FLASK_ENV=production FLASK_APP=app.py python -m flask run
 ```
## Running migrations
```bash
python {name_of_migration}.py
```

# Setting database details
Copy the example details to a file called db_details and set user and password to your local user and db password
```bash
cp config/db_details.py.example config/db_details.py
```

## populate_dbbikes_database.py
To run this script every five minutes ssh to EC2 instance and enter the command:

```bash
crontab -e 
```

and enter the following:

```bash
*/5 * * * * /home/ubuntu/anaconda3/bin/python ~/populate_dbbikes_database.py >> ~/populate.log
```

The script outputs its prints to populate.log

