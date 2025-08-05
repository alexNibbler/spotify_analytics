import spotify_cli_analysis


def main():
    spotify_cli_analysis.menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exiting...")