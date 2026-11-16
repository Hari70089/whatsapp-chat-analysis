import streamlit as st
import preprocesser
import helper
import matplotlib.pyplot as plt

st.sidebar.title('Whatsapp Chat Analysis')

uploaded_file = st.sidebar.file_uploader(
    "Upload your message",
    type=['txt']
)

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()

    data = bytes_data.decode('utf-8')

    df = preprocesser.preprocesser(data)

    st.dataframe(df)

    st.write("Total Messages:", df.shape[0])

    # fetch unique users

    user_list = df['user'].unique().tolist()
    if 'group notifications' in user_list:
        user_list.remove('group notifications')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox(
        "Show analytic user to:", user_list
    )

    if st.sidebar.button(" Show Analytic"):
        num_message, words, num_media_message, num_length = helper.fetch_stact(selected_user, df)
        st.title("Top Statics of Whatsapp Chat")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_message)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media share")
            st.title(num_media_message)

        with col4:
            st.header("Links Share")
            st.title(num_length)

    if selected_user == 'Overall':
        st.title("Most Busy User")
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='red')
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

    st.title("Most Common Words")
    most_common_df = helper.most_common_words(selected_user, df)
    st.dataframe(most_common_df)

    fig, ax = plt.subplots()

    ax.bar(most_common_df['word'], most_common_df['count'], color='red')
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)
