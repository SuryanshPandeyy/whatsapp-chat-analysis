import re
import pandas as pd


def convert_date(dates):
    new_date = []
    for i in dates:
        date = i.split(',')[0].split('/')
        time = i.split(',')[1]
        date[2] = '20' + i.split('/')[2].split(',')[0]
        date = '/'.join(date) + ',' + time
        new_date.append(date)
    return new_date


def split_user_message(df):
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group-notification')
            messages.append(entry[0])

    return users, messages


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    new_date = convert_date(dates)

    df = pd.DataFrame({'user_message': messages, 'message_date': new_date})
    df["message_date"] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users, messages = split_user_message(df)
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
