#!/usr/bin/env python
# coding: utf-8

# # Case 3: Laadpaal Data

# ### Importeren packages

# In[1]:


#importeren van de packages
import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import plotly as plt


# ### Importeren data

# In[2]:


#importeren van de data
df1 = pd.read_csv('laadpaaldata.csv')
#df1.head()


# In[3]:


#Geen rijen worden verwijderd na deze functie, dit betekent dat deze dataset goede/complete informatie bevat.
df1.dropna()


# In[4]:


df1.duplicated()
df1.drop_duplicates()


# In[5]:


URL = 'https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=100&compact=true&verbose=false&key=d72b2b71-ac69-4b31-8f6e-39e8481cda42'
response = requests.get(url=URL).json()
df2 = pd.DataFrame.from_dict(response)
#df2.head()


# In[6]:


#in df2 worden veel rijen verwijderd na de dropna functie, in deze dataset mist veel data
df2.dropna()


# In[7]:


df2.duplicated(subset='ID', keep=False)


# In[8]:


#df2.columns


# In[9]:


URL2 ='https://opendata.rdw.nl/resource/w4rt-e856.json'
response2 = requests.get(url=URL2).json()
df3 = pd.DataFrame.from_dict(response2)
#df3.head()


# In[10]:


df3.duplicated(subset='kenteken', keep=False)
df3.drop_duplicates()


# In[11]:


#df3.columns


# In[51]:


# In[65]:




# In[55]:




# In[17]:


#add new colomn brandstofsoort
import numpy as np
df3['Brandstof_soort'] = np.where(df3['cilinderinhoud'] == 'NaN', 'Brandstof', 'Elektrisch')
#df3.head(30)


# In[18]:


#getallen omzetten in datetime
#df3['datum_tenaamstelling']
df3= df3.assign(datum_tenaamstelling = pd.to_datetime(df3['datum_tenaamstelling'], format='%Y%m%d'))
#df3.head()


# In[19]:


#sorteren op maand
df3.sort_values(by='datum_tenaamstelling')


# In[22]:


df3 = df3.sort_values(by=['datum_tenaamstelling'], ascending = True)


# ### Schrijven code

# In[84]:


#Histogram van de laadtijd
df1.drop(df1.index[df1['ChargeTime']<0], inplace=True)
df1.drop(df1.index[df1['ChargeTime']>12], inplace=True)

fig = px.histogram(df1, x="ChargeTime")

fig.add_vline(x=np.median(df1.ChargeTime), line_dash = 'dash', line_color = 'red')
fig.add_vline(x=np.mean(df1.ChargeTime), line_dash = 'dash', line_color = 'green')

fig.update_layout(
    title_text='Laadtijden per auto (t/m 12 uur lang)',
    xaxis_title_text='Laadtijd (in uren)',
    yaxis_title_text="Hoeveelheid auto's")

fig.add_annotation(x=0.9, y=0.9,
            text= 'Red is median and green is mean' ,
            showarrow=False,
            yshift=10,
            xref="paper",
            yref="paper",
            bordercolor="#ffffff",
            borderwidth=0.5,
            bgcolor="#293f95",
            opacity=0.8,
            font=dict(
            family="Courier New, monospace",
            size=16,
            color="#ffffff"
            ))

# In[68]:


# met onderstaande regel kun je kiezen vanaf welke datum gekeken moet worden, dit maakt de diagram overzichtelijker
df4 = df3[df3['datum_tenaamstelling'] > '2021-09-01T00:00:00.000']

fig3 =px.ecdf(df4, x='datum_tenaamstelling')

fig3.update_layout(
    title_text='Kans op verkochte autos vanaf oktober 2021 tot oktober 2022')


# In[69]:


# met onderstaande regel kun je kiezen vanaf welke datum gekeken moet worden, dit maakt de diagram overzichtelijker
df4 = df3[df3['datum_tenaamstelling'] > '2021-09-01T00:00:00.000']

fig4 =px.histogram(df4, x='datum_tenaamstelling')
fig4.update_layout(
    title_text='Aantal verkochte autos vanaf september 2021 tot oktober 2022')



# In[95]:


#regressie lijn
df1.drop(df1.index[df1['ConnectedTime']>60], inplace=True)

fig5 = px.scatter(df1, x="ConnectedTime", y="TotalEnergy", color='MaxPower', trendline="lowess", trendline_options=dict(frac=0.1))
fig5.update_layout(
    title_text='Opgeladen stroom en vermogen vs Connected Time')

# In[97]:

#latitude and longitude bevinden zich in adressinfo
#df2['AddressInfo'].iloc[0]

objs = [df2, pd.DataFrame(df2['AddressInfo'].tolist()).iloc[:, :10]]
dfnew = pd.concat(objs, axis=1).drop('AddressInfo', axis=1)
#dfnew.head()

dfnew.rename(columns={'Latitude':'lat'}, inplace=True)
dfnew.rename(columns={'Longitude':'lon'}, inplace=True)
#dfnew.head()

import plotly.express as px
fig8 = px.scatter_mapbox(dfnew, lat="lat", lon="lon", color='Title', text = 'Title', zoom=6)
fig8.update_layout(mapbox_style="open-street-map")

# In[100]:
#Radioknoppen in de sidebar die navigatie over de pagina mogelijk maken. 
pages = st.sidebar.radio('paginas', options=['Home','Laadtijden', 'Kans verkocht auto', 'Aantal verkocht auto', 'Stroom vs Tijd', 'Map', 'Einde'], label_visibility='hidden')

if pages == 'Home':
    st.title("Welkom op het allermooiste dashboard van groep 25!")
elif pages == 'Laadtijden':
    st.plotly_chart(fig)
elif pages == 'Kans verkocht auto':
    st.plotly_chart(fig3)
elif pages == 'Aantal verkocht auto':
    st.plotly_chart(fig4)
elif pages == 'Stroom vs Tijd':
    st.plotly_chart(fig5)
elif pages == 'Map':
    st.plotly_chart(fig8)
elif pages == 'Einde':
    st.title('Bedankt voor het bezoeken!')
    st.header('Groep 25: Edine van Breemen, Jasper Bloem, Martijn de Rooij en Sven Koller.')

# In[ ]:




