# dublin_bikes_project

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
