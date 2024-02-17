import streamlit as st
from streamlit_chat import message
import requests


def create_response(message):
    url = ""  # 実際のエンドポイントURLに置き換えてください
    data = {"message": message}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return "エラーが発生しました。管理者へお問い合わせください"


if 'history' not in st.session_state:
    st.session_state['history'] = [{"is_user": False,
                                    "message": "株式会社TechSeekerに関する自動応答です"}]


# This container will be used to display the chat history.
response_container = st.container()
# This container will be used to display the user's input and the response from the ChatOpenAI model.
container = st.container()
with container:
    with st.form(key='my_form', clear_on_submit=True):
        placeholder_message = "株式会社TechSeekerに関する質問を入力してください"
        user_input = st.text_input("Input:",
                                   placeholder=placeholder_message,
                                   key='input')
        submit_button = st.form_submit_button(label='Send')

    if submit_button and user_input:
        answer = create_response(user_input)
        st.session_state['history'].append({"is_user": True,
                                            "message": user_input})
        st.session_state['history'].append({"is_user": False,
                                            "message": answer})

if st.session_state['history']:
    with response_container:
        for i, value in enumerate(st.session_state['history']):
            if value["is_user"]:
                message(value["message"],
                        is_user=True,
                        key=str(i) + '_user')
            else:
                message(value["message"],
                        key=str(i),
                        avatar_style="thumbs")
