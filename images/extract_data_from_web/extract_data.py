import pandas as pd

url = "https://bats.earth.sinica.edu.tw/Station/BATS_Stn_Summary.html"

htmlPage = pd.read_html(url)

# print(htmlPage)
print(f"total # of tables {len(htmlPage)}")

# print(htmlPage[1])

df = htmlPage[1]
columns = df.iloc[1, :].values
print(columns)

dict_list = []
for idx in range(2, df.shape[0]-3):
    _dict = {}
    for icol, col in enumerate(columns):
        _dict.update({col: df.iloc[idx, icol]})
    dict_list.append(_dict)

new_df = pd.DataFrame(dict_list)
print(new_df.head())

# save into csv file
new_df.to_csv('station_list.txt', index=False)
