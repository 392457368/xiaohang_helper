# 郑州航空工业管理学院 人工智能专业认知实习教学课件 - 第6天：项目开发 + 异常处理 + Git 协作

> 适用对象：人工智能专业大一学生
> 实习日期：2026 年 7 月 15 日（周三）
> 实习地点：学校实训室
> 今日主题：项目开发 + 异常处理 + Git 协作

---

## 今日定位

前面大家已经完成了 Python 基础语法、AI 辅助编程工具实战、大模型与 Prompt 工程学习，并在昨天完成了「小航」郑州航院校园信息查询 AI 助手的需求分析、功能模块设计、三类用户身份梳理和数据文件准备。

---

## 今日学习目标 vs 最终成果

| # | 学习目标 | 对应最终成果 |
|---|---------------------|------------------------|
| 1 | 能够使用 Git 完成代码的初始化、添加、提交和查看记录 | Git 仓库 + 提交记录截图 |
| 2 | 能够用 Streamlit 搭建 Web 界面（标题、身份选择框、问题输入框、回答显示区） | `src/app.py` 界面部分 |
| 3 | 能够调用硅基流动 API 实现 AI 问答（requests.post，解析 choices[0].message.content） | API 调用代码 |
| 4 | 能够编写身份分流 Prompt + 别名词典 + 防幻觉规则 | `src/prompts.py` |
| 5 | 能够实现推荐问题按钮（12 个） | 推荐问题区代码 |
| 6 | 能够实现电话黄页静态页（API 挂了兜底） | 黄页静态页代码 |
| 7 | 能够处理 API 异常（超时、网络错误、Key 失效） | 异常处理代码 + 测试记录 |
| 8 | 能够全程使用 AI 辅助编程 + 多轮 Git 提交 | AI 使用记录 + Git 提交日志 |
| 9 | 能够创建 GitHub 远程仓库并推送代码 | GitHub 仓库链接 + 页面截图 |

---

## 今日主线任务

本节课的核心任务是：

> 完成「小航」AI 助手的核心功能开发，掌握 Git 基本操作，程序对 API 异常、网络异常、数据缺失等情况有友好提示。

---

## 第一部分：Git 入门与版本控制基础（建议 50 分钟）

### 1. 导入问题

先请大家思考一个问题：

**如果代码改坏了，怎么回到之前的版本？如果多人同时修改代码，怎么合并？**

- 场景 1：你改了一段 Prompt，运行报错了，想回到修改之前的版本，但已经不记得原来怎么写的了。
- 场景 2：你和小组成员各写了一个模块（界面/API 调用/Prompt），需要把代码合并到一起，手动复制粘贴容易出错。
- 场景 3：你想看看自己今天一共改了哪些文件、改了什么内容。

**Git** 就是解决这些问题的工具--它像游戏的"存档系统"，可以随时保存代码状态，随时回退。

### 2. Git 安装

> 如果机房已预装 Git，可跳过安装步骤，直接进入"环境检查"。

#### 安装步骤

**Windows 系统：**

1. 打开 Git 官网下载页面：https://git-scm.com/install/windows
2. 下载 Windows 版安装包（64-bit Git for Windows Setup）
3. 运行安装程序，一路 Next，保持默认选项即可
4. 安装完成后，打开终端（PowerShell 或 CMD），输入以下命令验证：

```bash
git --version
```

如果显示 `git version 2.x.x`，说明安装成功。

**常见安装问题：**

| 问题 | 原因 | 解决办法 |
|------|------|---------|
| `git` 不是内部或外部命令 | 安装后没重启终端 | 关闭终端重新打开，或重启电脑 |
| 安装时选项太多不知道怎么选 | Git 安装选项很多 | 保持默认，一路 Next 即可 |

> **课堂提醒**：安装 Git 和第 1 天安装 Python 一样，都是"装工具"的步骤。Git 安装好后不需要单独打开 Git 的图形界面，我们全程在终端/PowerShell 里用命令操作。

### 3. 核心讲解：Git 基本概念

**Git 三个区域：**

```text
工作区（写代码的地方）
    ↓ git add
暂存区（准备提交的文件）
    ↓ git commit
仓库（已保存的版本记录）
```

**Git 基本命令：**

| 命令 | 作用 | 类比 |
|------|------|------|
| `git init` | 初始化仓库 | 创建一个新存档 |
| `git add 文件名` | 把文件加入暂存区 | 标记要保存的进度 |
| `git add .` | 把所有修改加入暂存区 | 标记全部进度 |
| `git commit -m "说明"` | 提交到仓库 | 保存存档 |
| `git log` | 查看提交历史 | 查看存档列表 |
| `git status` | 查看当前状态 | 查看哪些文件改了还没存 |

### 4. 现场演示：创建项目仓库

```bash
# 1. 创建项目目录并进入
mkdir xiaohang_helper
cd xiaohang_helper

# 2. 创建工程化目录结构
mkdir -p src tests data docs

# 3. 创建 __init__.py 和占位文件
touch src/__init__.py tests/__init__.py
touch src/app.py src/prompts.py src/api.py src/config.py
touch .gitignore requirements.txt README.md

# 4. 初始化 Git 仓库
git init

# 5. 查看状态
git status

# 6. 添加文件到暂存区
git add .

# 7. 提交
git commit -m "项目初始化：创建工程化目录结构"

# 8. 查看提交记录
git log

# 9. 再次修改文件后
git add .
git commit -m "实现硅基流动 API 调用和身份分流 Prompt"
```

**提交信息规范：**

```text
好的提交信息：
- "项目初始化：添加数据文件和 Streamlit 框架"
- "实现硅基流动 API 调用和身份分流 Prompt"
- "添加推荐问题按钮和电话黄页静态页"
- "完善 API 异常处理"

不好的提交信息：
- "update"
- "改了一下"
- "aaa"
```

### 5. 项目目录结构

「小航」项目采用工程化目录结构，请大家统一命名：

```text
xiaohang_helper/
├── src/                    # 源代码目录
│   ├── __init__.py
│   ├── app.py              # Streamlit 主程序
│   ├── prompts.py          # Prompt 工程（身份分流、别名、防幻觉）
│   ├── api.py              # 硅基流动 API 调用
│   └── config.py           # 配置项（API_URL、API_KEY 等）
├── data/                   # 数据文件（Markdown）
│   ├── 01_新生入学.md
│   ├── 02_办事流程.md
│   ├── 03_电话黄页.md
│   └── 04_应急防骗.md
├── tests/                  # 测试用例
│   └── __init__.py
├── docs/                   # 文档
├── .gitignore
├── requirements.txt        # 依赖清单
└── README.md
```

> **说明**：`src/` 放代码，`data/` 放数据文件，`tests/` 放测试，`docs/` 放文档。层次不要太深，大一阶段够用就行。

> 注意：本项目**只用两样技术**--Prompt 工程 + AI API 调用，界面用 Streamlit 框架。不要写 CLI 菜单，不要用 input()，不要用 JSON/CSV 数据，数据全部是 Markdown 文件。

### 6. 小任务 1：创建项目仓库并完成首次提交

**任务目标：**
为「小航」项目创建 Git 仓库，并完成首次提交。

**执行方式：在 Git Bash 中复制以下命令执行**

> **注意**：以下命令使用 `touch` 和 `mkdir -p`，需要在 **Git Bash** 中执行（安装 Git 后右键 -> "Open Git Bash here"）。不要在 PowerShell 或 CMD 中执行。

```bash
# 1. 创建项目目录并进入
mkdir xiaohang_helper
cd xiaohang_helper

# 2. 创建工程化目录结构
mkdir -p src tests data docs

# 3. 创建 __init__.py 和占位文件
touch src/__init__.py tests/__init__.py
touch src/app.py src/prompts.py src/api.py src/config.py
touch .gitignore requirements.txt README.md

# 4. 将第 5 天准备的 4 个 Markdown 文件复制到 data/ 目录
# （手动复制，或用命令：cp ../data/*.md data/）

# 5. 初始化 Git 仓库
git init

# 6. 添加所有文件到暂存区
git add .

# 7. 首次提交
git commit -m "项目初始化：创建工程化目录结构和数据文件"

# 8. 查看提交记录
git log
```

**观察点：**

- 学生是否理解 init / add / commit 三步流程
- 学生是否写了有意义的提交信息
- 学生是否能查看提交历史
- 数据文件是否放在 `data/` 目录、后缀是否为 `.md`

---

## 第二部分：核心功能开发（建议 120 分钟）

### 1. 本部分目标

本部分重点解决：
- 如何用 Streamlit 搭建 Web 界面（标题、身份选择框、问题输入框、回答显示区）
- 如何调用硅基流动 API 实现 AI 问答
- 如何编写身份分流 Prompt + 别名词典 + 防幻觉规则
- 如何实现推荐问题按钮和电话黄页静态页

### 2. 核心认知：AI 应用的两个关键

记住今天最重要的一句话：

> **AI 应用 = 一段精心写的 Prompt + 一次 API 调用。**

- **Prompt 工程**：把学校资料、用户身份、防幻觉规则、别名词典，全部写进 system prompt 里。
- **API 调用**：用 `requests.post` 把 prompt 和用户问题发给硅基流动，拿回 AI 的回答。

不需要写复杂的查询逻辑、不需要 if-else 判断用户问什么--这些全交给大模型。

**从第 5 天到第 6 天的升级：**

第 5 天我们用 `input()`/`print()` 写了一个 CLI（命令行）版本的最小可运行代码，验证了 API 调用和身份分流 Prompt。今天我们把它升级为 **Streamlit Web 界面**版本：

| 对比项 | 第 5 天（CLI 版本） | 第 6 天（Web 版本） |
|--------|-------------------|-------------------|
| 界面 | `input()` + `print()` | Streamlit（st.title/selectbox/text_input） |
| 交互 | 命令行一问一答 | Web 页面，有按钮、选择框 |
| API 调用 | `requests.post` | 同（不变） |
| Prompt | 三套身份分流 + 6 条硬规则 | 同（不变） |
| 数据读取 | 逐个 `open()` 读 4 个文件 | `Path("data").glob("*.md")` 通配读取 |

> 核心逻辑（Prompt + API 调用）完全一样，只是界面从命令行升级为 Web 页面。

### 3. 数据文件格式参考

数据文件是 Markdown，放在 `data/` 目录（第 5 天已创建）。例如 `03_电话黄页.md`：

```markdown
# 03 电话黄页

## 应急电话（24 小时）
- 校园 110（保卫处）：0371-61916110 ⚠ 以官方为准
- 学校总值班室：0371-61911000 ⚠ 以官方为准
- 火警：119
- 急救：120

## 行政办公
- 后勤管理处：0371-61912800 ⚠ 以官方为准
- 后勤服务热线/物业报修：0371-61913110 ⚠ 以官方为准
- 校医院急诊（24h）：0371-61912730 ⚠ 以官方为准
- 招生办公室：0371-61916161 ⚠ 以官方为准
```

`load_school_info()` 会把 4 个 md 文件拼成一段大文本，注入到 system prompt 里。

> **与第 5 天的区别**：第 5 天的代码逐个 `open()` 读取 4 个文件名，今天改用 `Path("data").glob("*.md")` 通配符读取--这样即使后续新增 md 文件（如 `05_交通出行.md`）也不用改代码。

### 4. 模块一：Streamlit 界面搭建

**功能清单：**

| 功能编号 | 功能名称 | 说明 |
|---------|---------|------|
| 1.1 | 应用标题 | st.title 显示"小航 · 郑州航院校园信息助手" |
| 1.2 | 身份选择框 | st.selectbox 选择"新生/在校生/教师" |
| 1.3 | 问题输入框 | st.text_input 输入问题 |
| 1.4 | 回答显示区 | st.write 显示 AI 回答 |

**参考代码骨架（src/app.py 界面部分）：**

```python
import requests
import streamlit as st
from pathlib import Path
from src.prompts import load_school_info, get_system_prompt

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "your_siliconflow_key"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

st.title("小航 · 郑州航院校园信息助手")
role = st.selectbox("你是?", ["新生", "在校生", "教师"])
question = st.text_input("有啥想问的?")
```

**观察点：**

- 学生是否能用 `streamlit run src/app.py` 跑起界面
- selectbox 三个选项是否齐全
- text_input 是否能输入并拿到值

### 5. 模块二：硅基流动 API 调用

**功能清单：**

| 功能编号 | 功能名称 | 说明 |
|---------|---------|------|
| 2.1 | 发送请求 | requests.post 到硅基流动 |
| 2.2 | 解析回答 | 取 result["choices"][0]["message"]["content"] |
| 2.3 | 显示回答 | st.write 显示 |

**参考代码骨架（src/app.py 调用部分）：**

```python
if question:
    data = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "system", "content": get_system_prompt(role, load_school_info())},
            {"role": "user", "content": question},
        ],
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        st.write(answer)
    except requests.exceptions.Timeout:
        st.error("AI 响应超时，请稍后再试")
    except requests.exceptions.ConnectionError:
        st.error("网络连接失败，请检查网络")
    except Exception as e:
        st.error(f"发生错误：{e}")
```

> 关键点：API 地址必须是 `https://api.siliconflow.cn/v1/chat/completions`，model 用 `Qwen/Qwen2.5-7B-Instruct`。**不要用** open.bigmodel.cn、不要用 ZhipuAI SDK、不要用 glm-4-flash。

**观察点：**

- 学生是否填了正确的 API_URL 和 API_KEY
- 是否能正确解析 `choices[0].message.content`
- 是否给请求加了 timeout

### 6. 模块三：Prompt 工程实现

**功能清单：**

| 功能编号 | 功能名称 | 说明 |
|---------|---------|------|
| 3.1 | 读取 md 文件 | load_school_info 拼接 4 个 md |
| 3.2 | 身份分流 | 三套 ROLE_PROMPTS（新生/在校生/教师） |
| 3.3 | 别名词典 | ALIAS_DICT 处理"航院/郑航/ZUA"等同义词 |
| 3.4 | 防幻觉规则 | 硬规则：禁编电话/金额、转帐提示、心理危机处理 |

**参考代码骨架（src/prompts.py）：**

```python
from pathlib import Path

ROLE_PROMPTS = {
    "新生":   "你像热心的大二学长，语气详细、口语化、多给鼓励。涉及金钱/转账无条件提示『先联系辅导员核实』",
    "在校生": "你像办事老司机学长，语气简洁。优先给：① 地点 ② 电话 ③ 所需材料 ④ 办结时间",
    "教师":   "你面向教师，语气专业礼貌。优先给：① 政策依据 ② 办事窗口 ③ 联系人",
}

ALIAS_DICT = """
【同义词表】
- "学校" "航院" "ZUA" "郑航" ≈ 郑州航空工业管理学院
- "新校区" "龙湖" "新校" ≈ 龙子湖校区
- "卡" "饭卡" "校卡" ≈ 校园一卡通
- "保安" "门卫" "校警" ≈ 保卫处
- "迁户口" "落户" ≈ 户籍迁入/迁出
- "调宿舍" "换宿舍" ≈ 宿舍调整申请
- "证明" "在读证明" ≈ 在校学籍证明
"""


def load_school_info():
    """读取 data/ 目录下所有 md 文件，拼成大文本"""
    return "\n\n".join(
        f"=== {f.name} ===\n{f.read_text(encoding='utf-8')}"
        for f in sorted(Path("data").glob("*.md"))
    )


def get_system_prompt(role, info):
    """组装完整 system prompt：身份 + 别名 + 硬规则 + 学校资料"""
    return f"""你是郑州航院校园信息助手「小航」。
{ROLE_PROMPTS[role]}
{ALIAS_DICT}

【硬规则】
1. 只能根据下面【学校资料】回答，没有的明说"我没收录，建议拨打 0371-61911000 总值班室"
2. 严禁编造电话号码、地址、办公时间、学费金额、人名
3. 涉及金钱/转账无条件提示"先联系辅导员核实，任何要求转账的都是诈骗"
4. 涉及心理危机(自杀、不想活等)，立即给：12320-5 心理援助 + 学校心理咨询中心 + 告诉辅导员
5. 不接入学校系统(教务/一卡通/财务)，被问"查我的 XX"礼貌拒绝
6. 回答末尾标注 [来源:文件名]

【学校资料】
{info}
"""
```

> 这就是「小航」的大脑。整段 prompt 决定 AI 怎么说话、怎么避坑。**Prompt 写得好，AI 就不胡说。**

**观察点：**

- load_school_info 是否用 Path("data").glob("*.md")
- 三套 ROLE_PROMPTS 是否区分了语气
- ALIAS_DICT 是否覆盖常见别名
- 硬规则是否包含防幻觉、转账提示、心理危机

### 7. 模块四：推荐问题按钮

**功能清单：**

| 功能编号 | 功能名称 | 说明 |
|---------|---------|------|
| 4.1 | 12 个推荐问题按钮 | st.button，按身份分类 |
| 4.2 | 点击填入问题 | 点击后把问题填到输入框 |

**参考代码骨架：**

```python
PRESET_QUESTIONS = {
    "新生": [
        "报到那天先去哪?",
        "学费什么时候交?",
        "宿舍是 4 人间还是 6 人间?",
        "有人冒充辅导员要钱怎么办?",
    ],
    "在校生": [
        "怎么开在读证明?",
        "校园卡丢了怎么补?",
        "转专业怎么转?",
        "图书馆几点关?",
    ],
    "教师": [
        "差旅怎么报销?",
        "调课怎么申请?",
        "教室设备坏了找谁?",
        "科研项目去哪申报?",
    ],
}

st.markdown("**试试这些问题：**")
cols = st.columns(4)
questions = PRESET_QUESTIONS.get(role, [])
for i, q in enumerate(questions):
    with cols[i % 4]:
        if st.button(q, key=f"q_{i}"):
            st.session_state["question"] = q
            st.rerun()
```

> 12 个按钮按当前身份显示对应 4 个问题（第 5 天设计），用 `st.columns(4)` 排成 4 列。点击后把问题塞进 session_state 并 rerun，问题自动填进输入框。切换身份时按钮自动切换为对应身份的问题。

**观察点：**

- 按钮是否满 12 个
- 点击是否能填入问题
- 是否按身份分组

### 8. 模块五：电话黄页静态页（兜底）

**功能清单：**

| 功能编号 | 功能名称 | 说明 |
|---------|---------|------|
| 5.1 | 静态黄页展示 | st.markdown 直接展示电话黄页 |
| 5.2 | API 挂了兜底 | AI 不可用时，用户还能查电话 |

**参考代码骨架：**

```python
st.divider()
st.header("📞 电话黄页（静态兜底）")
st.caption("AI 答不上来时，可以直接查这里")

yellow_page = """| 部门 | 电话 |
|------|------|
| 校园 110（保卫处 24h） | 0371-61916110 ⚠ 以官方为准 |
| 学校总值班室 | 0371-61911000 ⚠ 以官方为准 |
| 后勤管理处 | 0371-61912800 ⚠ 以官方为准 |
| 后勤服务热线/物业报修 | 0371-61913110 ⚠ 以官方为准 |
| 校医院急诊（24h） | 0371-61912730 ⚠ 以官方为准 |
| 招生办公室 | 0371-61916161 ⚠ 以官方为准 |
| 信息管理中心（网信中心） | 0371-61912718 ⚠ 以官方为准 |
"""
st.markdown(yellow_page)
```

> 为什么要有静态页？AI 可能超时、Key 可能失效、网络可能断。电话黄页是**纯静态 Markdown**，不依赖 API，永远能看——这是兜底思维。

**观察点：**

- 黄页是否能直接渲染
- 是否独立于 API（不依赖网络）

### 9. AI 辅助开发建议

使用 AI 辅助开发时，建议的 Prompt：

```text
【角色】你是一个 Streamlit + 大模型 API 入门教学助教。
【背景】我是大一学生，正在开发「小航」郑州航院校园信息查询 AI 助手。
【技术栈】Streamlit 框架 + 硅基流动（SiliconFlow）API（requests 库），不用 ZhipuAI SDK。
【任务】请帮我完成【模块名称】模块的开发。
【API 规范】
- API_URL = "https://api.siliconflow.cn/v1/chat/completions"
- model = "Qwen/Qwen2.5-7B-Instruct"
- headers 带 Authorization: Bearer <key>
【要求】
1. 数据文件是 Markdown，放在 data/ 目录，用 Path("data").glob("*.md") 读取。
2. 身份分新生/在校生/教师三套 system prompt。
3. 核心代码控制在 30-50 行，强调"Prompt + 一次 API 调用"。
4. 异常用 try-except，超时/网络/Key 失效都要处理。
5. 代码尽量简单，适合大一学生理解。
6. 请给出完整代码。
```

### 10. 小任务 2：完成分配模块的功能开发

**任务目标：**
各小组完成负责模块的开发，并整合到 `src/app.py` 主程序。

**任务要求：**

1. 按分组分工，每组完成 1-2 个模块。
2. 使用 AI 辅助编程工具加速开发。
3. 确保模块可以独立测试（如 Prompt 模块可单独 print 验证）。
4. 将模块整合到 `src/app.py` 主程序。
5. 运行 `streamlit run src/app.py`，测试各功能。
6. 每完成一个模块，执行一次 Git 提交。

**Git 提交节奏建议：**

| 提交时机 | 提交信息示例 |
|---------|------------|
| 创建项目目录和数据文件后 | `项目初始化：创建工程化目录结构和数据文件` |
| 完成 API 调用 + 身份分流 Prompt 后 | `实现硅基流动 API 调用和身份分流 Prompt` |
| 完成推荐问题按钮 + 电话黄页后 | `添加推荐问题按钮和电话黄页静态页` |
| 完成异常处理后 | `完善 API 异常处理` |

---

## 第三部分：异常处理与 Git 协作实践（建议 70 分钟）

### 1. 本部分目标

本部分重点解决：
- 如何处理 API 调用超时
- 如何处理网络连接失败
- 如何处理 API Key 失效
- 如何处理数据文件缺失
- 如何在开发过程中持续使用 Git 管理代码

### 2. 常见异常场景与处理

**场景一：API 调用超时**

```python
# ❌ 没有处理的情况
response = requests.post(API_URL, headers=HEADERS, json=data)
# 网络慢，程序一直卡住，用户以为死机了

# ✅ 有处理的情况
try:
    response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)
except requests.exceptions.Timeout:
    st.error("AI 响应超时，请稍后再试")
```

**场景二：网络连接失败**

```python
# ❌ 没有处理的情况
response = requests.post(API_URL, headers=HEADERS, json=data)
# 断网时直接抛 ConnectionError，程序崩溃

# ✅ 有处理的情况
try:
    response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)
except requests.exceptions.ConnectionError:
    st.error("网络连接失败，请检查网络")
```

**场景三：API Key 失效或错误**

```python
# ❌ 没有处理的情况
result = response.json()
# Key 错了，response 里是 {"error": "invalid api key"}，取 choices 直接 KeyError

# ✅ 有处理的情况
response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)
if response.status_code == 401:
    st.error("API Key 失效，请联系老师重新获取")
elif response.status_code != 200:
    st.error(f"API 异常，状态码：{response.status_code}")
```

**场景四：数据文件缺失**

```python
# ❌ 没有处理的情况
info = load_school_info()
# data/ 目录没有 md 文件，info 是空字符串，AI 没资料可查

# ✅ 有处理的情况
files = list(Path("data").glob("*.md"))
if not files:
    st.warning("数据文件缺失，请联系老师补齐 data/ 目录下的 md 文件")
else:
    info = load_school_info()
```

**场景五：用户输入空问题**

```python
# ❌ 没有处理的情况
question = st.text_input("有啥想问的?")
# 用户没输入直接点，发了个空消息给 API，浪费调用

# ✅ 有处理的情况
question = st.text_input("有啥想问的?")
if question and question.strip():
    # 调用 API
    ...
elif question is not None:
    st.info("请输入你的问题")
```

**场景六：API 返回格式异常**

```python
# ❌ 没有处理的情况
answer = result["choices"][0]["message"]["content"]
# API 返回格式不对，KeyError 程序崩溃

# ✅ 有处理的情况
try:
    answer = result["choices"][0]["message"]["content"]
    st.write(answer)
except (KeyError, IndexError):
    st.error("AI 返回格式异常，请重试")
```

### 3. 综合异常处理示例

以下是在 `src/app.py` 中整合所有异常处理的完整示例（核心约 40 行）：

```python
import requests
import streamlit as st
from pathlib import Path
from src.prompts import load_school_info, get_system_prompt

API_URL = "https://api.siliconflow.cn/v1/chat/completions"
API_KEY = "your_siliconflow_key"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

st.title("小航 · 郑州航院校园信息助手")
role = st.selectbox("你是?", ["新生", "在校生", "教师"])
question = st.text_input("有啥想问的?")

if question and question.strip():
    files = list(Path("data").glob("*.md"))
    if not files:
        st.warning("数据文件缺失，请补齐 data/ 目录下的 md 文件")
    else:
        data = {
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "messages": [
                {"role": "system", "content": get_system_prompt(role, load_school_info())},
                {"role": "user", "content": question},
            ],
        }
        try:
            response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)
            if response.status_code == 401:
                st.error("API Key 失效，请联系老师重新获取")
            else:
                result = response.json()
                answer = result["choices"][0]["message"]["content"]
                st.write(answer)
        except requests.exceptions.Timeout:
            st.error("AI 响应超时，请稍后再试")
        except requests.exceptions.ConnectionError:
            st.error("网络连接失败，请检查网络")
        except (KeyError, IndexError):
            st.error("AI 返回格式异常，请重试")
        except Exception as e:
            st.error(f"发生错误：{e}")
```

> 这就是「小航」的核心。整段代码不到 40 行，但功能完整：界面 + API 调用 + Prompt + 异常处理。**这就是 AI 应用的精髓——简单但有防护。**

### 4. 测试用例设计

请为「小航」AI 助手设计以下测试：

| 测试编号 | 测试场景 | 输入内容 | 预期结果 | 实际结果 | 是否通过 |
|---------|---------|---------|---------|---------|---------|
| 1 | 身份切换为新生 | 选"新生" + 问"宿舍几人间" | 学长语气详细回答 | 【填写】 | 【是/否】 |
| 2 | 身份切换为教师 | 选"教师" + 问"科研报销" | 专业礼貌回答 | 【填写】 | 【是/否】 |
| 3 | 推荐按钮点击 | 点"保卫处电话是多少？" | 问题填入输入框 | 【填写】 | 【是/否】 |
| 4 | 空输入 | 不输入直接回车 | 提示"请输入你的问题" | 【填写】 | 【是/否】 |
| 5 | API 超时 | timeout=1 + 正常提问 | 提示超时稍后再试 | 【填写】 | 【是/否】 |
| 6 | 网络断开 | 断网后提问 | 提示网络连接失败 | 【填写】 | 【是/否】 |
| 7 | Key 失效 | 填错 API_KEY | 提示 Key 失效联系老师 | 【填写】 | 【是/否】 |
| 8 | 数据文件缺失 | 删除 data/ 下 md | 提示数据文件缺失 | 【填写】 | 【是/否】 |
| 9 | 电话黄页静态页 | 滚到底部 | 显示电话表格 | 【填写】 | 【是/否】 |
| 10 | 别名词典 | 问"ZUA 怎么走" | 识别为郑州航院 | 【填写】 | 【是/否】 |
| 11 | 防幻觉（编电话） | 问"校长电话" | 不编造，建议打总值班室 | 【填写】 | 【是/否】 |
| 12 | 转账提示 | 问"怎么交学费" | 提示先联系辅导员核实 | 【填写】 | 【是/否】 |

### 5. 小任务 3：完善异常处理并提交代码

**任务目标：**
为项目添加异常处理，完成测试，并进行多轮 Git 提交。

**任务要求：**

1. 为 API 调用添加超时、网络、Key 失效处理。
2. 为数据文件读取添加缺失检测。
3. 为用户空输入添加提示。
4. 完成 12 条测试用例，记录测试结果。
5. 每修复一类异常，执行一次 Git 提交。
6. 最终提交信息示例：`完善 API 异常处理`

**Git 提交节奏：**

| 提交时机 | 提交信息 |
|---------|---------|
| 添加 API 超时处理后 | `添加 API 超时处理` |
| 添加 Key 失效检测后 | `添加 API Key 失效检测` |
| 添加数据文件缺失检测后 | `添加数据文件缺失检测` |
| 完成全部测试后 | `完善 API 异常处理，通过全部测试` |

**观察点：**

- 学生是否给 requests.post 加了 timeout
- 学生是否检查了 response.status_code
- 学生是否实际运行测试，而不是只写代码
- 学生是否按节奏进行 Git 提交
- 学生是否能说出异常处理的作用

---

## 第四部分：GitHub 远程仓库与代码托管（建议 30 分钟）

### 1. 本部分目标

本部分重点解决：
- 如何在 GitHub 上创建远程仓库
- 如何将本地代码推送到 GitHub
- 如何提交作业（通过 GitHub 仓库链接）

### 2. 为什么用 GitHub？

> 大一同学没有自己的服务器，也没有 GitLab 账号。GitHub 是全球最大的代码托管平台，**免费、公开仓库无限、注册即用**。

- 代码备份：电脑坏了代码还在
- 作业提交：把仓库链接发给老师即可
- 展示作品：GitHub 主页就是你的编程简历

### 3. 注册 GitHub 账号

1. 打开 https://github.com
2. 点击 "Sign up"
3. 填写用户名（建议用拼音+数字，如 `zhangsan2026`）、邮箱、密码
4. 验证邮箱（去邮箱点确认链接）

> **课堂提醒**：用户名一旦确定不好改，建议用"姓名拼音+入学年"。密码要记好，后面天天用。

### 4. 创建远程仓库

1. 登录 GitHub，点击右上角 `+` -> "New repository"
2. 填写仓库信息：

| 选项 | 填写内容 |
|------|---------|
| Repository name | `xiaohang_helper` |
| Description | 郑州航院校园信息助手 - 大一认知实习项目 |
| Public / Private | 选 **Private**（私有）或 **Public**（公开均可，建议 Private） |
| Add a README | 不勾选（本地已有） |
| Add .gitignore | 不选（本地已有） |

3. 点击 "Create repository"

### 5. 关联本地仓库并推送

创建完仓库后，GitHub 会显示推送命令。在 **Git Bash** 中执行：

```bash
# 1. 进入项目目录（如果已经在则跳过）
cd xiaohang_helper

# 2. 关联远程仓库（把你的用户名替换进去）
git remote add origin https://github.com/你的用户名/xiaohang_helper.git

# 3. 推送到 GitHub
git push -u origin master
```

> **首次推送注意**：
> - 第一次 push 会弹出 GitHub 登录窗口，输入账号密码或 Token
> - GitHub 已不支持密码认证，需要用 **Personal Access Token**（设置方法见下方）
> - 如果报错 `fatal: remote origin already exists`，说明之前已关联过，用 `git remote remove origin` 删除后重新关联

### 6. 获取 Personal Access Token（PAT）

GitHub 推送代码需要 Token 认证，步骤如下：

1. 登录 GitHub -> 右上角头像 -> "Settings"
2. 左侧菜单最底部 -> "Developer settings"
3. 左侧 -> "Personal access tokens" -> "Tokens (classic)"
4. 点击 "Generate new token" -> "Generate new token (classic)"
5. 填写：
   - Note: `xiaohang`（随便写，标记用途）
   - Expiration: 选 30 天或 90 天
   - 勾选 `repo`（完整仓库权限）
6. 点击 "Generate token"
7. **立刻复制 Token**（关闭页面后看不到）

> 推送时密码栏填这个 Token，不是 GitHub 密码。

### 7. 验证推送成功

1. 刷新 GitHub 仓库页面
2. 能看到 `src/`、`data/`、`README.md` 等文件
3. 能看到提交记录

### 8. 后续提交流程

以后每次修改代码后，提交并推送的完整流程：

```bash
git add .
git commit -m "提交信息说明"
git push
```

> 第一次推送用了 `git push -u origin master`，之后再推送只需要 `git push` 三个字。

### 9. 小任务 4：创建 GitHub 仓库并推送代码

**任务目标：**
将本地「小航」项目推送到 GitHub 远程仓库。

**任务要求：**
1. 注册 GitHub 账号（已有可跳过）。
2. 创建名为 `xiaohang_helper` 的远程仓库。
3. 在本地关联远程仓库。
4. 执行 `git push -u origin master` 推送代码。
5. 截图 GitHub 仓库页面（显示文件列表和提交记录）。
6. 将仓库链接提交给老师。

**观察点：**

- 学生是否成功注册 GitHub
- 是否完成了首次 push
- GitHub 仓库是否能看到 src/ 和 data/ 目录
- 是否理解 local（本地）和 remote（远程）的区别

---

## 课堂任务结果整理

请整理并收集以下课堂成果：

| 成果名称 | 结果形式 | 是否必交 | 提交方式 | 备注 |
|---------|---------|---------|---------|------|
| Git 仓库 | 项目文件夹 + git log 截图 | 是 | GitHub 仓库链接 | 至少 3 次提交 |
| GitHub 远程仓库 | 仓库 URL + 页面截图 | 是 | 提交链接给老师 | 含完整代码和提交记录 |
| Streamlit 主程序 | `src/app.py` + 运行截图 | 是 | GitHub 仓库 / 班级群 | 含界面 + API 调用 |
| Prompt 工程模块 | `src/prompts.py` | 是 | 班级群 / 教学平台 / 文件夹 | 含身份分流 + 别名 + 防幻觉 |
| 数据文件 | `data/*.md`（4 个） | 是 | 班级群 / 教学平台 / 文件夹 | 新生/办事/黄页/应急 |
| 推荐问题按钮 | src/app.py 中代码段 | 是 | 班级群 / 教学平台 / 文件夹 | 12 个按钮 |
| 电话黄页静态页 | src/app.py 中代码段 | 是 | 班级群 / 教学平台 / 文件夹 | 兜底展示 |
| 异常处理代码 | 代码文件 + 测试记录 | 是 | 班级群 / 教学平台 / 文件夹 | 至少 12 条测试 |
| AI 辅助编程记录 | 文档 / 表格 | 是 | 按学校要求提交 | 记录 prompt 和 AI 输出 |
| 今日实习日志 | 文档 / 纸质记录 / 在线表单 | 是 | 按学校要求提交 | 写清收获、问题和协作体会 |
| 进阶功能尝试 | 代码 / 截图 | 否 | 自愿提交 | 可作为课堂加分项 |

### 验收重点

- `streamlit run src/app.py` 是否能跑起 Web 界面
- API 是否用硅基流动（不是智谱/GLM）
- 三类身份是否真的给出不同语气
- 推荐按钮是否满 12 个且能填入问题
- 电话黄页静态页是否独立于 API
- API 异常输入是否有友好提示
- Git 提交记录是否完整
- 是否成功推送到 GitHub
- 是否全程使用 AI 辅助编程
- 小组分工是否实际落地

---

## 今日总结与次日衔接

### 今日常见问题提醒

- 问题 1：Git 提交时忘记先 `git add`，导致修改没有被提交。
- 问题 2：API_KEY 写错或忘换行，导致 401 鉴权失败。
- 问题 3：API_URL 写成 open.bigmodel.cn 或用了 ZhipuAI SDK（**应该用硅基流动 api.siliconflow.cn**）。
- 问题 4：忘记给 requests.post 加 timeout，网络慢时程序卡死。
- 问题 5：数据 md 文件没放在 `data/` 目录，导致 load_school_info 读不到。
- 问题 6：Streamlit 没装，`streamlit run src/app.py` 报命令找不到（应 `pip install streamlit requests`）。
- 问题 7：异常处理只写了 try-except 但没给用户提示，用户不知道发生了什么。
- 问题 8：小组分工后有人完成快有人完成慢，整合时需要等待。
- 问题 9：GitHub push 报 403 或要求密码，是因为没配 Token（需生成 PAT，见第四部分）。
- 问题 10：`git push` 报 `fatal: 'origin' does not appear to be a git repository`，是没执行 `git remote add origin`。

### 次日衔接

- 下一天主题：项目调试优化 + 实习报告/论文撰写。
- 提前准备内容：保留今天的「小航」项目代码、测试记录和 Git 仓库。
- 今天成果中需要带入后续的部分：
  - 项目代码将用于明天的调试优化和数据补充。
  - Git 仓库将继续使用，明天的修改也会提交。
  - 今天的测试记录将帮助明天发现和修复更多问题。
  - 今天的 Prompt 工程经验将帮助明天优化 AI 回答质量。

---

## 附：课堂巡视问题清单

巡视时可优先询问以下问题：

1. 你的 Git 仓库创建了吗？目前有几次提交？
2. 你负责的是哪个模块？目前完成了哪些功能？
3. `streamlit run src/app.py` 能跑起来吗？界面显示了什么？
4. 你的 API 用的是硅基流动还是智谱？（必须是 api.siliconflow.cn）
5. API_URL 是什么？model 是什么？怎么解析 AI 回答？
6. 三套身份 prompt 区别在哪？切换身份后回答一样吗？
7. 推荐问题按钮有几个？点击能填入问题吗？
8. 电话黄页静态页依赖 API 吗？API 挂了还能看吗？
9. 如果 API 超时，你的程序会怎么处理？断网呢？Key 失效呢？
10. data/ 目录下的 md 文件读不到时，你的程序会报错还是给提示？
11. 你用 AI 辅助了哪些代码编写？AI 生成的代码你检查过吗？
12. 你的 Git 提交信息写的是什么？能看懂吗？
13. 小组内是怎么分工的？遇到问题怎么沟通？
14. 你的 GitHub 仓库创建了吗？代码推上去了吗？把链接发给我。
15. push 的时候报错了吗？是怎么解决的？

---

*课件名称：郑州航空工业管理学院人工智能专业认知实习第 6 天课件*
*适用范围：2026 年 7 月大一认知实习，认知 + 技术体验混合型*
*说明：本课件聚焦课堂教学、项目开发实操、异常处理、Git 协作、成果整理与感悟分享，不包含企业参观带队、接待流程和安全管理流程。*
