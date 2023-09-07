from data_management import load_data_from_file, get_executable_relative_path
from classes import KRO_Tree
import os

df_aanzien = load_data_from_file(get_executable_relative_path("data", "KRO-aanzien-R22.csv"))
df_gebruik = load_data_from_file(get_executable_relative_path("data", "KRO-gebruik-R22_zonder-contact.csv"))

#%%

print(list(df_aanzien))
print(list(df_gebruik))

