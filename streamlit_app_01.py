import os
import streamlit as st
# import supabase
from supabase import create_client, Client

def logout_form(supabase_session):
    with st.form('log out'):
        st.write(F"{supabase_session.user.email}")
        submit = st.form_submit_button('log out')

    if submit:
        st.session_state.supabase_client.auth.sign_out()
        st.rerun()

def signup_form():
    st.title("sign up")
    with st.form('sign up'):
        signup_username = st.text_input(label='username', key='signup_username')
        signup_password = st.text_input(label='password', key='signup_password', type='password')
        submit = st.form_submit_button('sign up')

    if submit:
        print('sign up submitted')
        st.write(F'username={signup_username}')
        credentials = {}
        credentials['email'] = signup_username
        credentials['password'] = signup_password
        res = st.session_state.supabase_client.auth.sign_up(credentials)
        # st.write(F"{res}")
        # st.rerun() ?

def login_form():
    st.title("log in")
    with st.form('log in'):
        c1, c2  = st.columns([1, 1])
        username =c1.text_input('username', key='username')
        password = c1.text_input('password', key='password', type='password')
        submit = st.form_submit_button('log in')

    if submit:
        st.session_state.user_state = "login attempt"
        credentials = {}
        credentials['email'] = username
        credentials['password'] = password
        try:
            user = st.session_state.supabase_client.auth.sign_in_with_password(credentials)
            st.session_state.user_state = "logged in"
        except Exception as inst:
            # st.write(type(inst))    # the exception type
            st.write(F"inst.args={inst.args}")     # arguments stored in .args
            st.write(F"inst={inst}")
            st.session_state.user_state = "login error"

        if st.session_state.user_state == "logged in":
            st.rerun()

def button_clicked():
    if st.session_state.form_to_show == 'login':
        print('login -> signup')
        st.session_state.form_to_show = 'signup'
    else:
        print('signup -> login')
        st.session_state.form_to_show ='login'

def show_data():
    rows = st.session_state.supabase_client.table("Students").select("*").execute()
    
    st.write("dataframe")
    st.dataframe(rows.data)

    st.write("data_editor")
    st.data_editor(rows.data)

    # for row in rows.data:
    #     st.write(f"{row['first_name']} {row['last_name']}")
    table = st.session_state.supabase_client.table("Students")
    st.write(table)
    # st.write(F"{type(table)}")
    # st.write(st.session_state.supabase_client.postgrest)

def main():
    st.set_page_config(layout="wide")

    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase_client: Client = create_client(url, key)

    st.write(supabase_client)

    st.session_state.supabase_client = supabase_client
    st.session_state.user = supabase_client.auth.get_user()

    # st.session_state.form_to_show = "login"
    if "form_to_show" not in st.session_state:
        st.session_state.form_to_show = 'login' 

    with st.sidebar:
        st.title("Welcome!")
        st.write(__file__)
        if st.session_state.supabase_client:
            # supabase_session = st.session_state.supabase_client.auth.get_user()
            supabase_session = st.session_state.supabase_client.auth.get_session()
            if supabase_session:
                logout_form(supabase_session)
            else:
                st.write("log in or sign up to start")

                if st.session_state.form_to_show == 'signup':
                    button_label = 'log in'
                else:
                    button_label = 'sign up'

                st.button(button_label, on_click=button_clicked)

        # st.markdown(F"###### form to show={st.session_state.form_to_show}")

    # main pane
    if st.session_state.supabase_client:
        supabase_session = st.session_state.supabase_client.auth.get_session()
        if supabase_session:
            show_data()
        else:
            if st.session_state.form_to_show == 'signup':
                signup_form()
            else:
                login_form()

    # st.write(F"{supabase_client.rest_url}")


if __name__ == "__main__":
    main()
