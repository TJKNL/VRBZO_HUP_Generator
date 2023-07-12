from data_management import load_data_from_file, get_executable_relative_path
from classes import KRO_Tree
import os

df_aanzien = load_data_from_file(get_executable_relative_path("data", "KRO-aanzien-R22.csv"))
df_gebruik = load_data_from_file(get_executable_relative_path("data", "KRO-gebruik-R22_zonder-contact.csv"))


tree = KRO_Tree(df_aanzien, df_gebruik)

#%% Kinderdagverblijven Let op: de SBI code klopt niet. Het zijn er ook heel veel.
tree.filter_SBI(88911)
tree.filter("personen", ">", 10)
tree.set_risk("C")
tree.store_results()
tree.reset()

#%%
tree.filter("celfunctie", "==", 1)
tree.set_risk("C")
tree.store_results()
tree.reset()

#%% Gezondheidszorg met overnachting
tree.filter_SBI([861, 87])
tree.filter("personen", ">", 10)
tree.set_risk("C")
tree.store_results()
tree.reset()

#%%
# Industrie onmogelijk filterbaar, inzetdiepte is onbekend.



#%%
tree.filter("winkelfunctie", "==", 1)
tree.filter("woz_opp_nietwoon", ">", 1000)
# TODO: Wonen boven winkels data is niet beschikbaar of uit de KRO te halen.
tree.set_risk("C")
tree.store_results()
tree.reset()

#%%
tree.filter("sportfunctie", "==", 1)
tree.filter("woz_opp_nietwoon", ">", 1000)
tree.set_risk("C")
tree.store_results()
tree.reset()

#%%
tree.filter("onderwijsfunctie", "==", 1)
tree.filter("woz_opp_nietwoon", ">", 1000)
tree.filter("pandhoogte", ">", 20)
tree.set_risk("C")
tree.store_results()
tree.reset()

#%% Logies Functie
tree.filter_SBI([551, 552])
tree.filter("personen", ">", 10)
tree.set_risk("C")
tree.store_results()
tree.reset()

#%%
tree.filter("kantoorfunctie", "==", 1)
tree.filter("woz_opp_nietwoon", ">", 1000)
tree.filter("pandhoogte", ">", 20) # Dan B
tree.set_risk("B")
tree.store_results()
tree.reset()
# No objects above 70m
tree.filter("kantoorfunctie", "==", 1)
tree.filter("woz_opp_nietwoon", ">", 1000)
tree.filter("pandhoogte", ">", 70) # Dan C
tree.set_risk("C")
tree.store_results()
tree.reset()

#%% Filtering for personen still leads to problems. Not really viable.
# tree.filter("overigefunctie", "==", 1)
# tree.filter("personen", ">", 1000)
# # Can't filter for vehicle storage
# tree.set_risk("B")
# tree.store_results()
# tree.reset()

#%%
#tree.save_hup()
# Note that saving the A's as well is much more computationally expensive. It takes long!
tree.insert_dataframe_into_excel(get_executable_relative_path("HUP", "origineel (niet aanpassen).xlsx"), "Controle objecten", 2, add_A=False, remove_no_name=True)


#%%
#tree.get_history()
