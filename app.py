import streamlit as st
from jinja2 import Template

# 设置网页标题
st.title("上币信息自动化输出系统")
st.caption("运营只需输入一次变量，即可同时渲染内部与外部多套模版")

# ----------------- 🏢 模版定义 -----------------

# 模版 1：内部同步信息模版
INTERNAL_TEMPLATE = """【项目上线通知】

{{ project_name }} ({{ ticker }}) {{ lst_type_sub }}上币
1.1基础信息： 

- 代币全称：{{ project_name }}
- Ticker：{{ ticker }}
- 费率标准：{{ fee_level }}
- 代币类型：{{ network }}
- 上币母类型：{{ lst_type_main }}
- 上币子类型：{{ lst_type_sub }}
- 运营评级：{{ op_level }}
- 官网：{{ website }}

1.2项目情况：
{{ project_intro }}

2.时间线
- 上币公告/充值：{{ ann_time }}
- 交易：{{ trading_time }}
- 提现： {{ withdraw_time }}

3.市场宣发预算 ({{ budget_amount }} {{ ticker }}),参考价 {{ price }}

{{ marketing_budget_section }}"""

# 模版 2：外部宣发/官方公告模版
PUBLIC_ANNOUNCEMENT_TEMPLATE = """📣 官方首发 | 平台即将上线 {{ project_name }} ({{ ticker }})！

尊贵的全球用户：
平台非常高兴地宣布，我们将支持 {{ project_name }} ({{ ticker }}) 在现货交易市场上线！具体安排如下：

📅 上线时间线：
1. 充值开放时间：{{ ann_time }}
2. 现货交易开启：{{ trading_time }}
3. 提现开放时间：{{ withdraw_time }}

💡 项目简介：
{{ project_intro }}

🎁 丰富上线活动同步开启！
本次上线包含以下福利赛道，总奖池高达 {{ budget_amount }} {{ ticker }}：
{{ marketing_budget_section }}

风险提示：数字资产是创新型投资产品，价格波动较大，请理性判断自己的投资能力，谨慎做出投资决策。
平台团队
"""

# ----------------- 📋 左侧边栏：统一输入源 -----------------
st.sidebar.header("📋 请输入项目变量")

st.sidebar.subheader("基本信息")
p_name = st.sidebar.text_input("项目全称 (project_name)", value="")
p_ticker = st.sidebar.text_input("代币符号 (ticker)", value="")
p_website = st.sidebar.text_input("官方网站 (website)", value="")
p_network = st.sidebar.text_input("代币类型/主网 (network)", value="")
p_fee_level = st.sidebar.text_input("费率标准 (fee_level)", value="")
p_op_level = st.sidebar.text_input("运营评级 (op_level)", value="")

st.sidebar.subheader("上币类型")
p_lst_type_main = st.sidebar.text_input("上币母类型 (lst_type_main)", value="现货")
p_lst_type_sub = st.sidebar.text_input("上币子类型 (lst_type_sub)", value="常规")

st.sidebar.subheader("项目简介")
p_intro = st.sidebar.text_area("项目简介 (project_intro)", value="")

st.sidebar.subheader("时间线")
p_ann_time = st.sidebar.text_input("上币公告/充值时间 (ann_time)", value="TBD")
p_trading_time = st.sidebar.text_input("交易时间 (trading_time)", value="TBD")
p_withdraw_time = st.sidebar.text_input("提现时间 (withdraw_time)", value="TBD")

st.sidebar.subheader("预算与价格")
p_budget_amount = st.sidebar.number_input("总预算数量 (budget_amount)", min_value=0.0, value=0.0, step=1000.0)
p_price = st.sidebar.text_input("参考价 (price)", value="")

# 📊 动态预算分配
st.sidebar.subheader("📊 动态预算分配")
default_activities = "GemSlot, Learn2Earn, TG AMA/ X-Space, Twitter Giveaway, Telegram Quiz"
activity_input = st.sidebar.text_area("💡 动态修改活动类型：", value=default_activities)
activity_list = [act.strip() for act in activity_input.replace("，", ",").split(",") if act.strip()]

activity_ratios = {}
total_pct = 0

if activity_list:
    st.sidebar.caption("请为各活动分配比例 (%)")
    for act in activity_list:
        ratio = st.sidebar.number_input(f"🔸 {act} (%)", min_value=0, max_value=100, value=0, key=f"act_{act}")
        activity_ratios[act] = ratio
        total_pct += ratio

    if total_pct != 100 and p_budget_amount > 0:
        st.sidebar.warning(f"⚠️ 当前分配总和为 {total_pct}%，不等于 100%！")

# ----------------- 🚀 右侧主展示区：一键多发 -----------------

# 点击按钮生成
if st.sidebar.button("✨ 一键生成双端内容", type="primary"):
    
    # 1. 动态生成活动预算文本段落
    budget_lines = []
    for act, pct in activity_ratios.items():
        if pct > 0 and p_budget_amount > 0:
            calc_val = int(p_budget_amount * pct / 100)
            budget_lines.append(f"- {act}：{calc_val:,}")
        else:
            budget_lines.append(f"- {act}：")
            
    marketing_budget_section = "\n".join(budget_lines)
    formatted_budget = f"{int(p_budget_amount):,}" if p_budget_amount.is_integer() else f"{p_budget_amount:,.2f}"

    # 2. 组装公用数据包
    data = {
        "project_name": p_name,
        "ticker": p_ticker,
        "fee_level": p_fee_level,
        "network": p_network,
        "lst_type_main": p_lst_type_main,
        "lst_type_sub": p_lst_type_sub,
        "op_level": p_op_level,
        "website": p_website,
        "project_intro": p_intro,
        "ann_time": p_ann_time,
        "trading_time": p_trading_time,
        "withdraw_time": p_withdraw_time,
        "budget_amount": formatted_budget, 
        "price": p_price,
        "marketing_budget_section": marketing_budget_section
    }
    
    # 3. 分别渲染两套模版
    rendered_internal = Template(INTERNAL_TEMPLATE).render(data)
    rendered_public = Template(PUBLIC_ANNOUNCEMENT_TEMPLATE).render(data)
    
    # 4. 利用 Streamlit 的 Tabs 标签页优雅地并排展示
    st.write("### 🖨️ 自动化内容输出成功！")
    tab1, tab2 = st.tabs(["🏢 内部同步通知信息", "🌐 官方上币公告内容"])
    
    with tab1:
        st.caption("直接复制代码发到内部群、内部邮件等同步渠道")
        st.code(rendered_internal, language="markdown")
        
    with tab2:
        st.caption("直接复制代码粘贴至 CMS 或官方宣发公告平台")
        st.code(rendered_public, language="markdown")