import pandas as pd
import matplotlib
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import pymysql
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
#from sklearn.model_selection import cross_validate
#from sklearn.model_selection import cross_val_score
import pickle
#from  models.populate_dbbikes_database import *
import matplotlib.dates as mdates
from sqlalchemy import create_engine

USER = "ciara"
PASSWORD = "Ciara123"
PORT = "3306"
DB = "dbbikes"
URI = "dbbikes.cvr6gofoxmkp.us-east-2.rds.amazonaws.com"
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

sql = f"""
SELECT id, number, last_update, available_bikes, available_bike_stands FROM stations
GROUP BY id, day(last_update)
ORDER by id, last_update ASC;
"""
#last_update=datetime.datetime.fromtimestamp(station.get('last_update') / 1e3)
#print(sql)

bike_df = pd.read_sql_query(sql, engine)

bike_df['last_update'] = bike_df['last_update'].astype('datetime64[ns]')

#from datetime import datetime
bike_df['last_update'] = pd.to_datetime(bike_df['last_update'])

#bike_df.last_update = datetime.utcfromtimestamp(bike_df.last_update).strftime('%Y-%m-%d %H:%M:%S')
bike_df

bike_df.dtypes

bike_df.shape

bike_df.tail()

#Weather

sql = f"""

SELECT * FROM weather

"""

weather_df = pd.read_sql_query(sql, engine)

weather_df.dtypes

# category
weather_df['description'] = weather_df['description'].astype('category')

# datetime
weather_df['last_update_weather'] = weather_df['last_update_weather'].astype('datetime64[ns]')

weather_df.dtypes

weather_df.shape

weather_df.tail()

# Together - using pandas merge_asof

# https://pandas.pydata.org/docs/reference/api/pandas.merge_asof.html

# closest to

bike_df.sort_values('last_update', inplace=True)
weather_df.sort_values('last_update_weather', inplace=True)

df = pd.merge_asof(bike_df, weather_df, left_on='last_update', right_on='last_update_weather')

df.shape

df = df.drop(['last_update_weather'], axis=1)

df.tail(5)

df = df.drop(['id_y'], axis=1)

df = df.drop(['id_x'], axis=1)

df.tail(5)

#The Stations

stations = list(sorted(df.number.unique()))
print(stations)
print(len(stations))

#The Days

# New column called weekday with the number of the day of the week
df['weekday'] = df['last_update'].dt.dayofweek
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.weekday.html
df_monday = df[df.weekday == 0]
df_tuesday = df[df.weekday == 1]
df_wednesday = df[df.weekday == 2]
df_thursday = df[df.weekday == 3]
df_friday = df[df.weekday == 4]
df_saturday = df[df.weekday == 5]
df_sunday = df[df.weekday == 6]

#The Hours

# New column called hourly
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.hour.html
df['hourly'] = df['last_update'].dt.hour

# https://stackoverflow.com/questions/61124647/pandas-how-to-get-dummies-on-time-series-data
#  hours 0 to 23 will be 0 with one hour being 1
#hourly_dummies = pd.get_dummies(df['hourly'], prefix='hour')

hourly_dummies = pd.get_dummies(df['hourly'], prefix='hour')

# https://towardsdatascience.com/pandas-concat-tricks-you-should-know-to-speed-up-your-data-analysis-cd3d4fdfe6dd
df = pd.concat([df, hourly_dummies], axis=1)

# then drop original column - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop.html


# list of  hour dummies- # https://datatofish.com/list-column-names-pandas-dataframe/
hour_dummies = list(hourly_dummies)

df.drop(['hourly'], axis=1)

#The Dataframes

# dataframes based on day of week
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.weekday.html
# df_monday = df[df.weekday == 0]
# df_tuesday = df[df.weekday == 1]
# df_wednesday = df[df.weekday == 2]
# df_thursday = df[df.weekday == 3]
# df_friday = df[df.weekday == 4]
# df_saturday = df[df.weekday == 5]
# df_sunday = df[df.weekday == 6]

df_monday

df_tuesday

# Group by number of the station

# df_monday_station = df_monday.groupby(['number']).mean()
# df_tuesday_station = df_tuesday.groupby(['number'])
# df_wednesday_station = df_wednesday.groupby(['number'])
# df_thursday_station = df_thursday.groupby(['number'])
# df_friday_station = df_friday.groupby(['number'])
# df_saturday_station = df_saturday.groupby(['number'])
# df_sunday_station = df_sunday.groupby(['number'])

# df_monday_station

#Features

# Get all features
A = [hour_dummies]
B = ['description', 'temp', 'last_update']
features = (A + B)

print(A)

print(B)

print(features)

from itertools import chain

print(list(chain.from_iterable(features)))

#Training

# Taking each day individually

# Monday

for station in stations:

    # x-axis is the features

    a = df_monday

    x = a.groupby('number').temp

    # y-axis is the available_bikes
    y = a.groupby('number').available_bikes

    # y = a.available_bikes
    # This is from https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)
    model = LinearRegression(fit_intercept=False, normalize=False).fit(x_train, y_train)

    # Write to a pickle file
    with open('/?/pickles/Monday-' + str(station) + '.pkl', 'wb') as handle:
        pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Create vectors of predictions
    train_predictions = model.predict(X_train)
    print('Train predictions for station ', station, ": ", train_predictions)

    test_predictions = model.predict(X_test)
    print('Test predictions for station ', station, ": ", test_predictions)

    # R^2 - R-squared is a statistical measure of how close the data are to the fitted regression line.
    # r2 = metrics.r2_score(y_true, y_predict)
    r2 = metrics.r2_score(y_test, test_predictions)
    print(r2)

    # how well does the model behave compared to a chosen r2 ?
    # an r2 of 0.75 indicates that 25% of the variability in the outcome data cannot be explained by the model
    # initialise to get how many times the model outperforms r2 = 0.75
    i = 0
    if r2 > 0.75:
        i += 1

    print('Percentage of models that have outperformed R^2 = 0.75:', (i / 110) * 100)  # there are 110 stations
