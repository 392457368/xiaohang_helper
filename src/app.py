import sys
from pathlib import Path

# 确保项目根目录在 Python 搜索路径中（无论从哪个目录运行 streamlit run）
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import streamlit as st
from src.prompts import load_school_info, get_system_prompt

# 配置
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-orzelwpbyxqzxgqjggmoaoauzvltqauvwhwlmluawrhhetcv"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 页面标题
st.title("小航 · 郑州航院校园信息助手")

# 身份选择
role = st.selectbox("你是?", ["新生", "在校生", "教师"])

# 推荐问题库
PRESET_QUESTIONS = {
    "新生": [
        "报到那天先去哪?",
        "学费什么时候交?",
        "宿舍是4人间还是6人间?",
        "有人冒充辅导员要钱怎么办?"
    ],
    "在校生": [
        "怎么开在读证明?",
        "校园卡丢了怎么补?",
        "转专业怎么转?",
        "图书馆几点关?"
    ],
    "教师": [
        "差旅怎么报销?",
        "调课怎么申请?",
        "教室设备坏了找谁?",
        "科研项目去哪申报?"
    ]
}

# 推荐按钮区域
st.markdown("**试试这些问题:**")
cols = st.columns(4)
q_list = PRESET_QUESTIONS[role]
if "question" not in st.session_state:
    st.session_state["question"] = ""

for idx, q in enumerate(q_list):
    with cols[idx % 4]:
        if st.button(q, key=f"q{idx}"):
            st.session_state["question"] = q
            st.rerun()

# 问题输入框
question = st.text_input("有啥想问的?", value=st.session_state["question"])

# 静态电话黄页兜底
st.divider()
st.header("📞 电话黄页(静态兜底)")
yellow_text = """
| 部门 | 电话 |
|------|------|
| 校园110(保卫处24h) | 0371-61916110 ⚠ 以官方为准 |
| 学校总值班室 | 0371-61911000 ⚠ 以官方为准 |
| 后勤管理处 | 0371-61912800 ⚠ 以官方为准 |
| 后勤报修热线 | 0371-61913110 ⚠ 以官方为准 |
| 校医院急诊(24h) | 0371-61912730 ⚠ 以官方为准 |
| 招生办公室 | 0371-61916161 ⚠ 以官方为准 |
"""
st.markdown(yellow_text)

# AI问答逻辑+全量异常处理
if question and question.strip():
    md_files = list(Path("data").glob("*.md"))
    if not md_files:
        st.warning("数据文件缺失，请补齐data目录下md文件")
    else:
        sys_prompt = get_system_prompt(role, load_school_info())
        req_data = {
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "messages": [
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": question}
            ]
        }
        try:
            resp = requests.post(API_URL, headers=HEADERS, json=req_data, timeout=30)
            # key失效鉴权错误
            if resp.status_code == 401:
                st.error("API Key失效，请联系老师重新获取")
            elif resp.status_code != 200:
                st.error(f"API异常，状态码：{resp.status_code}")
            else:
                res_json = resp.json()
                try:
                    ans = res_json["choices"][0]["message"]["content"]
                    st.write("### AI回答：")
                    st.write(ans)
                except (KeyError, IndexError):
                    st.error("AI返回格式异常，请重试")
        except requests.exceptions.Timeout:
            st.error("AI响应超时，请稍后再试")
        except requests.exceptions.ConnectionError:
            st.error("网络连接失败，请检查网络")
        except Exception as e:
            st.error(f"发生未知错误：{e}")
elif question is not None and question.strip() == "":
    st.info("请输入你的问题")