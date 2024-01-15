import streamlit as st
import streamlit as st
from st_supabase_connection import SupabaseConnection


# Initialize connection.
conn = st.connection("supabase",type=SupabaseConnection)

print(F"conn={conn}")

# Perform query.
rows = conn.query("*", table="Students", ttl="10m").execute()

print(F"rows={rows}")

# Print results.
for row in rows.data:
    st.write(f"{row['first_name']} {row['last_name']}")



def button1_clicked():
    message = st.session_state.message1
    message += "שלום\n"
    st.session_state.message1=message
    return

def button2_clicked():
    message = st.session_state.message2
    message += " ?\n"
    # print(F"message1={message}")
    st.session_state.message2=message
    return

c1, c2  = st.columns([1, 1])
c1.button('Click here', key='button1', on_click=button1_clicked)
c1.text_area('message1', key='message1', height = 3, label_visibility="hidden")

c2.button('Click here', key='button2', on_click=button2_clicked)
c2.text_area('message2', key='message2', height = 3, label_visibility="hidden")
