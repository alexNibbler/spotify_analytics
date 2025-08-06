import pandas as pd
from prepare import CSV_PATH, load_dataset, clean_data, apply_IQR_to_single_column
from stats_functions import (
    genre_popularity,
    artist_popularity,
    covariance_check,
    pearson_corr,
    compare_less_and_more_popular_tracks_on_features
)

def load_menu() -> pd.DataFrame | None:
    print("1. Load default dataset")
    print("2. Load from specific file path")
    choice = input("Choose dataset loading option (1/2): ")
    if choice == "2":
        path = input("Enter full path to CSV file: ").strip()
    else:
        path = CSV_PATH

    try:
        df = load_dataset(path)
    except Exception as e:
        print("Failed to load dataset:", e)
        return None

    try:
        return clean_data(df)
    except Exception as e:
        print("Failed to load dataset:", e)
        return None

def analyze_feature_correlation(df: pd.DataFrame):
    FEATURES = ["tempo", "energy", "danceability", "loudness", "liveness", "valence", "duration", "acousticness",
                "speechiness"]

    print("Select a feature to correlate with popularity:")
    for i, feat in enumerate(FEATURES, 1):
        print(f"{i}. {feat}")

    choice = input("Enter feature number: ").strip()

    if not choice.isdigit() or int(choice) not in range(1, len(FEATURES) + 1):
        print("Invalid choice.")
    else:
        selected_feature = FEATURES[int(choice) - 1]
        df_iqr = apply_IQR_to_single_column(df, selected_feature)
        covariance_check(df_iqr, selected_feature)
        pearson_corr(df_iqr, selected_feature)

def menu():
    df = None
    while True:
        print("\nSpotify Data Analysis CLI")
        print("1. Load Dataset")
        print("2. Show Genre Popularity Over Time")
        print("3. Show Artist Popularity Over Time")
        print("4. Analyze Feature Correlation with Popularity")
        print("5. Compare popular tracks vs less popular by features")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            df = load_menu()
        elif choice == "2":
            if df is not None:
                genre_popularity(df)
            else:
                print("Please load a dataset first.")
        elif choice == "3":
            if df is not None:
                artist_popularity(df)
            else:
                print("Please load a dataset first.")
        elif choice == "4":
            if df is not None:
                analyze_feature_correlation(df)
            else:
                print("Please load a dataset first.")
        elif choice == "5":
            if df is not None:
                compare_less_and_more_popular_tracks_on_features(df)
            else:
                print("Please load a dataset first.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
