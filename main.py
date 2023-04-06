import streamlit as st
from home_page import content


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    

#  Create login Step
if 'login' not in st.session_state:
    st.session_state['login'] = False

main = st.empty()

if st.session_state['login']:
    with main:
        content()
else:
    _, middle, _ = st.columns([1,2, 1])
    with middle:
        with st.form('login_form'):
            st.subheader('用户登陆')
            user = st.text_input('用户名')
            password = st.text_input('密码',type='password')
            login_btn= st.form_submit_button('登陆', type='primary')
        if login_btn:    
            if user =='liu.ye'and password=='ly4sb':
                st.session_state['login'] = True
                st.experimental_rerun()
            else:
                st.error('Wrong username or password')
    



