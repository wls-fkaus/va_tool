import streamlit as st
import pandas as pd

# Load your cleaned CSV file
df_clean = pd.read_csv('clean_data.csv', dtype={'ID': str, 'PROGRAMS': str})

# Group programs per student
student_programs = df_clean.groupby('ID')['PROGRAMS'].apply(list).reset_index()

# Only keep students with multiple programs
student_programs = student_programs[student_programs['PROGRAMS'].apply(lambda x: len(x) > 1)]

# Create sorted combination string
student_programs['program_combo'] = student_programs['PROGRAMS'].apply(lambda x: ', '.join(sorted(x)))

# Count program combinations
combo_summary = student_programs['program_combo'].value_counts().reset_index()
combo_summary.columns = ['program_combo', 'count']

# Flag combos that contain at least one Associate's degree
combo_summary['has_associates'] = combo_summary['program_combo'].apply(
    lambda combo: any(p.startswith('A') for p in combo.split(', '))
)

# Top 10 combinations: With and Without Associates
combos_with_A = combo_summary[combo_summary['has_associates']].head(10)
combos_without_A = combo_summary[~combo_summary['has_associates']].head(10)

# Optional: Build program code → Actual Title map
program_title_map = df_clean.drop_duplicates(subset='PROGRAMS').set_index('PROGRAMS')['Actual Title'].to_dict()

# Function: Get titles for top 5 combos
def get_titles_for(combo_df):
    title_data = []
    for combo in combo_df.head(5)['program_combo']:
        codes = combo.split(', ')
        titles = [program_title_map.get(c, 'Unknown') for c in codes]
        title_data.append({'Program Combo': combo, 'Titles': ', '.join(titles)})
    return pd.DataFrame(title_data)

titles_with_df = get_titles_for(combos_with_A)
titles_without_df = get_titles_for(combos_without_A)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Top Program Combinations", layout="wide")

st.title("🎓 Top Program Combinations Dashboard")

tab1, tab2 = st.tabs(["With Associate's Degree", "Without Associate's Degree"])

with tab1:
    st.subheader("Top 10 Combinations (With Associate's Degree)")
    st.dataframe(combos_with_A, use_container_width=True)

    st.subheader("📊 Bar Chart")
    st.bar_chart(combos_with_A.set_index('program_combo')['count'])

    st.subheader("Top 5: Program Titles")
    st.dataframe(titles_with_df, use_container_width=True)

with tab2:
    st.subheader("Top 10 Combinations (Without Associate's Degree)")
    st.dataframe(combos_without_A, use_container_width=True)

    st.subheader("📊 Bar Chart")
    st.bar_chart(combos_without_A.set_index('program_combo')['count'])

    st.subheader("Top 5: Program Titles")
    st.dataframe(titles_without_df, use_container_width=True)
