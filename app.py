import streamlit as st
from jinja2 import Template
from datetime import datetime, timedelta
import re

# 设置网页标题
st.title("上币信息自动化输出系统")
st.caption("运营只需输入一次变量，即可同时输出多份内容")

# -----------------  辅助函数：安全解析与格式化千分位 -----------------
def parse_and_format_int(val_str, default_val=0):
    """将带逗号或非标准的输入安全转为整数，并返回(整数值, 千分位字符串)"""
    if not val_str:
        return default_val, f"{default_val:,}"
    # 移除用户可能输入的逗号、空格等干扰符
    clean_str = re.sub(r'[内部\, ]', '', str(val_str))
    # 提取开头的数字部分
    match = re.match(r'\d+', clean_str)
    if match:
        int_val = int(match.group())
        return int_val, f"{int_val:,}"
    return default_val, f"{default_val:,}"

# -----------------  辅助函数：自动转换 HODLer 快照时间 -----------------
def convert_snapshot_time_to_utc(snapshot_str):
    """
    将用户输入的 '2026-05-22 16:00 to 2026-05-27 16:00 (UTC+8)' 
    转换为 'From 16:00 on May 22, 2026 to 16:00 on May 27, 2026 (UTC)'
    """
    default_return = "From 16:00 on May 22, 2026 to 16:00 on May 27, 2026 (UTC)"
    if not snapshot_str:
        return default_return
        
    try:
        # 使用正则提取出两段日期时间字符串
        times = re.findall(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}\s+\d{1,2}:\d{2}', snapshot_str)
        if len(times) == 2:
            start_local = datetime.strptime(times[0], "%Y-%m-%d %H:%M")
            end_local = datetime.strptime(times[1], "%Y-%m-%d %H:%M")
            
            # 转换为 UTC 时间 (UTC+8 减去 8 小时)
            start_utc = start_local - timedelta(hours=8)
            end_utc = end_local - timedelta(hours=8)
            
            # 格式化为英文英文公告样式
            start_formatted = start_utc.strftime("%H:%M on %B %d, %Y")
            end_formatted = end_utc.strftime("%H:%M on %B %d, %Y")
            
            return f"From {start_formatted} to {end_formatted} (UTC)"
    except Exception:
        pass
    
    return snapshot_str

# -----------------  模版定义 -----------------

# 模版 1：内部同步信息模版
INTERNAL_TEMPLATE = """
**{{ project_name }} ({{ ticker }}) {{ lst_type_main }}**

**1.1基础信息：**

- 代币全称：{{ project_name }}
- Ticker：{{ ticker }}
- 费率标准：{{ fee_level }}
- 代币类型：{{ network }}
- 上币母类型：{{ lst_type_main }}
- 上币子类型：{{ lst_type_sub }}
- 运营评级：{{ op_level }}
- 官网：{{ website }}

**1.2项目情况：**

{{ project_intro_cn }}

**2.时间线 (UTC+8)**
- 上币公告/充值：{{ ann_time }}
- 交易：{{ trading_time }}
- 提现： {{ withdraw_time }}

{% if has_budget %}
**3.市场宣发预算 ({{ budget_amount }} {{ ticker }}),参考价${{ price }}**

{{ marketing_budget_section }}

请相关业务线于 <font color="red">**{{ submit_deadline_time }} UTC+8**</font> 前在模版中修改活动方案：
**[https://klarkchat.sg.larksuite.com/wiki/EScuwMotzimJ4YkGtvYlbfiWgah?renamingWikiNode=false](https://klarkchat.sg.larksuite.com/wiki/EScuwMotzimJ4YkGtvYlbfiWgah?renamingWikiNode=false)**
{% else %}
**3.市场宣发预算：**
{{ marketing_budget_section }}
{% endif %}

*相关信息属于商业机密，请各位控制传播范围
"""

# 模版 2：常规上币公告模版 
PUBLIC_ANNOUNCEMENT_TEMPLATE = """
**{{ world_premiere_tag }} {{ project_name }} ({{ ticker }}) Listed on KuCoin** 

KuCoin is proud to announce yet another great project coming to our Spot Trading platform.
{{ project_name }} ({{ ticker }}) will be available on KuCoin!

**Important Information**

1. [Deposits]({{ deposit_dynamic_link }}): Effective Immediately (Supported Network: {{ network }})
2. [Call Auction](https://www.kucoin.com/announcement/introducing-kucoins-call-auction-mechanism-for-new-trading-pairs): From {{ auction_start_time }} to {{ auction_end_time }} on {{ auction_date }} (UTC)
3. Trading: {{ trading_time_utc }}
4. Withdrawals: {{ withdraw_time_UTC }}
5. Trading Pair: {{ ticker }}/USDT
6. [Trading Bots](https://www.kucoin.com/trading-bot): When spot trading begins, {{ ticker }}/USDT will be available for Trading Bots.
The available services include: Spot Grid, Infinity Grid, DCA, Smart Rebalance, Spot Martingale, Spot Grid AI Plus and AI Spot Trend.

**What is {{ project_name }}?**

{{ project_intro_en }}

{{ official_links_section }}

Learn more about the Call Auction and find additional details in the: [Help Center](https://www.kucoin.com/support).

Risk Warning: Investing in cryptocurrency is akin to being a venture capital investor.
The cryptocurrency market is available worldwide 24/7 for trading with no market close or open times.
Please do your own risk assessment when deciding how to invest in cryptocurrency and blockchain technology.
KuCoin attempts to screen all tokens before they come to market.
However, even with the best due diligence, there are still risks when investing.
KuCoin is not liable for investment gains or losses.

[Sign Up on KuCoin Now](https://www.kucoin.com/ucenter/signup)

[Download the KuCoin App](https://www.kucoin.com/download)

[Follow Us on X (Twitter)](https://twitter.com/kucoincom)

[Join Us on Telegram](https://t.me/Kucoin_Exchange)

[Dive Into KuCoin's Global Communities](https://www.kucoin.com/land/community-collect)
"""

# 模版 3：GemPool 公告模版
PUBLIC_GEMPOOL_TEMPLATE = """
**Introducing {{ project_name }} ({{ ticker }}) on KuCoin GemPool!**
KuCoin is excited to announce that another great project, {{ project_name }} ({{ ticker }}), will be available on KuCoin GemPool.
Users can stake their {{ dynamic_pool_text }} into separate pools to farm {{ ticker }} tokens!

The trading of {{ project_name }} ({{ ticker }}) on KuCoin will start at {{ trading_time_utc }}.

Check the [<font color="red">**Listing Announcement**</font>](https://www.kucoin.com/announcement/en-introducing-arena-two-atwo-on-kucoin-gempool) for more information.

**About the Project**

{{ project_intro_en }}

{{ official_links_section }}

**GemPool Details ([Participate Now](https://www.kucoin.com/gempool))**

1. Total Supply: {{ total_supply }} {{ ticker }}
2. GemPool Total Rewards: {{ total_rewards }} {{ ticker }}
3. Campaign Period: from {{ start_time_simple }} to {{ end_time_simple }}
4. Staking Terms: KYC verification
{{ gempool_hard_cap_section }}

{{ gempool_dynamic_table }}

**Additional Bonuses**

(Bonus 1) Complete Quiz to Win Additional 10% Bonus!
During the campaign period, users participating in the GemPool activity and completing the quiz with all correct answers can enjoy an additional bonus of 10%!
For more details, please refer to the event page.

(Bonus 2) Boost the Rewards by Inviting Friends to Register and Join GemPool  Up to 2x Rewards!
During the campaign period, users can receive additional rewards by inviting friends to register and participate in the GemPool campaign.
To qualify as a valid invitation, the invitee must complete both registration and GemPool participation within the event period.

| Tier | Invitees | Bonus |
| :---: | :---: | :---: |
| 1 | 1 Valid Invitee | 20% |
| 2 | 2 Valid Invitees | 40% |
| 3 | 38 Valid Invitees | 70% |
| 4 | 9+ Valid Invitees | 100% |

* Inviter could enjoy multiple coefficient rewards if the invitee participates in multiple GemPool campaigns in the same period of time.

(Bonus 3) VIP Exclusive! Bonus Up to 50%!
During the campaign period, VIP users participating in the GemPool activity will get a chance to enjoy an exclusive bonus, which varies according to their VIP level!

| VIP Level | Bonus |
| :---: | :---: |
| VIP 1  4 | 10% |
| VIP 5  8 | 20% |
| VIP 9  12 | 50% |

(Bonus 4) Special Benefits for Loyal KCS Holders: Earn Up to 20% Bonus!
During the campaign period, KCS holders participating in the GemPool activity have the opportunity to enjoy an exclusive bonus, with the percentage depending on their KCS loyalty level!

| Level | Bonus |
| :---: | :---: |
| K1 (Explorer) | 5% |
| K2 (Voyager) | 10% |
| K3 (Navigator) | 15% |
| K4 (Pioneer) | 20% |
* For details of the KCS loyalty bonus, please view this page: https://www.kucoin.com/kcs


**Rewards Calculation** 

1. Rewards per user = (user's staked token / total staked token of all eligible participants)  corresponding prize pool.
2. Snapshots of user balances and total pool balances will be taken multiple times at any point of time each hour to get users hourly average balances and calculate user rewards.
3. Rewards will be calculated starting from the following hour after staking. User rewards will be updated hourly.

Notes

1. Once enable the Auto-Lock function, only rewards earned from GemPool event will be auto-locked. Your other balance remains unchanged;
2. Tokens can only be staked in one pool at a time.
For example, users cannot stake the same KCS into two different pools at the same time;
3. Rewards will be calculated and distributed every hour. Users can claim their rewards on an hourly basis;
4. Users will be able to stake before the farming period, however no reward will be generated until the farming period starts;
5. Users will be able to unstake their funds at any time with no delay and participate in any other available pools immediately.
No reward will be generated after you unstake your tokens;
6. Users will be able to manually claim the rewards each day.
Tokens staked in each pool and any unclaimed rewards will be automatically credited to the user's Funding Account at the end of each farming period;
7. At the end of each pool's farming period, the funds staked by users are expected to be automatically returned within approximately 30 minutes;
8. The users from the following countries/areas are not supported in this event: Singapore, Uzbekistan, Mainland China, Hong Kong Special Administrative Region, Thailand, Malaysia, Ontario, Canada, United Kingdom, United States of America, including all US territories;
9. In case of any discrepancy between the translated version and the English original version, the English version shall prevail;
10. The behavior of maliciously taking rewards will result in the cancellation of rewards.
KuCoin reserves the final right to interpret these terms and conditions, including but not limited to the modification, change, or cancellation of the activity, without further notice.
Please contact us if you have any questions;

11. If users have doubts about the result of the activities, please note the official appeal period for the result of activities is 2 months after the end of the campaign.
We will not accept any kind of appeal after this period.

[Sign Up on KuCoin Now](https://www.kucoin.com/ucenter/signup)

[Download the KuCoin App](https://www.kucoin.com/download)

[Follow Us on X (Twitter)](https://twitter.com/kucoincom)

[Join Us on Telegram](https://t.me/Kucoin_Exchange)

[Dive Into KuCoin's Global Communities](https://www.kucoin.com/land/community-collect)
"""

# 模版 4：HODLer 专属上币公告模版
PUBLIC_HODLER_COMBINED_TEMPLATE = """
**HODLer Airdrops: {{ project_name }} ({{ ticker }}) World Premiere Listing on KuCoin!**

KuCoin is excited to announce that another great project, {{ project_name }} ({{ ticker }}), will be listed on KuCoin Spot Trading with HODLer Airdrops.

**Important Information**

1. [Deposits]({{ deposit_dynamic_link }}): Effective Immediately (Supported Network: {{ network }})
2. [Call Auction](https://www.kucoin.com/announcement/introducing-kucoins-call-auction-mechanism-for-new-trading-pairs): From {{ auction_start_time }} to {{ auction_end_time }} on {{ auction_date }} (UTC)
3. Trading: {{ trading_time_utc }}
4. Withdrawals: {{ withdraw_time_UTC }}
5. Trading Pair: {{ ticker }}/USDT

**HODLer Airdrops Details ([Check Now](https://www.kucoin.com/hodler))**

1. Token Name (Ticker): {{ project_name }} ({{ ticker }})

2. Total Token Supply: {{ total_supply }} {{ ticker }}

3. HODLer Airdrops Token Rewards: {{ hodler_rewards }} {{ ticker }}

4. Minimum Holding Amount: 20 KCS

5. Holding Hard Cap: 10,000 KCS (Average holdings that exceed the hard cap will be displayed and rewarded based on the hard cap value)

6. Snapshot Period: {{ hodler_snapshot_period }}

7. Airdrop Distribution: {{ hodler_distribution_time }} [Allocated {{ ticker }} airdrops will be distributed 100% to the Funding Account]

8. Eligibility: To qualify for the airdrops, users must complete KYC/KYB verification from an eligible jurisdiction before the snapshot end time and have traded on KuCoin (Spot, Margin, Futures, or Trading Bot) within the past 90 days.
Trades made after 16:00 UTC on 27 May are not counted.

Learn more about KuCoin HODLer Airdrops via our [Announcement](https://www.kucoin.com/announcement/en-introducing-kucoin-hodler-airdrops-a-new-way-to-earn-by-holding) and in the [Help Center](https://www.kucoin.com/support/48142946141378).

**About the Project**

{{ project_intro_en }}

{{ official_links_section }}

**Addition Bonus**

Bonus 1: Special Benefits for Loyal KCS Holders  Earn Up to 20% Bonus

During the campaign period, KCS holders have the opportunity to enjoy an exclusive bonus, with the percentage depending on their KCS loyalty level.
| Level | Bonus |
| :---: | :---: |
| K1 (Explorer) | 5% |
| K2 (Voyager) | 10% |
| K3 (Navigator) | 15% |
| K4 (Pioneer) | 20% |
* For details of the KCS loyalty bonus, please visit [KuCoin KCS](https://www.kucoin.com/kcs).

Bonus 2: VIP Exclusive  Earn Up to 50% Bonus

VIP users will get a chance to enjoy an exclusive bonus, which varies according to their VIP level.
| VIP Level | Bonus |
| :---: | :---: |
| VIP 1  4 | 10% |
| VIP 5  8 | 20% |
| VIP 9  12 | 50% |

Bonus 3: New User Exclusive  Earn Up to 50% Bonus

New users who registered and completed their identify verification during the snapshot period will be eligible for an exclusive bonus of up to 50%.

Bonus 4: Futures Trading  Earn Up to 20% Bonus

During the snapshot peroid, users who completed futures trading of any trading pair will share a bonus rate based on their trading volume!
| Futures Trading Volume (USDT)| Bonus |
| :---: | :---: |
| 600 | 5% |
| 6,000 | 10% |
| 60,000 | 15% |
| 360,000 | 20% |

Notes

1. The holdings of required assets will be counted from Funding Account, Trading Account, Margin Account, Futures Account, Trading Bot Account, Financial Account, High-Frequency Trading Account and Wealth Account;
2. Reward calculations are capped at the hard cap limit, holdings above the hard cap are not counted.
Final Token Received = (Your Average Hourly Holdings / All Participants' Average Hourly Holdings)  Total Airdrop;
3. Airdrop will be distributed to your Funding Account;
4. The users from the following countries/areas are not supported in this event: The United States of America, including all US territories, Guam, Puerto Rico, Northern Mariana Islands, Central African Republic, Mainland China, Cuba, North Korea, Haiti, Hong Kong Special Administrative Region, Iran, Lebanon, Libya, Mali, Myanmar, Singapore, Somalia, South Sudan, Sudan, Uzbekistan, the Crimea region, the Kurdistan region, Canada, Malaysia, France, Yemen and the Netherlands;
5. When spot trading begins, SHARE/USDT will be available for Trading Bots.
The available services include: Spot Grid, Infinity Grid, DCA, Smart Rebalance, Spot Martingale, Spot Grid AI Plus and AI Spot Trend.
6. In case of any discrepancy between the translated version and the English original version, the English version shall prevail;
7. The behavior of maliciously taking rewards will result in the cancellation of rewards.
KuCoin reserves the final right to interpret these terms and conditions, including but not limited to the modification, change, or cancellation of the activity, without further notice.
Please contact us if you have any questions;
8. If users have doubts about the result of the activities, please note the official appeal period for the result of activities is 2 months after the end of the campaign.
We will not accept any kind of appeal after this period.
9. Apple Inc. is not a sponsor and is not affiliated with this event.

Disclaimer: This disclaimer governs your participation in the HODLer Airdrops "Campaign") on KuCoin's platform.
By participating, you acknowledge that KuCoin facilitates the Campaign, while each project partner ("Reward Provider") sets its own eligibility and reward rules.
KuCoin reserves the right to modify or terminate the Campaign at any time and is not liable for any issues related to rewards or technical problems.
Inquiries should be directed to the Reward Provider. For the full disclaimer, please refer to the HODLer Airdrops landing page.

Risk Warning: Investing in cryptocurrency is akin to being a venture capital investor.
The cryptocurrency market is available worldwide 24/7 for trading with no market close or open times.
Please do your own risk assessment when deciding how to invest in cryptocurrency and blockchain technology.
KuCoin attempts to screen all tokens before they come to market.
However, even with the best due diligence, there are still risks when investing.
KuCoin is not liable for investment gains or losses.

[Sign Up on KuCoin Now](https://www.kucoin.com/ucenter/signup)

[Download the KuCoin App](https://www.kucoin.com/download)

[Follow Us on X (Twitter)](https://twitter.com/kucoincom)

[Join Us on Telegram](https://t.me/Kucoin_Exchange)

[Dive Into KuCoin's Global Communities](https://www.kucoin.com/land/community-collect)
"""


# -----------------  左侧边栏 -----------------
st.sidebar.header(" 请输入项目变量")

activity_type = st.sidebar.selectbox(
    " 请选择上币模式：",
    ["常规上币", "GemPool上币", "HODLer上币"]
)

is_gempool_mode = (activity_type == "GemPool上币")
is_hodler_mode = (activity_type == "HODLer上币")

st.sidebar.subheader("基本信息")
p_name = st.sidebar.text_input("项目全称 (project_name)", value="Zama")
p_ticker = st.sidebar.text_input("代币符号 (ticker)", value="ZAMA")  
p_network = st.sidebar.text_input("代币类型/主网 (network)", value="ZAMA Network")
p_fee_level = st.sidebar.text_input("费率标准 (fee_level)", value="2")
p_op_level = st.sidebar.text_input("运营评级 (op_level)", value="S")

st.sidebar.subheader(" 官方项目链接")
p_website = st.sidebar.text_input("官方网站 (website)", value="XX")
p_twitter = st.sidebar.text_input("X / Twitter 链接", value="")
p_whitepaper = st.sidebar.text_input("白纸书链接 (Whitepaper)", value="")
p_contract = st.sidebar.text_input("代币合约/区块浏览器链接 (Token Contract)", value="")

st.sidebar.subheader("上币类型")
p_lst_type_main = st.sidebar.text_input("上币母类型 (lst_type_main)", value="首发上币")

default_sub_val = "GemPool首发" if is_gempool_mode else ("HODLer首发" if is_hodler_mode else "普通首发")
p_lst_type_sub = st.sidebar.text_input("上币子类型 (lst_type_sub)", value=default_sub_val)

st.sidebar.subheader("项目简介")
p_intro_cn = st.sidebar.text_area("项目中文简介 (用于内部同步)", value="XXX")
p_intro_en = st.sidebar.text_area("项目英文简介 (用于官方公告)", value="XXX")

st.sidebar.subheader("时间线")
p_ann_time = st.sidebar.text_input("上币公告/充值时间 (ann_time)", value="2026-05-27 18:00")
p_trading_time = st.sidebar.text_input("交易时间 (trading_time)", value="2026-05-28 18:00")
p_withdraw_time = st.sidebar.text_input("提现时间 (withdraw_time)", value="2026-05-29 18:00")

# 截止时间智能计算
submit_deadline_str = "2026-05-26 18:00"  
try:
    dt_trading_parse = datetime.strptime(p_trading_time.strip(), "%Y-%m-%d %H:%M")
    submit_deadline_str = (dt_trading_parse - timedelta(days=1)).strftime("%Y-%m-%d %H:%M")
except Exception:
    pass

st.sidebar.info(f"各部门方案提交截止时间默认为开交易前1天，即：\n**{submit_deadline_str}**，可按需修改")

st.sidebar.subheader("预算与价格")

# 引入是否有项目活动预算勾选开关
has_budget = st.sidebar.checkbox("是否有项目活动预算？", value=True)

if has_budget:
    if "budget_input_raw" not in st.session_state:
        st.session_state["budget_input_raw"] = ""

    budget_text = st.sidebar.text_input("总预算数量 (budget_amount)", value=st.session_state["budget_input_raw"])
    p_budget_amount, formatted_budget_str = parse_and_format_int(budget_text, default_val=10000000)
    st.session_state["budget_input_raw"] = formatted_budget_str

    p_price = st.sidebar.text_input("参考价 (price)", value="")

    # ======================== 动态预算分配 ========================
    st.sidebar.subheader(" 动态预算分配")
    default_activities = "GemSlot, Staking, Learn2Earn, TG AMA / X-Space, Twitter Giveaway, Telegram Quiz"
    activity_input = st.sidebar.text_area(" 动态修改活动类型：", value=default_activities)
    activity_list = [act.strip() for act in activity_input.replace("，", ",").split(",") if act.strip()]

    alloc_mode = st.sidebar.radio("选择分配模式：", ["按比例 (%) 分配", "按固定数量分配"])

    activity_values = {}  
    ticker_upper = p_ticker.strip().upper() if p_ticker.strip() else "TOKEN"

    current_total_pct = 0.0
    current_total_amt = 0.0

    if activity_list:
        for act in activity_list:
            act_clean = act.lower()
            if "gemslot" in act_clean: default_ratio = 35
            elif "staking" in act_clean: default_ratio = 30
            elif "learn2earn" in act_clean or "learn 2 earn" in act_clean: default_ratio = 15
            elif "tg ama" in act_clean: default_ratio = 10
            elif "twitter" in act_clean: default_ratio = 5
            elif "quiz" in act_clean: default_ratio = 5
            else: default_ratio = 0

            if alloc_mode == "按比例 (%) 分配":
                ratio = st.sidebar.number_input(f" {act} (%)", min_value=0, max_value=100, value=default_ratio, key=f"pct_{act}")
                current_total_pct += float(ratio)
                calc_amt = int(p_budget_amount * ratio / 100) if p_budget_amount > 0 else 0
                activity_values[act] = calc_amt
            else:
                state_key = f"amt_raw_store_{act}"
                if state_key not in st.session_state:
                    st.session_state[state_key] = "0"
                    
                amt_text_input = st.sidebar.text_input(f" {act} (数量)", value=st.session_state[state_key], key=f"amt_ui_{act}")
                act_amt_val, formatted_act_amt = parse_and_format_int(amt_text_input, default_val=0)
                st.session_state[state_key] = formatted_act_amt
                
                current_total_amt += float(act_amt_val)
                activity_values[act] = act_amt_val

        if alloc_mode == "按比例 (%) 分配":
            if abs(current_total_pct - 100.0) < 0.01:
                st.sidebar.success(f" 当前总比例：**{current_total_pct:.1f}%**")
            elif current_total_pct > 100.0:
                st.sidebar.error(f" 当前总比例：**{current_total_pct:.1f}%** (已超出 **{current_total_pct - 100.0:.1f}%**)！")
            else:
                st.sidebar.warning(f" 当前总比例：**{current_total_pct:.1f}%** (还差 **{100.0 - current_total_pct:.1f}%**)！")
        else:
            diff_amt = p_budget_amount - current_total_amt
            if abs(diff_amt) < 0.01:
                st.sidebar.success(f" 当前总数量：**{int(current_total_amt):,}** (已完美对齐总预算！)")
            elif diff_amt < 0:
                st.sidebar.error(f" 当前总数量：**{int(current_total_amt):,}** (超出了 **{int(abs(diff_amt)):,}** {ticker_upper})！")
            else:
                st.sidebar.warning(f" 当前总数量：**{int(current_total_amt):,}** (还剩 **{int(diff_amt):,}** {ticker_upper} 未分配)！")
else:
    # 彻底关闭预算状态
    st.sidebar.info("已选【无预算模式】，输出模版将自动置为：'暂无，请各业务线自行安排。'")
    p_budget_amount = 0
    p_price = "0"
    activity_list = []

# ==================================================================================

current_user_ticker = p_ticker.strip().upper() if p_ticker.strip() else ""
display_ticker = current_user_ticker if current_user_ticker else "{{ticker}}"
default_pools = [
    {"Supported Pools": "KCS", "Total Rewards (%)": 50},
    {"Supported Pools": "USDG", "Total Rewards (%)": 30},
    {"Supported Pools": display_ticker, "Total Rewards (%)": 20}
]

gempool_dynamic_table_markdown = ""
gempool_hard_cap_section_text = ""
current_total_supply = "TBD"
display_total_rewards = "TBD"
g_start_utc = "TBD"
g_end_utc = "TBD"
dynamic_pool_text = "KCS and USDG"

# 默认提供标准的本地 UTC+8 格式供运营直接使用
hodler_snapshot_val = "2026-05-22 16:00 to 2026-05-27 16:00 (UTC+8)"

if is_gempool_mode:
    st.sidebar.subheader(" GemPool 专属配置看板")
    g_total_supply = st.sidebar.text_input("项目总供应量 (Total Supply)", value="")
    
    if "gempool_rewards_raw" not in st.session_state:
        st.session_state["gempool_rewards_raw"] = ""
    g_rewards_text = st.sidebar.text_input("GemPool 总奖池数量", value=st.session_state["gempool_rewards_raw"])
    g_total_rewards, formatted_g_rewards = parse_and_format_int(g_rewards_text, default_val=100000)
    st.session_state["gempool_rewards_raw"] = formatted_g_rewards
    
    g_duration = st.sidebar.number_input("挖矿持续天数", min_value=1, value=7, step=1)
    g_start_time_raw = st.sidebar.text_input("挖矿开始时间 (如：2026-05-28 16:00)", value="2026-05-28 16:00")
    st.sidebar.markdown("##### 质押池分配比例表")
    gempool_pools_data = st.sidebar.data_editor(default_pools, num_rows="dynamic", key="gempool_table_editor")

elif is_hodler_mode:
    st.sidebar.subheader(" HODLer参数配置")
    g_total_supply = st.sidebar.text_input("项目总供应量 (Total Supply)", value="", key="hodler_total_supply_input")
    
    if "hodler_rewards_raw" not in st.session_state:
        st.session_state["hodler_rewards_raw"] = "0"
    h_rewards_text = st.sidebar.text_input("HODLer 总奖池数量", value=st.session_state["hodler_rewards_raw"])
    hodler_total_rewards, formatted_h_rewards = parse_and_format_int(h_rewards_text, default_val=0)
    st.session_state["hodler_rewards_raw"] = formatted_h_rewards
    
    # 引导文案更新为标准格式
    hodler_snapshot_val = st.sidebar.text_area("快照时间 (输入UTC+8时间，系统自动转换成UTC)", value=hodler_snapshot_val)


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
        dt_distribution_utc = dt_utc_trading - timedelta(hours=3)
        auto_distribution_str = dt_distribution_utc.strftime("%H:%M on %B %d, %Y (UTC)")
    else:
        auction_start_time, auction_end_time, auction_date = "TBD", "TBD", "TBD"
        auto_distribution_str = "3 hours before trading begins (UTC)"

    return {
        "trading_time_utc": trading_utc, "withdraw_time_UTC": withdraw_utc_cap, 
        "auction_start_time": auction_start_time, "auction_end_time": auction_end_time, "auction_date": auction_date,
        "hodler_distribution_time_calculated": auto_distribution_str
    }

# -----------------  右侧主展示区核心逻辑 -----------------
generate_clicked = st.sidebar.button(" 一键生成", type="primary", key="btn_trigger_submit_main")

if generate_clicked or "internal_val" in st.session_state:
    if generate_clicked:
        current_ticker = p_ticker.strip().upper() if p_ticker.strip() else "TOKEN"
        raw_supply = str(g_total_supply).strip() if 'g_total_supply' in locals() else ""
        current_total_supply = f"{int(raw_supply.replace(',', '')):,}" if raw_supply.replace(',', '').isdigit() else (raw_supply if raw_supply else "TBD")

        if is_gempool_mode:
            current_duration = int(g_duration) if 'g_duration' in locals() else 7
            current_pools = gempool_pools_data if ('gempool_pools_data' in locals() and gempool_pools_data is not None) else []
            
            def parse_local_time(t_str):
                for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"):
                    try: return datetime.strptime(t_str.strip(), fmt)
                    except: continue
                return None

            dt_gempool_start = parse_local_time(g_start_time_raw)
            dt_trade = parse_local_time(p_trading_time)
            display_total_rewards = f"{g_total_rewards:,}" if g_total_rewards > 0 else "TBD"

            table_lines = [
                f"| Supported Pools | Total Rewards ({current_ticker}) | Farming Period (UTC) |",
                "| :---: | :---: | :---: |"
            ]
            hard_cap_lines = ["5. Hourly Reward Hard Cap Per User:"]
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            
            valid_rows = []
            pool_names = []
            if current_pools:
                for row in current_pools:
                    if not isinstance(row, dict): continue
                    token = str(row.get("Supported Pools", "") or "").strip().upper()
                    if not token: continue
                    if token in ["PROJECT_TICKER", "{{TICKER}}"]: token = current_ticker
                    pct = float(row.get("Total Rewards (%)", 0) or 0)
                    valid_rows.append({"token": token, "pct": pct})
                    if token not in pool_names: pool_names.append(token)

            total_calculated = 0
            calculated_amts = []
            for row in valid_rows:
                allocated_amt = int(g_total_rewards * (row["pct"] / 100)) if g_total_rewards > 0 else 0
                calculated_amts.append(allocated_amt)
                total_calculated += allocated_amt
            if (g_total_rewards - total_calculated) != 0 and len(calculated_amts) > 0:
                calculated_amts[0] += (g_total_rewards - total_calculated)

            calculated_utc_starts = []
            calculated_utc_ends = []

            for idx, row in enumerate(valid_rows):
                token = row["token"]
                amt = calculated_amts[idx]
                pool_start_dt = dt_trade if token == current_ticker else dt_gempool_start
                
                if pool_start_dt:
                    pool_end_dt = pool_start_dt + timedelta(days=current_duration)
                    utc_start = pool_start_dt - timedelta(hours=8)
                    utc_end = pool_end_dt - timedelta(hours=8)
                    calculated_utc_starts.append(utc_start)
                    calculated_utc_ends.append(utc_end)
                    pool_utc_range = f"{utc_start.strftime('%Y-%m-%d %H:%M')} - {utc_end.strftime('%Y-%m-%d %H:%M')}"
                else:
                    pool_utc_range = "TBD"

                if g_total_rewards > 0 and amt > 0 and current_duration > 0:
                    hourly_cap = (amt * 0.10) / float(current_duration) / 24.0
                    cap_str = f"{int(round(hourly_cap)):,}"
                    amt_str = f"{amt:,}"
                else:
                    cap_str, amt_str = "TBD", "TBD"
                
                table_lines.append(f"| {token} | {amt_str} | {pool_utc_range} |")
                hard_cap_lines.append(f'<div style="margin-left: 20px; margin-top: 4px;">{alphabet[idx % len(alphabet)]}. {token} Pool: {cap_str} {current_ticker}</div>')
            
            gempool_dynamic_table_markdown = "\n".join(table_lines)
            gempool_hard_cap_section_text = "\n".join(hard_cap_lines)

            if calculated_utc_starts and calculated_utc_ends:
                g_start_utc = min(calculated_utc_starts).strftime("%H:%M on %B %d, %Y (UTC)")
                g_end_utc = max(calculated_utc_ends).strftime("%H:%M on %B %d, %Y (UTC)")

            if len(pool_names) == 1: dynamic_pool_text = pool_names[0]
            elif len(pool_names) == 2: dynamic_pool_text = f"{pool_names[0]} and {pool_names[1]}"
            else: dynamic_pool_text = ", ".join(pool_names[:-1]) + f" and {pool_names[-1]}"

        if has_budget:
            budget_lines = []
            for act in activity_list:
                val = activity_values.get(act, 0)
                budget_lines.append(f"- {act}：{int(val):,} {current_ticker}" if val > 0 else f"- {act}：")
            marketing_budget_section = "\n".join(budget_lines)
            display_budget_amount = f"{p_budget_amount:,}"
            display_price = p_price
        else:
            marketing_budget_section = "暂无，请各业务线自行安排。"
            display_budget_amount = "0"
            display_price = "0"
        
        times_data = get_announcement_times(p_trading_time, p_withdraw_time)
        generated_deposit_link = f"https://www.kucoin.com/assets/coin/{p_ticker.strip()}" if p_ticker.strip() else "https://www.kucoin.com/assets/coin"

        link_items = []
        for l_val, l_name in [(p_website, "Website"), (p_twitter, "X (Twitter)"), (p_whitepaper, "Whitepaper"), (p_contract, "Token Contract")]:
            if l_val.strip(): link_items.append(f"[{l_name}]({l_val.strip()})")
        official_links_section = " | ".join(link_items)

        world_premiere_tag = "World Premiere: " if "首发" in p_lst_type_main.strip() else ""
        display_hodler_rewards = f"{int(hodler_total_rewards):,}" if is_hodler_mode and hodler_total_rewards > 0 else "0"

        # 调用自动转换函数，将标准时间输入转换成符合要求的官方英文时区格式
        final_hodler_snapshot = convert_snapshot_time_to_utc(hodler_snapshot_val) if is_hodler_mode else ""

        data = {
            "has_budget": has_budget,  
            "project_name": p_name, "ticker": p_ticker, "fee_level": p_fee_level, "network": p_network,
            "lst_type_main": p_lst_type_main, "lst_type_sub": p_lst_type_sub, "op_level": p_op_level, "website": p_website,
            "project_intro_cn": p_intro_cn, "project_intro_en": p_intro_en, "ann_time": p_ann_time,
            "trading_time": p_trading_time, "withdraw_time": p_withdraw_time, "budget_amount": display_budget_amount, 
            "price": display_price, "marketing_budget_section": marketing_budget_section, "deposit_dynamic_link": generated_deposit_link,
            "world_premiere_tag": world_premiere_tag, "official_links_section": official_links_section,
            "total_supply": current_total_supply, "total_rewards": display_total_rewards,
            "start_time_simple": g_start_utc, "end_time_simple": g_end_utc,
            "gempool_dynamic_table": gempool_dynamic_table_markdown, "gempool_hard_cap_section": gempool_hard_cap_section_text,
            "dynamic_pool_text": dynamic_pool_text, "submit_deadline_time": submit_deadline_str, 
            "hodler_rewards": display_hodler_rewards, "hodler_snapshot_period": final_hodler_snapshot,
            "hodler_distribution_time": times_data.get("hodler_distribution_time_calculated", ""), **times_data 
        }
        
        st.session_state["internal_val"] = Template(INTERNAL_TEMPLATE).render(data)
        st.session_state["public_val"] = Template(PUBLIC_ANNOUNCEMENT_TEMPLATE).render(data)
        st.session_state["gempool_val"] = Template(PUBLIC_GEMPOOL_TEMPLATE).render(data)
        st.session_state["hodler_combined_val"] = Template(PUBLIC_HODLER_COMBINED_TEMPLATE).render(data)

    st.write("###  自动化内容输出成功！请注意校对！")
    allow_edit = st.checkbox(" 开启实时编辑模式（进行微调与校对）", value=False)
    
    if is_hodler_mode:
        tabs = st.tabs(["内部同步信息", "HODLer上币公告"])
        with tabs[0]:
            if allow_edit: st.session_state["internal_val"] = st.text_area("内部同步信息", value=st.session_state["internal_val"], height=600, key="ed_int", label_visibility="collapsed")
            else: st.markdown(st.session_state["internal_val"], unsafe_allow_html=True)
        with tabs[1]:
            if allow_edit: st.session_state["hodler_combined_val"] = st.text_area("HODLer公告", value=st.session_state["hodler_combined_val"], height=600, key="ed_hod", label_visibility="collapsed")
            else: st.markdown(st.session_state["hodler_combined_val"])
    elif is_gempool_mode:
        tabs = st.tabs(["内部同步信息", "上币公告", "GemPool活动公告"])
        with tabs[0]:
            if allow_edit: st.session_state["internal_val"] = st.text_area("内部同步", value=st.session_state["internal_val"], height=600, key="ed_g_int", label_visibility="collapsed")
            else: st.markdown(st.session_state["internal_val"], unsafe_allow_html=True)
        with tabs[1]:
            if allow_edit: st.session_state["public_val"] = st.text_area("上币公告", value=st.session_state["public_val"], height=600, key="ed_g_pub", label_visibility="collapsed")
            else: st.markdown(st.session_state["public_val"])
        with tabs[2]:
            if allow_edit: st.session_state["gempool_val"] = st.text_area("GemPool", value=st.session_state["gempool_val"], height=600, key="ed_g_gem", label_visibility="collapsed")
            else: st.markdown(st.session_state["gempool_val"], unsafe_allow_html=True)
    else:
        tabs = st.tabs(["内部同步信息", "上币公告"])
        with tabs[0]:
            if allow_edit: st.session_state["internal_val"] = st.text_area("内部", value=st.session_state["internal_val"], height=600, key="ed_n_int", label_visibility="collapsed")
            else: st.markdown(st.session_state["internal_val"], unsafe_allow_html=True)
        with tabs[1]:
            if allow_edit: st.session_state["public_val"] = st.text_area("公告", value=st.session_state["public_val"], height=600, key="ed_n_pub", label_visibility="collapsed")
            else: st.markdown(st.session_state["public_val"])