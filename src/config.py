# 硅基流动 API 配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-orzelwpbyxqzxgqjggmoaoauzvltqauvwhwlmluawrhhetcv"  # 请替换为你的实际 API Key

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 模型配置
MODEL = "zai-org/GLM-5.2"

# 超时时间（秒）
TIMEOUT = 30