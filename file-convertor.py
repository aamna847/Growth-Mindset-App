import streamlit as st # type: ignore
import pandas as pd # type: ignore
from io import BytesIO

# Set up the page
st.set_page_config(page_title="File Converter and Cleaner", layout="wide")
st.title("File Converter and Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert to different formats.")

# File uploader: Allows multiple files
files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

# Process files if uploaded
if files:
    for file in files:
        ext = file.name.split(".")[-1].lower()
        # Read the uploaded file
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        # Show file preview
        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Remove duplicates checkbox
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed")
            st.dataframe(df.head())

        # Fill missing values with mean for numeric columns
        if st.checkbox(f"Fill Missing Values with Mean - {file.name}"):
            df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
            st.success("Missing Values filled with mean")
            st.dataframe(df.head())

        # Column selection
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show chart for numeric columns
        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Format selection (CSV or Excel)
        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        # Convert and download button
        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()

            # Convert and write to the appropriate format
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime_type = "text/csv"
                new_name = file.name.replace(ext, "csv")

            else:  # Excel
                df.to_excel(output, index=False, engine="openpyxl")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            # Reset the output buffer to the beginning before download
            output.seek(0)

            # Provide download button
            st.download_button(
                label=f"Download {new_name}",
                data=output,
                file_name=new_name,
                mime=mime_type
            )

            st.success("Processing Completed!")
