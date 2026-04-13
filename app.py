"""
Go to Market & Early Traction
Entrepreneurship Simulation

A resource-management game where the learner launches a product,
allocates budget across channels, sets pricing, reacts to market
events, and races to hit early traction milestones over 6 weeks.
"""

import math
import random
from typing import Dict, List, Tuple, Any

import pandas as pd
import streamlit as st

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Go to Market & Early Traction",
    page_icon="🚀",
    layout="wide",
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Custom CSS for the game feel
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --purple-main: #6C4BEF;
    --purple-light: #EDE9FE;
    --purple-dark: #4C1D95;
    --green-accent: #10B981;
    --red-accent: #EF4444;
    --orange-accent: #F59E0B;
    --blue-accent: #3B82F6;
    --bg-cream: #FAFAF8;
}

.stApp {
    background-color: var(--bg-cream);
    font-family: 'Inter', sans-serif;
}

.game-header {
    background: linear-gradient(135deg, #6C4BEF 0%, #8B5CF6 50%, #A78BFA 100%);
    color: white;
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
}

.game-header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 700;
}

.game-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
    font-size: 1rem;
}

.metric-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.metric-card .metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1F2937;
}

.metric-card .metric-label {
    font-size: 0.8rem;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.3rem;
}

.channel-card {
    background: white;
    border: 2px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.2s;
}

.channel-card:hover {
    border-color: var(--purple-main);
}

.event-card {
    background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
    border: 2px solid #F59E0B;
    border-radius: 12px;
    padding: 1.2rem;
    margin: 1rem 0;
}

.event-card.negative {
    background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
    border-color: #EF4444;
}

.event-card.positive {
    background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
    border-color: #10B981;
}

.week-badge {
    display: inline-block;
    background: var(--purple-main);
    color: white;
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.9rem;
}

.insight-box {
    background: var(--purple-light);
    border-left: 4px solid var(--purple-main);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.95rem;
    color: #374151;
}

.score-ring {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin: 0 auto;
}

.result-narrative {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    line-height: 1.7;
    font-size: 0.95rem;
}

.stButton > button {
    background: linear-gradient(135deg, #6C4BEF, #8B5CF6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 0.95rem;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #5B3FD4, #7C4FE0);
    color: white;
}

.progress-bar-container {
    background: #E5E7EB;
    border-radius: 8px;
    height: 12px;
    overflow: hidden;
    margin: 0.5rem 0;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Constants and game data
# ---------------------------------------------------------------------------

TOTAL_WEEKS = 6
STARTING_BUDGET = 2500  # dollars
WEEKLY_BURN = 200       # fixed costs per week (hosting, tools, etc.)

# Product variants (continuing ThermaLoop from previous sims)
PRODUCTS = {
    "home_comfort": {
        "name": "ThermaLoop Home",
        "tagline": "Smart vents + app to eliminate hot/cold rooms",
        "base_price": 129,
        "target_customer": "Homeowners frustrated with uneven temperatures",
        "icon": "🏠",
    },
    "landlord_energy": {
        "name": "ThermaLoop Pro",
        "tagline": "Sensor kit + portal for landlords to cut HVAC waste",
        "base_price": 199,
        "target_customer": "Small landlords managing 5 to 50 units",
        "icon": "🏢",
    },
    "installer_tools": {
        "name": "ThermaLoop Installer Kit",
        "tagline": "Pro diagnostic kit for HVAC airflow issues",
        "base_price": 349,
        "target_customer": "HVAC installers and contractors",
        "icon": "🔧",
    },
}

# Marketing channels with characteristics
CHANNELS = {
    "social_organic": {
        "name": "Social Media (Organic)",
        "icon": "📱",
        "desc": "Post content on Instagram, TikTok, and Facebook. Small cash cost (tools, stock photos), heavy time commitment, slow to build.",
        "cost_per_week": 25,
        "time_investment": "High",
        "base_reach": 120,
        "base_conv": 0.012,
        "ramp_bonus": 0.25,  # improves 25% each consecutive week
        "quality": 0.7,
        "best_for": ["home_comfort"],
    },
    "paid_social": {
        "name": "Paid Social Ads",
        "icon": "💰",
        "desc": "Targeted ads on Facebook and Instagram. Fast reach, costs add up.",
        "cost_per_week": 350,
        "time_investment": "Low",
        "base_reach": 600,
        "base_conv": 0.022,
        "ramp_bonus": 0.08,
        "quality": 0.5,
        "best_for": ["home_comfort", "landlord_energy"],
    },
    "content_seo": {
        "name": "Content & SEO",
        "icon": "📝",
        "desc": "Blog posts, guides, and search optimization. Very slow start, compounds over time.",
        "cost_per_week": 100,
        "time_investment": "High",
        "base_reach": 40,
        "base_conv": 0.035,
        "ramp_bonus": 0.50,  # compounds heavily
        "quality": 0.85,
        "best_for": ["home_comfort", "landlord_energy", "installer_tools"],
    },
    "cold_outreach": {
        "name": "Cold Email / DM Outreach",
        "icon": "📧",
        "desc": "Direct messages to potential customers. Low cost, labor intensive, targeted.",
        "cost_per_week": 75,
        "time_investment": "Very High",
        "base_reach": 50,
        "base_conv": 0.05,
        "ramp_bonus": 0.05,
        "quality": 0.8,
        "best_for": ["landlord_energy", "installer_tools"],
    },
    "partnerships": {
        "name": "Partnerships & Referrals",
        "icon": "🤝",
        "desc": "Partner with complementary businesses. Slow to set up, high quality leads.",
        "cost_per_week": 150,
        "time_investment": "Medium",
        "base_reach": 30,
        "base_conv": 0.08,
        "ramp_bonus": 0.30,
        "quality": 0.9,
        "best_for": ["installer_tools", "landlord_energy"],
    },
    "trade_events": {
        "name": "Trade Shows & Events",
        "icon": "🎪",
        "desc": "Attend industry events. Expensive but face to face trust building.",
        "cost_per_week": 500,
        "time_investment": "Medium",
        "base_reach": 80,
        "base_conv": 0.10,
        "ramp_bonus": -0.10,  # diminishing returns from same events
        "quality": 0.95,
        "best_for": ["installer_tools", "landlord_energy"],
    },
    "influencer": {
        "name": "Influencer / Creator Collab",
        "icon": "🌟",
        "desc": "Partner with home improvement or HVAC creators. Bursty reach, hit or miss.",
        "cost_per_week": 300,
        "time_investment": "Low",
        "base_reach": 400,
        "base_conv": 0.015,
        "ramp_bonus": -0.05,
        "quality": 0.55,
        "best_for": ["home_comfort"],
    },
    "community": {
        "name": "Online Communities & Forums",
        "icon": "💬",
        "desc": "Engage in Reddit, niche forums, Facebook groups. Authentic but fragile.",
        "cost_per_week": 50,
        "time_investment": "High",
        "base_reach": 80,
        "base_conv": 0.03,
        "ramp_bonus": 0.25,
        "quality": 0.75,
        "best_for": ["home_comfort", "installer_tools"],
    },
}

# Pricing tiers relative to base price
PRICING_OPTIONS = {
    "aggressive_low": {
        "label": "Aggressive Low",
        "multiplier": 0.70,
        "conv_boost": 1.4,
        "margin": 0.15,
        "desc": "Price 30% below target to drive volume. Thin margins but fast adoption.",
    },
    "competitive": {
        "label": "Competitive",
        "multiplier": 0.90,
        "conv_boost": 1.15,
        "margin": 0.35,
        "desc": "Slightly below market to be attractive. Healthy margins, solid conversion.",
    },
    "value_based": {
        "label": "Value Based",
        "multiplier": 1.00,
        "conv_boost": 1.0,
        "margin": 0.50,
        "desc": "Price reflects the value delivered. Standard conversion, strong margins.",
    },
    "premium": {
        "label": "Premium",
        "multiplier": 1.25,
        "conv_boost": 0.70,
        "margin": 0.65,
        "desc": "Premium positioning. Fewer sales but higher margin per unit.",
    },
}

# Messaging angles to test
MESSAGING_OPTIONS = {
    "pain_focused": {
        "label": "Pain Focused",
        "desc": "Lead with the problem: 'Tired of rooms that are too hot or too cold?'",
        "resonance": {"home_comfort": 1.3, "landlord_energy": 1.1, "installer_tools": 0.8},
    },
    "savings_focused": {
        "label": "Savings Focused",
        "desc": "Lead with money: 'Cut your energy bill by up to 25%.'",
        "resonance": {"home_comfort": 1.0, "landlord_energy": 1.4, "installer_tools": 0.7},
    },
    "tech_innovation": {
        "label": "Tech & Innovation",
        "desc": "Lead with the product: 'Smart sensors that learn your home.'",
        "resonance": {"home_comfort": 0.8, "landlord_energy": 0.7, "installer_tools": 1.1},
    },
    "social_proof": {
        "label": "Social Proof",
        "desc": "Lead with others: 'Join 200+ homeowners who fixed their comfort.'",
        "resonance": {"home_comfort": 1.1, "landlord_energy": 1.2, "installer_tools": 1.3},
    },
    "roi_professional": {
        "label": "ROI / Professional",
        "desc": "Lead with business results: 'Reduce callbacks 30%. Diagnose in 5 minutes.'",
        "resonance": {"home_comfort": 0.6, "landlord_energy": 1.3, "installer_tools": 1.5},
    },
}

# Market events that can happen each week
MARKET_EVENTS = [
    {
        "week_trigger": 2,
        "title": "Competitor Launches Similar Product",
        "desc": "A well-funded competitor just launched a similar smart vent product at a lower price point. Your paid ad costs jump 20% as they bid on the same keywords.",
        "type": "negative",
        "effect": {"paid_social_cost_mult": 1.2, "conv_mult": 0.85},
        "response_options": {
            "differentiate": {
                "label": "Double down on differentiation",
                "desc": "Invest extra $200 to create comparison content showing your unique advantages.",
                "cost": 200,
                "effect": {"conv_mult": 1.1, "quality_boost": 0.1},
            },
            "undercut": {
                "label": "Temporarily drop price 15%",
                "desc": "Match their aggression with a limited time offer.",
                "cost": 0,
                "effect": {"conv_mult": 1.2, "margin_mult": 0.85},
            },
            "ignore": {
                "label": "Stay the course",
                "desc": "Focus on your existing customers and channels. Do not react.",
                "cost": 0,
                "effect": {"conv_mult": 0.95},
            },
        },
    },
    {
        "week_trigger": 3,
        "title": "Customer Success Story Goes Viral",
        "desc": "An early customer posted a video showing their energy bill before and after your product. It is getting shared widely.",
        "type": "positive",
        "effect": {"social_organic_reach_mult": 2.5, "conv_mult": 1.15},
        "response_options": {
            "amplify": {
                "label": "Boost the post with $300 ad spend",
                "desc": "Put money behind the organic momentum to maximize reach.",
                "cost": 300,
                "effect": {"reach_mult": 1.8, "conv_mult": 1.1},
            },
            "case_study": {
                "label": "Turn it into a case study",
                "desc": "Interview the customer and create detailed content. Takes time but lasting value.",
                "cost": 100,
                "effect": {"content_seo_reach_mult": 2.0, "quality_boost": 0.15},
            },
            "ride_wave": {
                "label": "Let it ride naturally",
                "desc": "Engage in comments but do not spend money. Save budget for later.",
                "cost": 0,
                "effect": {"conv_mult": 1.05},
            },
        },
    },
    {
        "week_trigger": 4,
        "title": "Supply Chain Delay",
        "desc": "Your manufacturer just told you the next batch of units will be 2 weeks late. You have limited inventory.",
        "type": "negative",
        "effect": {"max_sales_cap": 15},
        "response_options": {
            "waitlist": {
                "label": "Create an exclusive waitlist",
                "desc": "Turn scarcity into a feature. 'Limited batch, reserve yours now.' Capture emails.",
                "cost": 50,
                "effect": {"conv_mult": 1.1, "email_capture": 30},
            },
            "pause_ads": {
                "label": "Pause paid channels",
                "desc": "Stop spending on ads to conserve budget until inventory arrives.",
                "cost": 0,
                "effect": {"pause_paid": True, "budget_saved": 400},
            },
            "presell": {
                "label": "Offer pre-orders at a discount",
                "desc": "Sell units at 10% off for delivery in 2 weeks. Revenue now, delivery later.",
                "cost": 0,
                "effect": {"conv_mult": 1.25, "margin_mult": 0.90, "presale": True},
            },
        },
    },
    {
        "week_trigger": 5,
        "title": "Press Coverage Opportunity",
        "desc": "A home improvement blog with 50K monthly readers wants to review your product. They need a sample unit and a $150 sponsorship fee.",
        "type": "positive",
        "effect": {},
        "response_options": {
            "full_sponsor": {
                "label": "Send unit + pay sponsorship",
                "desc": "Go all in on the coverage. Could be a major credibility boost.",
                "cost": 280,
                "effect": {"bonus_reach": 800, "conv_mult": 1.2, "quality_boost": 0.2},
            },
            "unit_only": {
                "label": "Send unit, skip sponsorship",
                "desc": "They might still cover you, but it will not be a featured review.",
                "cost": 130,
                "effect": {"bonus_reach": 200, "conv_mult": 1.05},
            },
            "decline": {
                "label": "Pass on it",
                "desc": "Save the money. You are not sure the audience is the right fit.",
                "cost": 0,
                "effect": {},
            },
        },
    },
]

# Traction milestones (product-aware: B2B products have adjusted targets)
def get_milestones(product_key: str = None) -> List[Dict]:
    """Return milestones adjusted for product type. B2B products have lower
    customer count thresholds but higher revenue targets."""
    is_b2b = product_key in ("installer_tools", "landlord_energy")
    return [
        {"name": "First Sale", "target": 1, "metric": "total_sales", "points": 5, "icon": "🎉"},
        {"name": "10 Customers" if not is_b2b else "5 Customers", "target": 10 if not is_b2b else 5, "metric": "total_sales", "points": 10, "icon": "📈"},
        {"name": "25 Customers" if not is_b2b else "15 Customers", "target": 25 if not is_b2b else 15, "metric": "total_sales", "points": 15, "icon": "🔥"},
        {"name": "50 Customers" if not is_b2b else "30 Customers", "target": 50 if not is_b2b else 30, "metric": "total_sales", "points": 20, "icon": "💥"},
        {"name": "$1K Revenue Week", "target": 1000, "metric": "best_week_revenue", "points": 10, "icon": "💰"},
        {"name": "$5K Total Revenue" if not is_b2b else "$7K Total Revenue", "target": 5000 if not is_b2b else 7000, "metric": "total_revenue", "points": 15, "icon": "🏆"},
        {"name": "CAC Under $50" if not is_b2b else "CAC Under $100", "target": 50 if not is_b2b else 100, "metric": "cac_under", "points": 10, "icon": "🎯"},
        {"name": "Positive Unit Economics", "target": 1, "metric": "unit_econ_positive", "points": 15, "icon": "✅"},
        {"name": "3 Channels Tested", "target": 3, "metric": "channels_tested", "points": 5, "icon": "🧪"},
        {"name": "Repeat Customer", "target": 1, "metric": "repeat_customers", "points": 15, "icon": "🔄"},
    ]

# Default for initial use
MILESTONES = get_milestones()


# ---------------------------------------------------------------------------
# Session state initialization
# ---------------------------------------------------------------------------
def init_state():
    defaults = {
        "stage": "intro",
        "product_key": None,
        "pricing_key": None,
        "messaging_key": None,
        "week": 1,
        "budget": STARTING_BUDGET,
        "active_channels": [],
        "channel_history": {},    # channel -> list of weeks active
        "weekly_results": [],     # list of dicts per week
        "total_sales": 0,
        "total_revenue": 0.0,
        "total_ad_spend": 0.0,
        "total_leads": 0,
        "email_list": 0,
        "best_week_revenue": 0.0,
        "milestones_hit": [],
        "event_responses": {},    # week -> response key
        "current_event": None,
        "channels_ever_used": [],
        "rng_seed": random.randint(1, 9999),
        "weekly_channel_alloc": {},
        "repeat_customers": 0,
        "margin_modifier": 1.0,
        "conv_modifier": 1.0,
        "reach_modifier": 1.0,
        "quality_modifier": 0.0,
        "sales_cap": None,
        "pivot_count": 0,
        "spend_by_channel": {},  # week -> {channel: dollars}
        "name": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def get_product():
    return PRODUCTS.get(st.session_state.product_key, {})

def get_pricing():
    return PRICING_OPTIONS.get(st.session_state.pricing_key, {})

def get_messaging():
    return MESSAGING_OPTIONS.get(st.session_state.messaging_key, {})

def calculate_effective_price():
    product = get_product()
    pricing = get_pricing()
    return product.get("base_price", 100) * pricing.get("multiplier", 1.0)

def active_milestones():
    """Return milestones appropriate for the current product."""
    return get_milestones(st.session_state.get("product_key"))


def check_milestones():
    """Check and award milestones."""
    ss = st.session_state
    newly_hit = []
    for m in active_milestones():
        if m["name"] in ss.milestones_hit:
            continue
        metric = m["metric"]
        target = m["target"]
        hit = False
        if metric == "total_sales":
            hit = ss.total_sales >= target
        elif metric == "total_revenue":
            hit = ss.total_revenue >= target
        elif metric == "best_week_revenue":
            hit = ss.best_week_revenue >= target
        elif metric == "cac_under":
            if ss.total_sales > 0 and ss.total_ad_spend > 0:
                cac = ss.total_ad_spend / ss.total_sales
                hit = cac <= target
        elif metric == "unit_econ_positive":
            price = calculate_effective_price()
            pricing = get_pricing()
            margin = pricing.get("margin", 0.5) * ss.margin_modifier
            if ss.total_sales > 0:
                cac = ss.total_ad_spend / ss.total_sales
                hit = (price * margin) > cac
        elif metric == "channels_tested":
            hit = len(ss.channels_ever_used) >= target
        elif metric == "repeat_customers":
            hit = ss.repeat_customers >= target
        if hit:
            ss.milestones_hit.append(m["name"])
            newly_hit.append(m)
    return newly_hit


def project_channel(ch_key: str, spend: float, week: int = None) -> Dict[str, Any]:
    """Deterministic projection of a channel's funnel at a given spend level.
    Uses diminishing-returns scaling: reach ~ spend^0.7 relative to base cost.
    No randomness — for live preview before running the week.
    """
    ss = st.session_state
    ch = CHANNELS[ch_key]
    base_cost = max(ch["cost_per_week"], 1)
    if spend <= 0:
        return {"spend": 0, "reach": 0, "leads": 0, "sales": 0, "cac": 0,
                "conv_rate": 0, "saturation": 0}

    # Spend ratio with diminishing returns
    spend_ratio = spend / base_cost
    # saturation: once spend > 3x base, returns flatten hard
    scale = spend_ratio ** 0.7

    product_key = ss.product_key
    week = week or ss.week
    history = ss.channel_history.get(ch_key, [])
    consecutive = 0
    for w in range(week - 1, 0, -1):
        if w in history:
            consecutive += 1
        else:
            break

    reach_raw = ch["base_reach"] * (1 + ch["ramp_bonus"] * consecutive) * scale
    fit_bonus = 1.3 if product_key in ch.get("best_for", []) else 0.6
    reach = int(reach_raw * fit_bonus * ss.reach_modifier)

    pricing = get_pricing() or {"conv_boost": 1.0, "margin": 0.5, "multiplier": 1.0}
    messaging = get_messaging() or {"resonance": {}}
    msg_resonance = messaging.get("resonance", {}).get(product_key, 1.0)
    conv = ch["base_conv"] * pricing.get("conv_boost", 1.0) * msg_resonance * ss.conv_modifier
    conv = max(0.001, min(conv, 0.15))
    leads = int(reach * conv)

    # Expected close rate ~0.65 (mean of 0.5-0.8)
    avg_quality = ch["quality"] + ss.quality_modifier
    close_rate = 0.65 * min(avg_quality, 1.2)
    sales = int(leads * close_rate)

    saturation = min(1.0, spend_ratio / 3.0)  # 0-1, how saturated the channel is
    cac = spend / max(sales, 1) if sales > 0 else spend  # spend / projected sales

    return {
        "spend": spend, "reach": reach, "leads": leads,
        "sales": sales, "cac": cac, "conv_rate": conv,
        "saturation": saturation,
    }


def project_week(spend_by_channel: Dict[str, float]) -> Dict[str, Any]:
    """Project full-funnel outcomes for a week given spend per channel.
    Deterministic — for live UI preview."""
    ss = st.session_state
    total_spend = sum(spend_by_channel.values()) + WEEKLY_BURN
    total_reach = 0
    total_leads = 0
    total_sales = 0
    per_channel = {}
    for ch_key, spend in spend_by_channel.items():
        if spend <= 0:
            continue
        proj = project_channel(ch_key, spend)
        per_channel[ch_key] = proj
        total_reach += proj["reach"]
        total_leads += proj["leads"]
        total_sales += proj["sales"]

    price = calculate_effective_price()
    margin = (get_pricing() or {}).get("margin", 0.5) * ss.margin_modifier
    revenue = total_sales * price
    gross_profit = revenue * margin
    ad_spend = sum(spend_by_channel.values())
    cac = ad_spend / total_sales if total_sales > 0 else 0
    # LTV: assume 3x-equivalent value (repeat + referral); margin-adjusted
    ltv = price * margin * 3.0
    payback_months = (cac / (price * margin)) if (price * margin) > 0 and cac > 0 else 0
    ltv_cac = (ltv / cac) if cac > 0 else 0

    return {
        "per_channel": per_channel,
        "total_spend": total_spend,
        "ad_spend": ad_spend,
        "total_reach": total_reach,
        "total_leads": total_leads,
        "projected_sales": total_sales,
        "projected_revenue": revenue,
        "projected_gross_profit": gross_profit,
        "cac": cac,
        "ltv": ltv,
        "ltv_cac": ltv_cac,
        "payback_months": payback_months,
    }


def simulate_week(spend_by_channel: Dict[str, float]) -> Dict[str, Any]:
    """Run one week of go-to-market simulation with real funnel math.

    spend_by_channel: {channel_key: dollars_spent_this_week}. Channels with
    spend > 0 are active. Reach scales with spend^0.7 (diminishing returns),
    so doubling spend does NOT double reach — learners must grapple with
    channel saturation.
    """
    ss = st.session_state
    rng = random.Random(ss.rng_seed + ss.week * 137)

    product_key = ss.product_key
    pricing = get_pricing()
    messaging = get_messaging()
    price = calculate_effective_price()
    margin = pricing.get("margin", 0.5) * ss.margin_modifier

    total_reach = 0
    total_leads = 0
    total_cost = WEEKLY_BURN
    total_ad_spend = 0.0
    channel_results = {}
    active_channels = [k for k, v in spend_by_channel.items() if v > 0]

    for ch_key in active_channels:
        ch = CHANNELS[ch_key]
        spend = float(spend_by_channel[ch_key])
        base_cost = max(ch["cost_per_week"], 1)
        spend_ratio = spend / base_cost
        scale = spend_ratio ** 0.7  # diminishing returns

        # Calculate consecutive weeks for ramp bonus
        history = ss.channel_history.get(ch_key, [])
        consecutive = 0
        for w in range(ss.week - 1, 0, -1):
            if w in history:
                consecutive += 1
            else:
                break

        # Base reach with ramp + spend scaling
        reach = ch["base_reach"] * (1 + ch["ramp_bonus"] * consecutive) * scale

        # Channel fit bonus (strong penalty for misfit)
        fit_bonus = 1.3 if product_key in ch.get("best_for", []) else 0.6

        # Messaging resonance
        msg_resonance = messaging.get("resonance", {}).get(product_key, 1.0)

        # Apply modifiers with randomness
        reach = reach * fit_bonus * ss.reach_modifier
        reach = int(reach * rng.uniform(0.75, 1.25))

        # Conversion rate
        conv = ch["base_conv"] * pricing["conv_boost"] * msg_resonance * ss.conv_modifier
        conv = conv * rng.uniform(0.7, 1.3)
        conv = max(0.001, min(conv, 0.15))

        leads = int(reach * conv)
        leads = max(0, leads)

        total_reach += reach
        total_leads += leads
        total_cost += spend
        total_ad_spend += spend

        channel_results[ch_key] = {
            "reach": reach,
            "leads": leads,
            "cost": spend,
            "conv_rate": conv,
            "cac": spend / max(leads, 1),
            "saturation": min(1.0, spend_ratio / 3.0),
        }

    # Apply sales cap if active
    if ss.sales_cap is not None:
        total_leads = min(total_leads, ss.sales_cap)
        ss.sales_cap = None  # Reset after one week

    # Some leads convert to sales (not all leads buy)
    close_rate = rng.uniform(0.5, 0.8)
    # Quality modifier
    avg_quality = 0.7
    if active_channels:
        avg_quality = sum(CHANNELS[c]["quality"] for c in active_channels) / len(active_channels)
    avg_quality += ss.quality_modifier
    close_rate *= min(avg_quality, 1.2)

    sales = max(1 if total_leads >= 2 else 0, int(total_leads * close_rate))
    revenue = sales * price
    gross_profit = revenue * margin - total_cost

    # Chance of repeat customer after week 3
    repeat = 0
    if ss.week >= 3 and ss.total_sales > 5:
        repeat_chance = 0.05 * avg_quality * rng.uniform(0.5, 1.5)
        repeat = int(ss.total_sales * repeat_chance)
        repeat = max(0, min(repeat, 3))

    # Email list growth (some leads who don't buy still give email)
    email_signups = int((total_leads - sales) * rng.uniform(0.2, 0.5))
    email_signups = max(0, email_signups)

    # Compute week-level CAC, LTV, payback
    week_cac = total_ad_spend / sales if sales > 0 else 0
    week_ltv = price * margin * 3.0  # 3x contribution-margin dollars
    week_ltv_cac = (week_ltv / week_cac) if week_cac > 0 else 0
    week_payback = (week_cac / (price * margin)) if (price * margin) > 0 and week_cac > 0 else 0

    result = {
        "week": ss.week,
        "channels": active_channels,
        "channel_results": channel_results,
        "total_reach": total_reach,
        "total_leads": total_leads,
        "sales": sales,
        "repeat_sales": repeat,
        "revenue": revenue,
        "total_cost": total_cost,
        "ad_spend": total_ad_spend,
        "gross_profit": gross_profit,
        "week_cac": week_cac,
        "week_ltv": week_ltv,
        "week_ltv_cac": week_ltv_cac,
        "week_payback_months": week_payback,
        "margin": margin,
        "email_signups": email_signups,
        "close_rate": close_rate,
    }

    return result


def get_cac():
    ss = st.session_state
    if ss.total_sales > 0 and ss.total_ad_spend > 0:
        return ss.total_ad_spend / ss.total_sales
    return 0


def render_metric_card(label, value, color="#1F2937"):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: {color};">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def render_progress_bar(current, target, color="#6C4BEF"):
    pct = min(100, int((current / max(target, 1)) * 100))
    st.markdown(f"""
    <div class="progress-bar-container">
        <div class="progress-bar-fill" style="width: {pct}%; background: {color};"></div>
    </div>
    """, unsafe_allow_html=True)


def generate_weekly_narrative(result: Dict) -> str:
    """Generate a narrative paragraph explaining what happened this week."""
    sales = result["sales"]
    leads = result["total_leads"]
    reach = result["total_reach"]
    revenue = result["revenue"]
    week = result["week"]
    channels = result["channels"]

    # Find best and worst channel
    best_ch = None
    worst_ch = None
    if result["channel_results"]:
        sorted_chs = sorted(
            result["channel_results"].items(),
            key=lambda x: x[1]["leads"],
            reverse=True,
        )
        best_ch = sorted_chs[0]
        if len(sorted_chs) > 1:
            worst_ch = sorted_chs[-1]

    parts = []

    if week == 1:
        if sales == 0:
            parts.append(
                f"Your first week is about planting seeds, not harvesting. "
                f"You reached {reach:,} people and generated {leads} {'lead' if leads == 1 else 'leads'}, "
                f"but nobody bought yet. That is normal. Most channels need time to warm up."
            )
        else:
            parts.append(
                f"A strong start. In your very first week, you reached {reach:,} people, "
                f"converted {leads} leads, and closed {sales} sales for ${revenue:,.0f} in revenue. "
                f"First revenue is a huge milestone."
            )
    else:
        prev = None
        ss = st.session_state
        if len(ss.weekly_results) >= 2:
            prev = ss.weekly_results[-2]

        if prev and sales > prev["sales"]:
            growth = ((sales - prev["sales"]) / max(prev["sales"], 1)) * 100
            parts.append(f"Sales grew {growth:.0f}% over last week. Momentum is building.")
        elif prev and sales < prev["sales"]:
            parts.append("Sales dipped this week compared to last. Worth investigating why.")
        elif prev and sales == prev["sales"]:
            parts.append("Sales held steady this week. Consistent, but look for ways to break through.")

    if best_ch:
        ch_name = CHANNELS[best_ch[0]]["name"]
        ch_leads = best_ch[1]["leads"]
        parts.append(f"Your top performer was {ch_name} with {ch_leads} leads.")

    if worst_ch and worst_ch[1]["leads"] == 0:
        ch_name = CHANNELS[worst_ch[0]]["name"]
        parts.append(f"{ch_name} generated zero leads this week. Consider dropping it or giving it more time to ramp.")

    if result.get("repeat_sales", 0) > 0:
        parts.append(f"Great sign: {result['repeat_sales']} previous customers came back for more.")

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Stage: Intro
# ---------------------------------------------------------------------------
def render_intro():
    st.markdown("""
    <div class="game-header">
        <h1>🚀 Go to Market & Early Traction</h1>
        <p>You have built your product. Now it is time to find your first real customers.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="result-narrative">
    <strong>The Scenario</strong><br><br>
    Your ThermaLoop product is ready to ship. You have validated the problem, tested your assumptions, and
    built an MVP. Now comes the real test: can you get paying customers?
    <br><br>
    You start with <strong>$2,500</strong> in marketing budget and <strong>6 weeks</strong> to hit as many
    traction milestones as possible. Each week, you choose which marketing channels to activate, react to
    market events, and watch your metrics evolve. <strong>Profits from sales go back into your budget</strong>,
    so strong early weeks give you more runway to invest later.
    <br><br>
    <strong>Your goal:</strong> Maximize customers, revenue, and learning while keeping your unit economics healthy.
    Every dollar counts. Every channel choice matters. Every pivot has a cost.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("Let's Launch 🚀", key="btn_start", type="primary"):
        st.session_state.name = "Founder"
        st.session_state.stage = "choose_product"
        st.rerun()


# ---------------------------------------------------------------------------
# Stage: Choose Product
# ---------------------------------------------------------------------------
def render_choose_product():
    st.markdown("""
    <div class="game-header">
        <h1>📦 Choose Your Product</h1>
        <p>Which ThermaLoop variant are you taking to market?</p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, (key, prod) in enumerate(PRODUCTS.items()):
        with cols[i]:
            st.markdown(f"""
            <div class="channel-card" style="text-align: center; min-height: 200px;">
                <div style="font-size: 2.5rem;">{prod['icon']}</div>
                <h4 style="margin: 0.5rem 0 0.3rem 0;">{prod['name']}</h4>
                <p style="color: #6B7280; font-size: 0.85rem;">{prod['tagline']}</p>
                <p style="font-size: 0.8rem; color: #9CA3AF;"><strong>Base Price:</strong> ${prod['base_price']}</p>
                <p style="font-size: 0.8rem; color: #9CA3AF;">{prod['target_customer']}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Launch {prod['name']}", key=f"btn_prod_{key}"):
                st.session_state.product_key = key
                st.session_state.stage = "choose_strategy"
                st.rerun()


# ---------------------------------------------------------------------------
# Stage: Choose Strategy (Pricing + Messaging)
# ---------------------------------------------------------------------------
def render_choose_strategy():
    product = get_product()
    st.markdown(f"""
    <div class="game-header">
        <h1>🎯 Set Your Launch Strategy</h1>
        <p>Launching {product['name']}. Choose your pricing and messaging approach.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Pricing Strategy")
        st.markdown(f"*Base product price: ${product['base_price']}*")
        pricing_choice = st.radio(
            "Choose pricing",
            options=list(PRICING_OPTIONS.keys()),
            format_func=lambda k: f"{PRICING_OPTIONS[k]['label']} (${product['base_price'] * PRICING_OPTIONS[k]['multiplier']:.0f})",
            key="radio_pricing",
            label_visibility="collapsed",
        )
        p = PRICING_OPTIONS[pricing_choice]
        st.markdown(f"""
        <div class="insight-box">
            {p['desc']}<br>
            <strong>Margin:</strong> {p['margin']*100:.0f}% | <strong>Conversion boost:</strong> {'+' if p['conv_boost']>=1 else ''}{(p['conv_boost']-1)*100:.0f}%
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("##### Messaging Angle")
        messaging_choice = st.radio(
            "Choose messaging",
            options=list(MESSAGING_OPTIONS.keys()),
            format_func=lambda k: MESSAGING_OPTIONS[k]["label"],
            key="radio_messaging",
            label_visibility="collapsed",
        )
        m = MESSAGING_OPTIONS[messaging_choice]
        resonance = m["resonance"].get(st.session_state.product_key, 1.0)
        resonance_label = "Strong" if resonance >= 1.2 else "Good" if resonance >= 1.0 else "Weak" if resonance >= 0.8 else "Poor"
        resonance_color = "#10B981" if resonance >= 1.2 else "#3B82F6" if resonance >= 1.0 else "#F59E0B" if resonance >= 0.8 else "#EF4444"
        st.markdown(f"""
        <div class="insight-box">
            {m['desc']}<br>
            <strong>Fit for {product['name']}:</strong> <span style="color: {resonance_color}; font-weight: 600;">{resonance_label}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("")
    if st.button("Lock In Strategy & Start Week 1 🔒", key="btn_lock_strategy"):
        st.session_state.pricing_key = pricing_choice
        st.session_state.messaging_key = messaging_choice
        st.session_state.stage = "weekly_play"
        st.rerun()


# ---------------------------------------------------------------------------
# Stage: Weekly Play
# ---------------------------------------------------------------------------
def render_weekly_play():
    ss = st.session_state
    product = get_product()
    week = ss.week

    # If budget is below fixed burn, force end
    if ss.budget < WEEKLY_BURN:
        st.markdown(f"""
        <div class="game-header" style="background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);">
            <h1>💸 Runway Exhausted</h1>
            <p>You have ${ss.budget:,.0f} left but need ${WEEKLY_BURN} per week for fixed costs. Your launch window is over.</p>
        </div>
        """, unsafe_allow_html=True)
        weeks_played = len(ss.weekly_results)
        st.markdown(f"""
        <div class="result-narrative">
            You made it {weeks_played} of {TOTAL_WEEKS} weeks before running out of budget. In the real world,
            this is what "running out of runway" feels like. It does not mean your product failed; it means
            your burn rate outpaced your learning. The question to ask yourself: did you learn enough in those
            {weeks_played} weeks to know what to do next?
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
        if st.button("See Final Results 🏁", key="btn_forced_end"):
            ss.stage = "results"
            st.rerun()
        return

    # Check for market event this week
    event_this_week = None
    for evt in MARKET_EVENTS:
        if evt["week_trigger"] == week and week not in ss.event_responses:
            event_this_week = evt
            break

    # If there is an unresolved event, show it first
    if event_this_week and ss.current_event is None:
        ss.current_event = event_this_week

    if ss.current_event is not None:
        render_market_event(ss.current_event)
        return

    # Weekly dashboard header
    st.markdown(f"""
    <div class="game-header">
        <h1>Week {week} of {TOTAL_WEEKS}</h1>
        <p>{product['icon']} {product['name']} | Budget: ${ss.budget:,.0f} remaining</p>
    </div>
    """, unsafe_allow_html=True)

    # Metrics bar
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        render_metric_card("Total Customers", ss.total_sales, "#6C4BEF")
    with c2:
        render_metric_card("Total Revenue", f"${ss.total_revenue:,.0f}", "#10B981")
    with c3:
        render_metric_card("Email List", ss.email_list, "#3B82F6")
    with c4:
        cac = get_cac()
        cac_color = "#10B981" if cac < 50 else "#F59E0B" if cac < 100 else "#EF4444"
        render_metric_card("Avg CAC", f"${cac:,.0f}" if cac > 0 else "N/A", cac_color)
    with c5:
        render_metric_card("Budget Left", f"${ss.budget:,.0f}", "#EF4444" if ss.budget < 500 else "#1F2937")

    # Show previous week results if any
    if ss.weekly_results:
        last = ss.weekly_results[-1]
        with st.expander(f"Week {last['week']} Results", expanded=True):
            # Narrative
            narrative = generate_weekly_narrative(last)
            st.markdown(f"""
            <div class="result-narrative">
                {narrative}
            </div>
            """, unsafe_allow_html=True)

            rc1, rc2, rc3, rc4 = st.columns(4)
            with rc1:
                st.metric("Reach", f"{last['total_reach']:,}")
            with rc2:
                st.metric("Leads", last["total_leads"])
            with rc3:
                st.metric("Sales", last["sales"] + last.get("repeat_sales", 0))
            with rc4:
                st.metric("Revenue", f"${last['revenue']:,.0f}")

            # Channel breakdown with ROI
            if last["channel_results"]:
                st.markdown("**Channel Breakdown:**")
                # Allocate revenue proportionally by leads for per-channel ROI
                total_wk_leads = max(1, sum(cr["leads"] for cr in last["channel_results"].values()))
                wk_gross_profit = last["revenue"] * last.get("margin", 0.5)
                for ch_key, cr in last["channel_results"].items():
                    ch = CHANNELS[ch_key]
                    ch_cac_display = f"${cr['cac']:,.0f}" if cr['leads'] > 0 else "N/A"
                    # Revenue attribution: share of gross profit proportional to leads
                    attributed_gp = wk_gross_profit * (cr["leads"] / total_wk_leads)
                    ch_cost = max(1, cr["cost"])
                    roi_pct = ((attributed_gp - cr["cost"]) / ch_cost) * 100 if cr["cost"] > 0 else (attributed_gp * 100 if attributed_gp > 0 else 0)
                    roi_color = "#10B981" if roi_pct >= 0 else "#EF4444"
                    roi_display = f"<span style='color:{roi_color};font-weight:600;'>{roi_pct:+.0f}%</span>"
                    st.markdown(
                        f"{ch['icon']} **{ch['name']}**: "
                        f"Reach {cr['reach']:,} | Leads {cr['leads']} | "
                        f"Conv {cr['conv_rate']*100:.1f}% | "
                        f"CAC {ch_cac_display} | "
                        f"ROI {roi_display}",
                        unsafe_allow_html=True
                    )

            # Show newly hit milestones
            newly_hit = [m for m in active_milestones() if m["name"] in ss.milestones_hit]
            if newly_hit and last["week"] == ss.week - 1:
                recent_milestones = []
                # Check which milestones were just hit
                prev_sales_before = ss.total_sales - last["sales"] - last.get("repeat_sales", 0)
                for m in active_milestones():
                    if m["name"] in ss.milestones_hit:
                        if m["metric"] == "total_sales" and prev_sales_before < m["target"] <= ss.total_sales:
                            recent_milestones.append(m)
                        elif m["metric"] == "best_week_revenue" and last["revenue"] >= m["target"]:
                            recent_milestones.append(m)
                for m in recent_milestones:
                    st.success(f"{m['icon']} Milestone unlocked: **{m['name']}** (+{m['points']} pts)")

    # Milestones tracker
    with st.expander("🏆 Milestones", expanded=False):
        for m in active_milestones():
            hit = m["name"] in ss.milestones_hit
            status = "✅" if hit else "⬜"
            st.markdown(f"{status} {m['icon']} **{m['name']}** (+{m['points']} pts)")

    st.markdown("---")

    # Channel allocation — per-channel spend sliders
    st.markdown("##### Allocate Your Weekly Channel Budget")
    st.markdown(
        "*Move the sliders to set how much to spend on each channel this week. "
        "Doubling spend does not double reach — each channel has diminishing returns past its "
        "base cost, so you have to pick your bets. $0 means the channel is off.*"
    )

    available_budget = ss.budget - WEEKLY_BURN
    spend_by_channel: Dict[str, float] = {}
    total_channel_spend = 0.0

    # Build sliders in a grid
    ch_cols = st.columns(2)
    for i, (ch_key, ch) in enumerate(CHANNELS.items()):
        with ch_cols[i % 2]:
            fit = "🟢 Great fit" if ss.product_key in ch.get("best_for", []) else "🟡 Decent fit"
            base_cost = ch["cost_per_week"]
            consecutive = 0
            history = ss.channel_history.get(ch_key, [])
            for w in range(week - 1, 0, -1):
                if w in history:
                    consecutive += 1
                else:
                    break
            ramp_note = f" · Week {consecutive+1} momentum" if consecutive > 0 else ""

            # Slider range: $0 to 3x base cost (beyond 3x, saturation is extreme)
            max_spend = int(max(base_cost * 3, 100))
            step = 25 if base_cost <= 200 else 50
            st.markdown(
                f"**{ch['icon']} {ch['name']}** — base ${base_cost}/wk{ramp_note}",
                help=f"{ch['desc']} | {fit}",
            )
            slider_key = f"spend_{ch_key}_{week}"
            default_val = int(base_cost) if st.session_state.get(slider_key) is None else int(st.session_state.get(slider_key, base_cost))
            spend_val = st.slider(
                label=f"spend-{ch_key}",
                min_value=0,
                max_value=max_spend,
                value=default_val,
                step=step,
                key=slider_key,
                label_visibility="collapsed",
            )
            if spend_val > 0:
                spend_by_channel[ch_key] = float(spend_val)
                total_channel_spend += spend_val
            st.markdown(
                f"<span style='font-size: 0.8rem; color: #6B7280;'>{fit} · {ch['desc']}</span>",
                unsafe_allow_html=True,
            )

    st.markdown("")
    total_week_cost = total_channel_spend + WEEKLY_BURN
    remaining_after = ss.budget - total_week_cost

    # Live funnel projection — updates as sliders move
    proj = project_week(spend_by_channel)
    active_count = len([v for v in spend_by_channel.values() if v > 0])

    st.markdown("##### 🔬 Live Funnel Projection")
    st.markdown(
        "*Math updates as you move sliders. These are deterministic projections; "
        "actual weekly results include ±25% variance.*"
    )
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        st.metric("Projected Reach", f"{proj['total_reach']:,}")
    with fc2:
        st.metric("Projected Leads", f"{proj['total_leads']:,}")
    with fc3:
        st.metric("Projected Sales", f"{proj['projected_sales']:,}")
    with fc4:
        st.metric("Projected Revenue", f"${proj['projected_revenue']:,.0f}")

    ec1, ec2, ec3 = st.columns(3)
    with ec1:
        cac_color = "#10B981" if 0 < proj["cac"] < 75 else "#F59E0B" if proj["cac"] < 150 else "#EF4444"
        st.markdown(
            f"<div style='text-align:center;'><div style='color:#6B7280;font-size:0.85rem;'>Projected CAC</div>"
            f"<div style='color:{cac_color};font-size:1.4rem;font-weight:700;'>"
            f"${proj['cac']:,.0f}" + ("" if proj['cac'] > 0 else " —") + "</div></div>",
            unsafe_allow_html=True,
        )
    with ec2:
        ratio = proj["ltv_cac"]
        ratio_color = "#10B981" if ratio >= 3 else "#F59E0B" if ratio >= 1 else "#EF4444"
        ratio_label = f"{ratio:.1f} : 1" if ratio > 0 else "—"
        st.markdown(
            f"<div style='text-align:center;'><div style='color:#6B7280;font-size:0.85rem;'>LTV : CAC</div>"
            f"<div style='color:{ratio_color};font-size:1.4rem;font-weight:700;'>{ratio_label}</div></div>",
            unsafe_allow_html=True,
        )
    with ec3:
        pb = proj["payback_months"]
        pb_color = "#10B981" if 0 < pb < 12 else "#F59E0B" if pb < 18 else "#EF4444"
        pb_label = f"{pb:.1f} mo" if pb > 0 else "—"
        st.markdown(
            f"<div style='text-align:center;'><div style='color:#6B7280;font-size:0.85rem;'>Payback</div>"
            f"<div style='color:{pb_color};font-size:1.4rem;font-weight:700;'>{pb_label}</div></div>",
            unsafe_allow_html=True,
        )

    # Per-channel breakdown in expander
    if active_count > 0:
        with st.expander("Per-channel projection", expanded=False):
            for ch_key, pdata in proj["per_channel"].items():
                ch = CHANNELS[ch_key]
                sat_pct = int(pdata["saturation"] * 100)
                sat_color = "#10B981" if sat_pct < 50 else "#F59E0B" if sat_pct < 80 else "#EF4444"
                ch_cac = f"${pdata['cac']:,.0f}" if pdata["sales"] > 0 else "—"
                st.markdown(
                    f"{ch['icon']} **{ch['name']}** — ${pdata['spend']:,.0f} spend → "
                    f"{pdata['reach']:,} reach → {pdata['leads']:,} leads → {pdata['sales']:,} sales "
                    f"| CAC {ch_cac} "
                    f"| saturation <span style='color:{sat_color};font-weight:600;'>{sat_pct}%</span>",
                    unsafe_allow_html=True,
                )

    col_summary, col_action = st.columns([2, 1])
    with col_summary:
        st.markdown(f"""
        <div class="insight-box">
            <strong>Week {week} spend:</strong> ${total_week_cost:,.0f} (${WEEKLY_BURN} fixed + ${total_channel_spend:,.0f} channels)<br>
            <strong>Budget after this week:</strong> ${remaining_after:,.0f}<br>
            <strong>Channels active:</strong> {active_count}
        </div>
        """, unsafe_allow_html=True)

    with col_action:
        st.markdown("")
        can_proceed = remaining_after >= 0
        if not can_proceed:
            st.error("Over budget! Lower some spend.")

        if st.button(
            f"Run Week {week} ▶️",
            key=f"btn_run_week_{week}",
            disabled=not can_proceed or active_count == 0,
        ):
            run_week(spend_by_channel, total_week_cost)
            st.rerun()

    # Option to pivot strategy
    with st.expander("🔄 Pivot Strategy (costs momentum)", expanded=False):
        st.markdown("*Changing your pricing or messaging mid-launch costs you a week of channel momentum.*")
        new_pricing = st.selectbox(
            "Change pricing",
            options=list(PRICING_OPTIONS.keys()),
            format_func=lambda k: f"{PRICING_OPTIONS[k]['label']} (${get_product()['base_price'] * PRICING_OPTIONS[k]['multiplier']:.0f})",
            index=list(PRICING_OPTIONS.keys()).index(ss.pricing_key),
            key=f"pivot_pricing_{week}",
        )
        new_messaging = st.selectbox(
            "Change messaging",
            options=list(MESSAGING_OPTIONS.keys()),
            format_func=lambda k: MESSAGING_OPTIONS[k]["label"],
            index=list(MESSAGING_OPTIONS.keys()).index(ss.messaging_key),
            key=f"pivot_messaging_{week}",
        )
        if new_pricing != ss.pricing_key or new_messaging != ss.messaging_key:
            if st.button("Confirm Pivot 🔄", key=f"btn_pivot_{week}"):
                ss.pricing_key = new_pricing
                ss.messaging_key = new_messaging
                ss.pivot_count += 1
                # Reset channel momentum
                ss.channel_history = {}
                st.rerun()


def run_week(spend_by_channel, total_cost):
    """Execute one week of simulation given per-channel spend dict."""
    ss = st.session_state

    result = simulate_week(spend_by_channel)
    # Apply weekly cashflow: subtract all costs, add gross profit from sales (revenue * margin).
    # This models profit reinvestment — successful launches build a bigger budget.
    ss.budget -= total_cost
    ss.budget += result["revenue"] * result["margin"]
    ss.total_sales += result["sales"] + result["repeat_sales"]
    ss.total_revenue += result["revenue"]
    ss.total_ad_spend += result.get("ad_spend", total_cost - WEEKLY_BURN)
    ss.total_leads += result["total_leads"]
    ss.email_list += result["email_signups"]
    ss.repeat_customers += result["repeat_sales"]
    if result["revenue"] > ss.best_week_revenue:
        ss.best_week_revenue = result["revenue"]

    # Record spend allocation for the week
    ss.spend_by_channel[ss.week] = dict(spend_by_channel)

    # Update channel history
    active_channels = [k for k, v in spend_by_channel.items() if v > 0]
    for ch in active_channels:
        if ch not in ss.channel_history:
            ss.channel_history[ch] = []
        ss.channel_history[ch].append(ss.week)
        if ch not in ss.channels_ever_used:
            ss.channels_ever_used.append(ch)

    ss.weekly_results.append(result)

    # Check milestones
    check_milestones()

    # Reset modifiers (they were one-time from events)
    ss.conv_modifier = 1.0
    ss.reach_modifier = 1.0
    ss.quality_modifier = 0.0

    # Advance week
    ss.week += 1
    if ss.week > TOTAL_WEEKS:
        ss.stage = "results"
    else:
        ss.current_event = None


# ---------------------------------------------------------------------------
# Market event handler
# ---------------------------------------------------------------------------
def render_market_event(event):
    ss = st.session_state
    event_type = event.get("type", "neutral")
    css_class = event_type if event_type in ("positive", "negative") else ""

    st.markdown(f"""
    <div class="game-header">
        <h1>Week {ss.week} of {TOTAL_WEEKS}</h1>
        <p>A market event needs your attention before you proceed.</p>
    </div>
    """, unsafe_allow_html=True)

    icon = "⚡" if event_type == "negative" else "🌟" if event_type == "positive" else "📢"

    st.markdown(f"""
    <div class="event-card {css_class}">
        <h3 style="margin:0;">{icon} {event['title']}</h3>
        <p style="margin: 0.5rem 0 0 0;">{event['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### How do you respond?")
    for resp_key, resp in event["response_options"].items():
        cost_note = f" (Cost: ${resp['cost']})" if resp["cost"] > 0 else " (Free)"
        can_afford = resp["cost"] <= ss.budget
        col_btn, col_desc = st.columns([1, 3])
        with col_btn:
            if st.button(
                f"{resp['label']}{cost_note}",
                key=f"evt_resp_{resp_key}_{ss.week}",
                disabled=not can_afford,
            ):
                apply_event_response(event, resp_key)
                st.rerun()
        with col_desc:
            st.markdown(f"<span style='font-size: 0.85rem; color: #6B7280;'>{resp['desc']}</span>", unsafe_allow_html=True)


def apply_event_response(event, resp_key):
    ss = st.session_state
    resp = event["response_options"][resp_key]

    # Deduct cost
    ss.budget -= resp["cost"]

    # Apply event base effects
    base_fx = event.get("effect", {})
    if "conv_mult" in base_fx:
        ss.conv_modifier *= base_fx["conv_mult"]
    if "max_sales_cap" in base_fx:
        ss.sales_cap = base_fx["max_sales_cap"]

    # Apply response effects
    fx = resp.get("effect", {})
    if "conv_mult" in fx:
        ss.conv_modifier *= fx["conv_mult"]
    if "reach_mult" in fx:
        ss.reach_modifier *= fx["reach_mult"]
    if "margin_mult" in fx:
        ss.margin_modifier *= fx["margin_mult"]
    if "quality_boost" in fx:
        ss.quality_modifier += fx["quality_boost"]
    if "bonus_reach" in fx:
        ss.reach_modifier *= (1 + fx["bonus_reach"] / 500)
    if "email_capture" in fx:
        ss.email_list += fx["email_capture"]
    if "budget_saved" in fx:
        ss.budget += fx["budget_saved"]

    ss.event_responses[ss.week] = resp_key
    ss.current_event = None


# ---------------------------------------------------------------------------
# Stage: Results
# ---------------------------------------------------------------------------
def render_results():
    ss = st.session_state
    product = get_product()

    st.markdown(f"""
    <div class="game-header">
        <h1>🏁 Launch Complete!</h1>
        <p>Here are your 6-week go-to-market results for {product['name']}.</p>
    </div>
    """, unsafe_allow_html=True)

    # Summary metrics — headline
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("Total Customers", ss.total_sales, "#6C4BEF")
    with c2:
        render_metric_card("Total Revenue", f"${ss.total_revenue:,.0f}", "#10B981")
    with c3:
        cac = get_cac()
        render_metric_card("Avg CAC", f"${cac:,.0f}" if cac > 0 else "N/A", "#3B82F6")
    with c4:
        render_metric_card("Email List", ss.email_list, "#F59E0B")

    # Unit economics — the real measure of a launch
    price = calculate_effective_price()
    pricing = get_pricing() or {"margin": 0.5}
    margin = pricing.get("margin", 0.5) * ss.margin_modifier
    cm_per_unit = price * margin
    ltv = cm_per_unit * 3.0  # 3x-equivalent (repeat + referral)
    cac_now = get_cac()
    ltv_cac = (ltv / cac_now) if cac_now > 0 else 0
    payback = (cac_now / cm_per_unit) if cm_per_unit > 0 and cac_now > 0 else 0

    st.markdown("##### 📐 Unit Economics")
    uc1, uc2, uc3, uc4 = st.columns(4)
    with uc1:
        render_metric_card("Price (effective)", f"${price:,.0f}", "#1F2937")
    with uc2:
        render_metric_card("Contribution $ / sale", f"${cm_per_unit:,.0f}", "#1F2937")
    with uc3:
        ratio_color = "#10B981" if ltv_cac >= 3 else "#F59E0B" if ltv_cac >= 1 else "#EF4444"
        render_metric_card("LTV : CAC", f"{ltv_cac:.1f} : 1" if ltv_cac > 0 else "—", ratio_color)
    with uc4:
        pb_color = "#10B981" if 0 < payback < 12 else "#F59E0B" if payback < 18 else "#EF4444"
        render_metric_card("Payback (months)", f"{payback:.1f}" if payback > 0 else "—", pb_color)

    # Unit-econ verdict
    if ltv_cac >= 3 and payback < 12:
        verdict = "🟢 **Healthy unit economics** — LTV:CAC ≥ 3 and payback under 12 months. This is the zone where growth actually creates value."
    elif ltv_cac >= 1.5:
        verdict = "🟡 **Fragile unit economics** — you are making marginal money per customer, but not enough buffer to absorb shocks or fund growth."
    elif cac_now > 0:
        verdict = "🔴 **Negative unit economics** — each customer costs more than they return. Fix CAC (targeting, channel mix) or price/margin before scaling."
    else:
        verdict = "⚫ **Not enough customers to compute unit economics.** You did not reach a sample size to learn from."
    st.markdown(f"<div class='insight-box'>{verdict}</div>", unsafe_allow_html=True)

    # LTV assumption explanation (transparency / tooltip)
    with st.expander("Why LTV = 3× contribution margin?"):
        st.markdown(
            "We model LTV as **3× contribution margin per first sale** as a proxy for repeat purchase + referral. "
            "This is a **hardware/durable-goods heuristic**; a fuller SaaS formula is "
            "`LTV = ARPA × gross_margin / churn`. "
            "For HVAC retrofits the true LTV depends on warranty attach, "
            "service contracts, and referral rate — three levers your Round-1 learners should quantify "
            "before a Series A raise. The 3× multiple is deliberately conservative: sufficient to "
            "distinguish healthy from negative unit economics, without over-rewarding one-time transactions."
        )

    st.markdown("")

    # Score calculation
    milestone_points = sum(
        m["points"] for m in active_milestones() if m["name"] in ss.milestones_hit
    )
    efficiency_score = 0
    if ss.total_sales > 0 and cac_now > 0:
        # Score on LTV:CAC ratio — the universal unit-econ benchmark
        if ltv_cac >= 3:
            efficiency_score = 20
        elif ltv_cac >= 2:
            efficiency_score = 14
        elif ltv_cac >= 1:
            efficiency_score = 7
        # Payback bonus
        if 0 < payback < 12:
            efficiency_score += 5

    diversity_score = min(15, len(ss.channels_ever_used) * 3)
    adaptability_score = min(10, len(ss.event_responses) * 3)
    pivot_penalty = ss.pivot_count * 3

    total_score = milestone_points + efficiency_score + diversity_score + adaptability_score - pivot_penalty
    total_score = max(0, total_score)

    # Score display
    score_color = "#10B981" if total_score >= 70 else "#3B82F6" if total_score >= 45 else "#F59E0B" if total_score >= 25 else "#EF4444"
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0;">
        <div class="score-ring" style="background: {score_color};">
            {total_score}
        </div>
        <p style="font-size: 1.1rem; font-weight: 600; margin-top: 1rem;">Traction Score</p>
    </div>
    """, unsafe_allow_html=True)

    # Score breakdown
    st.markdown("##### Score Breakdown")
    score_items = [
        ("Milestones Hit", milestone_points, f"{len(ss.milestones_hit)} of {len(active_milestones())} milestones"),
        ("Unit Economics", efficiency_score, "Healthy margins vs acquisition cost"),
        ("Channel Diversity", diversity_score, f"{len(ss.channels_ever_used)} channels tested"),
        ("Adaptability", adaptability_score, f"{len(ss.event_responses)} market events handled"),
    ]
    if pivot_penalty > 0:
        score_items.append(("Pivot Cost", -pivot_penalty, f"{ss.pivot_count} strategy pivots"))

    for label, pts, note in score_items:
        color = "#10B981" if pts > 0 else "#EF4444" if pts < 0 else "#9CA3AF"
        sign = "+" if pts > 0 else ""
        st.markdown(f"**{label}**: <span style='color: {color}; font-weight: 600;'>{sign}{pts} pts</span> *({note})*", unsafe_allow_html=True)

    st.markdown("---")

    # Milestones
    st.markdown("##### 🏆 Milestones")
    col_hit, col_miss = st.columns(2)
    with col_hit:
        st.markdown("**Achieved:**")
        for m in active_milestones():
            if m["name"] in ss.milestones_hit:
                st.markdown(f"✅ {m['icon']} {m['name']} (+{m['points']})")
    with col_miss:
        st.markdown("**Missed:**")
        for m in active_milestones():
            if m["name"] not in ss.milestones_hit:
                st.markdown(f"⬜ {m['icon']} {m['name']} (+{m['points']})")

    st.markdown("---")

    # Week by week trend
    st.markdown("##### 📊 Weekly Trend")
    if ss.weekly_results:
        df = pd.DataFrame([
            {
                "Week": r["week"],
                "Sales": r["sales"],
                "Revenue": r["revenue"],
                "Leads": r["total_leads"],
                "Reach": r["total_reach"],
            }
            for r in ss.weekly_results
        ])
        c1, c2 = st.columns(2)
        with c1:
            st.line_chart(df.set_index("Week")[["Sales", "Leads"]])
        with c2:
            st.line_chart(df.set_index("Week")[["Revenue"]])

    st.markdown("---")

    # Propensity insights
    st.markdown("##### 🔍 What This Reveals About You")

    insights = generate_insights()
    for insight in insights:
        st.markdown(f"""
        <div class="insight-box">
            <strong>{insight['title']}</strong><br>
            {insight['text']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Actionable takeaways
    st.markdown("##### 🎯 Your Real World Action Items")
    actions = generate_actions()
    for i, action in enumerate(actions, 1):
        st.markdown(f"""
        <div class="result-narrative">
            <strong>{i}. {action['title']}</strong><br>
            {action['text']}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Messaging-to-channel fit analysis
    st.markdown("##### 🧭 Messaging-to-channel fit")
    msg_angle = ss.messaging.get("angle") if hasattr(ss, "messaging") and ss.messaging else None
    paid_spend = sum(r.get("channel_results", {}).get(ch, {}).get("spend", 0)
                     for r in ss.weekly_results
                     for ch in CHANNELS
                     if CHANNELS.get(ch, {}).get("cost_per_week", 0) > 0)
    organic_weeks = sum(1 for r in ss.weekly_results
                        for ch in r.get("channel_results", {})
                        if CHANNELS.get(ch, {}).get("cost_per_week", 0) == 0)
    fit_notes = []
    if msg_angle == "business_roi":
        fit_notes.append("Your **business-ROI messaging** pairs strongly with **outbound/paid** channels "
                         "(cold email, Google Ads, LinkedIn) — decision-makers search with cost/benefit language.")
        if paid_spend < 500:
            fit_notes.append("⚠️ You ran ROI messaging on almost no paid distribution. ROI-framed copy needs "
                             "volume to find the buyer. Consider pairing this angle with ≥ $1K/week in paid next round.")
    elif msg_angle == "technical_spec":
        fit_notes.append("Your **technical-spec messaging** pairs with **content/community** channels "
                         "(trade forums, SEO long-tail, spec sheets) where installers self-educate.")
    elif msg_angle == "comfort_lifestyle":
        fit_notes.append("Your **comfort/lifestyle messaging** pairs with **referral + social** channels — "
                         "the buyer is emotional, and social proof compounds faster than cold outreach here.")
    if not fit_notes:
        fit_notes.append("No dominant messaging angle detected. In real GTM, a crisp angle plus a matched "
                         "channel is worth more than five channels with a generic pitch.")
    for n in fit_notes:
        st.markdown(f"- {n}")

    st.markdown("---")

    # Principles the mechanics enforced
    st.markdown("##### What the mechanics enforced")
    st.markdown(
        "- **Early-adopter focus beats breadth.** Your GTM motion was tested against a specific "
        "early-adopter segment. The classic failure is firing channel tactics at a broad market "
        "before a beachhead is won.\n"
        "- **Unit-economics thresholds gate funding.** LTV:CAC ≥ 3 and payback < 12 months is the "
        "default institutional diligence screen. Below 1.5, growth is *value-destructive*; between "
        "1.5 and 3, the business is survivable but not fundable at priced-round terms.\n"
        "- **Retention is where channels are won or lost.** This sim collapses retention and referral "
        "into a flat 3× multiple. In real GTM, a 10% retention improvement compounds across cohorts "
        "and moves LTV:CAC more than most acquisition tactics."
    )

    st.markdown("---")

    # Restart
    st.markdown("")
    if st.button("🔄 Play Again", key="btn_restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def generate_insights() -> List[Dict]:
    ss = st.session_state
    insights = []

    # Channel preference insight
    most_used = {}
    for ch_key, weeks in ss.channel_history.items():
        most_used[ch_key] = len(weeks)
    if most_used:
        top_channel = max(most_used, key=most_used.get)
        ch_name = CHANNELS[top_channel]["name"]
        top_weeks = most_used[top_channel]

        # Also check total ad spend ratio to detect paid-heavy vs organic-heavy
        total_weeks_played = len(ss.weekly_results) or 1
        avg_weekly_ad_spend = ss.total_ad_spend / total_weeks_played

        if CHANNELS[top_channel]["cost_per_week"] == 0 and avg_weekly_ad_spend < 100:
            insights.append({
                "title": "You Lean Toward Free Channels",
                "text": (
                    f"You used {ch_name} for {top_weeks} out of {total_weeks_played} weeks. "
                    "Founders who favor free channels are often scrappy and budget-conscious, which is great for survival. "
                    "The trade-off: organic channels are slow to scale. "
                    "In the real world, the best go-to-market strategies blend free and paid channels, "
                    "using organic to build trust and paid to accelerate when you find product-market fit."
                ),
            })
        elif CHANNELS[top_channel]["cost_per_week"] >= 300 or avg_weekly_ad_spend >= 350:
            insights.append({
                "title": "You Invest Heavily in Paid Acquisition",
                "text": (
                    f"You relied on {ch_name} for {top_weeks} weeks, "
                    f"spending an average of ${avg_weekly_ad_spend:,.0f}/week on marketing. "
                    "This shows confidence in spending to learn fast, which is valuable for speed. "
                    "The risk: paid channels can mask weak organic demand. If you turn off the ads and nobody shows up, "
                    "you have a traffic problem, not a product. "
                    "Real founders test whether customers find them without ads as a health check."
                ),
            })
        else:
            insights.append({
                "title": "You Balance Cost and Reach",
                "text": (
                    f"Your most-used channel was {ch_name} ({top_weeks} weeks), a mid-cost option. "
                    "This suggests you think carefully about ROI, weighing spend against expected return. "
                    "That is a strong instinct. The next level is running two or three channels simultaneously "
                    "to find your best-performing combination faster."
                ),
            })

    # Pricing insight
    pricing = get_pricing()
    if pricing.get("multiplier", 1.0) < 0.85:
        insights.append({
            "title": "You Compete on Price",
            "text": (
                "You chose aggressive pricing, sacrificing margin for volume. "
                "This works when you need to build a user base fast or when the market is commoditized. "
                "But be careful: low prices attract price-sensitive customers who are often the hardest to retain. "
                "Many successful startups price higher than they think they should, then justify it with great onboarding."
            ),
        })
    elif pricing.get("multiplier", 1.0) >= 1.2:
        insights.append({
            "title": "You Lean Premium",
            "text": (
                "You priced at a premium. This signals confidence in your product's value, which can attract "
                "higher-quality customers who stick around. Premium pricing also gives you more margin to invest "
                "in customer success. The challenge: you need a compelling story about why you are worth more than alternatives."
            ),
        })

    # Pivot behavior
    if ss.pivot_count == 0:
        insights.append({
            "title": "You Stayed Committed to Your Strategy",
            "text": (
                "You launched with a plan and stuck with it. Consistency is valuable because channels and messaging "
                "take time to work. Many founders give up on a channel too early. "
                "The flip side: if your initial assumptions were wrong, sticking too long means burning runway on something "
                "that will not work. The art is knowing when patience is wisdom versus stubbornness."
            ),
        })
    elif ss.pivot_count >= 2:
        insights.append({
            "title": "You Pivot Frequently",
            "text": (
                f"You pivoted {ss.pivot_count} times in 6 weeks. This shows responsiveness to data, but each pivot "
                "resets your momentum. In the real world, changing your pricing or messaging confuses early customers "
                "and forces you to rebuild trust. Try to gather enough data (usually 2 to 3 weeks) before pivoting."
            ),
        })

    # Diversity of approach
    if len(ss.channels_ever_used) >= 5:
        insights.append({
            "title": "You are an Experimenter",
            "text": (
                f"You tested {len(ss.channels_ever_used)} different channels. You clearly value learning and exploration. "
                "This is excellent in early stages when you do not know what works. "
                "The next step is doubling down: once you find a channel that works, pour resources into it before testing new ones."
            ),
        })
    elif len(ss.channels_ever_used) <= 2:
        insights.append({
            "title": "You are Focused",
            "text": (
                f"You stuck with just {len(ss.channels_ever_used)} channels. Deep focus can be powerful, "
                "especially if those channels are working. But in early-stage go-to-market, you often do not know what works "
                "until you try it. Consider running small, cheap tests in new channels to discover unexpected winners."
            ),
        })

    # Unspent budget insight
    budget_utilization = (STARTING_BUDGET - ss.budget) / STARTING_BUDGET
    if budget_utilization < 0.5:
        insights.append({
            "title": "You Hoarded Cash",
            "text": (
                f"You still have ${ss.budget:,.0f} of your ${STARTING_BUDGET:,} budget unspent. "
                "In a simulation (and in a real early-stage launch), unspent budget is unlearned lessons. "
                "Every dollar you did not spend is a test you did not run, an audience you did not reach, "
                "a hypothesis you did not validate. The goal is not to save money; it is to learn as fast as possible "
                "whether this business works. Lean in."
            ),
        })

    return insights


def generate_actions() -> List[Dict]:
    ss = st.session_state
    actions = []

    # Based on what they actually did
    if ss.total_sales < 10:
        actions.append({
            "title": "Focus on Your First 10 Customers",
            "text": (
                "Your simulation showed limited traction. Before scaling any channel, do things that do not scale: "
                "reach out to 20 potential customers personally, offer to set up the product for them, "
                "and learn exactly what made them say yes or no. Those conversations are worth more than any ad campaign."
            ),
        })
    elif ss.total_sales < 30:
        actions.append({
            "title": "Find Your Channel-Market Fit",
            "text": (
                "You have early traction but have not found a repeatable channel yet. "
                "Pick your two best-performing channels from this simulation and run a focused 2-week test in the real world. "
                "Track cost per lead and cost per customer for each. The one with the best unit economics is your foundation."
            ),
        })
    else:
        actions.append({
            "title": "Scale What is Working",
            "text": (
                "You found real traction. The next step is pouring fuel on the fire. "
                "Take your best channel and increase spend 50% each week while monitoring CAC closely. "
                "When CAC starts rising faster than revenue, you have hit that channel's ceiling and it is time to add a second."
            ),
        })

    # Email list action
    if ss.email_list > 20:
        actions.append({
            "title": "Activate Your Email List",
            "text": (
                f"You built a list of {ss.email_list} contacts. In the real world, this is gold. "
                "Set up a simple 3-email nurture sequence: (1) value-add content related to their pain, "
                "(2) a customer story or case study, (3) a limited-time offer. "
                "Email consistently converts at 2 to 5x the rate of cold traffic."
            ),
        })

    # Unit economics action
    cac = get_cac()
    price = calculate_effective_price()
    pricing = get_pricing()
    if cac > 0:
        margin_per = price * pricing.get("margin", 0.5)
        if cac > margin_per:
            actions.append({
                "title": "Fix Your Unit Economics",
                "text": (
                    f"Your CAC (${cac:,.0f}) is higher than your margin per unit (${margin_per:,.0f}). "
                    "This means you lose money on every customer you acquire. Before spending more on marketing, "
                    "either raise your price, reduce your acquisition cost, or find a way to increase lifetime value "
                    "(subscriptions, upsells, referral programs)."
                ),
            })

    actions.append({
        "title": "Build Your 30 Day Launch Plan",
        "text": (
            "Take what you learned here and write a simple 4-week plan: "
            "Week 1: Reach out to 20 potential customers manually. "
            "Week 2: Launch your top channel with a small budget ($200 to $500). "
            "Week 3: Measure, learn, adjust messaging. "
            "Week 4: Double down on what works, cut what doesn't. "
            "The goal is not perfection, it is speed of learning."
        ),
    })

    return actions


# ---------------------------------------------------------------------------
# Main routing
# ---------------------------------------------------------------------------
stage = st.session_state.stage
if stage == "intro":
    render_intro()
elif stage == "choose_product":
    render_choose_product()
elif stage == "choose_strategy":
    render_choose_strategy()
elif stage == "weekly_play":
    render_weekly_play()
elif stage == "results":
    render_results()
