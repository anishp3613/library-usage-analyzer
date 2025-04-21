import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO
import plotly.express as px

FILENAME = "library_usage.xlsx"


# Load data
def load_data():
    if os.path.exists(FILENAME):
        return pd.read_excel(FILENAME)
    else:
        return pd.DataFrame(columns=["Student Name", "Book Name", "Date Borrowed", "Date Returned"])


# Save data
def save_data(df):
    df.to_excel(FILENAME, index=False)


# Add new entry
def add_new_entry(df, student, book, borrowed_date, returned_date):
    # Convert to datetime if it's a date object
    borrowed_date = pd.to_datetime(borrowed_date)
    returned_date = pd.to_datetime(returned_date)
    

    new_row = {
        "Student Name": student,
        "Book Name": book,
        "Date Borrowed": borrowed_date,
        "Date Returned": returned_date
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    save_data(df)
    return df


# Create download link
def generate_download(df):
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

# Streamlit UI
st.title("📚 𝗟𝗶𝗯𝗿𝗮𝗿𝘆 𝗨𝘀𝗮𝗴𝗲 𝗔𝗻𝗮𝗹𝘆𝘇𝗲𝗿 𝗠𝗼𝗱𝘂𝗹𝗲")

df = load_data()

# --- Add New Entry ---
with st.expander("➕ Add New Entry"):
    student = st.text_input("Student Name")
    book = st.text_input("Book Name")
    borrowed_date = st.date_input("Date Borrowed", datetime.today())
    returned_date = st.date_input("Date Returned", datetime.today())

    if st.button("Add Entry"):
        if student and book:
            df = add_new_entry(df, student, book, borrowed_date, returned_date)
            st.success("✅ Entry added successfully!")
        else:
            st.error("Please enter all fields!")

# --- Display Data ---
st.subheader("📊 Current Library Data")
st.dataframe(df)

# --- Analytics ---
st.subheader("📈 Analytics")

# Books borrowed count
most_borrowed = df["Book Name"].value_counts().reset_index()
most_borrowed.columns = ["Book Name", "Count"]
st.plotly_chart(px.bar(most_borrowed, x="Book Name", y="Count", title="Most Borrowed Books"))

# Borrowing trend over time
# Convert 'Date Borrowed' to datetime (if it's not already)
df["Date Borrowed"] = pd.to_datetime(df["Date Borrowed"])

borrow_trend = df.groupby(df["Date Borrowed"].dt.date).size().reset_index(name="Borrowed Count")
st.plotly_chart(px.line(borrow_trend, x="Date Borrowed", y="Borrowed Count", title="Borrowing Trend Over Time"))

# Top students
top_students = df["Student Name"].value_counts().reset_index()
top_students.columns = ["Student Name", "Borrow Count"]
st.plotly_chart(px.pie(top_students, names="Student Name", values="Borrow Count", title="Top Library Users"))

# --- Download Updated File ---
st.subheader("⬇️ Download Updated File")
download_bytes = generate_download(df)
st.download_button("Download XLSX", data=download_bytes, file_name="updated_library_usage.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
