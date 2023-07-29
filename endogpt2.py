import os, sys, re
import streamlit as st
from streamlit_chat import message
import openai
from llama_index import StorageContext, load_index_from_storage

# メモリとchat_engine を st.session_state 保持する
if 'chat_engine' not in st.session_state:
    storage_context = StorageContext.from_defaults(persist_dir="./storage-kins")
    index = load_index_from_storage(storage_context)
    st.session_state.chat_engine = index.as_chat_engine(chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=False))

# 送信ボタンが押されたら問い合わせる
def do_question():
    question = st.session_state.question_input.strip()
    if question:
        #メッセージに質問を追加
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.question_input = ""

        #質問する
        text = str(st.session_state.chat_engine.chat(str(question)))
        response = re.sub(r'^\n','', text)
        #回答をメッセージに追加
        st.session_state.messages.append({'role': 'assistant', 'content': response})

def main():
    # セッションステートに messages リストを初期化する
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("endoGPT2 ver.0.1")
    st.markdown(
    """
     [@hortense667]((https://twitter.com/hortense667)) / 2023/07/29 『近代プログラマの夕』（1987～1995）や『先見日記』（2002～2005）などが読み込ませてあります。はげしく混乱することがあります。(c) 2023 Hortense S. Endo
    """
    )

    # messagesをループして、質問と回答を表示
    for msg in st.session_state.messages:
        if msg["role"] == "system":
            continue
        #右側に表示する回答はisUserをTrueとする。
        message((msg["content"]), is_user = msg["role"] == "assistant") 

    st.text_input("あなた", key="question_input")
    st.button("送信", on_click=do_question)

if __name__ == "__main__":
    main()  
