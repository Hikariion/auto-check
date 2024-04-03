import pandas as pd
import sys
from termcolor import colored

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
    for column in ['男通用', '女未婚', '女已婚']:
        df_prices[column] = df_prices[column].apply(normalize_value)
        df_packages[column] = df_packages[column].apply(normalize_value)

    # Merge the two dataframes on '项目名称' for comparison
    merged_df = pd.merge(df_packages[['项目名称', '男通用', '女未婚', '女已婚']],
                         df_prices[['项目名称', '男通用', '女未婚', '女已婚']],
                         on='项目名称',
                         suffixes=('_套餐表', '_价格表'))

    # Check if values match across the dataframes for each category
    merged_df['男通用_匹配'] = merged_df['男通用_套餐表'] == merged_df['男通用_价格表']
    merged_df['女未婚_匹配'] = merged_df['女未婚_套餐表'] == merged_df['女未婚_价格表']
    merged_df['女已婚_匹配'] = merged_df['女已婚_套餐表'] == merged_df['女已婚_价格表']

    filtered_mismatches = merged_df[~(merged_df['男通用_匹配'] & merged_df['女未婚_匹配'] & merged_df['女已婚_匹配'])]

    merged_df = pd.merge(
        df_prices[['项目名称', '男通用', '女未婚', '女已婚']],
        df_packages[['项目名称', '男通用', '女未婚', '女已婚']],
        on='项目名称',
        how='outer',
        indicator=True,
        suffixes=('_价格表', '_套餐表')
    )

    missing_in_packages = merged_df.loc[merged_df['_merge'] == 'right_only', '项目名称']

    return filtered_mismatches, missing_in_packages.tolist()

def can_convert_to_float(s):
    # 检查字符串是否是"NaN"
    if s.lower() == "nan":
        return False
    try:
        float(s)
        return True
    except ValueError:
        return False

def print_mismatches(mismatches):
    # 定义表头和列的宽度
    headers = mismatches.columns.tolist()
    print(colored(' | '.join(headers), 'cyan'))  # 打印表头

    # 遍历每一行打印
    for index, row in mismatches.iterrows():
        row_data = []
        is_mismatch = False  # 标记是否有不匹配的数据
        for col in headers:
            value = row[col]
            row_data.append(str(value))

        # 如果有不匹配的数据，则标记为True
        t = 0
        for value in row_data:
            if can_convert_to_float(value):
                if t == 0:
                    t = float(value)
                else:
                    if t != float(value):
                        is_mismatch = True
                        break

        # 如果有不匹配的数据，则整行标记为黄色，否则为默认颜色
        if is_mismatch:
            print(colored(' | '.join(row_data), 'yellow'))
        # else:
        #     print(' | '.join(row_data))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_price.py <path_to_prices_table> <path_to_packages_table>")
        sys.exit(1)

    file_path_prices = sys.argv[1]
    file_path_packages = sys.argv[2]

    mismatches, missing = compare_price_tables(file_path_prices, file_path_packages)

    print_mismatches(mismatches)

    print("\n--------------------------- 无法匹配的项目 --------------------------------\n")

    print(missing)
