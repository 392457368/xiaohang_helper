import os

# 1. 硅基流动基础配置
API_URL = "sk-orzelwpbyxqzxgqjggmoaoauzvltqauvwhwlmluawrhhetcv"
MODEL_NAME = "Qwen2.5-7B-Instruct"
# 填入自己的密钥
API_KEY = "sk-xxxxxx"

# 2. 读取data下四份md文件，拼接为知识库文本
def load_school_data():
    """加载四个Markdown知识库，拼接成完整文本"""
    data_folder = "data"
    full_content = ""
    md_list = ["01_新生入学.md", "02_教务办事.md", "03_后勤服务.md", "04_奖助资助.md"]
    for filename in md_list:
        file_path = os.path.join(data_folder, filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                full_content += f"\n====={filename}=====\n{f.read()}\n"
    return full_content

# 3. 根据身份切换对应System Prompt
def get_system_prompt(identity, school_data):
    # 全局别名+六条硬规则统一前缀
    base_rule = """【全局别名词典】
一卡通=校园卡；迎新系统=新生预报到平台；绩点=GPA；
绿色通道=贫困生入学帮扶通道；报修=后勤工单；
宿管中心=学生公寓管理处；教务处=教务科；资助中心=学生资助管理办公室

【强制6条防幻觉硬规则】
1. 知识库内无对应资料时，必须明确告知无收录，并统一给出咨询电话：0371-61911000，严禁编造答案。
2. 所有回答末尾必须标注引用来源MD文件名，格式为：【来源：xxx.md】。
3. 涉及金钱缴费、转账、收费类问题，必须附带防诈骗温馨提示，提醒谨防冒充辅导员、后勤人员的电信诈骗。
4. 收到轻生、心理危机类表述，立刻回复固定话术：请立刻拨打心理援助热线12320-5，同时联系本校心理咨询中心与辅导员进行紧急干预，不做多余安慰闲聊。
5. 任何身份用户查询他人成绩、学籍、隐私信息，统一礼貌拒绝：无法查询他人隐私数据，请本人登录校内系统自行查看。
6. 回答严格依据data目录四份Markdown知识库，禁止拓展校外政策、非本校规定、第三方机构代办业务内容。
"""
    if identity == "新生":
        prompt = f"""你是校园智能助手小航，服务对象为本科/研究生新生，回答风格详细全面，步骤拆解清晰。
{base_rule}
参考知识库：{school_data}
请结合新生场景，详细解答用户咨询。"""
    elif identity == "在校生":
        prompt = f"""你是校园智能助手小航，服务对象为在校老生，回答风格简洁凝练，重点标注地点、材料、办理时间、联系电话。
{base_rule}
参考知识库：{school_data}
请贴合在校生办事需求，精简给出办事关键信息。"""
    else: #教师
        prompt = f"""你是校园智能助手小航，服务对象为校内教职工教师，回答侧重政策依据、审批窗口、对接联系人、审批流程规范。
{base_rule}
参考知识库：{school_data}
面向教职工进行政策解读，明确审批对接部门与合规流程。"""
    return prompt

# 4. 调用硅基流动API函数
def ask_xiaohang(identity, question, school_data):
    import requests
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    sys_prompt = get_system_prompt(identity, school_data)
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3
    }
    resp = requests.post(API_URL, json=payload, headers=headers)
    if resp.status_code == 200:
        return resp.json()["choices"][0]["message"]["content"]
    else:
        return f"接口调用失败：{resp.status_code}"

# 5. 主交互入口
if __name__ == "__main__":
    # 加载知识库
    school_data = load_school_data()
    # 身份选择
    choice = input("输入编号：1新生 2在校生 3教师：")
    identity = {"1": "新生", "2": "在校生", "3": "教师"}.get(choice, "新生")
    question = input("你的问题：")
    answer = ask_xiaohang(identity, question, school_data)
    print(f"\n小航：{answer}")