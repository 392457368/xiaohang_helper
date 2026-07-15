import sys
from pathlib import Path

# 确保项目根目录在 Python 搜索路径中（无论从哪个目录运行 streamlit run）
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
import streamlit as st
from src.prompts import load_school_info, get_system_prompt

# ---------- 配置 ----------
API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "sk-orzelwpbyxqzxgqjggmoaoauzvltqauvwhwlmluawrhhetcv"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ---------- 页面设置 ----------
st.set_page_config(page_title="小航 · 郑州航院校园信息助手", page_icon="🏫", layout="centered")

# ---------- 推荐问题库 ----------
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

# ---------- 初始化 session_state ----------
if "question" not in st.session_state:
    st.session_state["question"] = ""
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []

# ---------- 页面标题 ----------
st.title("🏫 小航 · 郑州航院校园信息助手")
st.caption("你的贴心校园 AI 问答助手 —— 有问题，找小航！")

# ---------- 身份选择 ----------
role = st.selectbox("👤 选择你的身份", ["新生", "在校生", "教师"])

# ---------- 推荐问题按钮 ----------
st.markdown("#### 💡 试试这些问题：")
cols = st.columns(4)
q_list = PRESET_QUESTIONS[role]

for idx, q in enumerate(q_list):
    with cols[idx % 4]:
        if st.button(q, key=f"preset_{idx}", use_container_width=True):
            st.session_state["question"] = q
            st.session_state["submitted"] = True
            st.rerun()

# ---------- 输入区域 + 发送按钮 ----------
st.markdown("#### ✍️ 输入你的问题：")
col_input, col_btn = st.columns([5, 1])
with col_input:
    question = st.text_input(
        "问题输入",
        value=st.session_state["question"],
        placeholder="例如：宿舍是几人间？怎么补办校园卡？",
        label_visibility="collapsed"
    )
with col_btn:
    submit_clicked = st.button("📤 提问", key="submit_btn", use_container_width=True)

should_query = submit_clicked or st.session_state.get("submitted", False)

# ---------- AI 问答逻辑 + 全量异常处理 ----------
if should_query:
    st.session_state["submitted"] = False

    if question and question.strip():
        md_files = list(Path("data").glob("*.md"))
        if not md_files:
            st.warning("⚠️ 数据文件缺失，请补齐 data/ 目录下的 md 文件")
        else:
            with st.spinner("🤔 小航正在思考中…"):
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
                    if resp.status_code == 401:
                        st.error("🔑 API Key 失效，请联系老师重新获取")
                    elif resp.status_code != 200:
                        st.error(f"⚠️ API 异常，状态码：{resp.status_code}")
                    else:
                        res_json = resp.json()
                        try:
                            ans = res_json["choices"][0]["message"]["content"]
                            st.session_state["history"].append({"role": "user", "content": question})
                            st.session_state["history"].append({"role": "assistant", "content": ans})
                            st.success("✅ 回答如下：")
                            st.write(ans)
                        except (KeyError, IndexError):
                            st.error("⚠️ AI 返回格式异常，请重试")
                except requests.exceptions.Timeout:
                    st.error("⏱️ AI 响应超时，请稍后再试")
                except requests.exceptions.ConnectionError:
                    st.error("🌐 网络连接失败，请检查网络后重试")
                except Exception as e:
                    st.error(f"❌ 发生未知错误：{e}")
    else:
        st.info("💬 请输入你要问的问题")

# ---------- 历史记录 ----------
if st.session_state["history"]:
    st.divider()
    with st.expander("📋 查看历史对话", expanded=False):
        for i, msg in enumerate(st.session_state["history"]):
            if msg["role"] == "user":
                st.markdown(f"**🧑 你：** {msg['content']}")
            else:
                st.markdown(f"**🤖 小航：** {msg['content']}")
                if i < len(st.session_state["history"]) - 1:
                    st.markdown("---")

# ---------- 电话黄页（静态兜底） ----------
st.divider()
with st.expander("📞 电话黄页（静态兜底）", expanded=False):
    st.caption("AI 无法响应时，可在此直接查阅常用电话")
    yellow_text = """
| 部门 | 电话 |
|------|------|
| 校园110（保卫处24h） | 0371-61916110 ⚠ 以官方为准 |
| 学校总值班室 | 0371-61911000 ⚠ 以官方为准 |
| 后勤管理处 | 0371-61912800 ⚠ 以官方为准 |
| 后勤报修热线 | 0371-61913110 ⚠ 以官方为准 |
| 校医院急诊（24h） | 0371-61912730 ⚠ 以官方为准 |
| 招生办公室 | 0371-61916161 ⚠ 以官方为准 |
"""
    st.markdown(yellow_text)