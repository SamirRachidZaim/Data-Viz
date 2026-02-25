import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import altair as alt


# ============================================================================
# DATA GENERATION FUNCTIONS
# ============================================================================

def generate_time_series_data(num_periods=50, num_categories=4, seed=42):
    """
    Generate sample time series data with multiple categories.
    
    Parameters:
    -----------
    num_periods : int
        Number of time periods
    num_categories : int
        Number of categories to generate
    seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with Date column and category columns
    """
    np.random.seed(seed)
    dates = pd.date_range('2023-01-01', periods=num_periods)
    
    data = {'Date': dates}
    for i in range(num_categories):
        cat_name = f'Category_{chr(65+i)}'  # A, B, C, D, etc.
        data[cat_name] = np.random.randint(10, 150, num_periods)
    
    return pd.DataFrame(data)


def generate_sales_data(num_months=12, num_products=3, seed=42):
    """
    Generate sample product sales data.
    
    Parameters:
    -----------
    num_months : int
        Number of months of data
    num_products : int
        Number of products
    seed : int
        Random seed for reproducibility
        
    Returns:
    --------
    pd.DataFrame
        DataFrame with Date and product sales columns
    """
    np.random.seed(seed)
    dates = pd.date_range('2023-01-01', periods=num_months, freq='MS')
    
    data = {'Date': dates}
    for i in range(num_products):
        prod_name = f'Product_{chr(65+i)}'
        data[prod_name] = np.random.randint(100, 600, num_months)
    
    return pd.DataFrame(data)


# ============================================================================
# STREAM/FLOW VISUALIZATION FUNCTIONS
# ============================================================================

def create_plotly_streamgraph(df, title='Streamgraph'):
    """
    Create an interactive streamgraph using Plotly.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with Date column and value columns
    title : str
        Title of the visualization
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive Plotly figure
    """
    fig = go.Figure()
    
    # Get all columns except Date
    value_cols = [col for col in df.columns if col != 'Date']
    
    for col in value_cols:
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df[col],
            mode='lines',
            name=col,
            stackgroup='one',  # Creates the streamgraph effect
            fillcolor=f'rgba({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)}, 0.7)'
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Date',
        yaxis_title='Value',
        hovermode='x unified',
        height=500,
        template='plotly_white'
    )
    
    return fig


def create_stacked_area_chart(df, title='Stacked Area Chart'):
    """
    Create a stacked area chart using Matplotlib.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame with Date column and value columns (with Date as index or first column)
    title : str
        Title of the visualization
        
    Returns:
    --------
    matplotlib.figure.Figure
        Matplotlib figure object
    """
    # Set date as index if not already
    if 'Date' in df.columns:
        df_indexed = df.set_index('Date')
    else:
        df_indexed = df
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Get all columns
    columns = df_indexed.columns.tolist()
    values = [df_indexed[col].values for col in columns]
    
    ax.stackplot(range(len(df_indexed)), *values, labels=columns, alpha=0.7)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Value')
    ax.set_title(title)
    ax.legend(loc='upper left')
    ax.set_xticks(range(0, len(df_indexed), max(1, len(df_indexed)//5)))
    ax.set_xticklabels([df_indexed.index[i].strftime('%Y-%m') for i in range(0, len(df_indexed), max(1, len(df_indexed)//5))], rotation=45)
    
    plt.tight_layout()
    return fig


def create_altair_streamgraph(df, title='Stream-style Area Chart'):
    """
    Create a declarative streamgraph using Altair.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Long-format DataFrame with Date, Category, and Value columns
    title : str
        Title of the visualization
        
    Returns:
    --------
    altair.Chart
        Altair chart object
    """
    chart = alt.Chart(df).mark_area().encode(
        x='Date:T',
        y='Value:Q',
        color='Category:N',
        opacity=alt.value(0.7),
        tooltip=['Date:T', 'Category:N', 'Value:Q']
    ).properties(
        width=800,
        height=400,
        title=title
    ).interactive()
    
    return chart


def create_sankey_flow(categories, flows, values, title='Flow Diagram'):
    """
    Create a Sankey diagram for flow visualization.
    
    Parameters:
    -----------
    categories : list
        List of all node labels
    flows : list of tuples
        List of (source_idx, target_idx) pairs
    values : list
        List of flow values
    title : str
        Title of the visualization
        
    Returns:
    --------
    plotly.graph_objects.Figure
        Interactive Plotly Sankey figure
    """
    sources = [flow[0] for flow in flows]
    targets = [flow[1] for flow in flows]
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color='black', width=0.5),
            label=categories,
            color=['blue' if i < 3 else 'green' if 'Sales' in categories[i] else 'red' if 'Returns' in categories[i] else 'orange' 
                   for i in range(len(categories))]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values
        )
    )])
    
    fig.update_layout(
        title=title,
        font=dict(size=12),
        height=500
    )
    
    return fig


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    print("Generating sample data...")
    
    # Generate time series data
    ts_data = generate_time_series_data(num_periods=50, num_categories=4)
    print("Time series data shape:", ts_data.shape)
    print(ts_data.head())
    
    # Generate sales data
    sales_data = generate_sales_data(num_months=12, num_products=3)
    print("\nSales data shape:", sales_data.shape)
    print(sales_data.head())
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # 1. Plotly Streamgraph
    print("1. Creating Plotly streamgraph...")
    streamgraph = create_plotly_streamgraph(ts_data, title='Time Series Streamgraph')
    streamgraph.show()
    
    # 2. Matplotlib Stacked Area Chart
    print("2. Creating Matplotlib stacked area chart...")
    stacked_area = create_stacked_area_chart(sales_data, title='Sales Over Time - Stacked Area')
    plt.show()
    
    # 3. Altair Streamgraph (long format data needed)
    print("3. Creating Altair streamgraph...")
    ts_long = ts_data.melt(id_vars=['Date'], var_name='Category', value_name='Value')
    altair_chart = create_altair_streamgraph(ts_long, title='Altair Stream Visualization')
    altair_chart.show()
    
    # 4. Sankey Flow Diagram
    print("4. Creating Sankey flow diagram...")
    categories = ['Product A', 'Product B', 'Product C', 'Sales', 'Returns', 'Inventory']
    flows = [(0, 3), (1, 3), (2, 3), (3, 5), (3, 4)]
    values = [100, 150, 120, 370, 30]
    sankey = create_sankey_flow(categories, flows, values, title='Product Flow - Sales to Inventory')
    sankey.show()
    
    print("\nVisualization examples complete!")
