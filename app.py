
"""
Gap Analysis in Asset Liability Management (ALM)
The Mountain Path Academy — World of Finance
Prof. V. Ravichandran
https://themountainpathacademy.com
"""

import streamlit as st
import plotly.graph_objects as go
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

    /* ══════════════════════════════════════════════════════════════
       PERMANENT DARK THEME FIX — All dropdowns, popovers, menus,
       selectboxes, multiselects, inputs, and form controls.
       This block targets the BaseWeb UI library components that
       Streamlit uses internally. Without these overrides, dropdowns
       render with white/light backgrounds that clash with dark themes.
       ══════════════════════════════════════════════════════════════ */

    /* ── Selectbox / Dropdown trigger button ── */
    .stSelectbox [data-baseweb="select"],
    .stMultiSelect [data-baseweb="select"],
    div[data-baseweb="select"] {{
        background-color: {CARD_BG} !important;
        border-color: rgba(255,215,0,0.25) !important;
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    .stSelectbox [data-baseweb="select"]:hover,
    .stMultiSelect [data-baseweb="select"]:hover {{
        border-color: {GOLD} !important;
    }}
    .stSelectbox [data-baseweb="select"] *,
    .stMultiSelect [data-baseweb="select"] * {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    /* Arrow icon inside select */
    .stSelectbox svg, .stMultiSelect svg {{
        fill: {GOLD} !important;
    }}

    /* ── Dropdown popover / menu (the floating list) ── */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div {{
        background-color: {CARD_BG} !important;
        border: 1px solid rgba(255,215,0,0.3) !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
    }}
    [data-baseweb="menu"],
    [data-baseweb="menu"] > div,
    ul[role="listbox"],
    ul[role="listbox"] > li {{
        background-color: {CARD_BG} !important;
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    /* Dropdown list items */
    li[role="option"] {{
        background-color: {CARD_BG} !important;
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    li[role="option"]:hover,
    li[role="option"][aria-selected="true"],
    li[role="option"]:focus {{
        background-color: {MID_BLUE} !important;
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}
    /* Highlighted / focused option */
    [data-baseweb="menu"] [data-highlighted="true"],
    [data-baseweb="menu"] [aria-selected="true"] {{
        background-color: {MID_BLUE} !important;
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}

    /* ── Text inputs, number inputs, text areas ── */
    .stTextInput input, .stNumberInput input, .stTextArea textarea {{
        background-color: {CARD_BG} !important;
        border-color: rgba(255,215,0,0.25) !important;
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
        border-color: {GOLD} !important;
        box-shadow: 0 0 0 1px {GOLD} !important;
    }}

    /* ── Labels for all form widgets ── */
    .stSelectbox label, .stMultiSelect label, .stTextInput label,
    .stNumberInput label, .stTextArea label, .stSlider label,
    .stRadio label, .stCheckbox label {{
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
        font-weight: 600 !important;
    }}

    /* ── Radio buttons ── */
    .stRadio [role="radiogroup"] label {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    .stRadio [role="radiogroup"] label[data-checked="true"] {{
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}

    /* ── Expander (also needs dark body) ── */
    details[data-testid="stExpander"] {{
        background: {CARD_BG} !important;
        border: 1px solid rgba(255,215,0,0.15) !important;
        border-radius: 8px !important;
    }}
    details[data-testid="stExpander"] summary {{
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}
    details[data-testid="stExpander"] > div {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}

    /* ── Slider labels and value ── */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"],
    .stSlider [data-baseweb="slider"] div[role="slider"] + div {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}

    /* ── Dataframe / table dark theme ── */
    .stDataFrame, .stTable {{
        border: 1px solid rgba(255,215,0,0.15) !important;
        border-radius: 8px !important;
    }}

    /* ── Catch-all for any BaseWeb input wrapper ── */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-baseweb="input-container"] {{
        background-color: {CARD_BG} !important;
        border-color: rgba(255,215,0,0.25) !important;
    }}
    div[data-baseweb="input"] *,
    div[data-baseweb="base-input"] * {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}

    /* ══════════════════════════════════════════════════════════════
       END OF PERMANENT DARK THEME FIX
       ══════════════════════════════════════════════════════════════ */

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

    /* Metric delta colors */
    [data-testid="stMetricDelta"] svg {{
        fill: {TEXT} !important;
    }}
</style>
""")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA LAYER — All data from the Excel workbook
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BUCKETS = ["1-14D", "15-28D", "29D-3M", "3-6M", "6M-1Y", "1-3Y", "3-5Y", ">5Y"]

# ── From Assumptions Sheet ──
BANK_NAME = "Sample National Bank"
REPORT_DATE = "31-Mar-2025"
CURRENCY = "USD ($mm)"
TOTAL_ASSETS = 95000
EQUITY = 16000

# Balance Sheet Summary
BS_ASSETS = {
    "Cash & Balances with Central Bank": {"amount": 8500, "pct": 8.9},
    "Government Securities":             {"amount": 22000, "pct": 23.2},
    "Loans & Advances":                  {"amount": 55000, "pct": 57.9},
    "Interbank Placements":              {"amount": 6000, "pct": 6.3},
    "Fixed Assets & Others":             {"amount": 3500, "pct": 3.7},
}
BS_LIABILITIES = {
    "Demand Deposits (CASA)":   {"amount": 28000, "pct": 29.5},
    "Term Deposits":            {"amount": 35000, "pct": 36.8},
    "Borrowings (Interbank)":   {"amount": 12000, "pct": 12.6},
    "Other Liabilities":        {"amount": 4000, "pct": 4.2},
    "Shareholders' Equity":     {"amount": 16000, "pct": 16.8},
}

# ── From Assumptions Sheet: Interest Rate Assumptions ──
ASSET_RATES = [
    {"Category": "Cash & Central Bank Balances", "Rate": 4.00, "Type": "Fixed", "Freq": "Overnight", "Amount": 8500},
    {"Category": "Government Securities",        "Rate": 6.50, "Type": "Fixed", "Freq": "At Maturity", "Amount": 22000},
    {"Category": "Loans & Advances (Fixed)",     "Rate": 8.75, "Type": "Fixed", "Freq": "At Maturity", "Amount": 27000},
    {"Category": "Loans & Advances (Floating)",  "Rate": 9.20, "Type": "Floating", "Freq": "Quarterly", "Amount": 28000},
    {"Category": "Interbank Placements",         "Rate": 5.50, "Type": "Fixed", "Freq": "Monthly", "Amount": 6000},
]
LIABILITY_RATES = [
    {"Category": "Demand Deposits (CASA)",  "Rate": 3.50, "Type": "Floating", "Freq": "Discretionary", "Amount": 28000},
    {"Category": "Term Deposits",           "Rate": 6.50, "Type": "Fixed", "Freq": "At Maturity", "Amount": 35000},
    {"Category": "Borrowings (Interbank)",  "Rate": 5.80, "Type": "Floating", "Freq": "Monthly", "Amount": 12000},
    {"Category": "Other Liabilities",       "Rate": 2.00, "Type": "Fixed", "Freq": "N/A", "Amount": 4000},
]

# Rate Shock Scenarios from Assumptions
RATE_SHOCKS = [
    {"Scenario": "Parallel Up (+200 bps)", "bps": 200, "pct": 2.00},
    {"Scenario": "Parallel Up (+100 bps)", "bps": 100, "pct": 1.00},
    {"Scenario": "Base Case",              "bps": 0,   "pct": 0.00},
    {"Scenario": "Parallel Down (-100 bps)","bps": -100,"pct": -1.00},
    {"Scenario": "Parallel Down (-200 bps)","bps": -200,"pct": -2.00},
]

# ── From Liquidity Gap Sheet ──
ASSETS_LIQUIDITY = {
    "Cash & Central Bank":   [5500, 1500, 1000, 500,  0,     0,     0,     0],
    "Government Securities": [1000, 1000, 2500, 3000, 4000,  5500,  3000,  2000],
    "Loans & Advances":      [2000, 2500, 5000, 7000, 9000,  14000, 9500,  6000],
    "Interbank Placements":  [2500, 1500, 1200, 500,  200,   100,   0,     0],
    "Fixed Assets & Others": [0,    0,    0,    0,    0,     0,     500,   3000],
}
LIABILITIES_LIQUIDITY = {
    "Demand Deposits (CASA)":   [4200, 2800, 5600, 4200, 4200, 4200, 1400, 1400],
    "Term Deposits":            [2000, 2500, 5000, 6000, 7500, 7000, 3000, 2000],
    "Borrowings (Interbank)":   [3000, 2500, 2500, 2000, 1000, 500,  300,  200],
    "Other Liabilities":        [500,  500,  500,  500,  500,  500,  500,  500],
    "Shareholders' Equity":     [0,    0,    0,    0,    0,    0,    0,    16000],
}

# ── From Rate Sensitivity Gap Sheet ──
RSA_DATA = {
    "Cash & CB (O/N rate)":           [5500, 1500, 1000, 0,    0,    0,    0,    0],
    "Govt Securities (Maturing)":     [1000, 1000, 2500, 3000, 4000, 5500, 3000, 2000],
    "Loans — Floating (Repricing)":   [3500, 2000, 8000, 5500, 4000, 3000, 1500, 500],
    "Loans — Fixed (Maturing)":       [500,  1000, 2500, 3000, 4500, 6500, 4000, 5000],
    "Interbank Placements":           [2500, 1500, 1200, 500,  200,  100,  0,    0],
}
RSL_DATA = {
    "CASA (Repricing — Discretionary)": [4200, 2800, 5600, 4200, 4200, 4200, 1400, 1400],
    "Term Deposits (Maturing)":         [2000, 2500, 5000, 6000, 7500, 7000, 3000, 2000],
    "Interbank Borrowings (Floating)":  [3000, 2500, 2500, 2000, 1000, 500,  300,  200],
    "Other Rate-Sensitive Liabilities": [300,  200,  300,  200,  300,  200,  200,  200],
}

# ── From Dashboard Sheet: NII Impact ──
NII_IMPACT_TABLE = [
    {"+200 bps": 72, "+100 bps": 36, "Base Case": 0, "-100 bps": -36, "-200 bps": -72},
]
BASE_NII = 3005.25

# ── From Dashboard Sheet: Key Risk Metrics (exact values) ──
DASHBOARD_METRICS = {
    "Short-Term Gap (≤3M) / Total Assets":    {"value": -4.6, "threshold": "> -10%", "status": "PASS", "risk": "Medium"},
    "Cumulative 1-Year Gap / Total Assets":    {"value": -6.4, "threshold": "> -15%", "status": "PASS", "risk": "Medium"},
    "RSA / RSL Ratio (1-Year)":                {"value": 1.06, "threshold": "0.80x – 1.20x", "status": "PASS", "risk": "Low"},
    "NII at Risk (+200 bps) / Equity":         {"value": 0.45, "threshold": "< 5.0%", "status": "PASS", "risk": "Low"},
    "NII at Risk (+200 bps) / Base NII":       {"value": 2.4,  "threshold": "< 10.0%", "status": "PASS", "risk": "Low"},
    "Estimated Base NII ($mm)":                {"value": 3005, "threshold": "—", "status": "—", "risk": "—"},
    "Net Interest Margin (NIM)":               {"value": 3.16, "threshold": "> 2.00%", "status": "PASS", "risk": "Low"},
}

# ── From Dashboard Sheet: Key Observations ──
OBS_LIQUIDITY = "Negative short-term gaps (1-14D to 3-6M) indicate outflows exceed inflows — the bank relies on rolling funding or new deposits. Positive gaps in 1-3Y and 3-5Y buckets show long-term asset concentration. Monitor cumulative gap closely; it reaches -$6.1B at the 6M-1Y mark."
OBS_RATE = "The bank is ASSET-SENSITIVE (positive rate gap within 1-year horizon of $3.6B). Rising rates INCREASE NII (+$72mm for +200bps). Falling rates DECREASE NII. RSA/RSL ratio of 1.06x is within prudent limits. NII at Risk is well below the 5% of equity threshold."
OBS_OVERALL = "All key risk metrics are within regulatory thresholds (PASS). The bank's ALM position is moderately balanced with manageable liquidity and interest rate risk. Recommend monitoring the short-term cumulative gap and maintaining adequate liquidity buffers."

# ── From ALM Notes & Guide Sheet: Full Q&A (all 30 questions) ──
QA_DATA = {
    "Section 1: General ALM Concepts": [
        ("Q1. What is Asset Liability Management (ALM)?",
         "ALM is a risk management framework used by banks and financial institutions to manage the risks arising from mismatches between assets and liabilities. It focuses on two primary risks: (1) Liquidity Risk — the risk that maturing liabilities exceed maturing assets in any time period, creating a funding gap; and (2) Interest Rate Risk — the risk that changes in market interest rates adversely affect the bank's net interest income (NII) or economic value of equity (EVE). ALM ensures the bank can meet its obligations while optimizing profitability."),
        ("Q2. What is a Gap Analysis in ALM?",
         "Gap Analysis is the foundational ALM tool that compares the maturity (or repricing) profile of assets against liabilities across defined time buckets. The 'gap' in each bucket equals Assets minus Liabilities. A POSITIVE gap means assets exceed liabilities (asset-heavy), while a NEGATIVE gap means liabilities exceed assets (liability-heavy). The analysis is performed in two forms: (1) Structural Liquidity Gap — based on contractual maturity, and (2) Interest Rate Sensitivity Gap — based on repricing dates for rate-sensitive items."),
        ("Q3. What are the standard RBI/Basel time buckets used?",
         "This model uses the 8 standard maturity buckets prescribed by RBI (Reserve Bank of India) and aligned with Basel III guidelines: (1) 1-14 Days, (2) 15-28 Days, (3) 29 Days to 3 Months, (4) 3-6 Months, (5) 6 Months to 1 Year, (6) 1-3 Years, (7) 3-5 Years, (8) Over 5 Years. These buckets capture short-term liquidity exposure (buckets 1-3), medium-term funding gaps (buckets 4-5), and long-term structural mismatches (buckets 6-8)."),
        ("Q4. Why is ALM important for banks?",
         "Banks inherently borrow short (deposits) and lend long (loans/mortgages), creating a natural maturity mismatch. ALM is critical because: (1) Regulatory compliance — Basel III and local regulators (RBI, OCC, PRA) mandate ALM reporting and limits; (2) Earnings protection — mismatches expose NII to interest rate volatility; (3) Liquidity management — ensures the bank can meet withdrawal demands and maturing obligations; (4) Capital adequacy — EVE impact of rate changes affects economic capital; (5) Strategic planning — informs asset/liability mix, pricing decisions, and funding strategies."),
    ],
    "Section 2: Liquidity Gap Analysis": [
        ("Q5. What is the Structural Liquidity Gap?",
         "The Structural Liquidity Gap (also called Maturity Gap) shows the difference between assets and liabilities maturing in each time bucket based on contractual maturity. Formula: Periodic Gap = Total Assets Maturing – Total Liabilities Maturing in each bucket. A negative gap indicates a net cash outflow — the bank needs to raise funds or roll over maturing liabilities. In this model, assets include cash, government securities, loans, interbank placements, and fixed assets distributed by their maturity profiles."),
        ("Q6. What is the Periodic Gap vs. Cumulative Gap?",
         "PERIODIC GAP: The net difference between assets and liabilities maturing within a SINGLE time bucket. It shows the funding surplus or deficit for that specific period. CUMULATIVE GAP: The running total of all periodic gaps from the first bucket to the current bucket. Formula: Cumulative Gap(t) = Cumulative Gap(t-1) + Periodic Gap(t). The cumulative gap is more important for risk assessment because it shows the bank's total net funding position up to each point in time. A persistently negative cumulative gap signals structural funding dependency."),
        ("Q7. How should the Liquidity Gap ratios be interpreted?",
         "Three key ratios are calculated: (1) Gap as % of Total Assets = Periodic Gap / Total Assets — shows relative size of the mismatch vs. the bank's balance sheet; typically should stay within ±10%. (2) Cumulative Gap as % of Total Assets = Cumulative Gap / Total Assets — the most watched metric; RBI guideline suggests not exceeding -15% for the 1-year cumulative bucket. (3) Gap as % of Total Outflows = Periodic Gap / Total Liabilities in bucket — shows how much of the outflow is uncovered; a ratio of -30% means 30% of outflows in that bucket lack matching asset maturities."),
        ("Q8. Why do some buckets show negative gaps while others are positive?",
         "This is the natural consequence of bank business models. Short-term buckets (1-14D through 3-6M) typically show negative gaps because: (a) Deposits (especially demand deposits/CASA) are classified in short-term buckets as they can be withdrawn anytime, (b) A large portion of loans have longer maturities (1-5+ years). Long-term buckets (1-3Y, 3-5Y) show positive gaps because the bulk of loan portfolios mature in these tenors. This 'borrow short, lend long' pattern is how banks earn the term premium but creates liquidity risk."),
        ("Q9. What does it mean when cumulative gap reaches ($6,100) at the 6M-1Y bucket?",
         "The cumulative gap of ($6,100)mm at the 6M-1Y mark means that over the next 12 months, the bank's maturing liabilities exceed maturing assets by $6.1 billion. This represents 6.4% of total assets ($6,100 / $95,000). The bank must fund this gap through: (1) New deposit acquisition, (2) Rolling over maturing term deposits, (3) Interbank borrowing, (4) Selling/repo-ing liquid securities, or (5) Central bank facilities. While within regulatory limits (<15%), it requires active liquidity management and contingency planning."),
        ("Q10. How are asset categories distributed across maturity buckets?",
         "Each asset class has a characteristic maturity profile: CASH & CENTRAL BANK ($8.5B) — concentrated in shortest buckets (1-14D: $5.5B) as these are highly liquid overnight balances. GOVT SECURITIES ($22B) — spread across all buckets with concentration in medium-term (6M-3Y) reflecting a laddered investment portfolio. LOANS ($55B) — heaviest in 1-3Y ($14B) and 3-5Y ($9.5B) buckets, reflecting typical loan tenors. INTERBANK ($6B) — concentrated in short-term buckets (mostly <3M) as these are typically short-dated placements. FIXED ASSETS ($3.5B) — placed in the longest bucket (>5Y) as they are non-maturing."),
    ],
    "Section 3: Interest Rate Sensitivity Gap": [
        ("Q11. What is the difference between Liquidity Gap and Rate Sensitivity Gap?",
         "LIQUIDITY GAP classifies ALL assets and liabilities by their contractual maturity date — when cash flows actually occur. It measures funding risk. RATE SENSITIVITY GAP classifies only RATE-SENSITIVE items by their next repricing date — when the interest rate resets. It measures interest rate risk. Key difference: A 10-year floating-rate loan reprices quarterly, so it appears in the '29D-3M' bucket for rate sensitivity (next repricing) but in the '3-5Y' or '>5Y' bucket for liquidity (contractual maturity). Non-rate-sensitive items (equity, fixed assets, non-interest-bearing deposits) may be excluded from rate sensitivity analysis."),
        ("Q12. What are Rate-Sensitive Assets (RSA) and Rate-Sensitive Liabilities (RSL)?",
         "RSA are assets whose interest income changes when market rates change, either because they carry floating rates (repricing at intervals) or because they mature and are reinvested at new rates. In this model: Cash ($8B, overnight rate), Govt Securities ($22B, maturing/reinvested), Floating Loans ($28B, repricing quarterly), Fixed Loans ($27B, maturing), Interbank ($6B, short-term). Total RSA = $91B. RSL are liabilities whose interest cost changes with rate movements: CASA ($28B, discretionary repricing), Term Deposits ($35B, maturing/renewed), Interbank Borrowings ($12B, floating), Other ($1.9B). Total RSL = $76.9B. Equity ($16B) is excluded from RSL as it has no interest cost."),
        ("Q13. What does an RSA/RSL Ratio of 1.06x mean?",
         "The RSA/RSL ratio of 1.06x (within the 1-year horizon) means rate-sensitive assets exceed rate-sensitive liabilities by 6%. This indicates the bank is ASSET-SENSITIVE (also called 'positively gapped'). Implications: (1) When rates RISE → asset yields reprice upward faster/more than liability costs → NII INCREASES → beneficial. (2) When rates FALL → asset yields decline faster than funding costs → NII DECREASES → harmful. Prudent range: 0.80x–1.20x. Outside this range, the bank has significant directional rate exposure. At 1.06x, the position is slightly asset-sensitive but well within prudent limits."),
        ("Q14. What is the Cumulative 1-Year Rate Gap and why is it important?",
         "The Cumulative 1-Year Rate Gap ($3,600mm in this model) is the sum of all periodic rate sensitivity gaps within the first 5 time buckets (1-14D through 6M-1Y). It represents the net rate-sensitive position that will reprice within one year. This is the single most important number for NII-at-Risk analysis because: (1) It directly determines how much NII changes for a given rate shock: ΔNII = Cumulative Gap × ΔRate. (2) Regulators focus on the 1-year horizon for earnings risk limits. (3) It captures both maturing fixed-rate and repricing floating-rate exposures. At $3.6B positive, a +100bps rate increase adds approximately $36mm to annual NII."),
        ("Q15. How are floating-rate loans different from fixed-rate loans in this analysis?",
         "FLOATING-RATE LOANS ($28B): Classified by their REPRICING DATE, not maturity. A 20-year mortgage on a quarterly floating rate appears in the 29D-3M bucket because the rate resets every quarter. The full principal amount is rate-sensitive in the near-term. These drive most of the bank's rate sensitivity. FIXED-RATE LOANS ($27B): Classified by their MATURITY DATE. The rate is locked until maturity, so they only become rate-sensitive when they mature and must be reinvested. A 5-year fixed loan at 8.75% stays at that rate regardless of market movements. The split between fixed and floating determines how responsive the bank's asset yield is to rate changes."),
        ("Q16. Why is CASA (Demand Deposits) classified as rate-sensitive?",
         "CASA deposits ($28B) have a key characteristic: the bank sets the rate at its DISCRETION (not by contract or market benchmark). This makes them rate-sensitive because: (1) Banks typically adjust CASA rates (currently 3.50%) in response to market rate changes, though with a lag and asymmetry — they raise deposit rates slowly when rates rise, and cut quickly when rates fall. (2) In a rising rate environment, CASA represents a funding advantage as repricing is slower than market rates. (3) Behavioral modeling is complex — while contractually on-demand, a portion is considered 'core' (stable, non-withdrawable). The distribution across buckets ($4.2B per short-term bucket) reflects assumed behavioral run-off patterns."),
    ],
    "Section 4: NII Impact & Earnings at Risk": [
        ("Q17. How is the Base NII ($3,005mm) calculated?",
         "Base NII (Net Interest Income) is estimated as Total Interest Income minus Total Interest Expense using the weighted average rates from the Assumptions sheet. Interest Income = Cash×4.00% + Govt Sec×6.50% + Loans×avg(8.75%,9.20%) + Interbank×5.50% = $8,500×0.04 + $22,000×0.065 + $55,000×0.0898 + $6,000×0.055 = $340 + $1,430 + $4,938 + $330 = $7,038mm. Interest Expense = CASA×3.50% + Term Dep×6.50% + Borrowings×5.80% + Other×2.00% = $980 + $2,275 + $696 + $80 = $4,031mm. Base NII = $7,038 – $4,031 ≈ $3,005mm. This represents the bank's net interest margin of approximately 3.16% ($3,005/$95,000)."),
        ("Q18. How is the NII Impact (Earnings at Risk) calculated?",
         "NII Impact measures how much the bank's Net Interest Income changes under parallel interest rate shock scenarios. The standard formula is: ΔNII = Cumulative 1-Year Rate Gap × Rate Change. For this bank: Cumulative 1-Year Gap = $3,600mm; +200bps shock: ΔNII = $3,600 × 2.00% = +$72mm (NII increases); +100bps shock: ΔNII = $3,600 × 1.00% = +$36mm; -100bps shock: ΔNII = $3,600 × (-1.00%) = -$36mm (NII decreases); -200bps shock: ΔNII = $3,600 × (-2.00%) = -$72mm. This is a simplified linear approximation. In practice, banks use more sophisticated models accounting for optionality (prepayments, caps/floors), basis risk, and non-parallel shifts."),
        ("Q19. What is the significance of NII at Risk as % of Equity (0.45%)?",
         "NII at Risk as % of Equity measures the maximum potential NII loss relative to the bank's capital base. At 0.45% (for +200bps), this is well within the typical regulatory threshold of <5%. Interpretation: A +200bps rate shock would change NII by $72mm, which is only 0.45% of the bank's $16B equity. This means: (1) The bank's capital can easily absorb the earnings volatility from rate changes; (2) There is substantial headroom before breaching limits; (3) The bank could take on more rate risk if desired for strategic positioning. Banks with this metric >5% are considered to have high interest rate risk and may face regulatory scrutiny."),
        ("Q20. What does 'Parallel Shift' mean in rate shock scenarios?",
         "A parallel shift assumes ALL interest rates across the entire yield curve move by the same amount simultaneously. For example, +200bps parallel shift means: overnight rates increase by 2%, 3-month rates increase by 2%, 1-year rates increase by 2%, 5-year rates increase by 2%, etc. This is a simplification — in reality, rate changes are often non-parallel (short rates may move more than long rates, or vice versa). Advanced ALM models also test: (1) Steepening — short rates unchanged, long rates up; (2) Flattening — short rates up, long rates unchanged; (3) Inversion — short rates rise above long rates; (4) Basis shocks — LIBOR/SOFR spread widens. The ±200bps range aligns with Basel Committee's IRRBB prescribed shock scenarios."),
        ("Q21. Why is the bank asset-sensitive, and what does that imply for strategy?",
         "The bank is asset-sensitive (positive rate gap of $3.6B within 1 year) primarily because: (1) $28B of floating-rate loans reprice quickly (quarterly), while (2) A significant portion of liabilities are in fixed-rate term deposits ($35B) that only reprice at maturity. STRATEGIC IMPLICATIONS: In a rising rate environment, this position is FAVORABLE — asset yields increase before funding costs catch up. In a falling rate environment, it is UNFAVORABLE — asset yields drop first. If the bank's view is that rates will fall, it may consider: (a) Extending floating-rate loan tenors to fixed, (b) Shifting funding toward floating-rate borrowings, (c) Using interest rate swaps to convert the gap from positive to negative (pay-fixed, receive-floating)."),
    ],
    "Section 5: Dashboard Metrics & Regulatory Thresholds": [
        ("Q22. What does the Short-Term Gap (≤3M) / Total Assets metric tell us?",
         "This metric (-4.6% in this model) measures the bank's immediate liquidity exposure over the next 3 months. It is the cumulative gap for buckets 1-14D + 15-28D + 29D-3M, divided by total assets. Threshold: > -10% (i.e., the negative gap should not exceed 10% of total assets). At -4.6%, the bank has adequate short-term liquidity but is relying on rolling short-term funding. A breach (below -10%) would indicate severe near-term funding stress and trigger enhanced liquidity management, potential asset sales, or emergency borrowing facilities."),
        ("Q23. What does the Cumulative 1-Year Gap / Total Assets metric tell us?",
         "This metric (-6.4% in this model) extends the liquidity assessment to the full 1-year horizon. It shows that maturing liabilities exceed maturing assets by $6.1B over 12 months, representing 6.4% of the total balance sheet. Threshold: > -15% (RBI/Basel guideline). At -6.4%, the bank is well within the limit, meaning it has a manageable 1-year funding gap. Action triggers: -10% to -15% = enhanced monitoring and contingency planning; below -15% = regulatory breach requiring immediate remediation."),
        ("Q24. What is the Net Interest Margin (NIM) and is 3.16% good?",
         "NIM = Net Interest Income / Total Assets = $3,005mm / $95,000mm = 3.16%. NIM is the most fundamental profitability metric for banks — it measures how efficiently the bank earns interest on its asset base. Threshold: > 2.00% is the minimum prudent level; most healthy banks target 2.50%-3.50%. At 3.16%, this bank has a healthy NIM indicating: (1) Good spread between asset yields (~7.4% weighted avg) and liability costs (~4.2%), (2) Effective pricing of loans and deposits, (3) Reasonable asset mix with higher-yielding loans forming the majority. NIM can be enhanced by: increasing the loan-to-asset ratio, improving CASA ratio (cheaper funding), or repricing loans upward."),
        ("Q25. What do the PASS/BREACH indicators mean on the Dashboard?",
         "Each key metric is compared against regulatory or internal prudential thresholds: PASS (green) = Metric is within acceptable limits; no action required. BREACH (red) = Metric has crossed the threshold; requires immediate attention and remediation plan. Risk Levels provide additional granularity: ✅ Low = well within limits, no concern; ⚠️ Medium = within limits but approaching threshold, warrants monitoring; ❌ High = at or near breach level, urgent action needed. Currently all 7 metrics show PASS, with liquidity metrics at Medium risk and interest rate metrics at Low risk."),
        ("Q26. How should the RSA/RSL Ratio range of 0.80x-1.20x be interpreted?",
         "The RSA/RSL Ratio threshold of 0.80x-1.20x represents the 'neutral zone' where the bank's interest rate risk is considered manageable. Breakdown: <0.80x = Heavily liability-sensitive; NII highly vulnerable to rising rates. 0.80x-0.90x = Moderately liability-sensitive; some rate risk but manageable. 0.90x-1.10x = Nearly balanced; minimal directional rate risk (ideal for risk-averse banks). 1.10x-1.20x = Moderately asset-sensitive; benefits from rising rates (this bank at 1.06x). >1.20x = Heavily asset-sensitive; NII highly vulnerable to falling rates."),
    ],
    "Section 6: Practical Usage & Model Limitations": [
        ("Q27. How do I customize this model with my own bank's data?",
         "Step 1: Update the Assumptions sheet — change bank name, reporting date, balance sheet totals, and interest rates (all blue-colored inputs are editable). Step 2: Update the Liquidity Gap sheet — replace the asset and liability maturity distributions in each time bucket (rows 5-9 for assets, rows 13-17 for liabilities). Ensure each row sums to the total in the Assumptions sheet. Step 3: Update the Rate Sensitivity Gap sheet — replace RSA and RSL distributions based on your bank's repricing profile. Note: floating-rate items are classified by repricing date, fixed-rate by maturity date. Step 4: The Dashboard, gap calculations, NII impact, and charts all update automatically via formulas."),
        ("Q28. What are the key limitations of this Gap Analysis model?",
         "This model has several simplifications common to traditional gap analysis: (1) STATIC MODEL — assumes the balance sheet doesn't change over the projection period (no new loans, deposits, or repayments). (2) LINEAR NII IMPACT — assumes rate changes are fully passed through to all rate-sensitive items equally; in reality, deposit betas differ from loan betas. (3) NO OPTIONALITY — ignores prepayment risk on loans, early withdrawal of deposits, and embedded caps/floors. (4) PARALLEL SHIFTS ONLY — doesn't model curve twists, steepening, or basis risk. (5) NO BEHAVIORAL MODELING — CASA is distributed using assumed run-off patterns, not sophisticated behavioral models. (6) NO EVE ANALYSIS — measures only earnings (NII) impact, not Economic Value of Equity."),
        ("Q29. What is the difference between NII at Risk and EVE?",
         "NII at Risk (EARNINGS perspective): Measures how much annual Net Interest Income changes under a rate shock over a 1-year horizon. This model calculates NII at Risk. It focuses on short-term profitability impact and is the primary metric for ALCO decision-making. EVE (ECONOMIC VALUE perspective): Measures the change in the present value of all future cash flows from assets and liabilities when rates change. EVE captures the FULL lifetime impact of rate changes on the bank's economic value, including long-dated positions beyond 1 year. Basel IRRBB requires banks to report BOTH metrics. A bank can have low NII risk but high EVE risk if it has large long-dated mismatches beyond the 1-year horizon."),
        ("Q30. What actions can the ALCO take based on this Gap Analysis?",
         "The Asset Liability Committee (ALCO) uses gap analysis to make strategic decisions: LIQUIDITY MANAGEMENT: (1) Adjust deposit pricing to attract longer-term deposits and reduce short-term funding gaps. (2) Establish committed credit lines or repo facilities as contingency funding. (3) Maintain a liquid securities buffer (govt bonds) that can be quickly sold or pledged. INTEREST RATE MANAGEMENT: (1) If expecting rate cuts: shift loan book from floating to fixed rates; increase floating-rate borrowings; consider pay-floating, receive-fixed swaps. (2) If expecting rate hikes: maintain current asset-sensitive position; lock in fixed-rate funding at current levels; consider pay-fixed swaps on liabilities. BALANCE SHEET OPTIMIZATION: (1) Improve CASA ratio to reduce funding cost. (2) Diversify funding sources to reduce concentration risk. (3) Align asset origination tenors with funding availability."),
    ],
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def compute_gaps(assets_dict, liabilities_dict):
    total_assets = [sum(x) for x in zip(*assets_dict.values())]
    total_liabilities = [sum(x) for x in zip(*liabilities_dict.values())]
    periodic_gap = [a - l for a, l in zip(total_assets, total_liabilities)]
    cumulative_gap = list(np.cumsum(periodic_gap))
    return total_assets, total_liabilities, periodic_gap, cumulative_gap


def fmt(val, prefix="$", suffix="mm"):
    if val >= 0:
        return f"{prefix}{val:,.0f}{suffix}"
    return f"({prefix}{abs(val):,.0f}{suffix})"


def plotly_theme():
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
                color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.7rem; letter-spacing:-0.5px;">{title}</h2>
        </div>
        {"<p style='margin:0 0 0 44px; color:" + MUTED + "; -webkit-text-fill-color:" + MUTED + "; font-size:0.95rem;'>" + subtitle + "</p>" if subtitle else ""}
        <div style="height:2px; background:linear-gradient(90deg, {GOLD}, transparent); margin-top:8px;"></div>
    </div>
    """)


def metric_card(label, value, threshold="", status="PASS", risk="Low"):
    sc = GREEN if status == "PASS" else (RED if status == "BREACH" else MUTED)
    rc_map = {"Low": GREEN, "Medium": ORANGE, "High": RED, "—": MUTED}
    ri_map = {"Low": "✅", "Medium": "⚠️", "High": "❌", "—": ""}
    rc = rc_map.get(risk, MUTED)
    ri = ri_map.get(risk, "")
    st.html(f"""
    <div style="user-select:none; background:{CARD_BG}; border:1px solid rgba(255,215,0,0.15);
        border-radius:12px; padding:18px; text-align:center; min-height:145px;
        display:flex; flex-direction:column; justify-content:center;">
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.78rem; font-weight:600;
            text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">{label}</div>
        <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;
            font-size:1.7rem; font-weight:700; margin-bottom:4px;">{value}</div>
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem; margin-bottom:6px;">
            Threshold: {threshold}</div>
        <div style="display:flex; justify-content:center; gap:10px; font-size:0.78rem;">
            <span style="color:{sc}; -webkit-text-fill-color:{sc}; font-weight:700;">{status}</span>
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
# SIDEBAR — FIXED: no absolute positioning, uses normal flow
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    st.html(f"""
    <div style="user-select:none; text-align:center; padding:10px 0 15px 0;">
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

    # ── Sidebar Footer: normal document flow (NOT absolute) ──
    st.html(f"""
    <div style="user-select:none; margin-top:40px; padding:15px 10px; text-align:center;
        border-top:1px solid rgba(255,215,0,0.2);">
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem; margin-bottom:4px;">
            Prof. V. Ravichandran</div>
        <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.65rem; margin-bottom:8px;">
            NMIMS Bangalore | BITS Pilani<br>RV University Bangalore | GIM</div>
        <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
            <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
                style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.72rem; text-decoration:none;">LinkedIn</a>
            <a href="https://github.com/trichyravis" target="_blank"
                style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.72rem; text-decoration:none;">GitHub</a>
            <a href="https://themountainpathacademy.com" target="_blank"
                style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.72rem; text-decoration:none;">themountainpathacademy.com</a>
        </div>
    </div>
    """)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER BANNER
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
                {BANK_NAME} · Report Date: {REPORT_DATE} · Currency: {CURRENCY}</div>
        </div>
        <div style="text-align:right;">
            <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;
                font-size:2.2rem; font-weight:800;">${TOTAL_ASSETS:,}</div>
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

    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Short-Term Gap (≤3M) / TA", "–4.6%", "> –10%", "PASS", "Medium")
    with c2: metric_card("Cum. 1-Year Gap / TA", "–6.4%", "> –15%", "PASS", "Medium")
    with c3: metric_card("RSA / RSL Ratio (1Y)", "1.06x", "0.80x – 1.20x", "PASS", "Low")
    with c4: metric_card("NII at Risk / Equity", "0.45%", "< 5.0%", "PASS", "Low")

    st.html("<div style='height:10px;'></div>")
    c5, c6, c7, c8 = st.columns(4)
    with c5: metric_card("NII at Risk / Base NII", "2.4%", "< 10.0%", "PASS", "Low")
    with c6: metric_card("Estimated Base NII", "$3,005mm", "—", "—", "—")
    with c7: metric_card("Net Interest Margin", "3.16%", "> 2.00%", "PASS", "Low")
    with c8: metric_card("Total Assets", "$95,000mm", "—", "—", "—")

    st.html("<div style='height:18px;'></div>")

    col_l, col_r = st.columns(2)

    # ── Liquidity Gap Profile (from Dashboard sheet) ──
    with col_l:
        pg = [1300, -1800, -3900, -1700, 0, 7400, 7800, -9100]
        cg = [1300, -500, -4400, -6100, -6100, 1300, 9100, 0]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=BUCKETS, y=pg, name="Periodic Gap",
            marker=dict(color=[GREEN if v >= 0 else RED for v in pg], opacity=0.8),
            text=[fmt(v) for v in pg], textposition="outside", textfont=dict(size=9)))
        fig.add_trace(go.Scatter(x=BUCKETS, y=cg, name="Cumulative Gap", mode="lines+markers",
            line=dict(color=GOLD, width=3), marker=dict(size=8, color=GOLD)))
        fig.update_layout(**plotly_theme(), title=dict(text="Liquidity Gap Profile", font=dict(color=GOLD)),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)),
            height=380, margin=dict(l=50, r=20, t=50, b=60), yaxis_title="Gap ($mm)")
        fig.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        st.plotly_chart(fig, use_container_width=True, key="dash_liq")

    # ── Rate Sensitivity Gap Profile (from Dashboard sheet) ──
    with col_r:
        rsa_vals = [13000, 7000, 15200, 12000, 12700, 15100, 8500, 7500]
        rsl_vals = [9500, 8000, 13400, 12400, 13000, 11900, 4900, 3800]
        rate_pg = [a - l for a, l in zip(rsa_vals, rsl_vals)]
        rate_cg = list(np.cumsum(rate_pg))

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=BUCKETS, y=rate_pg, name="Rate Gap",
            marker=dict(color=[TEAL if v >= 0 else ORANGE for v in rate_pg], opacity=0.8),
            text=[fmt(v) for v in rate_pg], textposition="outside", textfont=dict(size=9)))
        fig2.add_trace(go.Scatter(x=BUCKETS, y=rate_cg, name="Cumulative Rate Gap", mode="lines+markers",
            line=dict(color=ORANGE, width=3), marker=dict(size=8, color=ORANGE)))
        fig2.update_layout(**plotly_theme(), title=dict(text="Rate Sensitivity Gap Profile", font=dict(color=GOLD)),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)),
            height=380, margin=dict(l=50, r=20, t=50, b=60), yaxis_title="Gap ($mm)")
        fig2.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        st.plotly_chart(fig2, use_container_width=True, key="dash_rate")

    # ── NII Impact by Rate Scenario (from Dashboard sheet) ──
    st.html(f"<div style='height:10px;'></div>")
    scenarios = ["+200 bps", "+100 bps", "Base Case", "-100 bps", "-200 bps"]
    nii_impacts = [72, 36, 0, -36, -72]
    pct_nii = [2.4, 1.2, 0.0, -1.2, -2.4]
    pct_eq = [0.45, 0.23, 0.0, -0.23, -0.45]

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=scenarios, y=nii_impacts, name="NII Impact ($mm)",
        marker=dict(color=[GREEN if v >= 0 else RED for v in nii_impacts], opacity=0.85),
        text=[f"${v:+,}" for v in nii_impacts], textposition="outside", textfont=dict(size=11, color=TEXT)))
    fig3.update_layout(**plotly_theme(),
        title=dict(text="NII Impact by Rate Scenario (from Dashboard)", font=dict(color=GOLD, size=15)),
        height=340, margin=dict(l=50, r=20, t=50, b=40), yaxis_title="ΔNII ($mm)")
    fig3.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
    st.plotly_chart(fig3, use_container_width=True, key="dash_nii")

    # ── Key Observations (from Dashboard sheet) ──
    st.html(f"<div style='height:10px;'></div>")
    info_card("🔵 Liquidity Risk Assessment", OBS_LIQUIDITY, ORANGE)
    info_card("🟢 Interest Rate Risk Assessment", OBS_RATE, GREEN)
    info_card("📋 Overall Position", OBS_OVERALL, GOLD)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: LIQUIDITY GAP ANALYSIS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📊 Liquidity Gap Analysis":
    section_header("Structural Liquidity Gap Analysis",
        "Maturity profile of ALL assets & liabilities by contractual maturity date (Liquidity Gap Sheet)", "📊")

    ta, tl, pg, cg = compute_gaps(ASSETS_LIQUIDITY, LIABILITIES_LIQUIDITY)

    tab1, tab2, tab3 = st.tabs(["📊 Gap Charts", "📋 Detailed Tables", "🔍 Ratio Analysis"])

    with tab1:
        # Stacked bars
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Asset Maturity Profile", "Liability Maturity Profile"),
            horizontal_spacing=0.08)
        a_cols = [MID_BLUE, TEAL, GREEN, LIGHT_BLUE, MUTED]
        for i, (nm, vals) in enumerate(ASSETS_LIQUIDITY.items()):
            fig.add_trace(go.Bar(x=BUCKETS, y=vals, name=nm, marker_color=a_cols[i], opacity=0.85), row=1, col=1)
        l_cols = [RED, ORANGE, PURPLE, MUTED, GOLD]
        for i, (nm, vals) in enumerate(LIABILITIES_LIQUIDITY.items()):
            fig.add_trace(go.Bar(x=BUCKETS, y=vals, name=nm, marker_color=l_cols[i], opacity=0.85), row=1, col=2)
        fig.update_layout(**plotly_theme(), barmode="stack", height=420,
            legend=dict(orientation="h", yanchor="bottom", y=-0.35, font=dict(size=9)),
            margin=dict(l=50, r=20, t=50, b=80))
        st.plotly_chart(fig, use_container_width=True, key="liq_stacked")

        # Gap chart
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=BUCKETS, y=pg, name="Periodic Gap",
            marker=dict(color=[GREEN if v >= 0 else RED for v in pg], opacity=0.8),
            text=[fmt(v) for v in pg], textposition="outside", textfont=dict(size=10)))
        fig2.add_trace(go.Scatter(x=BUCKETS, y=cg, name="Cumulative Gap", mode="lines+markers+text",
            line=dict(color=GOLD, width=3), marker=dict(size=10, color=GOLD),
            text=[fmt(v) for v in cg], textposition="top center", textfont=dict(size=9, color=GOLD)))
        fig2.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        fig2.update_layout(**plotly_theme(),
            title=dict(text="Liquidity Gap — Periodic & Cumulative ($mm)", font=dict(color=GOLD, size=16)),
            height=420, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="Gap ($mm)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig2, use_container_width=True, key="liq_gap")

    with tab2:
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Asset Maturity Profile ($mm)</h4>")
        adf = pd.DataFrame(ASSETS_LIQUIDITY, index=BUCKETS).T
        adf["Total"] = adf.sum(axis=1)
        adf = pd.concat([adf, pd.DataFrame(adf.sum(), columns=["TOTAL ASSETS"]).T])
        st.dataframe(adf.style.format("{:,.0f}"), use_container_width=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Liability & Equity Maturity Profile ($mm)</h4>")
        ldf = pd.DataFrame(LIABILITIES_LIQUIDITY, index=BUCKETS).T
        ldf["Total"] = ldf.sum(axis=1)
        ldf = pd.concat([ldf, pd.DataFrame(ldf.sum(), columns=["TOTAL LIABILITIES"]).T])
        st.dataframe(ldf.style.format("{:,.0f}"), use_container_width=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Gap Analysis Results</h4>")
        gap_pct = [g / TOTAL_ASSETS * 100 for g in pg]
        cum_pct = [g / TOTAL_ASSETS * 100 for g in cg]
        outflow_pct = [g / l * 100 if l != 0 else 0 for g, l in zip(pg, tl)]
        gdf = pd.DataFrame({
            "Periodic Gap": pg, "Cumulative Gap": cg,
            "Gap % of TA": gap_pct, "Cum Gap % of TA": cum_pct,
            "Gap % of Outflows": outflow_pct
        }, index=BUCKETS).T
        st.dataframe(gdf.style.format("{:,.1f}"), use_container_width=True)

    with tab3:
        gap_pct = [g / TOTAL_ASSETS * 100 for g in pg]
        cum_pct = [g / TOTAL_ASSETS * 100 for g in cg]

        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=BUCKETS, y=gap_pct, name="Gap % of TA", marker_color=MID_BLUE, opacity=0.7))
        fig3.add_trace(go.Scatter(x=BUCKETS, y=cum_pct, name="Cum Gap % of TA",
            mode="lines+markers", line=dict(color=GOLD, width=3), marker=dict(size=8)))
        fig3.add_hline(y=-10, line_dash="dash", line_color=RED, line_width=1.5,
            annotation_text="Short-term limit: -10%", annotation_position="bottom right",
            annotation_font=dict(color=RED, size=10))
        fig3.add_hline(y=-15, line_dash="dash", line_color=RED, line_width=2,
            annotation_text="RBI/Basel limit: -15%", annotation_position="bottom right",
            annotation_font=dict(color=RED, size=10))
        fig3.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        fig3.update_layout(**plotly_theme(),
            title=dict(text="Gap Ratios vs Regulatory Thresholds (%)", font=dict(color=GOLD, size=16)),
            height=420, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="%",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig3, use_container_width=True, key="liq_ratio")

        info_card("⚠️ The Funding Valley",
            f"Cumulative gap reaches <b style='color:{RED}; -webkit-text-fill-color:{RED};'>($6,100mm)</b> at 6M–1Y, "
            "representing <b>6.4%</b> of total assets. Within RBI limit of 15% but requires active management.", ORANGE)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: RATE SENSITIVITY GAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📈 Rate Sensitivity Gap":
    section_header("Interest Rate Sensitivity Gap Analysis",
        "Rate-sensitive assets vs liabilities by next repricing date (Rate Sensitivity Gap Sheet)", "📈")

    rsa_t = [sum(x) for x in zip(*RSA_DATA.values())]
    rsl_t = [sum(x) for x in zip(*RSL_DATA.values())]
    rg = [a - l for a, l in zip(rsa_t, rsl_t)]
    rcg = list(np.cumsum(rg))
    ratio = [a / l if l != 0 else 0 for a, l in zip(rsa_t, rsl_t)]

    tab1, tab2, tab3 = st.tabs(["📊 Gap Charts", "📋 Detailed Tables", "📐 RSA/RSL Ratio"])

    with tab1:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=BUCKETS, y=rsa_t, name="RSA", marker_color=TEAL, opacity=0.8))
        fig.add_trace(go.Bar(x=BUCKETS, y=rsl_t, name="RSL", marker_color=ORANGE, opacity=0.8))
        fig.update_layout(**plotly_theme(), barmode="group",
            title=dict(text="RSA vs RSL by Time Bucket ($mm)", font=dict(color=GOLD, size=16)),
            height=400, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="Amount ($mm)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True, key="rate_bar")

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=BUCKETS, y=rg, name="Rate Gap (RSA-RSL)",
            marker=dict(color=[TEAL if v >= 0 else RED for v in rg], opacity=0.8),
            text=[fmt(v) for v in rg], textposition="outside", textfont=dict(size=10)))
        fig2.add_trace(go.Scatter(x=BUCKETS, y=rcg, name="Cumulative Rate Gap",
            mode="lines+markers", line=dict(color=ORANGE, width=3), marker=dict(size=10, color=ORANGE)))
        fig2.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
        fig2.update_layout(**plotly_theme(),
            title=dict(text="Rate Gap — Periodic & Cumulative ($mm)", font=dict(color=GOLD, size=16)),
            height=400, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="Gap ($mm)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, font=dict(size=11)))
        st.plotly_chart(fig2, use_container_width=True, key="rate_gap")

    with tab2:
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Rate-Sensitive Assets ($mm) — Total RSA: $91,000mm</h4>")
        rdf = pd.DataFrame(RSA_DATA, index=BUCKETS).T
        rdf["Total"] = rdf.sum(axis=1)
        rdf = pd.concat([rdf, pd.DataFrame(rdf.sum(), columns=["TOTAL RSA"]).T])
        st.dataframe(rdf.style.format("{:,.0f}"), use_container_width=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Rate-Sensitive Liabilities ($mm) — Total RSL: $76,900mm</h4>")
        sdf = pd.DataFrame(RSL_DATA, index=BUCKETS).T
        sdf["Total"] = sdf.sum(axis=1)
        sdf = pd.concat([sdf, pd.DataFrame(sdf.sum(), columns=["TOTAL RSL"]).T])
        st.dataframe(sdf.style.format("{:,.0f}"), use_container_width=True)

        # NII Impact table from Rate Sensitivity Gap sheet
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>NII Impact Analysis (Earnings at Risk)</h4>")
        cum_1y = 3600
        st.html(f"<p style='color:{TEXT}; -webkit-text-fill-color:{TEXT}; font-size:0.9rem;'>Cumulative 1-Year Rate Gap: <b style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>${cum_1y:,}mm</b> &nbsp;|&nbsp; Base NII: <b style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>${BASE_NII:,.2f}mm</b></p>")
        nii_df = pd.DataFrame({
            "Scenario": ["+200 bps", "+100 bps", "Base Case", "-100 bps", "-200 bps"],
            "NII Impact ($mm)": [72, 36, 0, -36, -72],
            "% of Base NII": ["2.4%", "1.2%", "0.0%", "-1.2%", "-2.4%"],
            "% of Equity": ["0.45%", "0.23%", "0.00%", "-0.23%", "-0.45%"],
        })
        st.dataframe(nii_df, use_container_width=True, hide_index=True)

    with tab3:
        fig3 = go.Figure()
        fig3.add_hrect(y0=0, y1=0.80, fillcolor=RED, opacity=0.08, line_width=0)
        fig3.add_hrect(y0=0.80, y1=0.90, fillcolor=ORANGE, opacity=0.06, line_width=0)
        fig3.add_hrect(y0=0.90, y1=1.10, fillcolor=GREEN, opacity=0.08, line_width=0,
            annotation_text="Neutral Zone (0.90x–1.10x)", annotation_position="top left",
            annotation_font=dict(size=9, color=GREEN))
        fig3.add_hrect(y0=1.10, y1=1.20, fillcolor=ORANGE, opacity=0.06, line_width=0)
        fig3.add_hrect(y0=1.20, y1=2.2, fillcolor=RED, opacity=0.08, line_width=0)
        fig3.add_trace(go.Scatter(x=BUCKETS, y=ratio, mode="lines+markers+text",
            line=dict(color=GOLD, width=3), marker=dict(size=12, color=GOLD, line=dict(width=2, color=BLUE)),
            text=[f"{r:.2f}x" for r in ratio], textposition="top center", textfont=dict(size=10, color=GOLD)))
        fig3.add_hline(y=1.0, line_dash="dash", line_color=GREEN, line_width=1)
        fig3.add_hline(y=0.80, line_dash="dot", line_color=ORANGE, line_width=1)
        fig3.add_hline(y=1.20, line_dash="dot", line_color=ORANGE, line_width=1)
        fig3.update_layout(**plotly_theme(),
            title=dict(text="RSA/RSL Ratio Across Time Buckets", font=dict(color=GOLD, size=16)),
            height=450, margin=dict(l=50, r=20, t=60, b=60), yaxis_title="RSA / RSL Ratio",
            yaxis=dict(range=[0.5, 2.2]), showlegend=False)
        st.plotly_chart(fig3, use_container_width=True, key="ratio_chart")

        c1, c2 = st.columns(2)
        with c1:
            info_card("🟢 Asset-Sensitive Position",
                "1-Year RSA/RSL = 1.06x. Rates RISE → NII INCREASES. The bank benefits from rising rate environments.", GREEN)
        with c2:
            info_card("📊 Why RSA ($91B) > RSL ($76.9B)?",
                "Difference of $14.1B is primarily Shareholders' Equity ($16B) which funds assets but carries no interest cost.", LIGHT_BLUE)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: NII IMPACT SIMULATOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "💰 NII Impact Simulator":
    section_header("NII Impact Simulator — Earnings at Risk",
        "Interactive rate shock analysis (formula from Rate Sensitivity Gap Sheet)", "💰")

    c1, c2 = st.columns(2)
    with c1:
        info_card("📥 Interest Income = $7,038mm",
            "Cash×4.00%=$340 · Govt Sec×6.50%=$1,430 · Loans×8.98%=$4,938 · Interbank×5.50%=$330", GREEN)
    with c2:
        info_card("📤 Interest Expense = $4,031mm",
            "CASA×3.50%=$980 · Term Dep×6.50%=$2,275 · Borrowings×5.80%=$696 · Other×2.00%=$80", RED)

    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Base NII", f"${BASE_NII:,.0f}mm")
    with c2: st.metric("Net Interest Margin", "3.16%")
    with c3: st.metric("Cum. 1-Year Rate Gap", "$3,600mm")

    st.html(f"<div style='height:10px;'></div>")
    st.html(f"<div style='user-select:none; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:Playfair Display,serif; font-size:1.3rem; font-weight:700;'>🎛️ Rate Shock Simulator</div>")

    rate_shock = st.slider("Parallel Rate Shock (basis points)", min_value=-300, max_value=300, value=200, step=25)

    cum_1y = 3600
    d_nii = cum_1y * (rate_shock / 10000)
    new_nii = BASE_NII + d_nii

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Rate Shock", f"{rate_shock:+d} bps")
    with c2: st.metric("ΔNII Impact", f"${d_nii:+,.0f}mm", delta=f"{d_nii / BASE_NII * 100:+.2f}% of Base NII")
    with c3: st.metric("New NII", f"${new_nii:,.0f}mm", delta=f"${d_nii:+,.0f}mm")
    with c4: st.metric("NII at Risk / Equity", f"{d_nii / EQUITY * 100:+.2f}%",
        delta="BREACH" if abs(d_nii / EQUITY * 100) > 5 else "PASS")

    bps_range = list(range(-300, 325, 25))
    impacts = [cum_1y * (s / 10000) for s in bps_range]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=[f"{s:+d}" for s in bps_range], y=impacts,
        marker=dict(color=[GREEN if n >= 0 else RED for n in impacts], opacity=0.7),
        hovertemplate="Rate: %{x}bps<br>ΔNII: $%{y:,.0f}mm<extra></extra>"))
    fig.add_trace(go.Scatter(x=[f"{rate_shock:+d}"], y=[d_nii], mode="markers",
        marker=dict(size=18, color=GOLD, symbol="diamond", line=dict(width=2, color=BLUE)),
        name=f"Selected: {rate_shock:+d}bps"))
    fig.add_hline(y=EQUITY * 0.05, line_dash="dash", line_color=RED, line_width=1.5,
        annotation_text="5% of Equity = $800mm", annotation_position="top right",
        annotation_font=dict(color=RED, size=10))
    fig.add_hline(y=-EQUITY * 0.05, line_dash="dash", line_color=RED, line_width=1.5)
    fig.add_hline(y=0, line_dash="solid", line_color=MUTED, line_width=1)
    fig.update_layout(**plotly_theme(),
        title=dict(text="NII Impact Across Rate Scenarios ($mm)", font=dict(color=GOLD, size=16)),
        height=420, margin=dict(l=50, r=20, t=60, b=60),
        xaxis_title="Rate Shock (bps)", yaxis_title="ΔNII ($mm)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, font=dict(size=11)))
    st.plotly_chart(fig, use_container_width=True, key="nii_sim")

    info_card("💡 Asset-Sensitive Interpretation",
        "Positive 1-year rate gap of $3,600mm → bank is <b>asset-sensitive</b>. "
        "Rising rates → NII increases. At just 0.45% of equity for +200bps, substantial headroom exists.", GOLD)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: BALANCE SHEET & ASSUMPTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📋 Balance Sheet & Assumptions":
    section_header("Balance Sheet & Interest Rate Assumptions",
        "From Assumptions Sheet — Sample National Bank, 31-Mar-2025", "📋")

    tab1, tab2, tab3 = st.tabs(["📊 Balance Sheet", "📐 Interest Rates", "📈 NII Waterfall"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = go.Figure(go.Pie(
                labels=list(BS_ASSETS.keys()),
                values=[v["amount"] for v in BS_ASSETS.values()],
                hole=0.5, textinfo="label+percent",
                marker=dict(colors=[MID_BLUE, TEAL, GREEN, LIGHT_BLUE, MUTED],
                    line=dict(color=BLUE, width=2)),
                textfont=dict(size=10, color=TEXT)))
            fig.update_layout(**plotly_theme(),
                title=dict(text="Asset Composition", font=dict(color=GOLD, size=15)),
                height=380, margin=dict(l=20, r=20, t=50, b=20),
                annotations=[dict(text="<b>$95B</b>", x=0.5, y=0.5, font_size=18, font_color=GOLD, showarrow=False)])
            st.plotly_chart(fig, use_container_width=True, key="bs_asset_pie")

        with c2:
            fig2 = go.Figure(go.Pie(
                labels=list(BS_LIABILITIES.keys()),
                values=[v["amount"] for v in BS_LIABILITIES.values()],
                hole=0.5, textinfo="label+percent",
                marker=dict(colors=[RED, ORANGE, PURPLE, MUTED, GOLD],
                    line=dict(color=BLUE, width=2)),
                textfont=dict(size=10, color=TEXT)))
            fig2.update_layout(**plotly_theme(),
                title=dict(text="Liability & Equity Composition", font=dict(color=GOLD, size=15)),
                height=380, margin=dict(l=20, r=20, t=50, b=20),
                annotations=[dict(text="<b>$95B</b>", x=0.5, y=0.5, font_size=18, font_color=GOLD, showarrow=False)])
            st.plotly_chart(fig2, use_container_width=True, key="bs_liab_pie")

        # Tables
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Assets</h4>")
        adf = pd.DataFrame([{"Category": k, "Amount ($mm)": f"${v['amount']:,}", "% of Total": f"{v['pct']:.1f}%"}
            for k, v in BS_ASSETS.items()])
        st.dataframe(adf, use_container_width=True, hide_index=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Liabilities & Equity</h4>")
        ldf = pd.DataFrame([{"Category": k, "Amount ($mm)": f"${v['amount']:,}", "% of Total": f"{v['pct']:.1f}%"}
            for k, v in BS_LIABILITIES.items()])
        st.dataframe(ldf, use_container_width=True, hide_index=True)

    with tab2:
        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Asset Interest Rates (from Assumptions Sheet)</h4>")
        ardf = pd.DataFrame(ASSET_RATES)
        ardf["Rate"] = ardf["Rate"].apply(lambda x: f"{x:.2f}%")
        ardf["Amount"] = ardf["Amount"].apply(lambda x: f"${x:,}")
        st.dataframe(ardf, use_container_width=True, hide_index=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Liability Interest Rates (from Assumptions Sheet)</h4>")
        lrdf = pd.DataFrame(LIABILITY_RATES)
        lrdf["Rate"] = lrdf["Rate"].apply(lambda x: f"{x:.2f}%")
        lrdf["Amount"] = lrdf["Amount"].apply(lambda x: f"${x:,}")
        st.dataframe(lrdf, use_container_width=True, hide_index=True)

        st.html(f"<h4 style='color:{GOLD}; -webkit-text-fill-color:{GOLD};'>Rate Shock Scenarios (from Assumptions Sheet)</h4>")
        rsdf = pd.DataFrame(RATE_SHOCKS)
        st.dataframe(rsdf, use_container_width=True, hide_index=True)

        info_card("💡 Key Observation",
            f"Weighted Avg Asset Yield ≈ <b>7.4%</b> | Weighted Avg Funding Cost ≈ <b>4.2%</b> → "
            f"NIM = <b>3.16%</b>, comfortably above the 2.00% prudential threshold.", GOLD)

    with tab3:
        inc = [("Cash & CB", 340), ("Govt Sec", 1430), ("Loans", 4938), ("Interbank", 330)]
        exp = [("CASA", -980), ("Term Dep", -2275), ("Borrowings", -696), ("Other", -80)]

        labels = [i[0] for i in inc] + ["Total Income"] + [e[0] for e in exp] + ["Total Expense", "NET NII"]
        vals = [i[1] for i in inc] + [sum(v for _, v in inc)] + [e[1] for e in exp] + [sum(v for _, v in exp)] + \
               [sum(v for _, v in inc) + sum(v for _, v in exp)]

        fig_wf = go.Figure(go.Waterfall(
            x=labels, y=vals,
            measure=["relative"]*4 + ["total"] + ["relative"]*4 + ["total", "total"],
            connector=dict(line=dict(color=MUTED, width=1)),
            increasing=dict(marker_color=GREEN), decreasing=dict(marker_color=RED),
            totals=dict(marker_color=GOLD),
            textposition="outside", text=[f"${abs(v):,.0f}" for v in vals],
            textfont=dict(size=9, color=TEXT)))
        fig_wf.update_layout(**plotly_theme(),
            title=dict(text="NII Waterfall — Income & Expense Breakdown ($mm)", font=dict(color=GOLD, size=16)),
            height=450, margin=dict(l=50, r=20, t=60, b=80), xaxis=dict(tickangle=-30))
        st.plotly_chart(fig_wf, use_container_width=True, key="nii_waterfall")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: ALM KNOWLEDGE BASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📚 ALM Knowledge Base":
    section_header("ALM Knowledge Base — Q&A Guide",
        "All 30 questions from the ALM Notes & Guide sheet", "📚")

    info_card("📖 About This Knowledge Base",
        "Comprehensive Q&A covering all aspects of Gap Analysis in ALM — drawn directly from the "
        "companion Excel model's 'ALM Notes & Guide' sheet. Select a section below.", GOLD)

    section = st.selectbox("Select Section", list(QA_DATA.keys()), key="qa_section")

    bc_map = {
        "Section 1: General ALM Concepts": MID_BLUE,
        "Section 2: Liquidity Gap Analysis": TEAL,
        "Section 3: Interest Rate Sensitivity Gap": ORANGE,
        "Section 4: NII Impact & Earnings at Risk": GREEN,
        "Section 5: Dashboard Metrics & Regulatory Thresholds": PURPLE,
        "Section 6: Practical Usage & Model Limitations": GOLD,
    }

    for i, (q, a) in enumerate(QA_DATA[section]):
        with st.expander(f"❓ {q}", expanded=(i == 0)):
            st.html(f"""
            <div style="user-select:none; color:{TEXT}; -webkit-text-fill-color:{TEXT};
                font-size:0.92rem; line-height:1.7; padding:8px 4px;">{a}</div>
            """)

    # Quick reference formulas
    st.html(f"""
    <div style="user-select:none; background:{CARD_BG}; border:1px solid rgba(255,215,0,0.2);
        border-radius:12px; padding:24px; margin-top:25px;">
        <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-family:'Playfair Display',serif;
            font-size:1.2rem; font-weight:700; text-align:center; margin-bottom:16px;">
            ⚡ Quick Reference — Key Formulas & Thresholds</div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px;">
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem;">Periodic Gap</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.88rem; font-weight:600;">Assets − Liabilities</div></div>
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem;">NII Impact</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.88rem; font-weight:600;">ΔNII = Gap × ΔRate</div></div>
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem;">NIM</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.88rem; font-weight:600;">NII / Total Assets</div></div>
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px; margin-top:10px;">
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem;">Cum Gap / TA</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.88rem; font-weight:600;">&gt; −15% (RBI)</div></div>
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem;">RSA/RSL Ratio</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.88rem; font-weight:600;">0.80x – 1.20x</div></div>
            <div style="text-align:center; padding:12px; background:rgba(0,51,102,0.3); border-radius:8px;">
                <div style="color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.72rem;">NII at Risk / Equity</div>
                <div style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.88rem; font-weight:600;">&lt; 5.0%</div></div>
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
            style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; text-decoration:none;">LinkedIn</a>
        <a href="https://github.com/trichyravis" target="_blank"
            style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:0.8rem; text-decoration:none;">GitHub</a>
    </div>
</div>
""")
