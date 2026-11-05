import streamlit as st
import hmac
import time

@st.dialog("Autentikasi Diperlukan", width="small")
def secret_key_dialog(expectedKey, maxAttempts, lockoutInSeconds):
    st.markdown(
        """
        <div class="secret-key-label">
            MyTaiga Management Secret Key
        </div>
        """,
        unsafe_allow_html=True,
    )

    maxAttempts = max(1, int(maxAttempts))
    lockoutInSeconds = max(1, int(lockoutInSeconds))
    now = time.time()
    lock_until = st.session_state.get("lock_until", 0)

    if now < lock_until:
        remaining = max(1, int(lock_until - now + 0.999))
        st.error(
            f"Terlalu banyak percobaan gagal. "
            f"Coba lagi dalam {remaining} detik."
        )
        return

    if lock_until:
        st.session_state["failed_attempts"] = 0
        st.session_state["lock_until"] = 0

    with st.form("secret_key_form"):
        secret_key = st.text_input(
            "Taiga Pipeline Secret Key",
            placeholder="Masukkan Taiga Secret Key...",
            type="password",
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button(
            "Verifikasi",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not expectedKey:
            st.error("Secret Key belum dikonfigurasi.")
        elif hmac.compare_digest(
            secret_key.strip(),
            expectedKey.strip(),
        ):
            st.session_state["authenticated"] = True
            st.session_state["failed_attempts"] = 0
            st.session_state.pop("lock_until", None)
            st.session_state.pop("auth_error", None)
            st.rerun()
        else:
            attempts = st.session_state.get("failed_attempts", 0) + 1
            st.session_state["failed_attempts"] = attempts

            if attempts >= maxAttempts:
                st.session_state["lock_until"] = time.time() + lockoutInSeconds
                st.error(
                    "Batas percobaan tercapai. Akses dikunci selama "
                    f"{lockoutInSeconds} detik."
                )
            else:
                remaining = maxAttempts - attempts
                st.error(f"Secret Key salah. Sisa percobaan: {remaining}")


def Login(secretKey, maxAttempts, lockoutInSeconds):
    if not st.session_state.get("authenticated", False):
        secret_key_dialog(secretKey, maxAttempts, lockoutInSeconds)
        st.stop()