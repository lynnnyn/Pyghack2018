
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[41]:


champ_fuel = pd.read_csv("fuel_card_export_new.csv")


# In[42]:


fuel = champ_fuel[(champ_fuel["Product Class"] != "Non-Fuel") & (champ_fuel["Product Class"] != "Service")]


# In[43]:


prod_vs_price = fuel.groupby('Product Class', as_index=False)['Unit Cost'].mean()
prod_vs_price = prod_vs_price.sort_values(by="Unit Cost")
prod_vs_price


# In[90]:


fuel["Product Class"].value_counts()


# In[46]:


city_vs_price = fuel.groupby('Merchant City', as_index=False)['Unit Cost'].mean()
city_vs_price = city_vs_price.sort_values(by="Unit Cost")
#plt.plot(city_vs_price["Merchant City"], city_vs_price["Unit Cost"],marker = "o")
y_pos = np.arange(len(city_vs_price["Merchant City"]))
plt.bar(y_pos, city_vs_price["Unit Cost"], align='center', alpha=0.5)
plt.xticks(y_pos, city_vs_price["Merchant City"], rotation = 60)
plt.ylabel('Annual fuel price')
plt.ylim(2.0,2.6)
plt.title('Annual fuel price VS City')
plt.show()
#fuel_for_price = pd.DataFrame()


# In[49]:


fuel["Merchant City"].value_counts()


# In[50]:


import datetime
fuel["Month"] = pd.DatetimeIndex(fuel["Transaction Date"]).month
fuel["Weekday"] = pd.DatetimeIndex(fuel["Transaction Date"]).weekday


# In[236]:


fuel["Weekday"].value_counts()
weekday_vs_price = fuel.groupby("Weekday", as_index=False)['Unit Cost'].mean()
plt.plot(weekday_vs_price["Weekday"], weekday_vs_price["Unit Cost"],marker = "o")
plt.ylabel('Unit price mean')
plt.xlabel('Weekday')
#plt.ylim(2.1,2.7)
plt.title('Unit price change with Weekday')


# In[84]:


fuel["Month"].value_counts()
month_vs_price = fuel.groupby("Month", as_index=False)['Unit Cost'].mean()
plt.plot(month_vs_price["Month"], month_vs_price["Unit Cost"],marker = "o")
plt.ylabel('Unit price mean')
plt.xlabel('Month')
plt.ylim(2.1,2.7)
plt.title('Unit price change with Month')


# In[135]:


unleaded.sort_values(by = 'Unit Cost')


# In[118]:


address_vs_price = fuel.groupby(["Merchant Street Address","Product Class"], as_index=False)['Unit Cost'].mean()
unleaded = address_vs_price[address_vs_price["Product Class"]=="Unleaded"]
unleaded =unleaded.sort_values(by = 'Unit Cost')
diesel = address_vs_price[address_vs_price["Product Class"]=="Diesel"]
diesel =diesel.sort_values(by = "Unit Cost")
unlead_prem = address_vs_price[address_vs_price["Product Class"]=="Unleaded Premium"]
unlead_prem.sort_values(by = "Unit Cost")
unlead_mid = address_vs_price[address_vs_price["Product Class"]=="Unleaded Mid-Grade"]
unlead_mid.sort_values(by = "Unit Cost")
E_85 = address_vs_price[address_vs_price["Product Class"]=="E-85"]
E_85.sort_values(by = "Unit Cost")


# In[99]:


diesel.sort_values(by = "Unit Cost")


# In[240]:


unleaded_all = fuel[fuel["Product Class"] == "Unleaded"]
diesel_all = fuel[fuel["Product Class"] == "Diesel"]


# In[241]:


unleaded_all.groupby("Merchant Brand",as_index=False)['Unit Cost'].mean().sort_values(by='Unit Cost')


# In[242]:


diesel_all.groupby("Merchant Brand",as_index=False)['Unit Cost'].mean().sort_values(by='Unit Cost')


# In[181]:


merchant_address = fuel["Merchant Street Address"].value_counts()>=0
x = merchant_address[merchant_address == True].index


# In[173]:


fuel["Merchant Street Address"].value_counts()


# In[182]:


unleaded[unleaded["Merchant Street Address"].isin(x)]


# In[183]:


diesel[diesel["Merchant Street Address"].isin(x)]


# In[247]:


total = fuel[fuel["Merchant Street Address"]=="507 W University Ave"]["Units"].sum()
price = fuel[fuel["Merchant Street Address"]=="507 W University Ave"]["Unit Cost"].mean()
unit_price_differ = price - fuel[fuel["Merchant Street Address"]=="810 W Green St"]["Unit Cost"].mean()
annual_save = total * unit_price_differ
annual_save


# In[249]:


#G_507_W_uni = unleaded_all[unleaded_all["Merchant Street Address"] == "507 W University Ave"]
#test = G_507_W_uni.groupby("Month")['Unit Cost'].mean()
#test
annual_save = 0
c = ["507 W University Ave","306 E Main St","508 S Vine St"]
for i in c:
    total = fuel[fuel["Merchant Street Address"]==i]["Units"].sum()
    price = fuel[fuel["Merchant Street Address"]==i]["Unit Cost"].mean()
    unit_price_differ = price - fuel[fuel["Merchant Street Address"]=="810 W Green St"]["Unit Cost"].mean()
    annual_save = annual_save + total * unit_price_differ
annual_save


# In[296]:


total = fuel[fuel["Merchant Street Address"]=="1509 E University Ave"]["Units"].sum()
price = fuel[fuel["Merchant Street Address"]=="1509 E Universi  ty Ave"]["Net Cost"].sum()
#unit_price_differ = price - fuel[fuel["Merchant Street Address"]=="2100 E University Ave"]["Unit Cost"].mean()
annual_save =  total * fuel[fuel["Merchant Street Address"]=="2100 E University Ave"]["Unit Cost"].mean() - price
annual_save


# In[295]:


total = fuel[fuel["Merchant Street Address"]=="1605 N Cunningham Ave"]["Units"].sum()
price = fuel[fuel["Merchant Street Address"]=="1605 N Cunningham Ave"]["Net Cost"].sum()
#unit_price_differ = price - fuel[fuel["Merchant Street Address"]=="1809 N Cunningham Ave"]["Unit Cost"].mean()
annual_save =  total * fuel[fuel["Merchant Street Address"]=="1809 N Cunningham Ave"]["Unit Cost"].mean()- price
annual_save


# In[294]:


annual_save = 0
c = ["507 W University Ave","306 E Main St","508 S Vine St"]
for i in c:
    total = fuel[fuel["Merchant Street Address"]==i]["Units"].sum()
    price = fuel[fuel["Merchant Street Address"]==i]["Net Cost"].sum()
    #unit_price_differ = price - fuel[fuel["Merchant Street Address"]=="810 W Green St"]["Unit Cost"].mean()
    annual_save = annual_save + (total * fuel[fuel["Merchant Street Address"]=="810 W Green St"]["Unit Cost"].mean() - price)
annual_save


# In[134]:


plt.plot(test.index, test.values,marker = "o")
plt.ylabel('Unleaded Unit price mean')
plt.xlabel('Month')
plt.title('Unit price of unleaded in 507 W University ave with Month')


# In[184]:


gas_address = fuel["Merchant Street Address"] +"," + fuel["Merchant City"] + "," + fuel["Merchant State / Province"] +","+ fuel["Merchant Postal Code"]
address = gas_address.unique()


# In[147]:


import requests
import logging
import time


# In[148]:


logger = logging.getLogger("root")
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


# In[152]:


API_KEY = 'AIzaSyCO6xWAy1F4WEAAArjT8qgEgFjZc77B7ds'
data =pd.DataFrame({"Address":address}) 
addresses = (data[address_column_name] + ',USA').tolist()


# In[167]:


# Create a list to hold results
results = []
add = []
# Go through each address in turn
for address in addresses:
    geocode_result = get_google_location(address, API_KEY)    
    geo_result = [geocode_result["formatted_address"],geocode_result["latitude"],geocode_result["longitude"]]
    add.append(geo_result)
    results.append(geocode_result)           


# In[169]:


address_map = pd.DataFrame(add,columns=["Address","Latitude","Longitude"])
address_map.to_csv("address_location.csv", index= False)


# In[166]:


def get_google_location(address, api_key=None):

    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)+ "&key={}".format(api_key)
    results = requests.get(geocode_url)
    results = results.json()
       
    answer = results['results'][0]
    output = {
        "formatted_address" : answer.get('formatted_address'),
        "latitude": answer.get('geometry').get('location').get('lat'),
        "longitude": answer.get('geometry').get('location').get('lng'),
        "accuracy": answer.get('geometry').get('location_type'),
        "google_place_id": answer.get("place_id"),
        "type": ",".join(answer.get('types')),
        "postcode": ",".join([x['long_name'] for x in answer.get('address_components') 
                                  if 'postal_code' in x.get('types')])
        }
    
    return output


# In[193]:


address_map["Street"] = address_map["Address"].str.split(",").str[0]


# In[203]:


density = pd.DataFrame(unleaded_all["Merchant Street Address"].value_counts())


# In[208]:


x = pd.DataFrame.merge(address_map,density,left_on="Street",right_index= True,how = "inner")


# In[210]:


map_unleaded = pd.DataFrame.merge(x,unleaded,left_on="Street",right_on="Merchant Street Address",how = "inner")


# In[224]:


map_unleaded.to_csv("map_unleaded.csv",index= False)


# In[227]:


density = pd.DataFrame(diesel_all["Merchant Street Address"].value_counts())
x = pd.DataFrame.merge(address_map,density,left_on="Street",right_index= True,how = "inner")
map_diesel = pd.DataFrame.merge(x,diesel,left_on="Street",right_on="Merchant Street Address",how = "inner")
map_diesel.to_csv("map_diesel.csv",index= False)


# In[267]:


fuel.groupby("Department")["Net Cost"].sum().sort_values()


# In[266]:


#Vehicle Description
fuel["Vehicle Description"].value_counts()
fuel.groupby("Vehicle Description")["Units"].sum().sort_values()
model = fuel["Vehicle Description"].str.split(" ").str[-2:]
" ".join(model.iloc[1])
x = []
for i in model:
    y = " ".join(i)
    x.append(y)
    
fuel["model"] = x
fuel["model"].value_counts()
fuel.groupby("model")["Unit Cost"].mean().sort_values()
filby_distance = fuel[(fuel["Distance Driven"]>=100) & (fuel["Distance Driven"]<=300)]
filby_distance.groupby("model")["Fuel Economy"].mean().sort_values()

