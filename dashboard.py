import streamlit as st
import gspread
import pandas as pd
import plotly.express as px
from google.oauth2 import service_account
import plotly.graph_objects as go


# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive", ],
)

gc = gspread.authorize(credentials)

# Open the Google Sheet by name

sheet = gc.open_by_key('1cdQ9aq1D3pRARU7tENRoQVraoIkuzNLDBwdbRi3dcHU').sheet1


# Read the data from the sheet
data = sheet.get_all_records()

# Create Dataframe
df = pd.DataFrame(data)


st.write(df)


user_date = "A"

# create a new DataFrame with the user input data
new_df = pd.DataFrame(user_data)


with st.form(key='my_form'):
    if st.form_submit_button(label="Submit"):
        try:
            new_df = new_df.fillna(0)

            # Get the number of rows that have data
            num_rows = len(sheet.get_all_values())

            # Calculate the starting cell for new data (considering the header is only added once)
            start_cell = f"A{num_rows + 1}" if num_rows > 0 else "A1"

            # Append the data
            if num_rows == 0:
                # If the sheet is empty, also include the headers
                sheet.update(start_cell, [new_df.columns.values.tolist()] + new_df.values.tolist())
            else:
                # Otherwise, just append the data rows
                sheet.update(start_cell, new_df.values.tolist())

                st.write(f"New data written to sheet: {update_details}")

        except Exception as e:
            st.error(f"An error occurred: {e}")


