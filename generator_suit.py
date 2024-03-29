import pandas as pd
import numpy as np
import sys

pd.set_option('future.no_silent_downcasting', True)

class Man:
    def __init__(self, name, ori_price):
        self.name = name
        self.ori_price = ori_price
        self.price = int(ori_price)
class ManList:
    def __init__(self):
        self.list = []
    def add(self, man):
        self.list.append(man)

class MarriedWoman:
    def __init__(self, name, ori_price):
        self.name = name
        self.ori_price = ori_price
        self.price = int(ori_price)
class MarriedWomanList:
    def __init__(self):
        self.list = []
    def add(self, woman):
        self.list.append(woman)

class UnmarriedList:
    def __init__(self, name, ori_price):
        self.name = name
        self.ori_price = ori_price
        self.price = int(ori_price)
class UnmarriedWomanList:
    def __init__(self):
        self.list = []
    def add(self, unmarried_woman):
        self.list.append(unmarried_woman)

def clean_dataframe(df):
    # Replace "赠送" and "/" with NaN
    df_cleaned = df.replace("赠送", np.nan).replace("/", np.nan)

    # Drop rows with any NaN values
    df_cleaned = df_cleaned.dropna(how='any')

    return df_cleaned

def print_list(list):
    for item in list:
        print(item.name, item.ori_price, item.price)

def read_price_table(file_path, total_price=998, ratio = 1):
    df = pd.read_excel(file_path)

    # For men
    df_man = df[['序号', '类别', '项目名称', '意义', '科室', '注意事项', '男性']].copy()
    df_man.rename(columns={'男性': '价格'}, inplace=True)
    df_man = clean_dataframe(df_man)

    # For unmarried women
    df_unmarried_women = df[['序号', '类别', '项目名称', '意义', '科室', '注意事项', '未婚女性']].copy()
    df_unmarried_women.rename(columns={'未婚女性': '价格'}, inplace=True)
    df_unmarried_women = clean_dataframe(df_unmarried_women)

    # For married women
    df_married_women = df[['序号', '类别', '项目名称', '意义', '科室', '注意事项', '已婚女性']].copy()
    df_married_women.rename(columns={'已婚女性': '价格'}, inplace=True)
    df_married_women = clean_dataframe(df_married_women)

    man_list = ManList()
    married_woman_list = MarriedWomanList()
    unmarried_woman_list = UnmarriedWomanList()

    for index, row in df_man.iterrows():
        man = Man(name=row['项目名称'], ori_price=row['价格'])
        man_list.add(man)

    for index, row in df_married_women.iterrows():
        woman = MarriedWoman(name=row['项目名称'], ori_price=row['价格'])
        married_woman_list.add(woman)

    for index, row in df_unmarried_women.iterrows():
        unmarried_woman = UnmarriedList(name=row['项目名称'],
                                        ori_price=row['价格'])
        unmarried_woman_list.add(unmarried_woman)

    man_package = gen_single_package(man_list.list, total_price, ratio)
    woman_package = gen_single_package(married_woman_list.list, total_price, ratio)
    unmarried_package = gen_single_package(unmarried_woman_list.list, total_price, ratio)




def knapsack(N, V, w, v):
    dp = [0] * (V + 1)
    path = [[False for _ in range(V + 1)] for _ in range(N + 1)]

    for i in range(1, N + 1):
        for j in range(V, v[i] - 1, -1):
            if dp[j] < dp[j - v[i]] + w[i]:
                dp[j] = dp[j - v[i]] + w[i]
                path[i][j] = True

    # 找到选择的物品
    chosen_items = []
    volume = V
    for i in range(N, 0, -1):
        if path[i][volume]:
            chosen_items.append(i)
            volume -= v[i]

    print(f'max value: {dp[V]}')
    return dp[V], chosen_items[::-1]

def gen_single_package(list, total_price, ratio):
    # 预处理 list, 提出list中价格大于 total_price * ratio 的元素
    for p in list:
        if p.price > total_price * ratio:
            # 将 p 从 list 中删除
            list.remove(p)

    # 在 list 前面加一个空元素，使得 list 的索引从 1 开始
    list.insert(0, None)

    # 处理背包问题
    sum = total_price
    n = len(list)

    path = [[0] * 30005 for _ in range(30005)]
    dp = [0] * (30005)

    for i in range(1, n):
        for j in range(sum, -1, -1):
            if j >= list[i].price:
                if dp[j] <= dp[j - list[i].price] + list[i].price:
                    dp[j] = dp[j - list[i].price] + list[i].price
                    path[i][j] = 1
    res = []

    # 回溯路径
    i, j = n - 1, sum
    while i > 0 and j > 0:
        if path[i][j] == 1:
            print(list[i].price)
            res.append(list[i])
            j -= list[i].price
        i -= 1

    print(f'max value: {dp[sum]}')

    return res

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python compare_price.py <path_to_prices_table>")
        sys.exit(1)

    price_table_file_path = sys.argv[1]

    read_price_table(price_table_file_path)
