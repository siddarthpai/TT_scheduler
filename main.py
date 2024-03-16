import streamlit as st
import pandas as pd

def main():
    st.title("Dynamic Table Creation")

    # Collect user input for table creation
    num_rows = st.number_input("Enter the number of rows:", min_value=1, value=5)
    num_columns = st.number_input("Enter the number of columns:", min_value=1, value=3)

    # Create an empty DataFrame to store user data
    data = []
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            row.append(st.text_input(f"Row {i+1}, Column {j+1}"))
        data.append(row)

    # Convert the data list into a DataFrame
    df = pd.DataFrame(data, columns=[f"Column {j+1}" for j in range(num_columns)])

    # Display the DataFrame as a table
    st.write(df)

if __name__ == "__main__":
    main()