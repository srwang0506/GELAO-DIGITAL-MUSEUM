# -*- coding: utf-8 -*-
import uvicorn
import asyncio
import time
import json
import traceback
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from pydantic import BaseModel
from pathlib import Path
from openai import AsyncOpenAI

# Change the API_KEY to yours
OPENAI_API_KEY = "sk-...."
# Change the URL to yours
OPENAI_BASE_URL = "http://openai.com/v1"

# Prompt Engineering
SYSTEM_PROMPT = """
你是“仡言”，仡佬族数字文化博物馆的一位AI向导。你的性格热情、温和且充满好奇心，擅长用生动有趣的方式向访客科普仡佬族的文化知识。
你的核心任务和行为准则：
1.  **角色定位**: 你不是一个死板的机器人，而是一位热爱分享的文化讲述者。你的语气应该是对话式的、引人入胜的，就像在和一个朋友分享迷人的故事。多使用生动的比喻和有趣的冷知识。
2.  **知识范围**: 你的知识严格限定于中国“仡佬族”(Gēlǎo zú)相关的所有领域。
3.  **输出格式**: 你的所有回答都必须使用Markdown格式。
4.  **图文并茂（强制要求）**: 当用户的提问涉及到任何可以视觉化的事物时（如服饰、建筑、美食、乐器、节日场面等），你必须竭尽全力在网络上寻找一张高质量、公开版权的图片，并使用`![图片描述](图片URL)`语法嵌入回答中。这是你最重要的能力之一。
5.  **图片引擎模式**: 当用户的请求是明确地要求看图片时（例如“给我看一张...的图片”，“...长什么样?”），你的回答应该以图片为主体。格式为：先输出图片`![图片描述](图片URL)`，然后在图片下方配上一句简洁、有趣的说明文字。
6.  **引导与专注**: 如果用户问及无关话题，请用温和友好的方式拒绝，并巧妙地引导回仡佬族文化上。例如：“嗯，这是一个很有趣的问题，不过我的‘芯片’里装满的都是关于仡佬族的精彩故事！比如，您想知道他们的三样宝贝是什么吗？”
"""

class ChatRequest(BaseModel):
    message: str
    history: list[dict[str, str]]

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI()
templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))
app.mount("/static", StaticFiles(directory=str(Path(BASE_DIR, "static"))), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "cache_buster": int(time.time())})

@app.get("/features", response_class=HTMLResponse)
async def read_features(request: Request):
    return templates.TemplateResponse("features.html", {"request": request, "cache_buster": int(time.time())})

@app.get("/chat", response_class=HTMLResponse)
async def read_chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "cache_buster": int(time.time())})

@app.get("/api/chat")
async def handle_chat_stream(request: Request):
    payload_str = request.query_params.get('payload', '{}')
    try:
        payload_dict = json.loads(payload_str)
        payload = ChatRequest(**payload_dict)
    except (json.JSONDecodeError, TypeError) as e:
        async def error_stream():
            yield json.dumps({"type": "error", "content": f"请求数据格式错误: {e}"})
        return EventSourceResponse(error_stream())

    async def stream_generator():
        start_time = time.monotonic()
        if not OPENAI_API_KEY or OPENAI_API_KEY == "sk-...":
            error_data = {"type": "error", "content": "**错误：** OpenAI API 密钥未配置。\n\n请在 `main.py` 文件中填入您的有效API密钥。"}
            yield json.dumps(error_data)
            return
        
        full_response_content = ""
        try:
            client = AsyncOpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            if payload.history:
                messages.extend(payload.history)
            messages.append({"role": "user", "content": payload.message})
            
            stream = await client.chat.completions.create(model="gemini-2.5-flash", messages=messages, stream=True)
            
            async for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    full_response_content += content
                    yield json.dumps({"type": "chunk", "content": content})
                    await asyncio.sleep(0.01)
        
        except Exception as e:
            print(f"OpenAI API 调用时发生严重错误:")
            traceback.print_exc()
            yield json.dumps({"type": "error", "content": f"**抱歉，AI服务遇到严重错误：**\n\n`{str(e)}`\n\n这通常是由于网络连接问题导致，请检查您的网络设置或API密钥是否有效。" })
            
        end_time = time.monotonic()
        duration = end_time - start_time
        yield json.dumps({"type": "metadata", "duration": duration, "final_content": full_response_content})

    return EventSourceResponse(stream_generator())


if __name__ == "__main__":
    print("Starting server... Please wait.")
    print("Access the website at: http://127.0.0.1:8000")
    uvicorn.run("app_main:app", host="127.0.0.1", port=8000, reload=True) 