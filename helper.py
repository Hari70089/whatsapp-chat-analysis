from urlextract import URLExtract
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

extractor = URLExtract()


def fetch_stact(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(str(message).split())

    num_media_message = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(str(message)))

    return num_messages, len(words), num_media_message, len(links)


def most_busy_users(df):
    x = df['user'].value_counts().head()

    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df


def most_common_words(selected_user, df):
    f = open('stop_words.txt', 'r', encoding='utf-8')
    stop_words = set(f.read().split())
    f.close()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notifications']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in str(message).lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def plot_common_words(common_df):
    common_df = common_df.rename(columns={0: 'word', 1: 'count'})

    # chat formatting tokens and words from "This message was deleted" lines
    drop = {'-', '–', 'omitted>', '<sticker', 'deleted', 'message'}
    common_df = common_df[~common_df['word'].isin(drop)]
    common_df = common_df.sort_values('count', ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.bar(common_df['word'], common_df['count'], color='#e53935')
    ax.bar_label(bars, padding=3)
    ax.set_title('Most Common Words in Chat', fontsize=14)
    ax.set_xlabel('Word')
    ax.set_ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    plt.show()


# ---- usage ----
# df must already have 'user' and 'message' columns from your chat-parsing code
selected_user = 'Overall'
df = ...  # replace with your preprocessed DataFrame

common_df = most_common_words(selected_user, df)
plot_common_words(common_df)
