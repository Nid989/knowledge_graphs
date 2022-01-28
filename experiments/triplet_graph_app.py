from streamlit_agraph import agraph, Config, TripleStore
import streamlit as st
import pandas as pd

store = TripleStore()

# Read dataset (CSV)
df = pd.read_csv('Pyvis-Network-Graph-Streamlit\data\data_v2.csv')

# Set header title
st.title('Network Graph Visualization of Collegium Knowledge Graphs')

# # Define list of selection options and sort alphabetically
entity_list = ['relation_VERB', 'relation_ADP', 'relation_ADV', 'relation_AUX']
entity_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
selected_item = st.multiselect('Select a field to start with', entity_list)

# Set info message on initial site load
if len(selected_item) == 0:
       st.text('Choose at least 1 drug to get started')

# Create network graph when user selects >= 1 item
else:
       df_select = df[df[selected_item[0]] == 1][['source', 'weight', 'target']]
       
       # df_select = df.loc[df.columns.tolist.isin(selected_item) | df.columns.tolist.isin(selected_item)][['source', 'relation', 'target']]
       df_select = df_select.reset_index(drop=True)
       
       nodes, edges = [], []

       if len(selected_item) == 1:
              sample_df = df[df[selected_item[0]] == 1]
       elif len(selected_item) == 2:
              sample_df = df[(df[selected_item[0]] == 1) | (df[selected_item[1]] == 1)]
              sample_df = sample_df[~sample_df.duplicated()]
       elif len(selected_item) == 3:
              sample_df = df[(df[selected_item[0]] == 1) | (df[selected_item[1]] == 1) | (df[selected_item[2]] == 1)]
              sample_df = sample_df[~sample_df.duplicated()]
       elif len(selected_item) == 4:
              sample_df = df[(df[selected_item[0]] == 1) | (df[selected_item[1]] == 1) | (df[selected_item[2]] == 1) | (df[selected_item[3]] == 1)]
              sample_df = sample_df[~sample_df.duplicated()]

       sample_df = sample_df[['source', 'relation', 'target']]

       for _, row in sample_df.iterrows():
              source, relation, target = row['source'], row['relation'], row['target']
              store.add_triple(source, relation, target, "")

       config = Config(
              width=1000, 
              height=800, 
              directed=True,
              nodeHighlightBehavior=True, 
              highlightColor="#F7A7A6", # or "blue"
              collapsible=True,
              node={'labelProperty':'label', "color": "lightgreen"},
              link={'labelProperty': 'label', 'renderLabel': True},
              # **kwargs e.g. node_size=1000 or node_color="blue"
              ) 

       return_value = agraph(list(store.getNodes()), list(store.getEdges()), config)