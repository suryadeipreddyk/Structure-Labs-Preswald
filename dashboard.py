from preswald import connect, get_df, text, selectbox, slider, table, plotly, text_input, sidebar
import plotly.express as px

connect()

# Load the Netflix titles dataset
df = get_df("netflix_titles")

# Dashboard Title
text("# Netflix Titles Dashboard")

# 1) Filter by Type (Movie/TV Show)
types = ["All"] + sorted(df["type"].dropna().unique().tolist())
type_sel = selectbox("Select Type", types)
if type_sel != "All":
    df = df[df["type"] == type_sel]

# 2) Filter by Release Year Range
text("## Filter by Release Year Range")
start_year = slider(
    label="Start Year",
    min_val=int(df["release_year"].min()),
    max_val=int(df["release_year"].max()),
    step=1,
    default=int(df["release_year"].min())
)
end_year = slider(
    label="End Year",
    min_val=int(df["release_year"].min()),
    max_val=int(df["release_year"].max()),
    step=1,
    default=int(df["release_year"].max())
)
# Ensure valid range
if start_year > end_year:
    start_year, end_year = end_year, start_year

# Apply year filters
df = df[(df["release_year"] >= start_year) & (df["release_year"] <= end_year)]

# 3) Line Chart: Number of Titles by Release Year
text("## Titles by Release Year")
counts = df.groupby("release_year").size().reset_index(name="count")
fig1 = px.line(
    counts,
    x="release_year",
    y="count",
    markers=True,
    title="Number of Titles by Release Year"
)
plotly(fig1)

# 4) Bar Chart: Top 10 Genres
text("## Top 10 Genres")
genres = df["listed_in"].dropna().str.split(", ").explode()
top_genres = genres.value_counts().nlargest(10).reset_index()
top_genres.columns = ["genre", "count"]
fig2 = px.bar(
    top_genres,
    x="genre",
    y="count",
    title="Top 10 Genres"
)
plotly(fig2)

# 5) Pie Chart: Proportion of Movies vs TV Shows
text("## Proportion of Movies vs TV Shows")
type_counts = df["type"].value_counts().reset_index()
type_counts.columns = ["type", "count"]
fig3 = px.pie(
    type_counts,
    values="count",
    names="type",
    title="Proportion of Movies vs TV Shows"
)
plotly(fig3)

# 6) Heatmap: Release Year vs Genre
text("## Release Year vs Genre Heatmap")
df_genre = df.assign(genre=df["listed_in"].dropna().str.split(", ")).explode("genre")
genre_years = df_genre.groupby(["release_year", "genre"]).size().reset_index(name="count")
pivot = genre_years.pivot(index="genre", columns="release_year", values="count").fillna(0)
fig4 = px.imshow(
    pivot,
    title="Heatmap of Titles by Release Year and Genre",
    labels={"x": "Release Year", "y": "Genre", "color": "Count"},
    aspect="auto"
)
plotly(fig4)

# 7) Treemap: Content Type Breakdown by Genre
text("## Content Type Breakdown by Genre")
genre_type_counts = df_genre.groupby(["type", "genre"]).size().reset_index(name="count")
fig5 = px.treemap(
    genre_type_counts,
    path=["type", "genre"],
    values="count",
    title="Content Type Breakdown by Genre"
)
plotly(fig5)

# 8) Genre Trends Over Time
text("## Genre Trends Over Time")
fig6 = px.area(
    genre_years,
    x="release_year",
    y="count",
    color="genre",
    title="Genre Trends Over Time"
)
plotly(fig6)

# 9) Top Directors with Most Releases
text("## Top Directors with Most Releases on Netflix")
df_directors = df["director"].dropna().str.split(", ").explode()
director_counts = df_directors.value_counts().reset_index()
director_counts.columns = ["director", "count"]
top_directors = director_counts.head(5)
fig7 = px.bar(
    top_directors,
    x="director",
    y="count",
    title="Top Directors with Most Releases on Netflix",
    color="count",
    color_continuous_scale="Blues"
)
plotly(fig7)

# 10) Top Cast Members with Most Appearances
text("## Top Cast Members with Most Appearances on Netflix")
df_cast = df["cast"].dropna().str.split(", ").explode()
cast_counts = df_cast.value_counts().reset_index()
cast_counts.columns = ["cast_member", "count"]
top_cast = cast_counts.head(5)
fig8 = px.bar(
    top_cast,
    x="cast_member",
    y="count",
    title="Top Cast Members with Most Appearances on Netflix",
    color="count",
    color_continuous_scale="Viridis"
)
plotly(fig8)
