import streamlit as st
import json
import pandas as pd
import WFCtimeTable
import numpy as np
import time

def load_subjects():
    with open("subjects.json", "r") as file:
        return json.load(file)

def main():
    st.title("Time Table Scheduler")
    
    semesters = ['Sem I', 'Sem II', 'Sem III', 'Sem IV', 'Sem V', 'Sem VI', 'Sem VII', 'Sem VIII']
    selected_semester = st.selectbox("Select a semester:", semesters)

    subjects_data = load_subjects()
    subjects = subjects_data.get(selected_semester, [])

    num_teachers = {}
    if subjects: 
        with st.expander("Enter number of teachers for each subject"):
            num_teachers = {}
            for subject in subjects:
                num_teachers[subject] = st.number_input(f"Enter the number of teachers for {subject}:",
                                                        min_value=0, value=1)
            st.write("Number of teachers for each subject:")
            st.write(num_teachers)

    num_classes = {}
    if subjects: 
        with st.expander("Enter number of classes for each subject"):
            num_classes = {}
            for subject in subjects:
                num_classes[subject] = st.number_input(f"Enter the number of classes ( per week ) for {subject}:",
                                                        min_value=0, value=1)
            st.write("Number of classes for each subject per week:")
            st.write(num_classes)
    
    num_sections = st.number_input("Enter the number of sections:", min_value=1, value=3)
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    classes = ['Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8', 'Period 9']

    collapsed_function = WFCtimeTable.main(num_class=num_classes, num_teach=num_teachers, num_secs=num_sections)
    if collapsed_function is None:
        st.warning('IMPOSSIBLE STATE REACHED. Please check constraints', icon="⚠️")
        return
    
    collapsed_function = np.array(list(map(lambda x: f"{x.cls}", collapsed_function))).reshape([num_sections,5,9])

    for section_num in range(num_sections):
        st.subheader(f"{selected_semester} - Section {chr(section_num + 65)}")
        df = pd.DataFrame(collapsed_function[section_num],index=days_of_week, columns=classes)
        st.write(df, use_container_width=True) 
        st.write('---')  

if __name__ == "__main__":
    main()
