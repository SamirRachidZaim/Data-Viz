# Data Science Visuals in Python

A guide to creating professional data science visualizations in Python.

## Essential Libraries

### Core Visualization Libraries
- **Matplotlib**: Low-level plotting library, foundation for most Python visualization
- **Seaborn**: Statistical visualization built on Matplotlib, great for exploratory analysis
- **Plotly**: Interactive, web-based visualizations
- **Altair**: Declarative visualization grammar
- **ggplot2** (via `plotnine`): Grammar of graphics for Python

### Data Manipulation
- **Pandas**: Data manipulation and analysis
- **Polars**: Fast data frames for large datasets
- **NumPy**: Numerical computing

## Installation with UV

```bash
uv pip install matplotlib seaborn plotly altair plotnine pandas polars numpy scipy
```

## Common Visualization Tasks

### 1. Basic Plots with Matplotlib
```python
import matplotlib.pyplot as plt
import numpy as np

# Line plot
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Sine Wave')
plt.show()
```

### 2. Statistical Plots with Seaborn
```python
import seaborn as sns
import pandas as pd

# Load data
df = pd.read_csv('data.csv')

# Distribution plot
sns.histplot(data=df, x='column_name', kde=True)
plt.show()

# Scatter plot with regression line
sns.regplot(data=df, x='x_col', y='y_col')
plt.show()

# Heatmap
sns.heatmap(df.corr(), cmap='coolwarm', annot=True)
plt.show()
```

### 3. Interactive Plots with Plotly
```python
import plotly.express as px
import pandas as pd

df = pd.read_csv('data.csv')

# Scatter plot
fig = px.scatter(df, x='col1', y='col2', color='category',
                 title='Interactive Scatter Plot')
fig.show()

# Bar chart
fig = px.bar(df, x='category', y='value')
fig.show()
```

### 4. Grammar of Graphics with Plotnine
```python
from plotnine import *
import pandas as pd

df = pd.read_csv('data.csv')

(ggplot(df, aes(x='x_col', y='y_col'))
 + geom_point()
 + geom_smooth(method='loess')
 + theme_minimal()
 + labs(title='Visualization'))
```

### 5. Stream/Flow Visualizations

See `ggstream-exploration.py` for comprehensive examples of streamgraphs, stacked area charts, and flow diagrams using Plotly, Matplotlib, and Altair.

## Best Practices

### Design
- Use consistent color palettes (consider colorblind-friendly options)
- Label axes clearly with units
- Use descriptive titles and legends
- Maintain high contrast for readability
- Limit the number of elements per plot
- **Where possible, always show the raw values instead of transformations** to maintain data integrity and transparency
- **Ensure flexibility with figure legends, axes, and titles** to enable customization for different audiences and use cases

### Data Preparation
```python
# Clean and prepare data before plotting
df = df.dropna()  # Remove missing values
df = df[df['column'] > threshold]  # Filter outliers
df = df.sort_values('date')  # Sort temporal data
```

### Styling
```python
# Set style for all plots
sns.set_style("whitegrid")
sns.set_palette("husl")

# Or customize individual plots
plt.figure(figsize=(12, 6))
plt.rcParams['font.size'] = 12
```

### Installation
- **Use UV for package management** whenever possible for faster, more reliable dependency installation and management
```bash
uv pip install matplotlib seaborn plotly altair pandas numpy
```

### Report and Visualization Types
- **Create static reports** (PNG, PDF) for presentations, publications, and archival purposes
- **Create interactive visuals** (HTML, Jupyter notebooks) for exploration, dashboards, and stakeholder engagement
- Choose the appropriate format based on your use case and audience needs

## Saving and Exporting and Exporting Figures
```python
plt.savefig('output.png', dpi=300, bbox_inches='tight')
# For interactive plots with Plotly
fig.write_html('output.html')
```

## Workflow Example

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv('data.csv')

# 2. Explore
print(df.head())
print(df.describe())

# 3. Clean
df = df.dropna()

# 4. Visualize
plt.figure(figsize=(14, 6))

# Subplot 1: Distribution
plt.subplot(1, 2, 1)
sns.histplot(data=df, x='feature', kde=True)

# Subplot 2: Relationship
plt.subplot(1, 2, 2)
sns.scatterplot(data=df, x='feature1', y='feature2', hue='category')

plt.tight_layout()
plt.savefig('analysis.png', dpi=300)
plt.show()
```

## Resources

- [Matplotlib Documentation](https://matplotlib.org)
- [Seaborn Documentation](https://seaborn.pydata.org)
- [Plotly Documentation](https://plotly.com/python)
- [Plotnine Documentation](https://plotnine.readthedocs.io)
- [Color Brewer Palettes](https://colorbrewer2.org)
