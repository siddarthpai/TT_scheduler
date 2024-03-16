import streamlit as st
import pandas as pd

def main():
    st.title("Time Table Scheduler")
    
    semesters = ['Sem I', 'Sem II', 'Sem III', 'Sem IV', 'Sem V', 'Sem VI', 'Sem VII', 'Sem VIII']
    selected_semester = st.selectbox("Select a semester:", semesters)
    num_teachers = {}
    if selected_semester == 'Sem VI':
        with st.expander("Enter number of teachers for each subject"):
            num_teachers = {}
            for subject in ['UE21CS341B Compiler Design', 'UE21CS351B Cloud Computing',
                            'UE21CS352B Object Oriented Analysis & Design using Java',
                            'Elective A', 'Elective B']:
                num_teachers[subject] = st.number_input(f"Enter the number of teachers for {subject}:",
                                                        min_value=0, value=1)
            st.write("Number of teachers for each subject:")
            st.write(num_teachers)
    num_sections = st.number_input("Enter the number of sections:", min_value=1, value=3)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    classes = ['Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8', 'Period 9']

    for section_num in range(num_sections):
        st.subheader(f"{selected_semester} - Section {chr(section_num + 65)}")
        df = pd.DataFrame(index=days_of_week, columns=classes) 

        st.write(df, use_container_width=True) 
        st.write('---')  

if __name__ == "__main__":
    main()
