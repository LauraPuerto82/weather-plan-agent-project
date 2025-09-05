import streamlit as st

def inject_global_css():
    st.markdown(
        """
        <style>
          /* Bring titles up a bit */
          section.main > div.block-container { padding-top: .25rem; }
          .block-container h1 { margin-top: .25rem; margin-bottom: .35rem; }

          /* Cards */
          .section-card {
            padding: 1.25rem 1.5rem;
            border: 1px solid rgba(250,250,250,0.08);
            border-radius: 14px;
            background: rgba(250,250,250,0.02);
            margin-top: .15rem;
          }

          /* Extra space between the chat card and the chat input line */
          [data-testid="stChatInput"] {
            margin-top: .85rem;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
