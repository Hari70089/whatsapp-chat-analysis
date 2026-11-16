
import re
import pandas as pd


def preprocesser(data):

    pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s\]\s'

    messages = re.split(pattern, data)[1:]

    dates = re.findall(
        r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2})\s\]',
        data
    )

    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    df['message_date'] = pd.to_datetime(
        df['message_date'],
        format='%m/%d/%y, %H:%M:%S'
    )

    df.rename(columns={'message_date': 'data'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:

        entry = re.match(r'([^:]+):\s(.*)', message, re.DOTALL)

        if entry:
            users.append(entry.group(1))
            messages.append(entry.group(2))
        else:
            users.append('group notifications')
            messages.append(message)

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['data'].dt.year
    df['month'] = df['data'].dt.month_name()
    df['day'] = df['data'].dt.day
    df['hour'] = df['data'].dt.hour
    df['minute'] = df['data'].dt.minute
    df['second'] = df['data'].dt.second

    return df
