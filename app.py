# 以下を「app.py」に書き込み
import streamlit as st
import openai



# パスワードを設定
correct_password = st.secrets.mieai_pw.correct_password

# パスワードの入力フィールドを追加
password = st.text_input("パスワードを入力してください", type="password")

# パスワードが正しい場合の処理
if password == correct_password:

    openai.api_key = st.secrets.OpenAIAPI.openai_api_key
    
    system_prompt = """
    あなたは優秀な人の悩みを解決するコーチです。
    悩みに対して質問を行ったりして深堀も行ってください。
    様々な手法やアドバイスで相談者の悩みの解決方法を提案することができます。
    あなたの役割はコーチングを行うことなので、例えば以下のような悩み以外ことを聞かれても、絶対に答えないでください。
    
    * 芸能人
    * 料理
    * 科学
    * 歴史
    """
    
    # st.session_stateを使いメッセージのやりとりを保存
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", "content": system_prompt}
            ]
    
    # チャットボットとやりとりする関数
    def communicate():
        messages = st.session_state["messages"]
    
        user_message = {"role": "user", "content": st.session_state["user_input"]}
        messages.append(user_message)
    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
    
        bot_message = response["choices"][0]["message"]
        messages.append(bot_message)
    
        st.session_state["user_input"] = ""  # 入力欄を消去
    
    
    # ユーザーインターフェイスの構築
    st.title("「みえAi」コーチングボット")
    st.image("mieai.png")
    st.write("悩み事は何ですか？")
    
    user_input = st.text_input("悩み事を下に入力してください。", key="user_input", on_change=communicate)
    
    if st.session_state["messages"]:
        messages = st.session_state["messages"]
    
        for message in reversed(messages[1:]):  # 直近のメッセージを上に
            speaker = "🙂"
            if message["role"]=="assistant":
                speaker="🤖"
    
            st.write(speaker + ": " + message["content"])

    import csv
    
    # 会話ログをCSVファイルに保存する関数
    def save_conversation_to_csv(conversation, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Role", "Message"])  # ヘッダー行を書き込む
            for message in conversation:
                writer.writerow([message["role"], message["content"]])
    
    # 会話ログを取得
    if st.session_state["messages"]:
        messages = st.session_state["messages"]
    
    # CSVファイルに保存
    # カスタマイズされた保存場所
    save_path = '"C:\Users\yumem\OneDrive\デスクトップ\mieai\mieai.csv"'
    save_conversation_to_csv(messages[1:], save_path)



else:
    # パスワードが間違っている場合のメッセージを表示
    st.write("パスワードが正しくありません。アプリにアクセスするために正しいパスワードを入力してください。")
