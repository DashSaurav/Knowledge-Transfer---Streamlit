import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, datetime,timedelta
import calendar
from pages import read_data

def graph_date():
    title = '<h1 style="font-family:sans-serif; color:Red; font-size: 30px;"><center>Some Complex Graphs</center></h1>'
    st.markdown(title,unsafe_allow_html=True)  
    st.subheader("Activity Chart")  
    a1,a2,a3,a4 = st.columns(4)
    with a1:
        li_year = ["2022"]
        opt_year = st.selectbox('Select Year for Analytics', li_year)
    with a2:
        CHOICES = {13: "Week 13", 14: "Week 14", 15: "Week 15",16: "Week 16",17: "Week 17",18: "Week 18",
                    19: "Week 19",20: "Week 20",21: "Week 21",22: "Week 22",}
        opt = st.selectbox("Select Week for Analytics", CHOICES.keys(), format_func=lambda x:CHOICES[ x ])
    with a4:
        t = "<div> <br></div>"
        st.markdown(t, unsafe_allow_html=True)
        currenttime = datetime.today()
        onlydate = currenttime.day
        onlymonth = currenttime.strftime("%b")
        onlyyear = currenttime.year
        onlyday = calendar.day_name[currenttime.weekday()]
        st.info(f"""{onlyday} , {onlydate} {onlymonth} {onlyyear}""")  


    def getDateRangeFromWeek(p_year,p_week):
        firstdayofweek = datetime.strptime(f'{p_year}-W{int(p_week)-1}-1', "%Y-W%W-%w").date()
        lastdayofweek = firstdayofweek + timedelta(days=6.9)
        return firstdayofweek, lastdayofweek
    #Call function to get dates range 
    firstdate, lastdate =  getDateRangeFromWeek(opt_year,opt)
    #st.write(firstdate, lastdate)

    #st.write(read_data.s_time_of_non_comliance_func('2022-03-24', 'M1 Separation Room', 4))

    # dynamically 
    def timestr_to_num(timestr):
        return mdates.date2num(datetime.strptime('0' + timestr if timestr[1] == ':' else timestr, '%H:%M:%S'))

    week_12_df = read_data.cleaning_times(firstdate,lastdate)
    #st.write(week_12_df)
    wk_df = pd.DataFrame(week_12_df)
    #st.write(wk_df)
    #wk_df = wk_df[(wk_df["Date"] >= str(firstdate)) & (wk_df["Date"] <= str(lastdate))]

    fig, ax = plt.subplots(figsize=(10, 5))
    operations = pd.unique(wk_df['date'])
    try:
        for date in operations:
            i = 0
            for row in wk_df[wk_df['date'] == date].itertuples():
                i = i+1
                left = timestr_to_num(row.start_floor)
                right = timestr_to_num(row.finish_floor)
                left_deep = timestr_to_num(row.start_deep)
                right_deep = timestr_to_num(row.finish_deep)
                if i == 1:
                    rect1 = ax.barh(date, left=timestr_to_num('00:00:00'), width=timestr_to_num('23:59:00') - timestr_to_num('00:00:00'), height=0.3, color='lightgray')
                rect2 = ax.barh(date, left=left, width=right - left, height=0.3, color='tab:blue', label = 'Floor Cleaning')
                rect3 = ax.barh(date, left=left_deep, width=right_deep - left_deep, height=0.3, color='red', label = 'Deep Cleaning')
        ax.set_xlim(timestr_to_num('00:00:00'), timestr_to_num('23:59:00'))
        ax.set_ylim(firstdate,lastdate)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))  # display ticks as hours and minutes
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # set a tick every hour
        ax.legend(handles=[rect2, rect3], bbox_to_anchor=(1.0, 1.0))
        ax.grid(True)
        st.pyplot(fig)
    except:
        st.header("No Data")

    st.subheader("Heatmap")
    col = st.columns(3)
    with col[0]:
        val1 = st.number_input("Give A threshold value for M1", max_value=10, value=2)
    with col[1]:
        val2 = st.number_input("Give A threshold value for M2", max_value=10, value=2)
    with col[2]:
        dm = st.date_input("Provide a date on which Heatmap to be shown")
    st.subheader("Roomwise Hourly Non-Compliances.")
    #heat_map_data= read_data.heat_map_func(str(currenttime.date()),saved_result,saved_result1)
    heat_map_data= read_data.heat_map_func(str(dm),val1,4)
    # heat_map_data = {"M1":[0,0,0,0,0,0,3,8,9,9,9,15,15,13,7,16,5,5,0,0,0,0,0,0],
    #                 "M2":[0,0,0,0,0,3,5,8,7,10,10,15,15,14,19,2,2,2,0,0,0,0,0,0]}
    save_path = "pages\images"
    image = read_data.create_dashboard_occ_heatmap(heat_map_data,save_path,cmap='Reds')
    st.write(image)