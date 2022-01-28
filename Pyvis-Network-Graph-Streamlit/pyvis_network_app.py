import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

# Read dataset (CSV)
df = pd.read_csv('data\data_v2.csv')

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
    
    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'source', 'target', 'weight')

    # Initiate PyVis network object
    KG_net = Network(
        height='400px',
        width="100%",
        bgcolor='#222222', 
        font_color='white'
        )

    # Take Networkx graph and translate it to a PyVis graph format
    KG_net.from_nx(G)

    # Generate network with specific layout settings
    KG_net.repulsion(
        node_distance=420, 
        central_gravity=0.33,
        spring_length=110, 
        spring_strength=0.10,
        damping=0.95
        )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        KG_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = "C:\\Users\\nidbh\\Desktop\\Textify.ai\\Knowledge_graphs\\Pyvis-Network-Graph-Streamlit\\html_files"
        KG_net.save_graph(f'{path}\\pyvis_graph.html')
        HtmlFile = open(f'{path}\\pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)