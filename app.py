import streamlit as st
from jinja2 import Template
from datetime import datetime, timedelta

# 设置网页标题
st.title("上币信息自动化输出系统")
st.caption("运营只需输入一次变量，即可同时输出内部同步信息和上币公告")

# ----------------- 🏢 模版定义 -----------------

# 模版 1：内部同步信息模版
INTERNAL_TEMPLATE = """
{{ project_name }} ({{ ticker }}) {{ lst_type_main }}
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
{{ project_intro_cn }}

2.时间线 (UTC+8)
- 上币公告/充值：{{ ann_time }}
- 交易：{{ trading_time }}
- 提现： {{ withdraw_time }}

3.市场宣发预算 ({{ budget_amount }} {{ ticker }}),参考价${{ price }}

{{ marketing_budget_section }}"""

# 模版 2：上币公告模版 
PUBLIC_ANNOUNCEMENT_TEMPLATE = """
{{ world_premiere_tag }} {{ project_name }} ({{ ticker }}) Listed on KuCoin 

KuCoin is proud to announce yet another great project coming to our Spot Trading platform. 

{{ project_name }} ({{ ticker }}) will be available on KuCoin!

Important Information
1. [Deposits]({{ deposit_dynamic_link }}): Effective Immediately (Supported Network: {{ network }})
2. [Call Auction](https://www.kucoin.com/announcement/introducing-kucoins-call-auction-mechanism-for-new-trading-pairs): From {{ auction_start_time }} to {{ auction_end_time }} on {{ auction_date }} (UTC)
3. Trading: {{ trading_time_utc }}
4. Withdrawals: {{ withdraw_time_UTC }}
5. Trading Pair: {{ ticker }}/USDT
6. [Trading Bots](https://www.kucoin.com/trading-bot): When spot trading begins, {{ ticker }}/USDT will be available for Trading Bots. The available services include: Spot Grid, Infinity Grid, DCA, Smart Rebalance, Spot Martingale, Spot Grid AI Plus and AI Spot Trend.

What is {{ project_name }}?

{{ project_intro_en }}

{{ official_links_section }}

Learn more about the Call Auction and find additional details in the: [Help Center](https://www.kucoin.com/support).

Risk Warning: Investing in cryptocurrency is akin to being a venture capital investor. The cryptocurrency market is available worldwide 24/7 for trading with no market close or open times. Please do your own risk assessment when deciding how to invest in cryptocurrency and blockchain technology. KuCoin attempts to screen all tokens before they come to market. However, even with the best due diligence, there are still risks when investing. KuCoin is not liable for investment gains or losses.

[Sign Up on KuCoin Now](https://www.kucoin.com/ucenter/signup)

[Download the KuCoin App](https://www.kucoin.com/download)

[Follow Us on X (Twitter)](https://twitter.com/kucoincom)

[Join Us on Telegram](https://t.me/Kucoin_Exchange)

[Dive Into KuCoin's Global Communities](https://www.kucoin.com/land/community-collect)
"""

# 模版 3：gempool公告模版 
PUBLIC_GEMPOOL_TEMPLATE = """
Introducing {{ project_name }} ({{ ticker }}) on KuCoin GemPool!

KuCoin is excited to announce that another great project, {{ project_name }} ({{ ticker }}), will be available on KuCoin GemPool. Users can stake their KCS and USDT into separate pools to farm {{ ticker }} tokens!

The trading of {{ project_name }} ({{ ticker }}) on KuCoin will start at {{ trading_time_utc }}.

Check the Listing Announcement for more information.

About the Project

{{ project_intro_en }}

{{ official_links_section }}

GemPool Details (Participate Now)

1. Total Supply: {{ total_supply }} {{ ticker }}
2. GemPool Total Rewards: {{ total_rewards }} {{ ticker }}
3. Campaign Period: from {{ start_time_simple }} to {{ end_time_simple }}
4. Staking Terms: KYC verification
5. Hourly Reward Hard Cap Per User:
{{ gempool_hard_cap_section }}

{{ gempool_dynamic_table }}

Additional Bonuses

(Bonus 1) Complete Quiz to Win Additional 10% Bonus!
During the campaign period, users participating in the GemPool activity and completing the quiz with all correct answers can enjoy an additional bonus of 10%! For more details, please refer to the event page.
(Bonus 2) Boost the Rewards by Inviting Friends to Register and Join GemPool — Up to 2x Rewards!
During the campaign period, users can receive additional rewards by inviting friends to register and participate in the GemPool campaign. To qualify as a valid invitation, the invitee must complete both registration and GemPool participation within the event period.

| Tier | Invitees | Bonus |
| :--- | :--- | :--- |
| 1 | 1 Valid Invitee | 20% |
| 2 | 2 Valid Invitees | 40% |
| 3 | 3–8 Valid Invitees | 70% |
| 4 | 9+ Valid Invitees | 100% |

* Inviter could enjoy multiple coefficient rewards if the invitee participates in multiple GemPool campaigns in the same period of time.

(Bonus 3) VIP Exclusive! Bonus Up to 50%!
During the campaign period, VIP users participating in the GemPool activity will get a chance to enjoy an exclusive bonus, which varies according to their VIP level!

| VIP Level | Bonus |
| :--- | :--- |
| VIP 1 – 4 | 10% |
| VIP 5 – 8 | 20% |
| VIP 9 – 12 | 50% |

(Bonus 4) Special Benefits for Loyal KCS Holders: Earn Up to 20% Bonus!
During the campaign period, KCS holders participating in the GemPool activity have the opportunity to enjoy an exclusive bonus, with the percentage depending on their KCS loyalty level!

| Level | Bonus |
| :--- | :--- |
| K1 (Explorer) | 5% |
| K2 (Voyager) | 10% |
| K3 (Navigator) | 15% |
| K4 (Pioneer) | 20% |

Notes:
1. Tokens can only be staked in one pool at a time. For example, users cannot stake KCS in the KCS Pool while simultaneously staking KCS in another pool.
2. Rewards will be calculated hourly based on the user's staking volume relative to the total pool volume.
3. Users can accumulate and claim their rewards directly into their Funding Account at any time.

* For details of the KCS loyalty bonus, please view this page: https://www.kucoin.com/kcs


Rewards Calculation 

Rewards per user = (user's staked token / total staked token of all eligible participants) × corresponding prize pool.
Snapshots of user balances and total pool balances will be taken multiple times at any point of time each hour to get users’ hourly average balances and calculate user rewards.
Rewards will be calculated starting from the following hour after staking. User rewards will be updated hourly.
 

Notes

1. Once enable the Auto-Lock function, only rewards earned from GemPool event will be auto-locked. Your other balance remains unchanged;

2. Tokens can only be staked in one pool at a time. For example, users cannot stake the same KCS into two different pools at the same time;

3. Rewards will be calculated and distributed every hour. Users can claim their rewards on an hourly basis;

4. Users will be able to stake before the farming period, however no reward will be generated until the farming period starts;

5. Users will be able to unstake their funds at any time with no delay and participate in any other available pools immediately. No reward will be generated after you unstake your tokens;

6. Users will be able to manually claim the rewards each day. Tokens staked in each pool and any unclaimed rewards will be automatically credited to the user's Funding Account at the end of each farming period;

7. At the end of each pool's farming period, the funds staked by users are expected to be automatically returned within approximately 30 minutes;

8. The users from the following countries/areas are not supported in this event: Singapore, Uzbekistan, Mainland China, Hong Kong Special Administrative Region, Thailand, Malaysia, Ontario, Canada, United Kingdom, United States of America, including all US territories;

9. In case of any discrepancy between the translated version and the English original version, the English version shall prevail;

10. The behavior of maliciously taking rewards will result in the cancellation of rewards. KuCoin reserves the final right to interpret these terms and conditions, including but not limited to the modification, change, or cancellation of the activity, without further notice. Please contact us if you have any questions;

11. If users have doubts about the result of the activities, please note the official appeal period for the result of activities is 2 months after the end of the campaign. We will not accept any kind of appeal after this period.

[Sign Up on KuCoin Now](https://www.kucoin.com/ucenter/signup)

[Download the KuCoin App](https://www.kucoin.com/download)

[Follow Us on X (Twitter)](https://twitter.com/kucoincom)

[Join Us on Telegram](https://t.me/Kucoin_Exchange)

[Dive Into KuCoin's Global Communities](https://www.kucoin.com/land/community-collect)

"""


# ----------------- 📋 左侧边栏：统一输入源 -----------------
st.sidebar.header("📋 请输入项目变量")

# 让运营选择活动类型模式
activity_type = st.sidebar.selectbox(
    "💡 请选择本次上币活动类型模式：",
    ["常规上币", "GemPool上币", "HODLer上币"]
)

is_gempool_mode = (activity_type == "GemPool上币")
is_hodler_mode = (activity_type == "HODLer上币")

st.sidebar.subheader("基本信息")
p_name = st.sidebar.text_input("项目全称 (project_name)", value="")

# 📍 调整顺序：优先把 ticker 的输入源拿到前面，方便下面默认配置动态抓取
p_ticker = st.sidebar.text_input("代币符号 (ticker)", value="STAY")  
p_network = st.sidebar.text_input("代币类型/主网 (network)", value="")
p_fee_level = st.sidebar.text_input("费率标准 (fee_level)", value="")
p_op_level = st.sidebar.text_input("运营评级 (op_level)", value="")

st.sidebar.subheader("🔗 官方项目链接")
p_website = st.sidebar.text_input("官方网站 (website)", value="")
p_twitter = st.sidebar.text_input("X / Twitter 链接", value="")
p_whitepaper = st.sidebar.text_input("白皮书链接 (Whitepaper)", value="")
p_contract = st.sidebar.text_input("代币合约/区块浏览器链接 (Token Contract)", value="")

st.sidebar.subheader("上币类型")
p_lst_type_main = st.sidebar.text_input("上币母类型 (lst_type_main)", value="首发上币")

default_sub_val = "GemPool首发" if is_gempool_mode else ("HODLer首发" if is_hodler_mode else "普通首发")
p_lst_type_sub = st.sidebar.text_input("上币子类型 (lst_type_sub)", value=default_sub_val)

st.sidebar.subheader("项目简介")
p_intro_cn = st.sidebar.text_area("项目中文简介 (用于内部同步)", value="")
p_intro_en = st.sidebar.text_area("项目英文简介 (用于官方公告)", value="")

st.sidebar.subheader("时间线")
st.sidebar.caption("💡 提示：输入本地北京时间格式如：2026-05-27 21:00")
p_ann_time = st.sidebar.text_input("上币公告/充值时间 (ann_time)", value="2026-05-27 18:00")
p_trading_time = st.sidebar.text_input("交易时间 (trading_time)", value="2026-05-28 18:00")
p_withdraw_time = st.sidebar.text_input("提现时间 (withdraw_time)", value="2026-05-29 18:00")

st.sidebar.subheader("预算与价格")
p_budget_amount = st.sidebar.number_input("总预算数量 (budget_amount)", min_value=0.0, value=0.0, step=1000.0)
p_price = st.sidebar.text_input("参考价 (price)", value="")

# 📊 动态预算分配
st.sidebar.subheader("📊 动态预算分配")
default_activities = "GemSlot, Learn2Earn, TG AMA/ X-Space, Twitter Giveaway, Telegram Quiz"
activity_input = st.sidebar.text_area("💡 动态修改活动类型：", value=default_activities)
activity_list = [act.strip() for act in activity_input.replace("，", ",").split(",") if act.strip()]

alloc_mode = st.sidebar.radio("选择分配模式：", ["按比例 (%) 分配", "按固定数量分配"])

activity_values = {}  
total_pct = 0
total_amt_input = 0

if activity_list:
    st.sidebar.caption(f"请为各活动输入 {'比例 (%)' if alloc_mode == '按比例 (%) 分配' else '代币数量'}")
    for act in activity_list:
        if alloc_mode == "按比例 (%) 分配":
            ratio = st.sidebar.number_input(f"🔸 {act} (%)", min_value=0, max_value=100, value=0, key=f"pct_{act}")
            total_pct += ratio
            activity_values[act] = int(p_budget_amount * ratio / 100) if p_budget_amount > 0 else 0
        else:
            amt = st.sidebar.number_input(f"🔸 {act} (数量)", min_value=0, value=0, step=100, key=f"amt_{act}")
            total_amt_input += amt
            activity_values[act] = amt

    if alloc_mode == "按比例 (%) 分配" and total_pct != 100 and p_budget_amount > 0:
        st.sidebar.warning(f"⚠️ 当前分配总和为 {total_pct}%，不等于 100%！")
    elif alloc_mode == "按固定数量分配" and p_budget_amount > 0:
        if total_amt_input > p_budget_amount:
            st.sidebar.error(f"🚨注意：当前活动数量总和 ({total_amt_input:,}) 已超过总预算 ({int(p_budget_amount):,})！请注意核对。")
        elif total_amt_input < p_budget_amount:
            st.sidebar.warning(f"⚠️ 提示：当前活动数量总和 ({total_amt_input:,}) 小于总预算 ({int(p_budget_amount):,})")

# ⛏️ 💎 GemPool 专属看板配置
if is_gempool_mode:
    st.sidebar.markdown("---")
    st.sidebar.subheader("⛏️ GemPool 专属配置看板")
    g_total_supply = st.sidebar.text_input("项目总供应量 (Total Supply)", value="1,000,000,000")
    g_total_rewards = st.sidebar.number_input("GemPool 总奖池数量", min_value=0, value=200000, step=10000)
    g_duration = st.sidebar.number_input("挖矿持续天数", min_value=1, value=7, step=1)
    
    st.sidebar.caption("💡 提示：请输入活动北京起止时间：")
    g_start_time_raw = st.sidebar.text_input("挖矿开始时间 (如：2026-05-28 16:00)", value="2026-05-28 16:00")
    g_end_time_raw = st.sidebar.text_input("挖矿结束时间 (如：2026-06-04 16:00)", value="2026-06-04 16:00")
    
    st.sidebar.markdown("##### 🪙 质押池分配比例表")
    st.sidebar.caption("💡 可在表格底部点击 `+ Add row` 添加新币种，或选择行按 Delete 删除。")
    
    # 📍【核心修改点】：通过把 p_ticker 的真实值注入到表格中，直接解决默认显示的第三项变成真实本币参数的问题
    current_user_ticker = p_ticker.strip().upper() if p_ticker.strip() else "TOKEN"
    
    default_pools = [
        {"Supported Pools": "KCS", "Total Rewards (%)": 50},
        {"Supported Pools": "USDG", "Total Rewards (%)": 30},
        {"Supported Pools": current_user_ticker, "Total Rewards (%)": 20}
    ]
    gempool_pools_data = st.sidebar.data_editor(default_pools, num_rows="dynamic", key="gempool_table_editor")

# 💰 💎 Hodler 专属看板配置
elif is_hodler_mode:
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 HODLer参数配置")
    hodler_total_rewards = st.sidebar.number_input("HODLer 奖池数量", min_value=0, value=150000, step=10000)
    st.sidebar.info("💡 已成功激活HODLer模式配置面板。")


# 工具函数
def get_announcement_times(p_trading_str, p_withdraw_str):
    def parse_time(t_str):
        for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"):
            try: return datetime.strptime(t_str.strip(), fmt)
            except ValueError: continue
        return None

    dt_trading = parse_time(p_trading_str)
    dt_withdraw = parse_time(p_withdraw_str)

    trading_utc = (dt_trading - timedelta(hours=8)).strftime("%H:%M on %B %d, %Y (UTC)") if dt_trading else p_trading_str
    withdraw_utc_cap = (dt_withdraw - timedelta(hours=8)).strftime("%H:%M on %B %d, %Y (UTC)") if dt_withdraw else p_withdraw_str

    if dt_trading:
        dt_utc_trading = dt_trading - timedelta(hours=8)
        dt_auction_start = dt_utc_trading - timedelta(hours=1) 
        auction_start_time = dt_auction_start.strftime("%H:%M") 
        auction_end_time = dt_utc_trading.strftime("%H:%M")     
        auction_date = dt_utc_trading.strftime("%B %d, %Y")      
    else:
        auction_start_time, auction_end_time, auction_date = "TBD", "TBD", "TBD"

    return {
        "trading_time_utc": trading_utc,
        "withdraw_time_UTC": withdraw_utc_cap, 
        "auction_start_time": auction_start_time,
        "auction_end_time": auction_end_time,
        "auction_date": auction_date
    }

def convert_time_to_utc(time_str):
    for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"):
        try:
            dt = datetime.strptime(time_str.strip(), fmt)
            return (dt - timedelta(hours=8)).strftime("%H:%M on %B %d, %Y (UTC)")
        except ValueError: continue
    return time_str if time_str else "TBD"

# 📍【核心修改点】：移除原先的 <br> 网页换行标记，改用标准的短横线进行单行完美展示，彻底剔除原生乱码
def convert_to_vertical_utc_range(start_str, end_str):
    def parse_to_utc_dt(t_str):
        for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"):
            try: return datetime.strptime(t_str.strip(), fmt) - timedelta(hours=8)
            except ValueError: continue
        return None
    dt_start = parse_to_utc_dt(start_str)
    dt_end = parse_to_utc_dt(end_str)
    if dt_start and dt_end:
        return f"{dt_start.strftime('%Y-%m-%d %H:%M')} - {dt_end.strftime('%Y-%m-%d %H:%M')}"
    return "TBD"


# ----------------- 🚀 右侧主展示区：一键多发 -----------------

if st.sidebar.button("✨ 一键生成", type="primary"):
    
    current_duration = locals().get('g_duration', 7)
    current_pools = locals().get('gempool_pools_data', [])
    current_start_raw = locals().get('g_start_time_raw', "")
    current_end_raw = locals().get('g_end_time_raw', "")
    current_total_supply = locals().get('g_total_supply', "TBD")
    current_total_rewards = locals().get('g_total_rewards', 200000)
    current_ticker = p_ticker.strip().upper() if p_ticker.strip() else "TOKEN"

    g_start_utc = convert_time_to_utc(current_start_raw)
    g_end_utc = convert_time_to_utc(current_end_raw)
    vertical_farming_period = convert_to_vertical_utc_range(current_start_raw, current_end_raw)

    # 动态表格与硬顶拼装
    table_lines = [
        f"| Supported Pools | Total Rewards ({current_ticker}) | Farming Period (UTC) |",
        "| :--- | :--- | :--- |"
    ]
    
    hard_cap_lines = [] 
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    
    if is_gempool_mode and current_pools:
        for idx, row in enumerate(current_pools):
            token = row.get("Supported Pools", "").strip() if row.get("Supported Pools") else ""
            
            if not token:
                continue
                
            if token.upper() == "PROJECT_TICKER" or token == "{{ticker}}":
                token = current_ticker
            else:
                token = token.upper()
                
            pct = row.get("Total Rewards (%)", 0)
            amt = int(current_total_rewards * (pct / 100))
            
            table_lines.append(f"| {token} | {amt:,} | {vertical_farming_period} |")
            
            if current_duration > 0:
                hourly_cap = (amt * 0.10) / current_duration / 24
                final_int_cap = int(round(hourly_cap))
                cap_str = f"{final_int_cap:,}"
            else:
                cap_str = "0"
                
            char_prefix = alphabet[idx % len(alphabet)]
            hard_cap_lines.append(f"    {char_prefix}. {token} Pool: {cap_str} {current_ticker}")
            
    else:
        table_lines.append(f"| TBD Pool | TBD | TBD |")
        hard_cap_lines.append("    a. TBD Pool: TBD")
        
    gempool_dynamic_table_markdown = "\n".join(table_lines)
    gempool_hard_cap_section_text = "\n".join(hard_cap_lines)

    # 活动预算处理
    budget_lines = []
    for act in activity_list:
        val = activity_values.get(act, 0)
        if val > 0:
            budget_lines.append(f"- {act}：{val:,}")
        else:
            budget_lines.append(f"- {act}：")
            
    marketing_budget_section = "\n".join(budget_lines)
    formatted_budget = f"{int(p_budget_amount):,}" if p_budget_amount.is_integer() else f"{p_budget_amount:,.2f}"

    times_data = get_announcement_times(p_trading_time, p_withdraw_time)

    clean_ticker = p_ticker.strip() 
    generated_deposit_link = f"https://www.kucoin.com/assets/coin/{clean_ticker}" if clean_ticker else "https://www.kucoin.com/assets/coin"

    link_items = []
    if p_website.strip(): link_items.append(f"[Website]({p_website.strip()})")
    if p_twitter.strip(): link_items.append(f"[X (Twitter)]({p_twitter.strip()})")
    if p_whitepaper.strip(): link_items.append(f"[Whitepaper]({p_whitepaper.strip()})")
    if p_contract.strip(): link_items.append(f"[Token Contract]({p_contract.strip()})")
    official_links_section = " | ".join(link_items) if link_items else ""

    world_premiere_tag = "World Premiere: " if "首发上币" in p_lst_type_main.strip() else ""

    # 打包传参字典
    data = {
        "project_name": p_name,
        "ticker": p_ticker,
        "fee_level": p_fee_level,
        "network": p_network,
        "lst_type_main": p_lst_type_main,
        "lst_type_sub": p_lst_type_sub,
        "op_level": p_op_level,
        "website": p_website,
        "project_intro_cn": p_intro_cn, 
        "project_intro_en": p_intro_en, 
        "ann_time": p_ann_time,
        "trading_time": p_trading_time,
        "withdraw_time": p_withdraw_time,
        "budget_amount": formatted_budget, 
        "price": p_price,
        "marketing_budget_section": marketing_budget_section,
        "deposit_dynamic_link": generated_deposit_link,
        "world_premiere_tag": world_premiere_tag,
        "official_links_section": official_links_section,
        
        # GemPool 专属绑定变量
        "total_supply": current_total_supply,
        "total_rewards": f"{current_total_rewards:,}",
        "start_time_simple": g_start_utc,
        "end_time_simple": g_end_utc,
        "gempool_dynamic_table": gempool_dynamic_table_markdown,
        "gempool_hard_cap_section": gempool_hard_cap_section_text,
        **times_data 
    }
    
    rendered_internal = Template(INTERNAL_TEMPLATE).render(data)
    rendered_public = Template(PUBLIC_ANNOUNCEMENT_TEMPLATE).render(data)
    rendered_gempool = Template(PUBLIC_GEMPOOL_TEMPLATE).render(data)
    
    st.write("### 🖨️ 自动化内容输出成功！")
    
    if is_gempool_mode:
        tab1, tab2, tab3 = st.tabs(["内部同步信息", "上币公告", "GemPool活动公告"])
    else:
        tab1, tab2 = st.tabs(["内部同步信息", "上币公告"])
        
    with tab1:
        st.caption("运营使用时需对内容进行二次校验")
        st.code(rendered_internal, language="markdown")
        
    with tab2:
        st.caption("运营使用时需对内容进行二次校验")
        st.markdown("---")
        st.markdown(rendered_public)
        st.markdown("---")
        
    if is_gempool_mode:
        with tab3:
            st.caption("运营使用时需对内容进行二次校验")
            st.markdown("---")
            st.markdown(rendered_gempool)
            st.markdown("---")