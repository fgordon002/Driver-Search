import streamlit as st
import numpy as np
import pandas as pd
from utils import *

#read in the data
@st.cache_data
def load_data():
    max_scores = pd.read_csv("Data/Maxscores_alldrivers_allneurons.csv", index_col=0)
    neuron_metadata = pd.read_csv("Data/neuron_metadata.csv", index_col=0)
    driver_metadata = pd.read_csv("Data/driver_metadata.csv", index_col=0)
    return max_scores, neuron_metadata, driver_metadata

#define the app
def app():

    #load data
    max_scores, neuron_metadata, driver_metadata = load_data()

    # Set the title
    st.title('Driver Search')

    # Text info
    st.markdown('''Welcome to the driver search app! In this app, you can query specific neurons or groups of neurons and get a summary of which Gen1 Gal4 or Vienna Tile drivers 
                they express. You can also get information about where in the genome drivers are inserted and which genes they are linked to.'''
                )

    st.markdown('''The data on this website are sourced from NeuronBridge, which uses an underlying CDM or PPDM algorithm to match connectome skeletons (EM) to light
            microscopy images (LM). This algorithm gives each LM-EM combination a score, based on pixel correlation, representing the strength of the match. 
            NeuronBridge allows for driver search on their website, but not in the same way that this website does. On NeuronBridge, for example, you cannot 
            search for the best driver for a neuron hemilineage, nor can you get aggregate driver information about all neurons of a type. This website aims to display 
            aggregate information about drivers for groups of neurons in a digestible manner, as well as connect driver information to cis-regulatory information.''')

    st.markdown('''As mentioned, the data for this website was sourced from the NeuronBridge backend, but in a specific manner: on NeuronBridge, many multi color flip out (MCFO)
                LM images are taken for each driver with each LM MCFO image labeling a subset of the neurons encompassed by the driver as a whole. The data this website is built 
                on is a condensed version of these data, where each neuron-driver pair is represented by the max score NeuronBridge recorded for that pair among all of its images.
                The process for creating this condensed dataset is outlined below:''')

    # Display Schematic for data collection

    st.image("/Users/finleygordon/Desktop/Lab/Driver_search/score_collection_schematic.jpg", caption="Data Collection Schematic", use_container_width=False)

    st.markdown('''The max score data can be linked to metadata about neurons from the connectome as well as metadata about drivers. The final data structure that 
                this website sources its information from resembles an AnnData or Seurat object, where a cell by feature matrix (max score matrix) is connected to other
                dataframes containing more information about the cells and features.''')

    st.image("/Users/finleygordon/Desktop/Lab/Driver_search/data_schematic.jpg", caption = "Data Structure", use_container_width=True)

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('''You can query these data **here**:''')

    # Add the input section for querying data
    st.markdown('### Query Parameters:')
    
    # User selects how many top drivers to display
    n = st.number_input('Number of drivers to display:', min_value=1, value=5)

    #user selects minimum percent of cells expressing
    percent = st.number_input('Minimum percent of cells with driver score:', min_value=0, max_value= 100, value=0)
    
    # User selects the filter1 field and filter2 values for the query
    filter1 = st.selectbox('Select cell grouping:', ['type', 'cell_class', 'ito_lee_hemilineage', 'fru'])
    
    # Get the unique values for filter1 to help the user choose filter2 values
    filter2_options = neuron_metadata[filter1].unique()
    
    # User selects multiple filter2 values
    filter2 = st.multiselect(f'Select values for {filter1}:', filter2_options)

    # Check if filter2 has been selected
    if filter2:
        # Call the top_drivers function with user inputs
        result_df = top_drivers(n, filter1, filter2, 
                                pct_express = percent,
                                neuron_data = neuron_metadata, 
                                driver_data = driver_metadata, 
                                score_data = max_scores)
        
        # Display the resulting dataframe
        st.write('### Top Drivers DataFrame:')
        st.write(result_df, use_container_width=False)
    else:
        st.warning('Please select at least one filter value to query the data.')

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('''Curious about one of the drivers above?''')

    st.markdown('''Input the driver here to see how the distribution of scores for 
                your group (type, hemilineage, class, etc.) of neurons compares to the distribution of scores for all neurons 
                for the specified driver.''')
    
    select_driver = st.selectbox('Select driver to visualize:', max_scores.drop('bodyID', axis=1).columns)

    if filter2:
        # make comparative histograms
        fig = driver_histogram(select_driver, filter1, filter2, neuron_data=neuron_metadata, score_data=max_scores)
        
        # Display histograms
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f'Please query the data before visualizing score distributions')

    st.markdown('<hr>', unsafe_allow_html=True)

    st.markdown('''If you are more interested in NeuronBridge, how they obtained their data, or what their website offers, you can 
                read about them [here](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-024-05732-7) or 
                access their website [here](https://neuronbridge.janelia.org/).''')
    
    st.markdown('''If you want to know what the expression patterns of any of these drivers look like, you can see this on the 
                [FlyLight website](https://flweb.janelia.org/cgi-bin/flew.cgi).''')

# Run the app
if __name__ == "__main__":
    app()









