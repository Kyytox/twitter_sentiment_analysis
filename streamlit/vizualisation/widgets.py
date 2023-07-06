import streamlit as st
import datetime
import calendar

# element selector radio for the frequency of the graph
def get_freq_option(index):
    lst_options = ['per day', 'every 3 days', 'per week', 'per month']    
    freq_option = st.radio('Time frequency :', lst_options, index=0, horizontal=True, key=index)

    print("freq_option", freq_option)

    # use match case to select the frequency of the graph
    if freq_option == 'per day':
        return 'D'
    elif freq_option == 'every 3 days':
        return '3D'
    elif freq_option == 'per week':
        return 'W'
    elif freq_option == 'per month':
        return 'M'
    else:
        return 'D'



def create_year_month_selection():
    this_year = datetime.date.today().year
    this_month = datetime.date.today().month
    report_year = st.selectbox('', range(this_year, this_year - 4, -1), key=3)
    month_name_lst = calendar.month_name[1:]
    report_month_str = st.radio('', month_name_lst, index=this_month - 1, horizontal=True, key=4)
    report_month = list(calendar.month_name).index(str(report_month_str))
    return report_year, report_month