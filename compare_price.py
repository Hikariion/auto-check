import pandas as pd
import sys
from tabulate import tabulate

def compare_price_tables(file_path_prices, file_path_packages):
    # Load the uploaded Excel files
    df_prices = pd.read_excel(file_path_prices)
    df_packages = pd.read_excel(file_path_packages)

    # Normalize data function: Convert "赠送" to 0 and handle missing data represented by "\"
    def normalize_value(value):
        if value == "赠送":
            return 0
        elif value == "\\":
            return None
        elif value == "/":
            return None
        else:
            return value

    # Apply the normalization function to relevant columns in both dataframes
    for column in ['男性', '未婚女性', '已婚女性']:
        df_prices[column] = df_prices[column].apply(normalize_value)
        df_packages[column] = df_packages[column].apply(normalize_value)

    # Merge the two dataframes on '项目名称' for comparison
    merged_df = pd.merge(df_packages[['项目名称', '男性', '未婚女性', '已婚女性']],
                         df_prices[['项目名称', '男性', '未婚女性', '已婚女性']],
                         on='项目名称',
                         suffixes=('_套餐表', '_价格表'))

    # Check if values match across the dataframes for each category
    merged_df['男性_匹配'] = merged_df['男性_套餐表'] == merged_df['男性_价格表']
    merged_df['未婚女性_匹配'] = merged_df['未婚女性_套餐表'] == merged_df['未婚女性_价格表']
    merged_df['已婚女性_匹配'] = merged_df['已婚女性_套餐表'] == merged_df['已婚女性_价格表']

    filtered_mismatches = merged_df[~(merged_df['男性_匹配'] & merged_df['未婚女性_匹配'] & merged_df['已婚女性_匹配'])]

    merged_df = pd.merge(
        df_prices[['项目名称', '男性', '未婚女性', '已婚女性']],
        df_packages[['项目名称', '男性', '未婚女性', '已婚女性']],
        on='项目名称',
        how='outer',
        indicator=True,
        suffixes=('_价格表', '_套餐表')
    )

    missing_in_packages = merged_df.loc[merged_df['_merge'] == 'right_only', '项目名称']

    return filtered_mismatches, missing_in_packages.tolist()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_price.py <path_to_prices_table> <path_to_packages_table>")
        sys.exit(1)

    file_path_prices = sys.argv[1]
    file_path_packages = sys.argv[2]

    mismatches, missing = compare_price_tables(file_path_prices, file_path_packages)

    print(mismatches)

    print(missing)
    # print(tabulate(mismatches, headers='keys', tablefmt='psql', showindex=False))
    #
    # print("\n--------------------------------------------------------\n")
    #
    # print(tabulate())
