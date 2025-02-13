import pandas as pd
import streamlit as st
from streamlit_timeline import st_timeline 
import sys

def plot_interactive_timeline(df, datetime_col, category_col, event_tittle_col, event_detail_col, title="Events Timeline"):
    """ 
    Plots an interactive timeline of events.
    """
    
    st.title(title)

    
    df.fillna('', inplace=True)
    # Prepare data for timeline
    items = []
    for index, row in df.iterrows():
        
        items.append({
            'id': index,
            'title': row[event_tittle_col],
            'content': row[event_detail_col],
            'start': row[datetime_col].strftime('%Y-%m-%d %H:%M:%S'),
            'group': row[category_col]
        })
        

    return st_timeline(items, groups=[{"id": r, "content": r} for i, r in enumerate(df[category_col].unique())], 
                       options={
                           "align":"left"
                       },height="600px")

# Example usage
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python timeline.py <csv_file>")
        sys.exit(1)
 
    csv_file = sys.argv[1]

    # Input dataframe
    df = pd.read_csv(csv_file, parse_dates=['SendDatetime'])


    # Creating the timeline
    tl = plot_interactive_timeline(df, 'SendDatetime', 'SenderRoleName', "CleanedText" , 'EventDescription')
    st.write(tl)
    
    
# TODO find a way to order the events by ID: first event on top.