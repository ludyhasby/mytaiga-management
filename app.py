import streamlit as st
from helpers.env import LoadEnv
from helpers.style import pageInit
from usecase.login import Login
from usecase.dashboard import dashboard
from usecase.appendactivities import appendActivities

def auth(secretKeyInput, secretKeyExpected):
    return secretKeyInput == secretKeyExpected

st.set_page_config(
    page_title="Management Taiga",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if __name__ == "__main__":
    env = LoadEnv()
    pageInit()
    Login(env['secretKey'], env['maxAttempts'], env['lockoutSeconds'])
    st.markdown(
        """
        <div class="topbar">
        <div>
            <div class="brand"><span style="color:#b81120">●</span> Management Taiga</div>
            <div class="eyebrow">DATA PIPELINE v1.0.0</div>
        </div>
        <div class="version">MYPTM · READY</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.segmented_control(
        "Navigasi",
        options=["Dashboard", "Tambah Aktivitas"],
        default="Dashboard",
        label_visibility="collapsed",
        width="stretch",
    )

    match page:
        case "Dashboard":
            dashboard()
            st.stop()
        case "Tambah Aktivitas":
            appendActivities()
            st.stop()
