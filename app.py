from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# 비동기 클라이언트 객체 생성
aclient = AsyncOpenAI(api_key=config['API']['KEY'])

# FastAPI 객체 생성
app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서의 요청 허용
    allow_credentials=True,  # 쿠키 등 자격 증명을 포함한 요청 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더를 포함한 요청 허용
)


# /chat 경로로 요청이 들어올 떄, 실행되는 함수
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()  # 클라이언트로부터 받은 요청의 본문을 JSON으로 비동기적으로 읽음
    user_message = data.get("message")  # JSON에서 message 키에 해당하는 값을 추출
    response = await generate_response(user_message)
    return {"response": response}


# chat gpt 3.5-turbo로 부터 답변 받아오기
async def generate_response(user_message: str) -> str:
    response = await aclient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Data Scientist Sanghyun and scheduling for studying data science."},
            {"role": "user", "content": user_message}
        ])
    print(response.choices[0].message.content)
    return response.choices[0].message.content

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)