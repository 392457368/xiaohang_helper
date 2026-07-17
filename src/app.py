import sys
from pathlib import Path

# 确保项目根目录在 Python 搜索路径中（无论从哪个目录运行 streamlit run）
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
import time

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

# ---------- 电话精准匹配（不经过 AI，100% 准确） ----------
PHONE_DB = {
    "校园110 / 保卫处（24小时）": {
        "phone": "0371-61916110",
        "keywords": ["校园110", "保卫处", "保安", "门卫", "校警", "报警", "110", "安全", "治安"],
    },
    "学校总值班室": {
        "phone": "0371-61911000",
        "keywords": ["总值班室", "值班室", "总值班", "值班"],
    },
    "后勤管理处": {
        "phone": "0371-61912800",
        "keywords": ["后勤管理处", "后勤管理", "后勤处"],
    },
    "后勤报修热线": {
        "phone": "0371-61913110",
        "keywords": ["后勤报修", "报修", "维修", "修东西", "水管", "灯泡", "空调坏", "门锁坏", "厕所堵", "马桶"],
    },
    "校医院急诊（24小时）": {
        "phone": "0371-61912730",
        "keywords": ["校医院", "急诊", "看病", "医生", "医务室", "医院", "生病", "发烧", "受伤"],
    },
    "招生办公室": {
        "phone": "0371-61916161",
        "keywords": ["招生办", "招生办公室", "招生", "录取", "报考", "咨询招生"],
    },
}

def match_phone(question: str):
    """匹配电话问题，返回 (部门名, 号码) 或 None"""
    q = question.lower().replace(" ", "")
    for dept, info in PHONE_DB.items():
        for kw in info["keywords"]:
            if kw in q:
                return dept, info["phone"]
    return None

# ---------- 页面设置 ----------
st.set_page_config(page_title="小航 · 郑州航院校园信息助手", page_icon="🏫", layout="centered")

# ---------- 推荐问题库（按类别） ----------
PRESET_QUESTIONS = {
    "新生指南": [
        "报到那天先去哪?",
        "学费什么时候交?",
        "宿舍是4人间还是6人间?",
        "军训准备啥?",
        "从火车站怎么到学校?",
    ],
    "办事流程": [
        "怎么开在读证明?",
        "校园卡丢了怎么补?",
        "转专业怎么转?",
        "图书馆几点关?",
        "补办校园卡流程",
    ],
    "应急防骗": [
        "有人冒充辅导员要钱怎么办?",
        "校园贷怎么识别?",
        "丢失物品去哪报备?",
        "遇到电信诈骗报警渠道",
    ],
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

# ---------- 推荐问题标签页 ----------
st.markdown("#### 💡 试试这些问题：")
tab_names = list(PRESET_QUESTIONS.keys())
tabs = st.tabs(tab_names)

for tab, name in zip(tabs, tab_names):
    with tab:
        cols = st.columns(2)
        for idx, q in enumerate(PRESET_QUESTIONS[name]):
            with cols[idx % 2]:
                if st.button(q, key=f"tab_{name}_{idx}", use_container_width=True):
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
        t0 = time.time()
        # ---------- 第一步：电话精准匹配（不走 AI，100% 准确） ----------
        phone_match = match_phone(question)
        if phone_match:
            dept, phone = phone_match
            ans = f"📞 **{dept}**\n\n电话：**{phone}**\n\n> ⚠ 以官方最新公布为准"
            now = datetime.now().strftime("%H:%M:%S")
            elapsed = time.time() - t0
            st.session_state["history"].insert(0, {
                "role": role, "question": question, "answer": ans, "time": now
            })
            st.success("✅ 回答如下：")
            st.write(ans)
            st.caption(f"回答字数：{len(ans)} 字 · 耗时：{elapsed:.1f} 秒")
        else:
            # ---------- 第二步：非电话问题走 AI ----------
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
                                now = datetime.now().strftime("%H:%M:%S")
                                elapsed = time.time() - t0
                                st.session_state["history"].insert(0, {
                                    "role": role, "question": question, "answer": ans, "time": now
                                })
                                st.success("✅ 回答如下：")
                                st.write(ans)
                                st.caption(f"回答字数：{len(ans)} 字 · 耗时：{elapsed:.1f} 秒")
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
    with st.expander(f"📋 历史记录（{len(st.session_state['history'])} 条）", expanded=False):
        col_clear = st.columns([5, 1])[1]
        with col_clear:
            if st.button("🗑 清空全部", key="clear_all", use_container_width=True):
                st.session_state["history"] = []
                st.rerun()

        for idx, record in enumerate(st.session_state["history"]):
            with st.container(border=True):
                c1, c2 = st.columns([20, 1])
                with c1:
                    st.caption(f"🕒 [{record['time']}] **{record['role']}** 提问：{record['question']}")
                    st.markdown(record["answer"])
                with c2:
                    if st.button("✕", key=f"del_{idx}", help="删除此条"):
                        st.session_state["history"].pop(idx)
                        st.rerun()

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