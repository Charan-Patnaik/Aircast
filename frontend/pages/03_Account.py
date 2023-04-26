import streamlit as st
import calendar
from datetime import datetime
# import streamlit.session_state as session_state


particles = [ "PM2.5"]
particle2 =["PM"]
particle3 =["NO"]
particle4 =["NO2"]
particle5 =["Ozone"]
st.header("Welcome to your account")
st.write("This is your aircast page")

years = datetime.today().year,datetime.today().year-1,datetime.today().year-2
months = list(calendar.month_name[1:])

st.header("Enter the day that you want to choose")
with st.form("Check you Air Quality",clear_on_submit = True):
    col1,col2 = st.columns(2)
    col1.selectbox("Select month:", months, key= "month")
    col1.selectbox("Select year:", years, key= "years")

st.header("Enter the air particles in  to determine the AQI")
with st.expander("Set the value of your parameters"):
    for p in particles:
        st.number_input(f"{p}:", min_value=0, format="%i", step=1 , key = p)

with st.expander("PM"):
    for p1 in particle2:
        st.number_input(f"{p1}:", min_value=0, format="%i", step=1 , key = p1)

with st.expander("NO"):
    for p2 in particle3:
        st.number_input(f"{p2}:", min_value=0, format="%i", step=1 , key = p2)

with st.expander("NO2"):
    for p3 in particle4:
        st.number_input(f"{p3}:", min_value=0, format="%i", step=1 , key = p3)

with st.expander("Ozone"):
    for p4 in particle5:
        st.number_input(f"{p4}:", min_value=0, format="%i", step=1 , key = p4)


st.form_submit('Submit')
