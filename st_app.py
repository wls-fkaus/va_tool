import streamlit as st
import pandas as pd
import altair as alt
import toml

# Set wide layout and page config
#st.set_page_config(page_title="Top Program Combinations", layout="wide")

# Load the config.toml file
config = toml.load('config.toml')

# Extract values for the page configuration
page_title = config.get('app', {}).get('title', 'Default Title')
layout = config.get('app', {}).get('layout', 'centered')

# Set the page config with values from config.toml
st.set_page_config(page_title="Top Program Combinations", layout="wide")

# Inject custom CSS for black and gold theme
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #FFD700;
    }
    .stApp {
        background-color: #000000;
    }
    table {
        color: #FFD700;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700 !important;
    }
    .css-1d391kg, .css-ffhzg2, .stTabs [role="tab"] {
        color: #FFD700 !important;
        background-color: #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)

# Page title
st.markdown("<h1 style='color:#FFD700;'>🎓 Top Program Combinations Dashboard</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📁 Upload a CSV file", type=["csv"])

# If a file is uploaded
if uploaded_file is not None:
    df_clean = pd.read_csv(uploaded_file, dtype={'ID': str, 'PROGRAMS': str})
    student_programs = df_clean.groupby('ID')['PROGRAMS'].apply(list).reset_index()
    student_programs = student_programs[student_programs['PROGRAMS'].apply(lambda x: len(x) > 1)]
    student_programs['program_combo'] = student_programs['PROGRAMS'].apply(lambda x: ', '.join(sorted(x)))
    combo_summary = student_programs['program_combo'].value_counts().reset_index()
    combo_summary.columns = ['program_combo', 'count']
    combo_summary['has_associates'] = combo_summary['program_combo'].apply(
        lambda combo: any(p.startswith('A') for p in combo.split(', '))
    )
    program_title_map = df_clean.drop_duplicates(subset='PROGRAMS').set_index('PROGRAMS')['Actual Title'].to_dict()

    def codes_to_titles(combo):
        codes = combo.split(', ')
        titles = [program_title_map.get(code, 'Unknown') for code in codes]
        return '\n'.join(titles)

    combo_summary['program_combo_titles'] = combo_summary['program_combo'].apply(codes_to_titles)

    def get_titles_for(combo_df):
        title_data = []
        for combo in combo_df.head(5)['program_combo']:
            codes = combo.split(', ')
            titles = [program_title_map.get(c, 'Unknown') for c in codes]
            title_data.append({'Program Combo': ', '.join(codes), 'Titles': ', '.join(titles)})
        return pd.DataFrame(title_data)

    combos_with_A = combo_summary[combo_summary['has_associates']].head(10)
    combos_without_A = combo_summary[~combo_summary['has_associates']].head(10)
    titles_with_df = get_titles_for(combos_with_A)
    titles_without_df = get_titles_for(combos_without_A)

    def render_table_with_newlines(df):
        html = """
        <style>
        table.custom {
            width: 100%;
            border-collapse: collapse;
            font-size: 15px;
        }
        table.custom thead {
            background-color: #000000;
            color: #FFD700;
        }
        table.custom th, table.custom td {
            padding: 10px;
            border-bottom: 1px solid #333;
        }
        </style>
        <table class='custom'>
        <thead>
        <tr>
        <th>📚 Program Combination</th>
        <th>👥 Count</th>
        </tr>
        </thead>
        <tbody>
        """
        for _, row in df.iterrows():
            title_html = "<br>".join(row['program_combo_titles'].split('\n'))
            html += f"<tr><td style='vertical-align:top'>{title_html}</td><td style='text-align:right'>{row['count']}</td></tr>"
        html += "</tbody></table>"
        st.markdown(html, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🌟 With Associate's Degree", "🚫 Without Associate's Degree"])

    with tab1:
        st.markdown("<h2 style='color:#FFD700;'>Top 10 Combinations (With Associate's Degree)</h2>", unsafe_allow_html=True)
        st.caption("These combinations include at least one Associate's degree per student.")
        st.markdown("#### 🧾 Combination Table")
        render_table_with_newlines(combos_with_A)
        st.markdown("#### 📊 Bar Chart")
        chart_with_A = alt.Chart(combos_with_A).mark_bar(color="#FFD700").encode(
            x=alt.X('count:Q', title='Number of Students'),
            y=alt.Y('program_combo_titles:N', sort='-x', title='Program Combination'),
            tooltip=['program_combo_titles', 'count']
        ).properties(height=400)
        st.altair_chart(chart_with_A, use_container_width=True)
        st.markdown("#### 🏷️ Top 5 Program Titles")
        st.dataframe(titles_with_df.style.set_properties(**{
            'background-color': '#000000',
            'color': '#FFD700',
        }), use_container_width=True)

    with tab2:
        st.markdown("<h2 style='color:#FFD700;'>Top 10 Combinations (Without Associate's Degree)</h2>", unsafe_allow_html=True)
        st.caption("These combinations exclude Associate's degrees.")
        st.markdown("#### 🧾 Combination Table")
        render_table_with_newlines(combos_without_A)
        st.markdown("#### 📊 Bar Chart")
        chart_without_A = alt.Chart(combos_without_A).mark_bar(color="#FFD700").encode(
            x=alt.X('count:Q', title='Number of Students'),
            y=alt.Y('program_combo_titles:N', sort='-x', title='Program Combination'),
            tooltip=['program_combo_titles', 'count']
        ).properties(height=400)
        st.altair_chart(chart_without_A, use_container_width=True)
        st.markdown("#### 🏷️ Top 5 Program Titles")
        st.dataframe(titles_without_df.style.set_properties(**{
            'background-color': '#000000',
            'color': '#FFD700',
        }), use_container_width=True)

