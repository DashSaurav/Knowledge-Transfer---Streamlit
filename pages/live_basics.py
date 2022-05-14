import streamlit as st


def demo():
    st.subheader("Basis")
    st.write("saurav")
    var1 = 23
    st.write(var1)


    st.info("Session is ON!")
    st.error("Error")
    st.warning("Warning")
    st.header("header")
    st.subheader("Subheader")
    pic = st.camera_input("Take a Pic")
    st.write(pic)