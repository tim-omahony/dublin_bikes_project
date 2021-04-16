# Dublin Bikes! :)

## What does that app do?
This web app displays current information on availability of bikes in the Dublin Bikes system using the JCDecaux API. Scrapers are run ever 5 minutes to retrieve the latest updates on availability of bikes and spaces at each station, as well as scraping the Open Weather API to retrieve information on the current weather in Dublin City.

The app uses predictive models to predict the number of bikes at a given station and the temperature in the City on a given day entered by the user.

## Link to the ec2 instance used by the application: 
http://ec2-3-141-5-42.us-east-2.compute.amazonaws.com/

## Link to the webpage the application is hosted on: 
http://dublinbikes.codes/

## Running the app:
#### Locally (through terminal)
 ```bash
FLASK_ENV=development FLASK_APP=app.py python -m flask run
````
#### In production (through terminal)
 ```bash
FLASK_ENV=production FLASK_APP=app.py python -m flask run
 ```
### Running migrations:
```bash
python3 -m {module_path.class}
```
e.g.
```bash
python3 -m dbbikes.workers.connection_import_data
```

## Setting database details:
Copy the example details to a file called db_details and set user and password to your local user and db password
```bash
cp config/db_details.py.example config/db_details.py
```
## How the scrapers are run on the ec2 instance:
### populate_dbbikes_database.py
To run the bikes script every five minutes ssh to EC2 instance and enter the command:

```bash
crontab -e 
```

and enter the following:

```bash
*/5 * * * * /home/ubuntu/anaconda3/bin/python ~/populate_dbbikes_database.py >> ~/populate.log
```
The script outputs its prints to populate.log

To run the weather script enter the following: 

```bash
*/5 * * * * /home/ubuntu/anaconda3/bin/python ~/weather_to_db.py
```

#### The app was made (with great love and attention) by Annmarie Monaghan, Ciara Purcell and Tim O'Mahony.
