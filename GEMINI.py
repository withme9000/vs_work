from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai
import os

# GEMINI(Google AI Studio) 무료 Token이 있어서 가능
# 서버실행(로컬만가능) uvicorn GEMINI:app --reload
# 서버실행(외부접속가능) uvicorn GEMINI:app --reload --host 0.0.0.0 --port 8000

GEMINI_API_KEY = "AIzaSyAB9csGaPCcv-1t1shG5TyOz-JqRLaTU7c"  # GEMINI API 키를 여기에 입력하세요

app = FastAPI()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


# 요청 모델
class ChatRequest(BaseModel):
    question: str


# 👉 GEMINI API
@app.post("/chat")
def chat(req: ChatRequest):
    response = model.generate_content(req.question)
    answer = response.text
    return {"answer": answer}


# 👉 웹페이지
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MCP Chat</title>
    </head>
    <body>
        <h2>GEMINI 질문</h2>

        <input type="text" id="question" style="width:300px;">
        <button onclick="ask()">질문하기</button>

        <p id="answer"></p>

        <script>
        async function ask() {
            const question = document.getElementById("question").value;

            const res = await fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question })
            });

            const data = await res.json();
            document.getElementById("answer").innerText = data.answer;
        }
        </script>
    </body>
    </html>
    """