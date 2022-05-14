import streamlit as st
from streamlit_option_menu import option_menu
from pages import calculator
from pages import static_graph, activity_graph, upload_data_graph, dynamic_graph, live_basics
import sqlite3
conn = sqlite3.connect('customer_feedback.db')
c = conn.cursor()

st.set_page_config(page_title="KT-S-App",page_icon="exclamation",
                layout="wide",initial_sidebar_state="expanded")

st.title("Knowledge Transfer Session")
st.sidebar.write("This is sidebar ***contains Menu Section.***")

with st.sidebar:
    opt = option_menu(
        menu_title="Main Menu",
        options=["Live Basics","Basics","Static Graph","Upload Data","Dynamic Graph","Complex Graphs","Feedback"],
        icons=["","tv","bar-chart-line-fill","upload","bar-chart-steps","activity","calendar3"],
        menu_icon="cast",
        default_index=0,
    )
if opt == "Live Basics":
    live_basics.demo()
if opt == "Basics":
    calculator.calci()
if opt == "Static Graph":
    static_graph.graph()
if opt == "Upload Data":
    upload_data_graph.upload_data() 
if opt == "Dynamic Graph":
    dynamic_graph.bar_graph() 
if opt == "Complex Graphs":
    activity_graph.graph_date()
if opt == "Feedback":
    def create_table():
        c.execute('CREATE TABLE IF NOT EXISTS feedback(date_submitted DATE, Q1 INTEGER, Q2 TEXT, Q3 TEXT, Q4 TEXT)')

    def add_feedback(date_submitted, Q1, Q2, Q3, Q4):
        c.execute('INSERT INTO feedback (date_submitted,Q1, Q2, Q3, Q4) VALUES (?,?,?,?,?)',(date_submitted,Q1, Q2, Q3, Q4))
        conn.commit()

    def main():

        st.title("Customer Feedback")

        d = st.date_input("Today's date",None, None, None, None) 
        
        question_1 = st.slider('Overall, how happy are you with the Visuals? (5 being very happy and 1 being very dissapointed)', 1,5,1)
        st.write('You selected:', question_1)

        question_2 = st.selectbox('Was these visuals fun and interactive?',('','Yes', 'No'))
        st.write('You selected:', question_2)

        question_3 = st.selectbox('Did your able to explore the ideas in our app?',('','Yes', 'No'))
        st.write('You selected:', question_3)

        question_4 = st.text_input('What could have been better?', max_chars=50)

        if st.button("Submit feedback"):
            create_table()
            add_feedback(d, question_1, question_2, question_3, question_4)
            st.success("Feedback submitted")

    if __name__ == '__main__':
        main()
