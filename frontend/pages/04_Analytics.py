import datetime
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import streamlit as st
import requests
import plotly.express as px
if "authentication_status" not in st.session_state:
   st.session_state["authentication_status"] = False
if 'user_status' not in st.session_state:
    st.session_state['user_status'] = 2  ## 1 for Admin and 2 for User
if 'user' not in st.session_state:
    st.session_state['user'] = ''
if "visibility" not in st.session_state:
    st.session_state.visibility = "hidden"
    st.session_state.disabled = False


## Inputs
# data = pd.DateFrame(col = ['Name','TimeFrame'])
hours = [str(x).zfill(2) for x in range(24)]

def analytics_admin():
    
        st.title('Analytics Dashboard :blue[Admin]')
        st.sidebar.markdown("# :blue[Admin] Dashboard")
        st.subheader("Daily API calls per User")
        column_1,column_2,column_3 = st.columns(3)
        ## GET API CALL for user list :
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        result_user_list = requests.get('http://localhost:8000/admin/all-users',headers=headers).json()
        # print(result_user_list)
        # print(type(result_user_list))

        ulist = result_user_list['users']
        df_result_user_list = pd.DataFrame(ulist)
        user_list = []
        for i in ulist:
            user_list.append(i['username'])
        
        # print(user_list)

        with column_1:
            st.session_state['user'] = st.selectbox(
            "Select the User",
            user_list,
            label_visibility="visible",
            disabled=st.session_state.disabled,
            key = "Plotly_1")
        with column_2:
            date_selected = st.date_input(
            "Select the date",
            # value = datetime.date(2022, 7, 28),
            min_value= datetime.date(2023, 3, 2), max_value=datetime.date.today(),key = "d1")
        with column_3:
            st.caption('Search')
            if st.button("GO"):
               st.session_state.visibility = "visible" 
            else:
                st.write(' ')
        if st.session_state.visibility == "visible":
            # if user == 'damg7245':
            # st.session_state['user_status'] = 2
            ## GET API CALL for Daily API calls per User
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            user_id = df_result_user_list.loc[df_result_user_list['username'] == st.session_state['user'], 'id'].item()
            # print(user)
            # print(user_id)
            date_request = date_selected.strftime("%m/%d/%Y")
            # print(date_request)
            payload = {'date_request':date_request}
            api_hits_daily = requests.get(f"http://localhost:8000/admin/api-hits-count/user/{user_id}",params = payload, headers=headers).json()
            # print(api_hits_daily)
            df_api_hits_daily = pd.DataFrame(api_hits_daily['api_req'])
            # print(df_api_hits_daily)
            fig_admin_requests = go.Figure()
            
            fig_admin_requests = px.line(df_api_hits_daily, x='time', y=['success','failuer'], color = 'variable',title='Request Count by User') #plot the line chart
            st.plotly_chart(fig_admin_requests)

            # if user == 'free':
            #     fig_admin_requests1 = go.Figure()
            #     d2 = pd.DataFrame({'Calls': np.random.randint(0,0,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
            #     fig_admin_requests1 = px.line(d2, x='Time of the Day', y='Calls', title='Request Count by User') #plot the line chart
            #     st.plotly_chart(fig_admin_requests1)
            # if user == 'gold':
            #     fig_admin_requests2 = go.Figure()
            #     d3 = pd.DataFrame({'Calls': np.random.randint(0,0,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
            #     fig_admin_requests2 = px.line(d3,x='Time of the Day', y='Calls', title='Request Count by User') #plot the line chart
            #     st.plotly_chart(fig_admin_requests1)


        st.subheader("Total API calls the previous day")
        ### GOES API POST CALL
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        
        # myobj = {'station': 'ABI-L1b-RadC' ,'year': year_goes ,'day': doy,'hour':hour,'file_name': str(sl_file)}
        # print(myobj)
        result = requests.get('http://localhost:8000/admin/api-hits-previous-days',headers=headers).json()
        code1 = requests.get('http://localhost:8000/admin/api-hits-previous-days',headers=headers).status_code
        # print(code1)
        
        variable_output = str(result['total_api_hits_in_previous_day'])
        # print(result['total_api_hits_in_previous_day'])
        html_str = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output}</p>
        """
        st.markdown(html_str, unsafe_allow_html=True)

####################################################################
        st.write(" ")
        st.subheader("Total Average calls last week")
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        
        # myobj = {'station': 'ABI-L1b-RadC' ,'year': year_goes ,'day': doy,'hour':hour,'file_name': str(sl_file)}
        # print(myobj)
        result = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-last-week',headers=headers).json()
        code1 = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-last-week',headers=headers).status_code
        # print(code1)
        
        variable_output_1 = str(result['total_api_hits_in_previous_week'])
        # variable_output_1 = '100'
        html_str_1 = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output_1}</p>
        """
    
        st.markdown(html_str_1, unsafe_allow_html=True)
   
####################################################################     
        # st.subheader("Success Vs Failed Calls")
        st.write(" ")
        column_1,column_2 = st.columns(2)
        with column_1:
            st.markdown("#### Total Success Calls")
            
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).json()
            code1 = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).status_code
            
            variable_output_2 = str(result['success_count'])
            
            html_str_2 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_2}</p>
            """
            st.markdown(html_str_2, unsafe_allow_html=True)
        with column_2:
            st.markdown("#### Total Failed Calls")
            
            
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).json()
            code1 = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).status_code
            
            variable_output_3 = str(result['failure_count'])
            
            html_str_3 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_3}</p>
            """
            st.markdown(html_str_3, unsafe_allow_html=True)
        ###########################################################
        st.write(" ")
        st.subheader("Each endpoint total number of calls")
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        result_api_list = requests.get('http://localhost:8000/admin/all-apis-hits-with-count',headers=headers).json()
        del result_api_list['success']
        list_api = list(result_api_list.keys())
        list_calls = list(result_api_list.values())
        df=pd.DataFrame(list(zip(list_api,list_calls)),columns=['API','count'])
        fig_api_requests = go.Figure()
            
        fig_api_requests = px.bar(df, x='API', y='count',title='total count of API calls') #plot the line chart
        st.plotly_chart(fig_api_requests)
            
def analytics_user():
    
        st.title('Analytics Dashboard :blue[User]')
        st.sidebar.markdown("# :blue[User] Dashboard")
        st.subheader("Daily API calls per User")
        column_2,column_3 = st.columns(2)
        # ## GET API CALL for user list :
        # token = st.session_state["authentication_status"]
        # headers = {'Authorization': f'Bearer {token}'}
        # result_user_list = requests.get('http://localhost:8000/admin/all-users',headers=headers).json()
        # # print(result_user_list)
        # # print(type(result_user_list))

        # ulist = result_user_list['users']
        # df_result_user_list = pd.DataFrame(ulist)
        # user_list = []
        # for i in ulist:
        #     user_list.append(i['username'])
        
        # print(user_list)

        # with column_1:
        #     user = st.selectbox(
        #     "Select the User",
        #     user_list,
        #     label_visibility="visible",
        #     disabled=st.session_state.disabled,
        #     key = "Plotly_1")
        with column_2:
            date_selected = st.date_input(
            "Select the date",
            # value = datetime.date(2022, 7, 28),
            min_value= datetime.date(2023, 3, 2), max_value=datetime.date.today(),key = "d1")
        with column_3:
            st.caption('Search')
            if st.button("GO"):
               st.session_state.visibility = "visible" 
            else:
                st.write(' ')
        if st.session_state.visibility == "visible":
            # if user == 'damg7245':
            st.session_state['user_status'] = 2
            ## GET API CALL for Daily API calls per User
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
           
            # print(user)
            # print(user_id)
            date_request = date_selected.strftime("%m/%d/%Y")
            # print(date_request)
            payload = {'date_request':date_request}
            api_hits_daily = requests.get("http://localhost:8000/admin/api-hits-count/user/1",params = payload, headers=headers).json()
            # print(api_hits_daily)
            df_api_hits_daily = pd.DataFrame(api_hits_daily['api_req'])
            # print(df_api_hits_daily)
            fig_admin_requests = go.Figure()
            
            fig_admin_requests = px.line(df_api_hits_daily, x='time', y=['success','failuer'], color = 'variable',title='Request Count by User') #plot the line chart
            st.plotly_chart(fig_admin_requests)

            # if user == 'free':
            #     fig_admin_requests1 = go.Figure()
            #     d2 = pd.DataFrame({'Calls': np.random.randint(0,0,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
            #     fig_admin_requests1 = px.line(d2, x='Time of the Day', y='Calls', title='Request Count by User') #plot the line chart
            #     st.plotly_chart(fig_admin_requests1)
            # if user == 'gold':
            #     fig_admin_requests2 = go.Figure()
            #     d3 = pd.DataFrame({'Calls': np.random.randint(0,0,24), 'Time of the Day': pd.date_range('00:00', '23:00', freq='H')})
            #     fig_admin_requests2 = px.line(d3,x='Time of the Day', y='Calls', title='Request Count by User') #plot the line chart
            #     st.plotly_chart(fig_admin_requests1)


        st.subheader("Total API calls the previous day")
        ### GOES API POST CALL
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        
        # myobj = {'station': 'ABI-L1b-RadC' ,'year': year_goes ,'day': doy,'hour':hour,'file_name': str(sl_file)}
        # print(myobj)
        result = requests.get('http://localhost:8000/admin/api-hits-previous-days',headers=headers).json()
        code1 = requests.get('http://localhost:8000/admin/api-hits-previous-days',headers=headers).status_code
        # print(code1)
        
        variable_output = str(result['total_api_hits_in_previous_day'])
        # print(result['total_api_hits_in_previous_day'])
        html_str = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output}</p>
        """
        st.markdown(html_str, unsafe_allow_html=True)

####################################################################
        st.write(" ")
        st.subheader("Total Average calls last week")
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        
        # myobj = {'station': 'ABI-L1b-RadC' ,'year': year_goes ,'day': doy,'hour':hour,'file_name': str(sl_file)}
        # print(myobj)

        
        result = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-last-week',headers=headers).json()
        code1 = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-last-week',headers=headers).status_code
        # print(code1)
        
        variable_output_1 = str(result['total_api_hits_in_previous_week'])
        # variable_output_1 = '100'
        html_str_1 = f"""
        <style>
        p.a {{
        font: bold 25px red;
        }}
        </style>
        <p class="a">{variable_output_1}</p>
        """
    
        st.markdown(html_str_1, unsafe_allow_html=True)
   
####################################################################     
        # st.subheader("Success Vs Failed Calls")
        st.write(" ")
        column_1,column_2 = st.columns(2)
        with column_1:
            st.markdown("#### Total Success Calls")
            
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).json()
            code1 = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).status_code
            
            variable_output_2 = str(result['success_count'])
            
            html_str_2 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_2}</p>
            """
            st.markdown(html_str_2, unsafe_allow_html=True)
        with column_2:
            st.markdown("#### Total Failed Calls")
            
            
            token = st.session_state["authentication_status"]
            headers = {'Authorization': f'Bearer {token}'}
            result = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).json()
            code1 = requests.get('http://localhost:8000/admin/all-apis-hits-with-count-compare-success-failure',headers=headers).status_code
            
            variable_output_3 = str(result['failure_count'])
            
            html_str_3 = f"""
            <style>
            p.a {{
            font: bold 25px red;
            }}
            </style>
            <p class="a">{variable_output_3}</p>
            """
            st.markdown(html_str_3, unsafe_allow_html=True)
        ###########################################################
        st.write(" ")
        st.subheader("Each endpoint total number of calls")
        token = st.session_state["authentication_status"]
        headers = {'Authorization': f'Bearer {token}'}
        result_api_list = requests.get('http://localhost:8000/admin/all-apis-hits-with-count',headers=headers).json()
        del result_api_list['success']
        list_api = list(result_api_list.keys())
        list_calls = list(result_api_list.values())
        df=pd.DataFrame(list(zip(list_api,list_calls)),columns=['API','count'])
        fig_api_requests = go.Figure()
            
        fig_api_requests = px.bar(df, x='API', y='count',title='total count of API calls') #plot the line chart
        st.plotly_chart(fig_api_requests)


##########  MAIN CODE #################
print("st.session_state[\"user_status\"]", st.session_state["user_status"])
print("st.session_state[\"authentication_status\"] ", st.session_state["authentication_status"])

if st.session_state["authentication_status"] == False:
      st.subheader("Please Login before use")

else :
    if st.session_state['user_status'] == 1:
        analytics_admin()
    else:
        analytics_user()