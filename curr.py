# Procurar Latim
latin_search = df[df['Name'].str.contains('latin', case=False, na=False)]
print(latin_search[['ID', 'Name', 'Glottocode', 'long_extinct', 'year_of_extinct']])