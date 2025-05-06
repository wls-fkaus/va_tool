import pandas as pd

# Load the CSV (force ID and PROGRAMS as strings)
df = pd.read_csv('Anonymized_SP25_Program_Rosters.csv', dtype={'ID': str, 'PROGRAMS': str})

df = df.drop(columns={'Current Status', 'Status Date', 'Current End Date', 'Advisor', 'Primary E-Mail', 'Smv Vetben Benefit ', 'Smv Vetben End Date '})


df['ID'] = df['ID'].str.strip()
df['PROGRAMS'] = df['PROGRAMS'].str.strip()

df.replace({'': pd.NA}, inplace=True)

df = df.dropna(subset=['PROGRAMS'])
df = df.dropna(subset=['ID'])

df = df[~df['PROGRAMS'].str.startswith('T', na=False)]
df = df[~df['PROGRAMS'].str.startswith('P', na=False)]

df = df[df['ID'].duplicated(keep=False)]
df.to_csv('clean_data.csv', index=False)


