import requests
from .config import API_URL, HEADERS, MODEL, TIMEOUT

def call_siliconflow(system_prompt: str, user_question: str) -> str:
    """
    调用硅基流动 API，返回 AI 回答文本。
    如果发生网络或 API 错误，抛出异常。
    """
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_question},
        ],
    }
    response = requests.post(API_URL, headers=HEADERS, json=data, timeout=TIMEOUT)
    response.raise_for_status()  # 如果状态码不是 200，抛出 HTTPError
    result = response.json()
    # 提取回答
    answer = result["choices"][0]["message"]["content"]
    return answer