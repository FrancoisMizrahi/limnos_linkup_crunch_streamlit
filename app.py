import streamlit as st
import linkup_api

st.set_page_config(page_title="LinkUp Cruncher", page_icon="🐉​", layout="wide")
st.title("LinkUp Crunch")


with st.sidebar:
    st.header("API key & Query")
    api_token = st.text_input("LinkUp API key", type="password")
    question = st.text_area("Your query", height=100)
    interval = st.slider("Polling interval (seconds)", 2, 20, 10)
    submit = st.button("Ask LinkUp", type="primary", disabled=not (api_token and question))


if submit:
    status_box = st.empty()
    table_placeholder = st.container()
    try:
        linkup_api.query_linkup(question, api_token, interval)
    except Exception as ex:
        st.error(str(ex))




