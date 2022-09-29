#!/usr/bin/env python
#coding: utf-8


# In[2]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# In[3]:
#deze dataframe komt van kaggle, het bestand is een csv bestand
df = pd.read_csv("womens-world-cup.csv")

# In[4]:
df.head()

# In[6]:
st.title("Womens World Cup 1991 - 2019")

# In[7]:
#adding new column total goals
#Nieuwe kolom gemaakt om aantal doeplunten per WK per land te kunnen bekijken.
df = df.assign(total_goals = df['matches_played']*df['goals_per_90'])
df.set_index('squad')
df.dropna()
#afronden van de totale doelpunten
df = df.round({'total_goals': 0})
df.head(15)

# In[8]:
#alle wedstrijden gespeeld = finale
meeste_wedstrijden= df['matches_played'].max()
print(meeste_wedstrijden)

# In[9]:
st.text('In deze tabladen is te zien welk team welke ronde heeft behaald.') 
st.text('Dit is gebasseerd op de gespeelde wedstrijden per wk.')
st.text('Het laatste tablad bevat de finalisten, troostfinales zijn ook hierin opgenomen.')
#Behaalde rondes
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Poule phase','1/8 finals', '1/4 finals', '1/2 finals', 'Finals'])

with tab1:  
    poule_phase_select= df.loc[df['matches_played'] < 4]
    st.dataframe(poule_phase_select)

with tab2:  
    achtste_finales= df.loc[df['matches_played'] == 4]
    st.dataframe(achtste_finales)
    
with tab3:    
    kwart_finales= df.loc[df['matches_played'] == 5]
    st.dataframe(kwart_finales)
    
with tab4:
    halve_finales= df.loc[df['matches_played'] == 6]
    st.dataframe(halve_finales)
    
with tab5:
    Finales= df.loc[df['matches_played'] == 7]
    st.dataframe(Finales)

# In[10]:
st.text('In deze data zijn twee kolommen toegevoegd: percentage_penalty & total_goals.')
st.text('Hieruit hebben we het volgende gevonden om de data te controleren, Ecuador heeft een penalty % van 100%.')
st.text('Dit is via internet te controleren.')

#Selecting the year
InputYear = st.sidebar.selectbox("Select Year", (1991, 1995, 1999, 2003, 2007, 2011, 2015, 2019))
InputSquad = st.sidebar.selectbox("Select Team", (df.squad.unique()))

Yearselect = (df['year']==InputYear) & (df['squad']== InputSquad)
st.dataframe(Yearselect)

# In[11]:
#Slicing the Age
InputAge = st.sidebar.slider("Select Age", 0, 50, (20, 30))
Ageselect = df[df["age"] == InputAge]
st.dataframe(Ageselect)

# In[12]:
#Gele kaarten
yellowcard = st.sidebar.checkbox('Yellow cards')
if yellowcard:
    numbercards = df['yellow_cards'].count()
    st.metric(label='Yellow cards', value=numbercards)
    
#In[13]:
#rode kaarten
redcard = st.sidebar.checkbox('Red cards')
if redcard:
    numbercardsred = df['red_cards'].count()
    st.metric(label='Red cards', value=numbercardsred)

# In[14]:
#Histogram
st.text('In deze grafiek zijn de totale doelpunten weergegeven.')
st.text('Met de selectbox was het de bedoeling om het jaar te kunnen selecteren.')
#show histogram
Show_histogram = st.sidebar.checkbox('Show histogram')
if Show_histogram:
    dropdown_buttons=[
    {'label': '1991', 'method': 'update',
    'args':[{'Visible': [True, False, False, False, False, False, False, False]},
           {'title':'1991'}]},
    {'label': '1995', 'method': 'update',
    'args':[{'Visible': [False, True, False, False, False, False, False, False]},
           {'title':'1995'}]},
    {'label': '1999', 'method': 'update',
    'args':[{'Visible': [False, False, True, False, False, False, False, False]},
           {'title':'1999'}]},
    {'label': '2003', 'method': 'update',
    'args':[{'Visible': [False, False, False, True, False, False, False, False]},
           {'title':'2003'}]},
    {'label': '2007', 'method': 'update',
    'args':[{'Visible': [False, False, False, False, True, False, False, False]},
           {'title':'2007'}]},
    {'label': '2011', 'method': 'update',
    'args':[{'Visible': [False, False, False, False, False, True, False, False]},
           {'title':'2011'}]},
    {'label': '2015', 'method': 'update',
    'args':[{'Visible': [False, False, False, False, False, False, True, False]},
           {'title':'2015'}]},
    {'label': '2019', 'method': 'update',
    'args':[{'Visible': [False, False, False, False, False, False, False, True]},
           {'title':'2019'}]}
]

for i in df.year.unique():
    df0 = df[df['year']==i]
    fig=px.histogram(df0, x='squad', y='total_goals')

fig.update_layout(
    {'updatemenus':[{'type':'dropdown', 'x':1.3, 'y':0.5, 'showactive': True, 'active': 0, 'buttons': dropdown_buttons}]
})

st.plotly_chart(fig)

fig.show()


# In[15]:

fix = px.histogram(df0, x='squad', y='age', color='squad',
            animation_frame='year')

st.plotly_chart(fig)
fix.show()

# In[16]:
fix = px.histogram(df0, x='squad', y='matches_played', color='squad',
            animation_frame='year')

st.plotly_chart(fig)
fix.show()

st.text('Uit de volgende histogrammen is gebleken dat teams met een lage gemiddelde leeftijd,')
st.text('Minder goede prestaties leveren dan teams met een hogere gemiddelde leeftijd.')

# In[10]:
# In[10]:
# In[10]:
# In[10]:
# In[10]:
# In[10]:
