# -*- coding: utf-8 -*-
import gradio as gr
import time

chatgpt_ui_css = """
/* --- Google Fonts --- */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500&display=swap');

/* --- CSS Variables (与主页完全统一) --- */
:root {
    --bg-color: #121212;
    --text-primary: #e8e8e8;
    --text-secondary: #a0a0a0;
    --accent-color: #c9b068;
    --border-color: rgba(255, 255, 255, 0.15);
    --container-bg: #1e1e1e;
}

/* --- 全局样式与Flex布局，实现输入框固定底部 --- */
.gradio-container {
    background-color: var(--bg-color);
    font-family: 'Noto Sans SC', sans-serif;
    display: flex;
    flex-direction: column;
    height: 100vh;
}
.contain {
    flex-grow: 1;
    overflow-y: auto; /* 让聊天内容区域可以滚动 */
    display: flex;
    flex-direction: column;
}

/* --- 欢迎界面样式 --- */
#welcome-container {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem;
}
#welcome-title {
    font-family: 'Noto Serif SC', serif;
    font-size: 2.5rem;
    color: var(--text-primary);
}
#welcome-subtitle {
    font-size: 1.1rem;
    color: var(--text-secondary);
    margin-bottom: 3rem;
}
#suggestion-row {
    gap: 1rem;
    justify-content: center;
}
#suggestion-row .gr-button {
    background-color: transparent !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-secondary) !important;
    transition: all 0.3s;
}
#suggestion-row .gr-button:hover {
    border-color: var(--accent-color) !important;
    color: var(--accent-color) !important;
    background-color: rgba(201, 176, 104, 0.05) !important;
}

/* --- 聊天内容区域 --- */
#chat-area {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem 1rem;
    flex-grow: 1;
}
#chatbot {
    background-color: transparent !important;
    box-shadow: none;
    border: none;
}
#chatbot .message-bubble {
    padding: 1rem !important;
    border-radius: 12px !important;
}
#chatbot .user .message-bubble {
    background-color: var(--bg-color) !important;
}
#chatbot .bot .message-bubble {
    background-color: var(--container-bg) !important;
}
#chatbot .message-bubble-text {
    font-size: 1rem !important;
    line-height: 1.7 !important;
    color: var(--text-primary) !important;
}
#chatbot [data-testid="bot"] > .avatar-container .avatar-name {
    color: var(--accent-color) !important;
    font-weight: 500;
}

/* --- 底部输入栏 --- */
#input-area-wrapper {
    width: 100%;
    background: var(--bg-color);
    padding: 1.5rem 0;
    border-top: 1px solid var(--border-color);
}
#input-area {
    max-width: 800px;
    margin: 0 auto;
    background: var(--container-bg);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 0.5rem;
    transition: border-color 0.3s;
}
#input-area:focus-within {
    border-color: var(--accent-color);
}
#input-textbox textarea {
    background-color: transparent !important;
    color: var(--text-primary) !important;
    border: none !important;
    box-shadow: none !important;
}
#submit-button {
    background: transparent !important;
    color: var(--text-secondary) !important;
    border: none !important;
    border-radius: 8px !important;
    transition: color 0.3s;
}
#submit-button:hover {
    color: var(--accent-color) !important;
}

/* 隐藏Gradio页脚 */
footer { display: none !important; }
"""

def create_chat_app():
    with gr.Blocks(theme=gr.themes.Base(), css=chatgpt_ui_css) as chat_interface:
        
        with gr.Column(visible=True, elem_id="welcome-container") as welcome_view:
            gr.Markdown("# 仡佬族数字文化博物馆", elem_id="welcome-title")
            gr.Markdown("我是AI守护者“仡言”，在此为您服务", elem_id="welcome-subtitle")
            with gr.Row(elem_id="suggestion-row"):
                suggestion_1 = gr.Button("介绍一下仡佬族的起源")
                suggestion_2 = gr.Button("仡佬族有什么特别的节日吗?")
                suggestion_3 = gr.Button("展示一些仡佬族的服饰")

        with gr.Column(visible=False, elem_id="chat-area") as chat_view:
            chatbot = gr.Chatbot(
                elem_id="chatbot",
                bubble_full_width=False,
                height=800,
                avatar_images=(None, "https://www.gstatic.com/lamda/images/sparkle_resting_v2_darkmode_230531.gif"),
                type="messages"
            )

        with gr.Column(elem_id="input-area-wrapper"):
            with gr.Row(elem_id="input-area"):
                msg_textbox = gr.Textbox(
                    elem_id="input-textbox",
                    placeholder="向“仡言”提问...",
                    show_label=False,
                    scale=7,
                    container=False
                )
                submit_btn = gr.Button(
                    "↑",
                    elem_id="submit-button",
                    scale=1
                )

        def respond(message, chat_history):
            chat_history.append({"role": "user", "content": message})
            bot_thinking_message = "正在从仡佬族文化知识库中为您查找答案..."
            chat_history.append({"role": "assistant", "content": bot_thinking_message})
            yield "", chat_history
            time.sleep(1.5)
            final_response = "找到了！仡佬族的三大宝是：**石、茶、药**。<br>![仡佬族石板房](https://img1.qunarzz.com/travel/d8/1709/8a/a5446006f14068b5.jpg_r_640x426x95_f1f87968.jpg)"
            chat_history[-1] = {"role": "assistant", "content": final_response}
            return "", chat_history

        def user_submit(message, history):
            return gr.update(visible=False), gr.update(visible=True), message, history

        def suggestion_click(suggestion_text, history):
            return gr.update(visible=False), gr.update(visible=True), suggestion_text, history

        msg_textbox.submit(user_submit, [msg_textbox, chatbot], [welcome_view, chat_view, msg_textbox, chatbot], queue=False).then(
            respond, [msg_textbox, chatbot], [msg_textbox, chatbot]
        )
        submit_btn.click(user_submit, [msg_textbox, chatbot], [welcome_view, chat_view, msg_textbox, chatbot], queue=False).then(
            respond, [msg_textbox, chatbot], [msg_textbox, chatbot]
        )

        suggestion_1.click(suggestion_click, [suggestion_1, chatbot], [welcome_view, chat_view, msg_textbox, chatbot], queue=False).then(
            respond, [msg_textbox, chatbot], [msg_textbox, chatbot]
        )
        suggestion_2.click(suggestion_click, [suggestion_2, chatbot], [welcome_view, chat_view, msg_textbox, chatbot], queue=False).then(
            respond, [msg_textbox, chatbot], [msg_textbox, chatbot]
        )
        suggestion_3.click(suggestion_click, [suggestion_3, chatbot], [welcome_view, chat_view, msg_textbox, chatbot], queue=False).then(
            respond, [msg_textbox, chatbot], [msg_textbox, chatbot]
        )
        
    return chat_interface

chat_app_instance = create_chat_app()