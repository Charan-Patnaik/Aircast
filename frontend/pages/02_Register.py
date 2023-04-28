import streamlit as st
from PIL import Image
import requests
def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}
if 'reg_status' not in st.session_state:
    st.session_state['reg_status'] = False
if 'done_status' not in st.session_state:
    st.session_state['done_status'] = False
if 'plan_id' not in st.session_state:
    st.session_state['plan_id'] = 1
if 'reg_button' not in st.session_state:
    st.session_state['reg_button'] = False
if '409_check' not in st.session_state:
    st.session_state['409_check'] = False
if st.session_state['reg_status'] == False and st.session_state['done_status'] == False:
    st.markdown("#### Please Use the Login Screen")
elif st.session_state['reg_status'] == True and st.session_state['done_status'] == True:
    st.success("Registration successful")
elif st.session_state['reg_status'] == True and st.session_state['done_status'] == False:

    st.title("Aircast - New User Registration")

    # Create an empty container
    placeholder = st.empty()


    # Input Fields

    with st.form("my_form"):     
        user_name = st.text_input("User Name")
        # last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        print(password,"password_2")
        print(user_name,"user_name_2")
        print(email,"email_2")

        # Checkbox for agreeing to terms
        agree_to_terms = st.checkbox("I agree to the terms and conditions")
        submitted = st.form_submit_button("Submit")

    
    # Validation logic
    if submitted:
        if not user_name:
            st.warning("Please enter your user name")
        # elif not last_name:
        #     st.warning("Please enter your last name")
        elif not email:
            st.warning("Please enter your email")
        elif not password:
            st.warning("Please enter your password")
        elif password != confirm_password:
            st.warning("Passwords do not match")
        elif not agree_to_terms:
            st.warning("Please agree to the terms and conditions")
        
        
        # else:
        #     st.success("Registration successful!")



    # creating three columns
    column_1,column_2,column_3 = st.columns(3)

    #displaying an image in each column
    with column_1:
        st.image("https://eztechassist.com/wp-content/uploads/2018/04/FREE-Membership-green-01-1.png",width=200,output_format="auto")
        #image address(https://eztechassist.com/wp-content/uploads/2018/04/FREE-Membership-green-01-1.png)
        st.write('Click here for more info on the free membership')
        if st.button("Join as a Free member :        10 API Calls"):
            st.session_state['plan_id'] = 1 
            print(password,"password_1")
            print(user_name,"user_name_1")
            print(email,"email_1")
            
            st.write("You're a free member!")
        # else:
        #     plan_id = 0


    with column_2:
        st.image("https://www.sicklecelldisease.org/wp-content/uploads/2019/01/Gold-Membership.png",width=200,output_format="auto")
        #image address(https://www.sicklecelldisease.org/wp-content/uploads/2019/01/Gold-Membership.png)
        st.write('Click here for more info on the Silver membership details')
        if st.button("Join as a GOLD member: 15 API Calls"):
            st.session_state['plan_id'] = 2
            st.write("You're a GOLD member!")

        
        # else:
        #     plan_id = 0

    with column_3:
        st.image("https://www.vafree.org/wp-content/uploads/2019/03/Platinum-Membership-e1553275136316.png",width=200,output_format="auto")
        #image address(https://www.sicklecelldisease.org/wp-content/uploads/2019/01/Silver-Membership.png)
        st.write('Click here for more info on the Gold membership details')
        if st.button("Join as a Platinum member :      20 API Calls"):
            st.session_state['plan_id'] = 3
            st.write("You're a Platinum member!")
        # else:
        #     plan_id = 0
    st.write(' ')
    col1, col2, col3 = st.columns([9,6,5])
    with col1:
        st.write(" ")
    with col2:
        if st.button("Register"):
            st.session_state['reg_button'] = True
        if st.session_state['reg_button'] == True:
            url = 'http://backend:8000/user/sign-up'
            print(user_name,"user_name")
            myobj = {'username': user_name ,'password': password, 'email' : email,'planId': st.session_state['plan_id']}
            print(password,"password")
            print(email,"email")
            print(st.session_state['plan_id'])
       
            result = requests.post(url, json = myobj)
            print(result.status_code)

            # print(result.json())

            if result.status_code == 201:
                x = result.json()
                placeholder.empty()
                st.session_state['409_check'] = True
                st.session_state['done_status'] = True
                placeholder = st.empty()
                st.success("Registration successful")
                # st.session_state['reg_status'] == True
        #    if st.session_state['reg_status'] == True and st.session_state['done_status'] == True:
        #         st.success("Registration successful")
            elif result.status_code == 404 or result.status_code == 422:
                placeholder.empty()
                st.error("Invalid username or email or password for Registration")
            elif result.status_code == 409 and st.session_state['409_check'] == False:
                placeholder.empty()
                st.error("User already exists")
           
            st.write(' ')
    with col3:
        st.write(" ")


