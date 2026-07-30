import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="AI Threat Detection Dashboard",
    layout="wide"
)

st.markdown("""
<style>

/* Hide Streamlit default header */
header {
    visibility: hidden;
}

/* Hide Main Menu */
#MainMenu {
    visibility: hidden;
}

/* Hide footer */
footer {
    visibility: hidden;
}

/* Entire App */
.stApp{
    background-color:#0E1117;
}

/* Main Content */
.main{
    background-color:#0E1117;
}

/* Metric Cards */
div[data-testid="stMetric"]{

    background:#171C26;

    border:1px solid #2A3140;

    border-radius:18px;

    padding:22px;

    transition:0.3s;

}

/* Hover Effect */

div[data-testid="stMetric"]:hover{

    border:1px solid #D4AF37;

    transform:translateY(-4px);

}

/* Metric Label */

div[data-testid="stMetricLabel"]{

    color:#D4AF37;

    font-size:18px;

}

/* Metric Value */

div[data-testid="stMetricValue"]{

    color:white;

    font-size:42px;

}

</style>
""", unsafe_allow_html=True)


st.markdown(
    """
# 🛡 SENTINEL AI
### Smart Surveillance Command Center
""")

csv_path = Path("logs/events.csv")

if csv_path.exists():

    df = pd.read_csv(csv_path)

    intrusion_count = len(df[df["Event"] == "Intrusion"])
    loitering_count = len(df[df["Event"] == "Loitering"])
    crowd_count = len(df[df["Event"] == "Crowd"])

   

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="🚨 Intrusions",
            value=intrusion_count,
            delta=None
        )
    with col2:
        st.metric(
            label="⏱ Loitering",
            value=loitering_count,
            delta=None
        )
    with col3:
        st.metric(
            label="👥 Crowd Alerts",
            value=crowd_count,
            delta=None
        )
    with col4:
        if intrusion_count > 10:
            threat = "🔴 HIGH"
        elif intrusion_count > 3:
            threat = "🟡 MEDIUM"
        else:
            threat = "🟢 LOW"
        st.metric(
            label="🛡 Threat Level",
            value=threat,
            delta=None
        )

    st.markdown("---")

    st.subheader("Recent Events")

    recent_df = df.iloc[::-1].reset_index(drop=True)
    st.dataframe(
        recent_df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.warning("No event log found.")