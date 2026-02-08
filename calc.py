import streamlit as st

st.set_page_config(page_title="マイ電卓", layout="centered")

# --- 記号を絶対に出現させるためのCSS ---
st.markdown("""
    <style>
    [data-testid="column"] {
        width: 23% !important;
        flex: 1 1 23% !important;
        min-width: 23% !important;
    }
    .stButton>button {
        height: 60px;
        border-radius: 12px;
        /* 文字サイズを少しだけ下げて、枠内からはみ出さないように固定 */
        font-size: 18px !important; 
        font-weight: bold;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📱 電卓")

if "formula" not in st.session_state:
    st.session_state.formula = ""

# 表示パネル
st.markdown(
    f"""
    <div style="background-color: #262730; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 2px solid #464855;">
        <h1 style="text-align: right; color: #ffffff; font-family: monospace; margin: 0; font-size: 35px;">
            {st.session_state.formula if st.session_state.formula else '0'}
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ボタン設定： (表示する文字, 計算に使う文字)
button_layout = [
    [('7', '7'), ('8', '8'), ('9', '9'), ('÷', '/')],
    [('4', '4'), ('5', '5'), ('6', '6'), ('×', '*')],  # ここで * を × に変更
    [('1', '1'), ('2', '2'), ('3', '3'), ('－', '-')],
    [('0', '0'), ('C', 'C'), ('←', '←'), ('＋', '+')],
    [('＝', '=')]
]

for row in button_layout:
    cols = st.columns(len(row))
    for i, (label, value) in enumerate(row):
        with cols[i]:
            is_op = value in ["/", "*", "-", "+", "=", "C", "←"]
            # keyを完全に固定して、Streamlitの混乱を防ぐ
            if st.button(label, key=f"final_btn_{value}_{button_layout.index(row)}_{i}",
                         use_container_width=True,
                         type="primary" if is_op else "secondary"):
                if value == "=":
                    try:
                        st.session_state.formula = str(
                            eval(st.session_state.formula))
                    except:
                        st.session_state.formula = "Error"
                elif value == "C":
                    st.session_state.formula = ""
                elif value == "←":
                    st.session_state.formula = st.session_state.formula[:-1]
                else:
                    if st.session_state.formula == "Error":
                        st.session_state.formula = ""
                    st.session_state.formula += value
                st.rerun()
