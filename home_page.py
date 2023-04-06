import streamlit as st
from io import BytesIO
import pandas as pd
import plotly.express as px


def split_item(s):
    s = s.replace('1、','1.')
    return s.split('\n1.', 1)[0]

def split_material(s):
    s = s.split('参考')[0].split('\n',1)
    if len(s)==2:
        return pd.Series([s[0], s[1]])
    else:
        return pd.Series([s[0], '无'])
    
def split_location(s):
    if '棚' in s:
        return pd.Series('顶棚')
    elif '地' in s:
        return pd.Series('地面')
    elif '墙' in s:
        return pd.Series('墙面')
    else:
        return pd.Series('其他')
    
    
    
    
def content():
    
# sidebar------------------------------------
    with st.sidebar:
        st.title('工程项目汇总')

        file_binary =  st.file_uploader("请选择工程文件上传", type=['xlsx']) 
        st.session_state['uploaded_file'] = file_binary
        category = st.radio(
            "选择汇总分类",
            ('位置','项目总称','具体材料')
        )
        # group_action = st.button("开始汇总", type="primary")


    # Main content------------------------------------

    raw_tab, processed_tab = st.tabs(["原始表格", "分类汇总"])
    with raw_tab:
        if file_binary:
            try:
                data =  pd.read_excel(file_binary,index_col=0)
                data.columns = data.iloc[2,:]
                data = data[pd.to_numeric(data.index, errors='coerce').notnull()][['项目编码','项目名称\n项目特征','计量单位','工程数量' ]]
                data = data.rename(columns = {'项目名称\n项目特征':'项目特征'})
                st.dataframe(data,use_container_width=True, height=450)
            except:
                st.warning('文件格式不符，请检查后刷新页面重新上传', icon="⚠️")

    with processed_tab:
        if file_binary:
            try:
                processed = data.copy()
                processed['项目'] = processed['项目特征'].apply(split_item)
                processed[['项目总称','具体材料']] = processed['项目'].apply(split_material)
                processed['位置'] = processed['项目总称'].apply(split_location)
                result = processed.groupby([category])['工程数量'].agg('sum').to_frame()
                if category=='具体材料':
                    result = result[result.index !='无']
                    result.index = [i[:14] for i in  result.index]
                    result.index.name='具体材料'

                col1, col2 = st.columns([3, 1])
                with col1:
                    fig = px.bar(result.reset_index(), x=category, y='工程数量')
                    # fig.update_xaxes(tickangle=60)
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    st.dataframe(result,height=500,use_container_width=True)


                all_result =processed.groupby(['位置','项目总称','具体材料','项目特征'])['工程数量'].agg('sum').to_frame()

                output = BytesIO()
                all_result.to_excel(output)
                st.download_button(
                    label="下载汇总数据",
                    data=output,
                    file_name='汇总.xlsx',          
                )
            except:
                st.warning('文件格式不符，请检查后刷新页面重新上传', icon="⚠️")