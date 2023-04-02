import streamlit as st
import pandas as pd



def split_item(s):
    s = s.replace('1、','1.')
    return s.split('\n1.', 1)[0]

def split_material(s):
    s = s.split('参考')[0].split('\n',1)
    if len(s)==2:
        return pd.Series([s[0], s[1]])
    else:
        return pd.Series([s[0], '无'])


# Layout

if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] =  None
 
  
main = st.empty()

if st.session_state['uploaded_file'] is None:
    with main.container():
        st.session_state['uploaded_file'] = st.file_uploader("请选择文件上传")
        st.button('上传')
else:
    with main.container():
        st.dataframe(data.head(),width=1200)



# Using "with" notation
with st.sidebar:
    st.title('工程项目汇总')
    
    add_selectbox = st.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

