import streamlit as st

def calci():
    st.subheader("Calculator Body.")
    col = st.columns(3)
    with col[0]:
        n1 = st.number_input("Insert a Number", value = 0, help= "Insert a Higher Number.")
    with col[2]:
        n2 = st.number_input("Insert another Number", value = 0, help= "Insert a Smaller number than Previous")

    sum = n1+n2
    diff = n1-n2
    mul = n1*n2

    if n1<n2:
        div = n2/n1
    elif n1==n2:
        div = 1.0
    else:
        div = n1/n2
    

    col1 = st.columns(4)
    with col1[0]:
        if st.button("SUM"):
            st.metric(label = "Sum",value = sum)
    with col1[1]:
        if st.button("Difference"):
            if diff < 0:
                st.metric(label="Difference",value=-(diff),delta=diff)
            else:
                st.metric(label = "Difference",value = diff,delta=diff)
    with col1[2]:
        if st.button("Multiplication"):
            st.metric(label = "Multiplication",value = mul)
    with col1[3]:
        if st.button("Division"):
            st.metric(label= "Division", value= div)


    st.subheader('Conditional Fromating')

    val = st.sidebar.number_input("Enter Threshold Value")
    col1, col2 = st.columns([2, 2])
    with col1:
        var1 = st.number_input('Insert a Conditional Number', value=0,help="Insert a value in Threshold")
        var2 = st.number_input('Insert another Conditional Number', value=0,help="Insert a value in Threshold")
        bt = st.button("Process")
    with col2:
        if bt:
            if var1 < val:
                st.metric("Lower Outcome",var1,var1-val)
            elif var1==val:
                st.metric("Netural Outcome",var1)
            else:
                st.metric("Higher Outcome",var1,var1-val)
        if bt:
            if var2 < val:
                st.metric("Lower Outcome",var2,var2-val)
            elif var2==val:
                st.metric("Netural Outcome",var2)
            else:
                st.metric("Higher Outcome",var2,var2-val)