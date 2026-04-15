
"""
Gap Analysis in Asset Liability Management (ALM)
The Mountain Path Academy — World of Finance
Prof. V. Ravichandran
https://themountainpathacademy.com
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ─── Page Config ───
st.set_page_config(
    page_title="Gap Analysis in ALM | The Mountain Path Academy",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Mountain Path Design System ───
GOLD = "#FFD700"
BLUE = "#003366"
MID_BLUE = "#004d80"
CARD_BG = "#112240"
TEXT = "#e6f1ff"
MUTED = "#8892b0"
GREEN = "#28a745"
RED = "#dc3545"
LIGHT_BLUE = "#ADD8E6"
ORANGE = "#FF8C00"
PURPLE = "#7B1FA2"
TEAL = "#00796B"
BG_GRADIENT = "linear-gradient(135deg,#1a2332,#243447,#2a3f5f)"

# ─── Custom CSS ───
st.html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');

    .stApp {{
        background: {BG_GRADIENT};
        font-family: 'Source Sans 3', sans-serif;
    }}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0a1628, #112240, #1a2332) !important;
        border-right: 2px solid {GOLD} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label {{
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
        font-weight: 600 !important;
    }}

    /* Hide default streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 4px;
        background: rgba(17,34,64,0.6);
        border-radius: 12px;
        padding: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 8px;
        color: {MUTED} !important;
        -webkit-text-fill-color: {MUTED} !important;
        font-weight: 600;
        padding: 8px 16px;
    }}
    .stTabs [aria-selected="true"] {{
        background: {BLUE} !important;
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
        border-bottom: 2px solid {GOLD} !important;
    }}

    /* Metric styling */
    [data-testid="stMetric"] {{
        background: {CARD_BG};
        border: 1px solid rgba(255,215,0,0.15);
        border-radius: 12px;
        padding: 16px;
    }}
    [data-testid="stMetric"] label {{
        color: {MUTED} !important;
        -webkit-text-fill-color: {MUTED} !important;
        font-size: 0.85rem !important;
    }}
    [data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
        font-family: 'Playfair Display', serif !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: {CARD_BG} !important;
        border: 1px solid rgba(255,215,0,0.2) !important;
        border-radius: 8px !important;
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}

    /* Dataframe */
    .stDataFrame {{
        border: 1px solid rgba(255,215,0,0.15);
        border-radius: 8px;
    }}

    /* Slider */
    .stSlider [data-baseweb="slider"] [role="slider"] {{
        background: {GOLD} !important;
    }}
</style>
""")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA LAYER — All data from the Excel workbook
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BUCKETS = ["1-14D", "15-28D", "29D-3M", "3-6M", "6M-1Y", "1-3Y", "3-5Y", ">5Y"]

# Balance Sheet
ASSETS_DATA = {
    "Cash & Central Bank":       [5500, 1500, 1000, 500,  0,     0,     0,     0],
    "Government Securities":     [1000, 1000, 2500, 3000, 4000,  5500,  3000,  2000],
    "Loans & Advances":          [2000, 2500, 5000, 7000, 9000,  14000, 9500,  6000],
    "Interbank Placements":      [2500, 1500, 1200, 500,  200,   100,   0,     0],
    "Fixed Assets & Others":     [0,    0,    0,    0,    0,     0,     500,   3000],
}

LIABILITIES_DATA = {
    "Demand Deposits (CASA)":   [4200, 2800, 5600, 4200, 4200, 4200, 1400, 1400],
    "Term Deposits":            [2000, 2500, 5000, 6000, 7500, 7000, 3000, 2000],
    "Borrowings (Interbank)":   [3000, 2500, 2500, 2000, 1000, 500,  300,  200],
    "Other Liabilities":        [500,  500,  500,  500,  500,  500,  500,  500],
    "Shareholders' Equity":     [0,    0,    0,    0,    0,    0,    0,    16000],
}

# Rate Sensitivity
RSA_DATA = {
    "Cash & CB (O/N rate)":         [5500, 1500, 1000, 0,    0,    0,    0,    0],
    "Govt Securities (Maturing)":   [1000, 1000, 2500, 3000, 4000, 5500, 3000, 2000],
    "Loans — Floating (Repricing)": [3500, 2000, 8000, 5500, 4000, 3000, 1500, 500],
    "Loans — Fixed (Maturing)":     [500,  1000, 2500, 3000, 4500, 6500, 4000, 5000],
    "Interbank Placements":         [2500, 1500, 1200, 500,  200,  100,  0,    0],
}

RSL_DATA = {
    "CASA (Discretionary)":         [4200, 2800, 5600, 4200, 4200, 4200, 1400, 1400],
    "Term Deposits (Maturing)":     [2000, 2500, 5000, 6000, 7500, 7000, 3000, 2000],
    "Interbank Borrowings":         [3000, 2500, 2500, 2000, 1000, 500,  300,  200],
    "Other Rate-Sensitive":         [300,  200,  300,  200,  300,  200,  200,  200],
}

# Interest Rates
ASSET_RATES = {
    "Cash & Central Bank": {"rate": 0.04, "type": "Fixed", "freq": "Overnight", "amount": 8500},
    "Government Securities": {"rate": 0.065, "type": "Fixed", "freq": "At Maturity", "amount": 22000},
    "Loans (Fixed Rate)": {"rate": 0.0875, "type": "Fixed", "freq": "At Maturity", "amount": 27000},
    "Loans (Floating Rate)": {"rate": 0.092, "type": "Floating", "freq": "Quarterly", "amount": 28000},
    "Interbank Placements": {"rate": 0.055, "type": "Fixed", "freq": "Monthly", "amount": 6000},
}

LIABILITY_RATES = {
    "Demand Deposits (CASA)": {"rate": 0.035, "type": "Floating", "freq": "Discretionary", "amount": 28000},
    "Term Deposits": {"rate": 0.065, "type": "Fixed", "freq": "At Maturity", "amount": 35000},
    "Borrowings (Interbank)": {"rate": 0.058, "type": "Floating", "freq": "Monthly", "amount": 12000},
    "Other Liabilities": {"rate": 0.02, "type": "Fixed", "freq": "N/A", "amount": 4000},
}

# Q&A Data
QA_DATA = {
    "General ALM Concepts": [
        ("What is Asset Liability Management (ALM)?",
         "ALM is a risk management framework used by banks and financial institutions to manage the risks arising from mismatches between assets and liabilities. It focuses on two primary risks: (1) Liquidity Risk — the risk that maturing liabilities exceed maturing assets in any time period, creating a funding gap; and (2) Interest Rate Risk — the risk that changes in market interest rates adversely affect the bank's net interest income (NII) or economic value of equity (EVE). ALM ensures the bank can meet its obligations while optimizing profitability."),
        ("What is a Gap Analysis in ALM?",
         "Gap Analysis is the foundational ALM tool that compares the maturity (or repricing) profile of assets against liabilities across defined time buckets. The 'gap' in each bucket equals Assets minus Liabilities. A POSITIVE gap means assets exceed liabilities (asset-heavy), while a NEGATIVE gap means liabilities exceed assets (liability-heavy). The analysis is performed in two forms: (1) Structural Liquidity Gap — based on contractual maturity, and (2) Interest Rate Sensitivity Gap — based on repricing dates for rate-sensitive items."),
        ("What are the standard RBI/Basel time buckets?",
         "The model uses 8 standard maturity buckets prescribed by RBI and aligned with Basel III: (1) 1-14 Days, (2) 15-28 Days, (3) 29 Days to 3 Months, (4) 3-6 Months, (5) 6 Months to 1 Year, (6) 1-3 Years, (7) 3-5 Years, (8) Over 5 Years. These capture short-term liquidity exposure (buckets 1-3), medium-term funding gaps (buckets 4-5), and long-term structural mismatches (buckets 6-8)."),
        ("Why is ALM important for banks?",
         "Banks inherently borrow short (deposits) and lend long (loans/mortgages), creating a natural maturity mismatch. ALM is critical because: (1) Regulatory compliance — Basel III and local regulators mandate ALM reporting; (2) Earnings protection — mismatches expose NII to rate volatility; (3) Liquidity management — ensures meeting withdrawal demands; (4) Capital adequacy — EVE impact affects economic capital; (5) Strategic planning — informs asset/liability mix and pricing."),
    ],
    "Liquidity Gap Analysis": [
        ("What is the Structural Liquidity Gap?",
         "The Structural Liquidity Gap (Maturity Gap) shows the difference between assets and liabilities maturing in each time bucket based on contractual maturity. Formula: Periodic Gap = Total Assets Maturing – Total Liabilities Maturing. A negative gap indicates a net cash outflow — the bank needs to raise funds or roll over maturing liabilities."),
        ("What is Periodic Gap vs. Cumulative Gap?",
         "PERIODIC GAP: The net difference in a SINGLE time bucket — funding surplus or deficit for that specific period. CUMULATIVE GAP: The running total of all periodic gaps from bucket 1 to current. Formula: Cumulative Gap(t) = Cumulative Gap(t-1) + Periodic Gap(t). The cumulative gap is more important because it shows total net funding position up to each point. A persistently negative cumulative gap signals structural funding dependency."),
        ("Why do some buckets show negative gaps?",
         "This is the natural consequence of bank business models. Short-term buckets typically show negative gaps because: (a) Deposits (especially CASA) are classified in short-term buckets as they can be withdrawn anytime, (b) A large portion of loans have longer maturities (1-5+ years). Long-term buckets show positive gaps because loan portfolios mature in these tenors. This 'borrow short, lend long' pattern is how banks earn the term premium but creates liquidity risk."),
        ("What does cumulative gap of ($6,100mm) at 6M-1Y mean?",
         "Over the next 12 months, the bank's maturing liabilities exceed maturing assets by $6.1 billion (6.4% of total assets). The bank must fund this through: (1) New deposit acquisition, (2) Rolling over term deposits, (3) Interbank borrowing, (4) Selling/repo-ing liquid securities, or (5) Central bank facilities. While within the regulatory limit (<15%), it requires active liquidity management."),
    ],
    "Rate Sensitivity Gap": [
        ("What is the difference between Liquidity Gap and Rate Sensitivity Gap?",
         "LIQUIDITY GAP classifies ALL items by contractual maturity date — when cash flows occur. It measures funding risk. RATE SENSITIVITY GAP classifies only RATE-SENSITIVE items by next repricing date — when the interest rate resets. Key difference: A 10-year floating-rate loan repricing quarterly appears in '29D-3M' for rate sensitivity but '>5Y' for liquidity. Non-rate-sensitive items (equity, fixed assets) may be excluded."),
        ("What are RSA and RSL?",
         "RSA (Rate-Sensitive Assets): Assets whose income changes with market rates — floating-rate items (repricing) or maturing fixed-rate items (reinvested). Total RSA = $91B. RSL (Rate-Sensitive Liabilities): Liabilities whose cost changes with rates. Total RSL = $76.9B. Equity ($16B) is excluded from RSL as it has no interest cost."),
        ("What does RSA/RSL Ratio of 1.06x mean?",
         "Rate-sensitive assets exceed liabilities by 6% within 1 year, making the bank ASSET-SENSITIVE. When rates RISE → asset yields increase faster than liability costs → NII INCREASES. When rates FALL → asset yields decline faster → NII DECREASES. Prudent range: 0.80x–1.20x. At 1.06x, the position is within prudent limits."),
        ("How are floating vs. fixed-rate loans classified?",
         "FLOATING-RATE LOANS ($28B): Classified by REPRICING DATE. A 20-year quarterly floating mortgage goes in '29D-3M' bucket. FIXED-RATE LOANS ($27B): Classified by MATURITY DATE. The rate is locked until maturity. A 5-year fixed loan at 8.75% stays at that rate regardless of market movements. The split determines how responsive the bank's asset yield is to rate changes."),
    ],
    "NII Impact & Earnings at Risk": [
        ("How is Base NII ($3,005mm) calculated?",
         "Interest Income: Cash×4.00% + Govt Sec×6.50% + Loans×~8.98% + Interbank×5.50% = $7,038mm. Interest Expense: CASA×3.50% + Term Dep×6.50% + Borrowings×5.80% + Other×2.00% = $4,031mm. Base NII = $7,038 – $4,031 = $3,005mm. NIM = $3,005/$95,000 = 3.16%."),
        ("How is NII Impact (Earnings at Risk) calculated?",
         "ΔNII = Cumulative 1-Year Rate Gap × Rate Change. With gap of $3,600mm: +200bps → +$72mm; +100bps → +$36mm; -100bps → -$36mm; -200bps → -$72mm. This is a simplified linear approximation. In practice, banks account for optionality, basis risk, and non-parallel shifts."),
        ("What does NII at Risk of 0.45% of Equity mean?",
         "A +200bps shock changes NII by $72mm, which is only 0.45% of the bank's $16B equity. This is well within the typical <5% threshold. The bank's capital can easily absorb earnings volatility, there's substantial headroom, and the bank could take on more rate risk if strategically desired."),
        ("What does 'Parallel Shift' mean?",
         "ALL rates across the entire yield curve move by the same amount simultaneously. A simplification. Basel IRRBB also tests: Steepening (short unchanged, long up), Flattening (short up, long unchanged), Inversion (short above long), Short rate shocks, and Basis shocks (SOFR vs T-bill spread widens). The ±200bps range aligns with Basel IRRBB prescribed scenarios."),
    ],
    "Dashboard & Regulatory": [
        ("What does Short-Term Gap / Total Assets of -4.6% tell us?",
         "Measures the bank's immediate liquidity exposure over the next 3 months. Threshold: > -10%. At -4.6%, the bank has adequate short-term liquidity but relies on rolling short-term funding. A breach (below -10%) would indicate severe near-term funding stress."),
        ("What is the NIM of 3.16% and is it good?",
         "NIM = NII / Total Assets = $3,005mm / $95,000mm = 3.16%. This is the most fundamental bank profitability metric. Threshold: > 2.00% minimum; most healthy banks target 2.50%-3.50%. At 3.16%, the bank has a healthy NIM indicating good spread between asset yields (~7.4%) and liability costs (~4.2%)."),
        ("How should RSA/RSL range of 0.80x-1.20x be interpreted?",
         "<0.80x = Heavily liability-sensitive; 0.80x-0.90x = Moderately liability-sensitive; 0.90x-1.10x = Nearly balanced (ideal); 1.10x-1.20x = Moderately asset-sensitive; >1.20x = Heavily asset-sensitive. At 1.06x, the bank has a slight asset-sensitive tilt, favorable in a rising rate environment."),
        ("What actions can the ALCO take?",
         "LIQUIDITY: Adjust deposit pricing, establish credit lines, maintain liquid securities buffer. RATE MANAGEMENT: If expecting rate cuts → shift to fixed loans, floating borrowings, pay-floating swaps. If expecting hikes → maintain asset-sensitive position, lock in fixed funding. OPTIMIZATION: Improve CASA ratio, diversify funding, align asset origination tenors with funding."),
    ],
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def compute_gaps(assets_dict, liabilities_dict):
    total_assets = [sum(x) for x in zip(*assets_dict.values())]
    total_liabilities = [sum(x) for x in zip(*liabilities_dict.values())]
    periodic_gap = [a - l for a, l in zip(total_assets, total_liabilities)]
    cumulative_gap = []
    running = 0
    for g in periodic_gap:
        running += g
        cumulative_gap.append(running)
    return total_assets, total_liabilities, periodic_gap, cumulative_gap


def format_num(val, prefix="$", suffix="mm"):
    if val >= 0:
        return f"{prefix}{val:,.0f}{suffix}"
    else:
        return f"({prefix}{abs(val):,.0f}{suffix})"


def make_plotly_theme():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(17,34,64,0.4)",
        font=dict(family="Source Sans 3, sans-serif", color=TEXT),
        xaxis=dict(gridcolor="rgba(136,146,176,0.15)", zerolinecolor=GOLD),
        yaxis=dict(gridcolor="rgba(136,146,176,0.15)", zerolinecolor=GOLD),
    )


def section_header(title, subtitle="", icon=""):
    st.html(f"""
    <div style="user-select:none; margin-bottom:20px;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;">
            <span style="font-size:1.8rem;">{icon}</span>
            <h2 style="margin:0; font-family:'Playfair Display',serif; font-weight:700;
                color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.7rem; letter-spacing:-0.5px;">
                {title}
            </h2>
        </div>
        {"<p style='margin:0 0 0 44px; color:" + MUTED + "; -webkit-text-fill-color:" + MUTED + "; font-size:0.95rem;'>" + subtitle + "</p>" if subtitle else ""}
        <div style="height:2px; background:linear-gradient(90deg, {GOLD}, transparent); margin-top:8px; border-radius:1px;"></div>
    </div>
    """)


def metric_card(label, value, threshold="", status="PASS", risk="Low"):
    status_color = GREEN if status == "PASS" else RED
    risk_colors = {"Low": GREEN, "Medium": ORANGE, "High": RED}
    rc = risk_colors.get(risk, MUTED)
    risk_icons = {"Low": "✅", "Medium": "⚠️", "High": "❌"}
    ri = risk_icons.get(risk, "")
    st.html(f"""
    <div style="user-select:none; background:{CARD_BG}; border:1px solid rgba(255,215,0,0.15);
        border-radius:12px; padding:18px; text-align:center; min-height:140px;
        display:flex; flex-direction:column; justify-content:center;">
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.8rem; font-weight:600;
            text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">{label}</div>
        <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;
            font-size:1.8rem; font-weight:700; margin-bottom:4px;">{value}</div>
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.75rem; margin-bottom:6px;">
            Threshold: {threshold}</div>
        <div style="display:flex; justify-content:center; gap:12px; font-size:0.8rem;">
            <span style="color:{status_color}; -webkit-text-fill-color:{status_color}; font-weight:700;">{status}</span>
            <span style="color:{rc}; -webkit-text-fill-color:{rc};">{ri} {risk}</span>
        </div>
    </div>
    """)


def info_card(title, content, border_color=GOLD):
    st.html(f"""
    <div style="user-select:none; background:{CARD_BG}; border-left:4px solid {border_color};
        border-radius:0 8px 8px 0; padding:16px 20px; margin:10px 0;">
        <div style="color:{border_color}; -webkit-text-fill-color:{border_color};
            font-weight:700; font-size:1rem; margin-bottom:8px; font-family:'Playfair Display',serif;">{title}</div>
        <div style="color:{TEXT}; -webkit-text-fill-color:{TEXT}; font-size:0.9rem; line-height:1.6;">{content}</div>
    </div>
    """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    st.html(f"""
    <div style="user-select:none; text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:2.2rem; margin-bottom:4px;">🏔️</div>
        <div style="font-family:'Playfair Display',serif; font-weight:700; font-size:1.2rem;
            color:{GOLD}; -webkit-text-fill-color:{GOLD}; letter-spacing:0.5px;">THE MOUNTAIN PATH</div>
        <div style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.75rem;
            letter-spacing:2px; text-transform:uppercase; margin-top:2px;">Academy — World of Finance</div>
        <div style="height:2px; background:linear-gradient(90deg, transparent, {GOLD}, transparent);
            margin:12px 20px 0 20px;"></div>
    </div>
    """)

    page = st.radio(
        "📑 Navigation",
        [
            "🏠 ALM Dashboard",
            "📊 Liquidity Gap Analysis",
            "📈 Rate Sensitivity Gap",
            "💰 NII Impact Simulator",
            "📋 Balance Sheet & Assumptions",
            "📚 ALM Knowledge Base",
        ],
        index=0,
    )

    st.html(f"""
    <div style="user-select:none; position:absolute; bottom:10px; left:0; right:0; padding:15px; text-align:center;
        border-top:1px solid rgba(255,215,0,0.15);">
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.7rem; margin-bottom:6px;">
            Prof. V. Ravichandran</div>
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.65rem; margin-bottom:4px;">
            NMIMS | BITS Pilani | RV Univ | GIM</div>
        <div style="display:flex; justify-content:center; gap:10px;">
            <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
                style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.7rem; text-decoration:none;">LinkedIn</a>
            <a href="https://github.com/trichyravis" target="_blank"
                style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.7rem; text-decoration:none;">GitHub</a>
        </div>
        <div style="margin-top:6px;">
            <a href="https://themountainpathacademy.com" target="_blank"
                style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.7rem; text-decoration:none;">
                themountainpathacademy.com</a>
        </div>
    </div>
    """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.html(f"""
<div style="user-select:none; background:linear-gradient(135deg, {BLUE}, {MID_BLUE}); border-radius:16px;
    padding:25px 35px; margin-bottom:25px; border:1px solid rgba(255,215,0,0.25);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:15px;">
        <div>
            <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;
                font-size:1.8rem; font-weight:700; letter-spacing:-0.5px;">
                Gap Analysis in Asset Liability Management</div>
            <div style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.95rem; margin-top:4px;">
                Sample National Bank · Report Date: 31-Mar-2025 · Currency: USD ($mm)</div>
        </div>
        <div style="text-align:right;">
            <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;
                font-size:2.2rem; font-weight:800;">$95,000</div>
            <div style="color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.8rem;">Total Assets ($mm)</div>
        </div>
    </div>
</div>
""")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: ALM DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if page == "🏠 ALM Dashboard":
    section_header("ALM Risk Dashboard", "Key risk metrics at a glance — all thresholds per RBI / Basel III", "📊")

    # Metric cards row 1
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Short-Term Gap (≤3M) / TA", "–4.6%", "> –10%", "PASS", "Medium")
    with c2:
        metric_card("Cum. 1-Year Gap / TA", "–6.4%", "> –15%", "PASS", "Medium")
    with c3:
        metric_card("RSA / RSL Ratio (1Y)", "1.06x", "0.80x – 1.20x", "PASS", "Low")
    with c4:
        metric_card("NII at Risk / Equity", "0.45%", "< 5.0%", "PASS", "Low")

    st.html("<div style='height:12px;'></div>")

    # Metric cards row 2
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        metric_card("NII at Risk / Base NII", "2.4%", "< 10.0%", "PASS", "Low")
    with c6:
        metric_card("Estimated Base NII", "$3,005mm", "—", "—", "—")
    with c7:
        metric_card("Net Interest Margin", "3.16%", "> 2.00%", "PASS", "Low")
    with c8:
        metric_card("Total Assets", "$95,000mm", "—", "—", "—")

    st.html("<div style='height:20px;'></div>")

    # Two charts side by side
    col_left, col_right = st.columns(2)

    with col_left:
        # Liquidity Gap Overview
        ta, tl, pg, cg = compute_gaps(ASSETS_DATA, LIABILITIES_DATA)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=BUCKETS, y=pg, name="Periodic Gap",
            marker=dict(color=[GREEN if v >= 0 else RED for v in pg], opacity=0.8),
            text=[format_num(v) for v in pg], textposition="outside", textfont=dict(size=9)))
        fig.add_trace(go.Scatter(x=BUCKETS, y=cg, name="Cumulative Gap", mode="lines+markers",
            line=dict(color=GOLD, width=3), marker=dict(size=8, color=GOLD)))
        fig.update_layout(**make_plotly_theme(), title=dict(text="Liquidity Gap Profile", font=dict(color=GOLD)),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)),
            height=380, margin=dict(l=50, r=20, t=50, b=60),
            yaxis_title="Gap ($mm)")
        fig.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Rate Sensitivity Gap Overview
        rsa_totals = [sum(x) for x in zip(*RSA_DATA.values())]
        rsl_totals = [sum(x) for x in zip(*RSL_DATA.values())]
        rate_pg = [a - l for a, l in zip(rsa_totals, rsl_totals)]
        rate_cg = []
        running = 0
        for g in rate_pg:
            running += g
            rate_cg.append(running)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=BUCKETS, y=rate_pg, name="Rate Gap",
            marker=dict(color=[TEAL if v >= 0 else ORANGE for v in rate_pg], opacity=0.8),
            text=[format_num(v) for v in rate_pg], textposition="outside", textfont=dict(size=9)))
        fig2.add_trace(go.Scatter(x=BUCKETS, y=rate_cg, name="Cumulative Rate Gap", mode="lines+markers",
            line=dict(color=ORANGE, width=3), marker=dict(size=8, color=ORANGE)))
        fig2.update_layout(**make_plotly_theme(), title=dict(text="Interest Rate Sensitivity Gap", font=dict(color=GOLD)),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)),
            height=380, margin=dict(l=50, r=20, t=50, b=60),
            yaxis_title="Gap ($mm)")
        fig2.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        st.plotly_chart(fig2, use_container_width=True)

    # Risk Assessment Summary
    st.html("<div style='height:10px;'></div>")
    info_card("📋 Overall Risk Assessment — Sample National Bank",
        "<b style='color:" + ORANGE + "; -webkit-text-fill-color:" + ORANGE + ";'>Liquidity Risk: MEDIUM</b> — "
        "Negative short-term gaps (1–14D to 3–6M) indicate outflows exceed inflows. "
        "Cumulative gap reaches –$6.1B at the 1-year mark — within limits but requiring active monitoring.<br><br>"
        "<b style='color:" + GREEN + "; -webkit-text-fill-color:" + GREEN + ";'>Interest Rate Risk: LOW</b> — "
        "The bank is asset-sensitive with positive 1-year rate gap of $3.6B. RSA/RSL ratio of 1.06x is well within "
        "prudent limits. NII at Risk is well below the 5% of equity threshold.<br><br>"
        "<b style='color:" + GREEN + "; -webkit-text-fill-color:" + GREEN + ";'>Overall:</b> "
        "All key risk metrics show PASS. The bank's ALM position is moderately balanced with manageable risk.",
        GREEN)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: LIQUIDITY GAP ANALYSIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📊 Liquidity Gap Analysis":
    section_header("Structural Liquidity Gap Analysis",
        "Maturity profile of ALL assets & liabilities by contractual maturity date", "📊")

    info_card("📘 What is the Structural Liquidity Gap?",
        "The structural liquidity gap distributes ALL assets and liabilities by their <b>contractual maturity date</b>. "
        "It answers: <i>\"In each future period, will the bank have enough maturing assets to cover maturing liabilities?\"</i>",
        MID_BLUE)

    ta, tl, pg, cg = compute_gaps(ASSETS_DATA, LIABILITIES_DATA)

    # Asset Maturity Profile
    tab1, tab2, tab3 = st.tabs(["📊 Gap Charts", "📋 Detailed Tables", "🔍 Ratio Analysis"])

    with tab1:
        # Stacked bar chart - Assets vs Liabilities
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Asset Maturity Profile", "Liability Maturity Profile"),
            horizontal_spacing=0.08)
        asset_colors = [MID_BLUE, TEAL, GREEN, LIGHT_BLUE, MUTED]
        for i, (name, vals) in enumerate(ASSETS_DATA.items()):
            fig.add_trace(go.Bar(x=BUCKETS, y=vals, name=name,
                marker_color=asset_colors[i % len(asset_colors)], opacity=0.85), row=1, col=1)
        
        liab_colors = [RED, ORANGE, PURPLE, MUTED, GOLD]
        for i, (name, vals) in enumerate(LIABILITIES_DATA.items()):
            fig.add_trace(go.Bar(x=BUCKETS, y=vals, name=name,
                marker_color=liab_colors[i % len(liab_colors)], opacity=0.85), row=1, col=2)

        fig.update_layout(**make_plotly_theme(), barmode="stack", height=420,
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, font=dict(size=9)),
            margin=dict(l=50, r=20, t=50, b=80))
        st.plotly_chart(fig, use_container_width=True)

        # Gap chart
        fig2 = go.Figure()
        colors_pg = [GREEN if v >= 0 else RED for v in pg]
        fig2.add_trace(go.Bar(x=BUCKETS, y=pg, name="Periodic Gap",
            marker=dict(color=colors_pg, opacity=0.8, line=dict(width=1, color="rgba(255,255,255,0.3)")),
            text=[format_num(v) for v in pg], textposition="outside", textfont=dict(size=10, color=TEXT)))
        fig2.add_trace(go.Scatter(x=BUCKETS, y=cg, name="Cumulative Gap", mode="lines+markers+text",
            line=dict(color=GOLD, width=3), marker=dict(size=10, color=GOLD, line=dict(width=2, color=BLUE)),
            text=[format_num(v) for v in cg], textposition="top center", textfont=dict(size=9, color=GOLD)))
        fig2.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        fig2.update_layout(**make_plotly_theme(),
            title=dict(text="Liquidity Gap — Periodic & Cumulative ($mm)", font=dict(color=GOLD, size=16)),
            height=420, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="Gap ($mm)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        # Asset table
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Asset Maturity Profile ($mm)</h4>")
        asset_df = pd.DataFrame(ASSETS_DATA, index=BUCKETS).T
        asset_df["Total"] = asset_df.sum(axis=1)
        totals_row = pd.DataFrame(asset_df.sum()).T
        totals_row.index = ["TOTAL ASSETS"]
        asset_df = pd.concat([asset_df, totals_row])
        st.dataframe(asset_df.style.format("{:,.0f}"), use_container_width=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Liability Maturity Profile ($mm)</h4>")
        liab_df = pd.DataFrame(LIABILITIES_DATA, index=BUCKETS).T
        liab_df["Total"] = liab_df.sum(axis=1)
        totals_row2 = pd.DataFrame(liab_df.sum()).T
        totals_row2.index = ["TOTAL LIABILITIES"]
        liab_df = pd.concat([liab_df, totals_row2])
        st.dataframe(liab_df.style.format("{:,.0f}"), use_container_width=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Gap Analysis Results ($mm)</h4>")
        gap_df = pd.DataFrame({
            "Periodic Gap": pg,
            "Cumulative Gap": cg,
            "Gap % of Total Assets": [g / 95000 * 100 for g in pg],
            "Cum Gap % of Total Assets": [g / 95000 * 100 for g in cg],
        }, index=BUCKETS).T
        st.dataframe(gap_df.style.format("{:,.1f}"), use_container_width=True)

    with tab3:
        # Ratio analysis
        gap_pct = [g / 95000 * 100 for g in pg]
        cum_gap_pct = [g / 95000 * 100 for g in cg]
        outflow_pct = [g / l * 100 if l != 0 else 0 for g, l in zip(pg, tl)]

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=BUCKETS, y=gap_pct, name="Gap % of Total Assets",
            marker_color=MID_BLUE, opacity=0.7))
        fig3.add_trace(go.Scatter(x=BUCKETS, y=cum_gap_pct, name="Cum Gap % of TA",
            mode="lines+markers", line=dict(color=GOLD, width=3), marker=dict(size=8)))

        # Threshold lines
        fig3.add_hline(y=-10, line_dash="dash", line_color=RED, line_width=1.5,
            annotation_text="Short-term threshold: -10%", annotation_position="bottom right",
            annotation_font=dict(color=RED, size=10))
        fig3.add_hline(y=-15, line_dash="dash", line_color=RED, line_width=2,
            annotation_text="RBI/Basel limit: -15%", annotation_position="bottom right",
            annotation_font=dict(color=RED, size=10))
        fig3.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)

        fig3.update_layout(**make_plotly_theme(),
            title=dict(text="Gap Ratios vs Regulatory Thresholds (%)", font=dict(color=GOLD, size=16)),
            height=420, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="Gap as % of Total Assets",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig3, use_container_width=True)

        info_card("⚠️ The Funding Valley",
            "The cumulative gap reaches its deepest point of <b style='color:" + RED + "; -webkit-text-fill-color:" + RED + ";'>($6,100mm)</b> "
            "at the 6M–1Y mark, representing <b>6.4% of total assets</b>. While within the RBI limit of 15%, "
            "this requires active liquidity management including deposit campaigns, committed credit lines, and "
            "contingency funding plans.", ORANGE)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: RATE SENSITIVITY GAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📈 Rate Sensitivity Gap":
    section_header("Interest Rate Sensitivity Gap Analysis",
        "Rate-sensitive assets vs liabilities by next repricing date", "📈")

    info_card("📘 Liquidity Gap vs Rate Sensitivity Gap — The Critical Distinction",
        "Liquidity Gap classifies ALL items by <b>contractual maturity</b> (when cash flows occur). "
        "Rate Sensitivity Gap classifies only <b>rate-sensitive items</b> by <b>next repricing date</b> (when rates reset). "
        "A 10-year floating loan repricing quarterly: Liquidity → '>5Y' bucket, Rate → '29D-3M' bucket.", MID_BLUE)

    rsa_totals = [sum(x) for x in zip(*RSA_DATA.values())]
    rsl_totals = [sum(x) for x in zip(*RSL_DATA.values())]
    rate_gap = [a - l for a, l in zip(rsa_totals, rsl_totals)]
    cum_rate_gap = []
    r = 0
    for g in rate_gap:
        r += g
        cum_rate_gap.append(r)
    rsa_rsl_ratio = [a / l if l != 0 else 0 for a, l in zip(rsa_totals, rsl_totals)]

    tab1, tab2, tab3 = st.tabs(["📊 Gap Charts", "📋 Detailed Tables", "📐 RSA/RSL Ratio"])

    with tab1:
        # RSA vs RSL grouped bar
        fig = go.Figure()
        fig.add_trace(go.Bar(x=BUCKETS, y=rsa_totals, name="RSA (Rate-Sensitive Assets)",
            marker_color=TEAL, opacity=0.8))
        fig.add_trace(go.Bar(x=BUCKETS, y=rsl_totals, name="RSL (Rate-Sensitive Liabilities)",
            marker_color=ORANGE, opacity=0.8))
        fig.update_layout(**make_plotly_theme(), barmode="group",
            title=dict(text="RSA vs RSL by Time Bucket ($mm)", font=dict(color=GOLD, size=16)),
            height=400, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="Amount ($mm)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)

        # Rate gap chart
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=BUCKETS, y=rate_gap, name="Rate Gap (RSA-RSL)",
            marker=dict(color=[TEAL if v >= 0 else RED for v in rate_gap], opacity=0.8),
            text=[format_num(v) for v in rate_gap], textposition="outside", textfont=dict(size=10)))
        fig2.add_trace(go.Scatter(x=BUCKETS, y=cum_rate_gap, name="Cumulative Rate Gap",
            mode="lines+markers", line=dict(color=ORANGE, width=3),
            marker=dict(size=10, color=ORANGE)))
        fig2.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        fig2.update_layout(**make_plotly_theme(),
            title=dict(text="Rate Sensitivity Gap — Periodic & Cumulative ($mm)", font=dict(color=GOLD, size=16)),
            height=400, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="Gap ($mm)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Rate-Sensitive Assets ($mm)</h4>")
        rsa_df = pd.DataFrame(RSA_DATA, index=BUCKETS).T
        rsa_df["Total"] = rsa_df.sum(axis=1)
        rsa_totals_row = pd.DataFrame(rsa_df.sum()).T
        rsa_totals_row.index = ["TOTAL RSA"]
        rsa_df = pd.concat([rsa_df, rsa_totals_row])
        st.dataframe(rsa_df.style.format("{:,.0f}"), use_container_width=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Rate-Sensitive Liabilities ($mm)</h4>")
        rsl_df = pd.DataFrame(RSL_DATA, index=BUCKETS).T
        rsl_df["Total"] = rsl_df.sum(axis=1)
        rsl_totals_row = pd.DataFrame(rsl_df.sum()).T
        rsl_totals_row.index = ["TOTAL RSL"]
        rsl_df = pd.concat([rsl_df, rsl_totals_row])
        st.dataframe(rsl_df.style.format("{:,.0f}"), use_container_width=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Gap Analysis Results</h4>")
        gap_results = pd.DataFrame({
            "Rate Gap (RSA-RSL)": rate_gap,
            "Cumulative Rate Gap": cum_rate_gap,
            "RSA/RSL Ratio": [f"{r:.2f}x" for r in rsa_rsl_ratio],
        }, index=BUCKETS).T
        st.dataframe(gap_results, use_container_width=True)

    with tab3:
        # RSA/RSL ratio chart with zones
        fig3 = go.Figure()

        # Zone shading
        fig3.add_hrect(y0=0, y1=0.80, fillcolor=RED, opacity=0.08, line_width=0,
            annotation_text="Heavily Liability-Sensitive", annotation_position="bottom left",
            annotation_font=dict(size=9, color=RED))
        fig3.add_hrect(y0=0.80, y1=0.90, fillcolor=ORANGE, opacity=0.06, line_width=0)
        fig3.add_hrect(y0=0.90, y1=1.10, fillcolor=GREEN, opacity=0.08, line_width=0,
            annotation_text="Neutral Zone", annotation_position="top left",
            annotation_font=dict(size=9, color=GREEN))
        fig3.add_hrect(y0=1.10, y1=1.20, fillcolor=ORANGE, opacity=0.06, line_width=0)
        fig3.add_hrect(y0=1.20, y1=2.1, fillcolor=RED, opacity=0.08, line_width=0,
            annotation_text="Heavily Asset-Sensitive", annotation_position="top left",
            annotation_font=dict(size=9, color=RED))

        fig3.add_trace(go.Scatter(x=BUCKETS, y=rsa_rsl_ratio, mode="lines+markers+text",
            name="RSA/RSL Ratio", line=dict(color=GOLD, width=3),
            marker=dict(size=12, color=GOLD, line=dict(width=2, color=BLUE)),
            text=[f"{r:.2f}x" for r in rsa_rsl_ratio], textposition="top center",
            textfont=dict(size=10, color=GOLD)))

        fig3.add_hline(y=1.0, line_dash="dash", line_color=GREEN, line_width=1)
        fig3.add_hline(y=0.80, line_dash="dot", line_color=ORANGE, line_width=1)
        fig3.add_hline(y=1.20, line_dash="dot", line_color=ORANGE, line_width=1)

        fig3.update_layout(**make_plotly_theme(),
            title=dict(text="RSA/RSL Ratio Across Time Buckets", font=dict(color=GOLD, size=16)),
            height=450, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="RSA / RSL Ratio",
            yaxis=dict(range=[0.5, 2.2], gridcolor="rgba(136,146,176,0.15)"),
            showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            info_card("🟢 Asset-Sensitive Position",
                "RSA/RSL = 1.06x (1-Year). Rates RISE → NII INCREASES. "
                "The bank benefits from rising rate environments.", GREEN)
        with col2:
            info_card("📊 Why RSA > RSL?",
                "Total RSA ($91B) exceeds RSL ($76.9B) by $14.1B. "
                "The difference is Shareholders' Equity ($16B) which has no interest cost.", LIGHT_BLUE)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: NII IMPACT SIMULATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "💰 NII Impact Simulator":
    section_header("NII Impact Simulator — Earnings at Risk",
        "Interactive rate shock analysis with customizable scenarios", "💰")

    # NII Calculation breakdown
    col1, col2 = st.columns(2)
    with col1:
        info_card("📥 Interest Income = $7,038mm",
            "Cash×4.00% = $340 · Govt Sec×6.50% = $1,430 · Loans×8.98% = $4,938 · Interbank×5.50% = $330", GREEN)
    with col2:
        info_card("📤 Interest Expense = $4,031mm",
            "CASA×3.50% = $980 · Term Dep×6.50% = $2,275 · Borrowings×5.80% = $696 · Other×2.00% = $80", RED)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Base NII", "$3,005mm")
    with c2:
        st.metric("Net Interest Margin", "3.16%")
    with c3:
        st.metric("Cum. 1-Year Rate Gap", "$3,600mm")

    st.html(f"<div style='height:15px;'></div>")

    # Interactive simulator
    st.html(f"""
    <div style="user-select:none; color:{GOLD}; -webkit-text-fill-color:{GOLD};
        font-family:'Playfair Display',serif; font-size:1.3rem; font-weight:700; margin-bottom:10px;">
        🎛️ Rate Shock Simulator</div>
    """)

    rate_shock = st.slider(
        "Parallel Rate Shock (basis points)",
        min_value=-300, max_value=300, value=200, step=25,
        help="Slide to simulate parallel interest rate changes"
    )

    cum_1y_gap = 3600  # $mm
    base_nii = 3005.25
    equity = 16000

    delta_nii = cum_1y_gap * (rate_shock / 10000)
    new_nii = base_nii + delta_nii
    pct_base_nii = delta_nii / base_nii * 100
    pct_equity = delta_nii / equity * 100

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Rate Shock", f"{'+' if rate_shock >= 0 else ''}{rate_shock} bps")
    with c2:
        color = "normal" if delta_nii >= 0 else "inverse"
        st.metric("ΔNII Impact", f"${delta_nii:+,.0f}mm", delta=f"{pct_base_nii:+.2f}% of Base NII")
    with c3:
        st.metric("New NII", f"${new_nii:,.0f}mm", delta=f"{delta_nii:+,.0f}mm")
    with c4:
        breach = abs(pct_equity) > 5
        st.metric("NII at Risk / Equity", f"{pct_equity:+.2f}%",
            delta="BREACH" if breach else "PASS")

    # Multi-scenario chart
    scenarios_bps = list(range(-300, 325, 25))
    nii_impacts = [cum_1y_gap * (s / 10000) for s in scenarios_bps]

    fig = go.Figure()
    colors = [GREEN if n >= 0 else RED for n in nii_impacts]
    fig.add_trace(go.Bar(x=[f"{s:+d}" for s in scenarios_bps], y=nii_impacts,
        marker=dict(color=colors, opacity=0.7),
        hovertemplate="Rate: %{x}bps<br>ΔNII: $%{y:,.0f}mm<extra></extra>"))

    # Highlight current selection
    current_impact = cum_1y_gap * (rate_shock / 10000)
    fig.add_trace(go.Scatter(x=[f"{rate_shock:+d}"], y=[current_impact], mode="markers",
        marker=dict(size=18, color=GOLD, symbol="diamond", line=dict(width=2, color=BLUE)),
        name=f"Selected: {rate_shock:+d}bps", showlegend=True))

    # Threshold lines
    fig.add_hline(y=equity * 0.05, line_dash="dash", line_color=RED, line_width=1.5,
        annotation_text="5% of Equity = $800mm", annotation_position="top right",
        annotation_font=dict(color=RED, size=10))
    fig.add_hline(y=-equity * 0.05, line_dash="dash", line_color=RED, line_width=1.5)
    fig.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)

    fig.update_layout(**make_plotly_theme(),
        title=dict(text="NII Impact Across Rate Shock Scenarios ($mm)", font=dict(color=GOLD, size=16)),
        height=420, margin=dict(l=50, r=20, t=60, b=60),
        xaxis_title="Rate Shock (bps)", yaxis_title="ΔNII ($mm)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)))
    st.plotly_chart(fig, use_container_width=True)

    # Standard scenarios table
    st.html(f"""<h4 style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;">
        Standard Rate Shock Scenarios</h4>""")
    scenarios = [200, 100, 0, -100, -200]
    scenario_data = []
    for s in scenarios:
        d = cum_1y_gap * (s / 10000)
        scenario_data.append({
            "Scenario": f"{'+' if s >= 0 else ''}{s} bps",
            "NII Impact ($mm)": f"${d:+,.0f}",
            "% of Base NII": f"{d / base_nii * 100:+.2f}%",
            "% of Equity": f"{d / equity * 100:+.2f}%",
            "Status": "PASS" if abs(d / equity * 100) < 5 else "BREACH"
        })
    st.dataframe(pd.DataFrame(scenario_data), use_container_width=True, hide_index=True)

    info_card("💡 Asset-Sensitive Interpretation",
        "The bank's <b>positive</b> 1-year rate gap of $3,600mm means it is <b>asset-sensitive</b>. "
        "Rising rates → NII increases (beneficial). Falling rates → NII decreases (harmful). "
        "At just 0.45% of equity for +200bps, there is substantial headroom before any regulatory concern.", GOLD)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: BALANCE SHEET & ASSUMPTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📋 Balance Sheet & Assumptions":
    section_header("Balance Sheet & Interest Rate Assumptions",
        "Sample National Bank — 31-Mar-2025", "📋")

    tab1, tab2 = st.tabs(["📊 Balance Sheet", "📐 Interest Rate Assumptions"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            # Asset pie chart
            asset_labels = ["Cash & CB", "Govt Securities", "Loans & Advances", "Interbank", "Fixed Assets"]
            asset_values = [8500, 22000, 55000, 6000, 3500]
            fig = go.Figure(go.Pie(
                labels=asset_labels, values=asset_values,
                hole=0.5, textinfo="label+percent",
                marker=dict(colors=[MID_BLUE, TEAL, GREEN, LIGHT_BLUE, MUTED],
                    line=dict(color=BLUE, width=2)),
                textfont=dict(size=11, color=TEXT)))
            fig.update_layout(**make_plotly_theme(),
                title=dict(text="Asset Composition ($95B)", font=dict(color=GOLD, size=15)),
                height=380, margin=dict(l=20, r=20, t=50, b=20),
                annotations=[dict(text="<b>$95B</b>", x=0.5, y=0.5, font_size=18, font_color=GOLD, showarrow=False)])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Liability pie chart
            liab_labels = ["CASA Deposits", "Term Deposits", "Borrowings", "Other Liabilities", "Equity"]
            liab_values = [28000, 35000, 12000, 4000, 16000]
            fig2 = go.Figure(go.Pie(
                labels=liab_labels, values=liab_values,
                hole=0.5, textinfo="label+percent",
                marker=dict(colors=[RED, ORANGE, PURPLE, MUTED, GOLD],
                    line=dict(color=BLUE, width=2)),
                textfont=dict(size=11, color=TEXT)))
            fig2.update_layout(**make_plotly_theme(),
                title=dict(text="Liability & Equity Composition ($95B)", font=dict(color=GOLD, size=15)),
                height=380, margin=dict(l=20, r=20, t=50, b=20),
                annotations=[dict(text="<b>$95B</b>", x=0.5, y=0.5, font_size=18, font_color=GOLD, showarrow=False)])
            st.plotly_chart(fig2, use_container_width=True)

        # Balance sheet table
        bs_data = {
            "Category": ["Cash & Central Bank", "Government Securities", "Loans & Advances",
                "Interbank Placements", "Fixed Assets & Others", "TOTAL ASSETS", "",
                "Demand Deposits (CASA)", "Term Deposits", "Borrowings (Interbank)",
                "Other Liabilities", "Shareholders' Equity", "TOTAL LIABILITIES & EQUITY"],
            "Amount ($mm)": [8500, 22000, 55000, 6000, 3500, 95000, "",
                28000, 35000, 12000, 4000, 16000, 95000],
            "% of Total": ["8.9%", "23.2%", "57.9%", "6.3%", "3.7%", "100.0%", "",
                "29.5%", "36.8%", "12.6%", "4.2%", "16.8%", "100.0%"],
        }
        st.dataframe(pd.DataFrame(bs_data), use_container_width=True, hide_index=True)

    with tab2:
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Asset Interest Rates</h4>")
        asset_rate_data = []
        for name, info in ASSET_RATES.items():
            asset_rate_data.append({
                "Category": name, "Current Rate": f"{info['rate']:.2%}",
                "Rate Type": info["type"], "Repricing Freq.": info["freq"],
                "Amount ($mm)": f"${info['amount']:,}"
            })
        st.dataframe(pd.DataFrame(asset_rate_data), use_container_width=True, hide_index=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif;'>Liability Interest Rates</h4>")
        liab_rate_data = []
        for name, info in LIABILITY_RATES.items():
            liab_rate_data.append({
                "Category": name, "Current Rate": f"{info['rate']:.2%}",
                "Rate Type": info["type"], "Repricing Freq.": info["freq"],
                "Amount ($mm)": f"${info['amount']:,}"
            })
        st.dataframe(pd.DataFrame(liab_rate_data), use_container_width=True, hide_index=True)

        # NII waterfall
        income_items = [
            ("Cash & CB", 8500 * 0.04), ("Govt Sec", 22000 * 0.065),
            ("Loans", 55000 * 0.0898), ("Interbank", 6000 * 0.055)
        ]
        expense_items = [
            ("CASA", -28000 * 0.035), ("Term Dep", -35000 * 0.065),
            ("Borrowings", -12000 * 0.058), ("Other", -4000 * 0.02)
        ]

        labels = [item[0] for item in income_items] + ["Total Income"] + \
                 [item[0] for item in expense_items] + ["Total Expense", "NET NII"]
        values = [item[1] for item in income_items] + [sum(v for _, v in income_items)] + \
                 [item[1] for item in expense_items] + [sum(v for _, v in expense_items)] + \
                 [sum(v for _, v in income_items) + sum(v for _, v in expense_items)]

        fig_wf = go.Figure(go.Waterfall(
            x=labels, y=values,
            measure=["relative"]*4 + ["total"] + ["relative"]*4 + ["total", "total"],
            connector=dict(line=dict(color=MUTED, width=1)),
            increasing=dict(marker_color=GREEN),
            decreasing=dict(marker_color=RED),
            totals=dict(marker_color=GOLD),
            textposition="outside",
            text=[f"${abs(v):,.0f}" for v in values],
            textfont=dict(size=9, color=TEXT),
        ))
        fig_wf.update_layout(**make_plotly_theme(),
            title=dict(text="NII Waterfall — Income & Expense Breakdown ($mm)", font=dict(color=GOLD, size=16)),
            height=450, margin=dict(l=50, r=20, t=60, b=80),
            xaxis=dict(tickangle=-30))
        st.plotly_chart(fig_wf, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: ALM KNOWLEDGE BASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📚 ALM Knowledge Base":
    section_header("ALM Knowledge Base",
        "Comprehensive Q&A guide covering all aspects of Gap Analysis in ALM", "📚")

    info_card("📖 About This Knowledge Base",
        "This comprehensive Q&A guide covers 30 key questions on ALM Gap Analysis, drawn from the "
        "companion Excel model and LaTeX reference document. Select a topic category below to explore.", GOLD)

    # Category selector
    category = st.selectbox("Select Topic", list(QA_DATA.keys()))

    border_colors = {
        "General ALM Concepts": MID_BLUE,
        "Liquidity Gap Analysis": TEAL,
        "Rate Sensitivity Gap": ORANGE,
        "NII Impact & Earnings at Risk": GREEN,
        "Dashboard & Regulatory": PURPLE,
    }

    bc = border_colors.get(category, GOLD)

    for i, (question, answer) in enumerate(QA_DATA[category]):
        with st.expander(f"❓ {question}", expanded=(i == 0)):
            st.html(f"""
            <div style="user-select:none; color:{TEXT}; -webkit-text-fill-color:{TEXT};
                font-size:0.92rem; line-height:1.7; padding:8px 4px;">
                {answer}
            </div>
            """)

    # Quick reference
    st.html(f"<div style='height:25px;'></div>")
    st.html(f"""
    <div style="user-select:none; background:{CARD_BG}; border:1px solid rgba(255,215,0,0.2);
        border-radius:12px; padding:24px; margin-top:10px;">
        <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;
            font-size:1.2rem; font-weight:700; text-align:center; margin-bottom:16px;">
            ⚡ Quick Reference — Key Formulas</div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px;">
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.75rem; margin-bottom:4px;">Periodic Gap</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.9rem; font-weight:600;">Assets<sub>t</sub> − Liabilities<sub>t</sub></div>
            </div>
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.75rem; margin-bottom:4px;">NII Impact</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.9rem; font-weight:600;">ΔNII = Gap × ΔRate</div>
            </div>
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.75rem; margin-bottom:4px;">NIM</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.9rem; font-weight:600;">NII / Total Assets</div>
            </div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:12px;">
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.75rem; margin-bottom:4px;">Cumulative Gap</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.9rem; font-weight:600;">Σ Periodic Gaps</div>
            </div>
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.75rem; margin-bottom:4px;">RSA/RSL Ratio</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.9rem; font-weight:600;">Total RSA / Total RSL</div>
            </div>
        </div>
    </div>
    """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER (All pages)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.html(f"""
<div style="user-select:none; margin-top:40px; padding:20px; text-align:center;
    border-top:2px solid rgba(255,215,0,0.2);">
    <div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
        font-size:1rem; font-weight:700; margin-bottom:4px;">
        🏔️ The Mountain Path Academy — World of Finance</div>
    <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.8rem; margin-bottom:6px;">
        Prof. V. Ravichandran · Visiting Faculty ·
        NMIMS Bangalore | BITS Pilani | RV University Bangalore | Goa Institute of Management</div>
    <div style="display:flex; justify-content:center; gap:20px; margin-top:6px;">
        <a href="https://themountainpathacademy.com" target="_blank"
            style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; text-decoration:none; font-weight:600;">
            themountainpathacademy.com</a>
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
            style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; text-decoration:none;">
            LinkedIn</a>
        <a href="https://github.com/trichyravis" target="_blank"
            style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; text-decoration:none;">
            GitHub</a>
    </div>
</div>
""")
