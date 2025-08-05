import pandas as pd
from pathlib import Path

CSV_PATH = "spotify_dataset_2010_2019.csv"


def load_dataset(file_path: Path = Path(CSV_PATH)) -> pd.DataFrame:
    encodings = ["utf-8", "latin1", "cp1252"]
    last_err = None
    for enc in encodings:
        try:
            return pd.read_csv(file_path, encoding=enc)
        except Exception as e:
            last_err = e
    else:
        if last_err:
            raise last_err


def iqr_filter(series: pd.Series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return (series >= lower) & (series <= upper)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns={
        "top genre": "genre",
        "bpm": "tempo",
        "nrgy": "energy",
        "dnce": "danceability",
        "dB": "loudness",
        "live": "liveness",
        "val": "valence",
        "dur": "duration",
        "acous": "acousticness",
        "spch": "speechiness",
        "pop": "popularity"
    })
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    df["genre"] = df["genre"].astype("category")
    df["artist"] = df["artist"].astype("category")
    df["year"] = df["year"].astype(int)

    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print(df.head(10))

    return df

def apply_IQR(df: pd.DataFrame):
    features_for_iqr = ["tempo", "energy", "danceability", "loudness", "liveness", "valence", "duration",
                        "acousticness", "speechiness", "popularity"]
    features_for_iqr = [c for c in features_for_iqr if c in df.columns]

    mask = pd.Series(True, index=df.index)
    for col in features_for_iqr:
        mask &= iqr_filter(df[col])

    df_iqr = df[mask].copy()
    print("Original rows:", len(df), " | After IQR:", len(df_iqr))

    return df_iqr
