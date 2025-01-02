import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def top_drivers(n, filter1, filter2, pct_express, neuron_data, driver_data, score_data): 

    #isolate the relevant body ids
    bodyids = pd.Series(
    neuron_data[neuron_data[filter1].isin(filter2)]
    ['hemibrain_id']
    )  

    #get top n mean driver scores for set of ids
    mean_df = pd.DataFrame(
    score_data[score_data['bodyID'].isin(bodyids)]
    .drop('bodyID', axis = 1)
    .mean()
    .sort_values(ascending=False)
    )

    #get percent expressing 
    pct_expressing = pd.DataFrame(
        score_data[score_data['bodyID'].isin(bodyids)]
        .drop('bodyID', axis = 1)
        .notna()
        .mean() 
        .sort_values(ascending=False)
    ) * 100

    #merge dfs
    merged_df = (
        mean_df.merge(pct_expressing, how = 'left', left_index=True, right_index=True)
        .merge(driver_data, how = 'left', left_index=True, right_on='driver_line')
        .reset_index()
        .drop(['index', 'X5', 'X6'], axis=1)
        .rename(columns = {'0_x': 'Average score', 
                 '0_y': 'Percent cells with score', 
                 'chromosome': 'Chromosome', 
                 'start': 'Start', 
                 'stop': 'Stop', 
                 'driver_line': 'Driver', 
                 'gene': 'Gene'})
        [['Driver', 'Average score', 'Percent cells with score', 'Gene', 'Chromosome', 'Start', 'Stop']]
    )

    if pct_express:
        merged_df = merged_df[merged_df['Percent cells with score'] >= pct_express]

    return merged_df.head(n)

def driver_histogram(driver, filter1, filter2, neuron_data, score_data): 

    #isolate the relevant body ids
    bodyids = pd.Series(
    neuron_data[neuron_data[filter1].isin(filter2)]
    ['hemibrain_id']
    )  

    #driver score df for body ids of interest
    select_cells_df = (
        score_data[score_data['bodyID'].isin(bodyids)]
        [driver]
    )

    #driver score df for rest of cells
    rest_cells_df = (
        score_data[~score_data['bodyID'].isin(bodyids)]
        [driver]
    )

    #
    filter2_formatted = ", ".join([item.replace('_', ' ') for item in filter2])

    #define figure 
    fig = make_subplots(
        rows = 1, cols = 2, 
        subplot_titles = (f'{driver} scores for all {filter2_formatted} cells', 
                          f'{driver} scores for all non {filter2_formatted} cells')
    )

    #first histogram trace (left plot)
    trace1 = go.Histogram(
        x = select_cells_df, 
        opacity= 0.5, 
        nbinsx = 50,
        name = f'{driver} scores for {filter2_formatted}',
        marker=dict(color = 'blue'), 
    )

    #second histogram trace (right plot)
    trace2 = go.Histogram(
        x = rest_cells_df, 
        opacity= 0.5, 
        nbinsx = 50,
        name = f'{driver} scores for all non {filter2_formatted} cells',
        marker=dict(color = 'red'), 
    )

    #add traces to subplots
    fig.add_trace(trace1, row = 1, col = 1)
    fig.add_trace(trace2, row = 1, col = 2)

    #update layout
    fig.update_layout(
        title=f"Side by side histograms for {driver} scores",
        showlegend=False,
        xaxis=dict(title=f'{driver} scores for {filter2_formatted} cells', 
                   range = [0, 50000]),
        yaxis=dict(title='Frequency'),
        xaxis2=dict(title=f'{driver} scores for non {filter2_formatted} cells', 
                    range =  [0, 50000]),
        yaxis2=dict(title='Frequency'), 
        font=dict(size=14),
        legend = dict(font = dict(size = 10))
    )

    return fig
