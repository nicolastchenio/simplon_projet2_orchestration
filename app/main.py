import pandas as pd
from modules.mon_module import add, print_data, square, sub


def main():
    """Run the application."""
    df = pd.read_csv("app/moncsv.csv")

    print(add(2, 3))
    print(sub(5, 2))
    print(square(4))
    print_data(df)


if __name__ == "__main__":
    main()
