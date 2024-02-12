import requests
import json
import pandas as pd
import streamlit as st
import OpenDartReader
from bs4 import BeautifulSoup
######################################################################################################################
crtfc_key = st.secrets["crtfc_key"]
dart = OpenDartReader(crtfc_key)
bgn_de = "20150101"
end_de = "20240101"
######################################################################################################################
test_input = st.text_input("💬 기업이름 입력", value="", placeholder=None, disabled=False, label_visibility="visible")
######################################################################################################################
if (test_input != "") and (test_input != None):
    corp_code = dart.find_corp_code(test_input)
    report_list = dart.list(corp_code, kind='C')
    target_rcept_no = report_list[report_list["report_nm"].str.contains("투자설명서")]["rcept_no"].tail(1).item()
    subdocs = dart.sub_docs(target_rcept_no, match='본문')
    report_url = subdocs.head(1)["url"].item()
    response = requests.get(report_url)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')#'html.parser')

    #for table in tables:
    #    nested_tables = table.find_all('table')
    #    for nested in nested_tables:
    #        # 중첩된 <table> 태그를 텍스트로 대체
    #        nested.replace_with(nested.get_text(separator=" ", strip=True))
    
    # 문서 url
    st.write(f"📍문서 url : [{test_input} 증권신고서 원본](%s)"%report_url)
    # 투자지표의 적합성 -> 선정 투자지표
    st.write("😁 투자지표의 적합성",pd.read_html(str([table for table in soup.find_all('table') if ("방법론의 적합성" in table.text) or ("투자지표의 적합성" in table.text) or ("투자지표 선정의 적합성" in table.text)][0]))[0])
    # 투자지표의 부적합성
    try:
        st.write("😢 투자지표의 부적합성",pd.read_html(str([table for table in soup.find_all('table') if ("방법론의 부적합성" in table.text) or ("투자지표의 부적합성" in table.text) or ("투자지표 선정의 부적합성" in table.text)][0]))[0])
    except:
        st.write("😢 투자지표의 부적합성",pd.read_html(str([table for table in soup.find_all('table') if ("방법론의 적합성" in table.text) or ("투자지표의 적합성" in table.text) or ("투자지표 선정의 적합성" in table.text)][1]))[0])
