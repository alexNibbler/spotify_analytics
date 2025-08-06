import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def interpret_correlation(r):
    if abs(r) >= 0.7:
        return "highly correlated"
    elif abs(r) >= 0.4:
        return "medium correlated"
    elif abs(r) >= 0.2:
        return "weakly correlated"
    else:
        return "not correlated"


def pearson_corr(df: pd.DataFrame, feature: str):
    if feature not in df.columns or "popularity" not in df.columns:
        print(f"Missing feature '{feature}' or 'popularity'.")
        return
    x = df[feature]
    y = df["popularity"]
    r = x.corr(y)
    interpretation = interpret_correlation(r)
    print(f"Pearson correlation between {feature} and popularity: r = {r:.3f} → {interpretation}.")
    plt.figure(figsize=(6,4))
    sns.scatterplot(x=x, y=y, alpha=0.6)
    plt.title(f"Pearson Correlation: {feature} vs Popularity")
    plt.xlabel(feature)
    plt.ylabel("Popularity")
    plt.grid(True)
    plt.show()

def covariance_check(df:pd.DataFrame, feature):
    if feature not in df.columns or "popularity" not in df.columns:
        print(f"Missing feature '{feature}' or 'popularity'.")
        return
    cov = np.cov(df[feature], df["popularity"])[0, 1]
    print(f"Covariance between {feature} and popularity: {cov:.2f}")

custom_colors = [
    "#e41a1c",  # red
    "#377eb8",  # blue
    "#4daf4a",  # green
    "#984ea3",  # purple
    "#ff7f00",  # orange
    "#a65628",  # brown
    "#f781bf",  # pink
    "#999999",  # gray
    "#dede00",  # yellow
    "#17becf",  # cyan
]


def genre_popularity(df: pd.DataFrame):
    genre_year_pop = df.groupby(["year", "genre"], observed=False)["popularity"].sum().reset_index()
    top_genres = genre_year_pop.groupby("genre", observed=False)["popularity"].sum().nlargest(10)
    print(top_genres)
    top_genres_names = top_genres.index.tolist()
    genre_year_top = genre_year_pop[genre_year_pop["genre"].isin(top_genres_names)]

    plt.figure(figsize=(12, 6))

    for i, genre in enumerate(top_genres_names):
        genre_data = genre_year_top[genre_year_top["genre"] == genre]
        plt.plot(genre_data["year"], genre_data["popularity"], label=genre, color=custom_colors[i])

    plt.title("Average Popularity of Top 10 Genres Over Time")
    plt.xlabel("Year")
    plt.ylabel("Popularity")
    plt.grid(True)
    plt.legend(title="Genre")
    plt.tight_layout()
    plt.show()


def artist_popularity(df: pd.DataFrame):
    artist_year_pop = df.groupby(["year", "artist"], observed=False)["popularity"].sum().reset_index()
    top_artists = artist_year_pop.groupby("artist", observed=False)["popularity"].sum().nlargest(10)
    print(top_artists)
    top_artists_names = top_artists.index.tolist()
    artist_year_top = artist_year_pop[artist_year_pop["artist"].isin(top_artists_names)]

    plt.figure(figsize=(12, 6))

    for i, artist in enumerate(top_artists_names):
        artist_data = artist_year_top[artist_year_top["artist"] == artist]
        plt.plot(artist_data["year"], artist_data["popularity"], label=artist, color=custom_colors[i])

    plt.title("Average Popularity of Top 10 Artists Over Time")
    plt.xlabel("Year")
    plt.ylabel("Popularity")
    plt.grid(True)
    plt.legend(title="Artist")
    plt.tight_layout()
    plt.show()

def popularity_label(x: float) -> str:
    if x >= 70:
        return "Popular"
    else:
        return "Less popular"

def interpret_p_value(p: float, mean_popular: float, mean_not_popular: float) -> str:
    if p < 0.05:
        conclusion = f"Feature is {"more" if mean_popular>mean_not_popular else "less"} inherent to popular"
        return f"Significant: {conclusion}"
    else:
        return "Not statistically strong"

def compare_less_and_more_popular_tracks_on_features(df):
    """Hypotheses
        - H_0: m1 = m2 (mean feature is the same for popular and less popular tracks)
        - H_1: m1 != m2 (means differ)
        We run independent samples t‑tests on several features.

        If p < 0.05, the difference in means is statistically significant — we reject the null hypothesis
        If p ≥ 0.05, we fail to reject — there's no strong evidence of a difference.
        """

    df["pop_group"] = df["popularity"].apply(popularity_label)
    df["pop_bucket3"] = pd.cut(df["popularity"], bins=[-np.inf, 50, 70, np.inf], labels=["Low", "Medium", "High"])
    df["pop_bucket3"] = df["pop_bucket3"].astype("category")

    df["genre"] = df["genre"].astype("category")

    features_to_compare = ["tempo","energy","danceability","loudness","liveness","valence","duration","acousticness","speechiness"]
    features_to_compare = [f for f in features_to_compare if f in df.columns]

    results = []
    for feat in features_to_compare:
        g1 = df.loc[df["pop_group"] == "Popular", feat].dropna()
        g2 = df.loc[df["pop_group"] == "Less popular", feat].dropna()
        # Welch's t-test (does not assume equal variances)
        t_stat, p_val = stats.ttest_ind(g1, g2, equal_var=False)
        results.append(
            {
                "feature": feat,
                "Popular_mean": g1.mean(),
                "LessPopular_mean": g2.mean(),
                "t": t_stat,
                "p": p_val,
                "Conclusion": interpret_p_value(p_val, mean_popular=g1.mean(), mean_not_popular=g2.mean())
             }
        )

    ttest_df = pd.DataFrame(results).sort_values("p")
    print(ttest_df)