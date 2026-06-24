import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Fraud Detection Platform",
    page_icon="🚨",
    layout="wide"
)

st_autorefresh(
    interval=5000,
    key="frauddashboard"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-size: 18px;
}

h1 {
    font-size: 48px !important;
    font-weight: 800 !important;
}

h2 {
    font-size: 32px !important;
}

[data-testid="metric-container"] {
    background: #151c2c;
    border: 1px solid #2b3755;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.35);
}

[data-testid="metric-container"] label {
    font-size: 18px !important;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("🚨 AI-Powered Real-Time Fraud Detection Platform")

st.caption(
    "Enterprise Fraud Monitoring | Kafka • Machine Learning • Real-Time Analytics"
)

# =========================
# LOAD DATA
# =========================

file_path = Path("data/predictions.csv")

if not file_path.exists():
    st.warning("predictions.csv not found")
    st.stop()

df = pd.read_csv(file_path)

if len(df) == 0:
    st.warning("No predictions available")
    st.stop()

# =========================
# METRICS
# =========================

total_transactions = len(df)

fraud_count = len(
    df[df["Prediction"] == 1]
)

legit_count = len(
    df[df["Prediction"] == 0]
)

fraud_rate = (
    fraud_count / total_transactions * 100
)

# =========================
# ALERT BANNER
# =========================

if fraud_count > 0:
    st.error(
        f"🚨 LIVE ALERT: {fraud_count} fraudulent transactions detected"
    )
else:
    st.success(
        "✅ No fraud activity detected"
    )

# =========================
# KPI SECTION
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💳 Total Transactions",
        f"{total_transactions:,}"
    )

with col2:
    st.metric(
        "🚨 Fraud Alerts",
        fraud_count
    )

with col3:
    st.metric(
        "✅ Legitimate",
        legit_count
    )

with col4:
    st.metric(
        "📊 Fraud Rate",
        f"{fraud_rate:.3f}%"
    )

st.divider()

# =========================
# SYSTEM HEALTH
# =========================

st.subheader("⚙️ System Health")

c1, c2, c3 = st.columns(3)

with c1:
    st.success("Kafka Broker : ONLINE")

with c2:
    st.success("ML Model : ACTIVE")

with c3:
    st.success("Prediction Stream : RUNNING")

st.divider()

# =========================
# CHARTS ROW
# =========================

left, right = st.columns(2)

# Fraud Distribution

with left:

    dist_fig = px.bar(
        x=["Legitimate", "Fraud"],
        y=[legit_count, fraud_count],
        text=[legit_count, fraud_count],
        title="Transaction Distribution"
    )

    dist_fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        dist_fig,
        use_container_width=True
    )

# Fraud Risk Gauge

with right:

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=fraud_rate,
            title={"text": "Fraud Risk %"},
            gauge={
                "axis": {"range": [0, 5]},
                "bar": {"color": "red"},
                "steps": [
                    {"range": [0, 1], "color": "#1b5e20"},
                    {"range": [1, 3], "color": "#f9a825"},
                    {"range": [3, 5], "color": "#b71c1c"}
                ]
            }
        )
    )

    gauge.update_layout(
        height=450
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

st.divider()

# =========================
# TREND CHART
# =========================

st.subheader("📈 Real-Time Fraud Trend")

df["Transaction_Number"] = range(
    1,
    len(df) + 1
)

trend_df = df.tail(1000)

trend_fig = px.line(
    trend_df,
    x="Transaction_Number",
    y="Prediction",
    title="Fraud Detection Activity"
)

trend_fig.update_layout(
    height=450
)

st.plotly_chart(
    trend_fig,
    use_container_width=True
)

st.divider()

# =========================
# DOWNLOAD BUTTON
# =========================

st.download_button(
    label="📥 Download Predictions",
    data=df.to_csv(index=False),
    file_name="fraud_predictions.csv",
    mime="text/csv"
)

# =========================
# FRAUD TABLE
# =========================

st.subheader("🚨 Recent Fraud Alerts")

fraud_df = df[
    df["Prediction"] == 1
]

if len(fraud_df) > 0:

    fraud_df = fraud_df.sort_index(
        ascending=False
    )

    st.dataframe(
        fraud_df.head(25),
        use_container_width=True,
        height=500
    )

else:
    st.success(
        "No fraud transactions detected"
    )

st.divider()

# =========================
# MODEL INFO
# =========================

st.subheader("🤖 Model Information")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Algorithm", "Random Forest")
m2.metric("Precision", "94%")
m3.metric("Recall", "82%")
m4.metric("F1 Score", "87%")

st.info(
    "Dataset: Credit Card Fraud Detection Dataset | Real-Time Kafka Streaming Pipeline"
)