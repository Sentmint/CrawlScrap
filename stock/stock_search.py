import glob
import os
import sys
import pandas as pd

# DECOMMISSIONED. Might be used later, not worth the hassle of keeping up to date nasdaq information as of now.

def find_stock(args: list[str]):
    found_stock = {}
    stock_dict = read_csv()
    args = [arg.lower() for arg in args]

    # Currently set up to only return the first match with the given cli arg.
    # Gets a bit out of hand otherwise given that we are using the found results as the search
    # parameter for the Twitter scraper, so # of args will always be # of searches done with Twitter scraper.
    for market in stock_dict:
        # Added so second for loop block doesn't check for argument if it was already found in Symbols
        # TODO: If we don't want to return multiple stocks from across markets,
        #  add a way to modify args between market loops. Ex: 'ZZZ' in both nasdaq and tsx
        name_args = args.copy()
        for arg in args:
            for key, value in market["Symbol"].items():
                if not isinstance(value, str):
                    continue
                if arg == value.lower():
                    found_stock[market["Symbol"][key]] = market["Name"][key]
                    print(found_stock)
                    name_args.remove(arg)
                    break

        for arg in name_args:
            for key, value in market["Name"].items():
                if not isinstance(value, str):
                    continue
                if arg in value.lower():
                    found_stock[market["Symbol"][key]] = market["Name"][key]
                    print(found_stock)
                    break

    return found_stock


def read_csv():
    stock_dict = []
    base_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(base_directory, "data")
    csv_files = glob.glob(os.path.join(data_directory, "*.csv"))

    for file in csv_files:
        df = pd.read_csv(file)
        stock_dict.append(df.to_dict())

    return stock_dict

#find_stock(sys.argv[1:])
