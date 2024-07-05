from urlextract import URLExtract
from wordcloud import WordCloud
extractor = URLExtract()


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_words = []
    num_messages = df.shape[0]
    num_media = df[df['message'] == '<Media omitted>\n'].shape[0]
    num_links = []
    for i in df['message']:
        num_links.extend(extractor.find_urls(i))
        num_words.extend(i.split())
    return num_messages, len(num_words), num_media, len(num_links)


def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df = round((df['user'].value_counts()/df.shape[0])*100).reset_index().rename(columns={'count': 'percent'})
    return x, new_df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc