import streamlit as st
# import streamlit.session_state as session_state

import requests
import streamlit as st
from streamlit_extras.switch_page_button import switch_page


## 
def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}

# Create an empty container
placeholder = st.empty()
placeholder_2 = st.empty()
placeholder_3 = st.empty()
placeholder_4 = st.empty()
placeholder_5 = st.empty()


actual_email = "admin"
actual_password = "admin"
session = requests.Session()

# Insert a form in the container
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = False
if 'user_status' not in st.session_state:
    st.session_state['user_status'] = 2    ## 1 for Admin and 2 for User
if 'forgot_status' not in st.session_state:
    st.session_state['forgot_status'] = False
if 'reg_status' not in st.session_state:
    st.session_state['reg_status'] = False
if st.session_state["authentication_status"] == False:
    with placeholder.form("login"):
        var = True
        # var_2 = True
        # var_3 = True
        # var_4 = True
        # var_5 = True
        st.markdown("#### Enter your credentials")
        username = st.text_input("UserName")
        password = st.text_input("Password", type="password")
        column_1,column_2,column_3 = st.columns([1,6,1.75])
        with column_1:
            submit = st.form_submit_button("Login")
            
        with column_2:
            submit_3 = st.form_submit_button("Register")
        # with column_3:
        #     submit_2 = st.form_submit_button("Forgot Password")
            
        # if st.button :   
    #     if submit_2:
    #         st.session_state['forgot_status'] = True
    #         switch_page('Forgot_password')

    if submit_3:
            st.session_state['reg_status'] = True
            switch_page('Register')



    if submit:
        # If the form is submitted and the email and password are correct,
        # clear the form/container and display a success message
        placeholder.empty()
        url = 'http://localhost:8000/user/login'
        myobj = {'username': username ,'password': password }
        result = requests.post(url, data = myobj)
        # print(x_status)
        st.write(result.status_code)
        if result.status_code == 200:
            x = result.json()    
            st.success("Login successful")
            log_username = x['username']
            log_token = x['access_token']
            st.session_state["user_status"] = x['userType']
            

            # print(log_username)
            # print(log_token)
        # Initialization of session state:
        
            st.session_state["authentication_status"] = log_token
            st.success("Login successful") 
            st.write(x)
            # if logout:
            #     st.session_state["authentication_status"] == False
            #     placeholder.empty()
        elif result.status_code == 404 or result.status_code == 401:
            # if 'shared' not in st.session_state:
            st.session_state["authentication_status"] == False
            st.error("Login failed ... Invalid credentials")
        # if st.session_state["authentication_status"] == log_token:
        #     st.success("Login successful") 
        # else:
        #     pass
else:
    st.header("User logged in Successfully")
    logout = st.button("Log Out")
    if logout:
        st.session_state["authentication_status"] = False
        st.header("Logged Out Successfully")
















































# ##------------------------------------------------------------------------------------------------------------
# # Define the title and other page settings

# st.set_page_config(page_title="Login Page", page_icon=":guardsman:", layout="centered")

# st.title('This is the title of your login page bro')
# # Define the login form
# def login():
#     # Display the login header
#     st.header("Login to your account")

#     # Define the input fields for username and password
#     username = st.text_input("Username")
#     password = st.text_input("Password", type="password")
#     st.session_state.is_logged_in = True


#     options = ['Standard', 'Premium', 'Pro']

#     plan = st.selectbox('Choose a plan', options)

#     st.write('You selected:', plan)



#         # Define the login button
#     if st.button("Login"):  
#         if username == "myusername" and password == "mypassword":
#             st.success("Logged in as {}".format(username))
#         else:
#             st.error("Incorrect username or password")





# # Call the login function
# login()
