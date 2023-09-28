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



def main():
    st.title("End of Day Review")

    # List of metrics
    metrics = ["Sleep", "Water", "Food", "Sun", "Mood", "Productivity", "Satiety", "Learning"]

    # Dictionary to store scores for each metric
    scores = {}

    # Loop through each metric and create a radio button selection for scores 1-5
    for metric in metrics:
        score = st.radio(f"Rate your {metric} today:", [1, 2, 3, 4, 5], horizontal=True)
        scores[metric] = score

    # You can add a button to finalize the review and maybe save/display the results
    if st.button("Submit Review"):
        st.write("Review Submitted!")
        st.write(scores)  # Displaying the scores, you can also save them elsewhere if needed

    # create a new DataFrame with the user input data
    new_df = pd.DataFrame(scores)


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

if __name__ == "__main__":
    main()






