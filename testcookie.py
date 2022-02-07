import altair as alt
from vega_datasets import data


source = data.cars()

# Brush for selection
brush = alt.selection(type='single', encodings=['x'])

# Histogram base
hist_base = alt.Chart(source).mark_bar(color='grey').encode(
    x=alt.X('Horsepower:Q', bin=True),
    y='count()',
).add_selection(brush)

# Histogram selection
hist_selection = alt.Chart(source).mark_bar().encode(
    x=alt.X('Horsepower:Q', bin=True),
    y='count()',
).transform_filter(brush)

# Base chart for data tables
ranked_text = alt.Chart(source).mark_text(align='right').encode(
    y=alt.Y('row_number:O',axis=None)
).transform_window(
    row_number='row_number()'
).transform_filter(
    brush
).transform_window(
    rank='rank(row_number)'
).transform_filter(
    alt.datum.rank<16
)

# Data Tables
horsepower = ranked_text.encode(text='Horsepower:N').properties(title=alt.TitleParams(text='Horsepower', align='right'))
mpg = ranked_text.encode(text='Miles_per_Gallon:N').properties(title=alt.TitleParams(text='MPG', align='right'))
origin = ranked_text.encode(text='Origin:N').properties(title=alt.TitleParams(text='Origin', align='right'))
text = alt.hconcat(horsepower, mpg, origin) # Combine data tables

# Build chart
alt.hconcat(
    hist_base+hist_selection,
    text
).resolve_legend(
    color="independent"
).configure_view(strokeWidth=0)