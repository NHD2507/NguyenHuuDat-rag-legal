# src/generator.py

import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv(".env")

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

PROMPT = """
Bạn là trợ lý pháp luật.

Chỉ trả lời dựa trên CONTEXT.

Nếu CONTEXT không chứa đủ thông tin để trả lời,
hãy trả lời chính xác:

"Không có thông tin trong tài liệu."

CONTEXT:
{context}

QUESTION:
{question}
"""


def generate_answer(question, context):

    prompt = PROMPT.format(
        context=context,
        question=question,
    )

    response = model.generate_content(
        prompt
    )

    return response.text