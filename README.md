# spotify_analytics

## Project Goal

The goal of the project is to find a recipe for the ultimate chart hit according to several song features. As the input, we use Spotify music 2010-2019 dataset. Here is the dataset source and description https://www.kaggle.com/datasets/leonardopena/top-spotify-songs-from-20102019-by-year

Here are the directions we'll try to analyze:
1. What audio features correlate with popularity? 
2. Trends in genres over the years 
3. Trends in artists over the years 
4. Compare popular tracks vs less popular tracks in terms of their characteristics (e.g. tempo, energy, etc.)

**Most popular genres are:**

| Genre | Popularity |
|------:|:-----------|
| dance pop | 21047 |
| pop | 4490 |
| canadian pop | 2456 |
| boy band | 1045 |
| electropop | 1007 |
| barbadian pop | 981 |
| canadian contemporary r&b | 699 |
| british soul | 684 |
| big room | 656 |
| neo mellow | 540 |

**Top 10 most popular artists:**

| Artist | Popularity |
|------:|:-----------|
| Justin Bieber | 1150 |
| Maroon 5 | 1123 |
| Katy Perry | 1056 |
| Rihanna | 981 |
| Lady Gaga | 964 |
| Bruno Mars | 936 |
| Ed Sheeran | 862 |
| Shawn Mendes | 851 |
| The Chainsmokers | 839 |
| Calvin Harris | 782 |

## t-test - Compare popular tracks vs less popular tracks in terms of their characteristics

We start with a hypothesis that mean feature is the same for popular and less popular tracks. According to t-test, the hypothesis could not be proved, so more popular tracks tend to be less energetic and more danceable.

| Feature       | Popular_mean | LessPopular_mean | t         | p         | Conclusion                                 |
|:-------------|:-------------|:-----------------|:----------|:----------|:--------------------------------------------|
| danceability | 65.942568    | 62.872964        | 2.840950  | 0.004652  | Significant: Feature is more inherent to popular |
| energy       | 68.972973    | 71.980456        | -2.275939 | 0.023203  | Significant: Feature is less inherent to popular |
| liveness     | 16.712838    | 18.798046        | -1.959668 | 0.050496  | Not statistically strong                    |
| duration     | 222.219595   | 227.042345       | -1.743014 | 0.081852  | Not statistically strong                    |
| acousticness | 15.013514    | 13.664495        | 0.798350  | 0.424983  | Not statistically strong                    |
| valence      | 52.918919    | 51.557003        | 0.743194  | 0.457655  | Not statistically strong                    |
| loudness     | -5.513514    | -5.641694        | 0.569133  | 0.569570  | Not statistically strong                    |
| tempo        | 118.229730   | 118.850163       | -0.306953 | 0.758985  | Not statistically strong                    |
| speechiness  | 8.371622     | 8.345277         | 0.043205  | 0.965552  | Not statistically strong                    |


## Correlation - What audio features correlate with popularity?

No correlation was found between tracks popularity and musical features

## Conclusions

Unfortunately, we could not find an ultimate recipe of 100% hit, which shows it's a very creative job to be a songwriter and music producer.
