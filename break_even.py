import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Color Pallette
color1 = '#0C04B4'
color2 = '#606D5D'
color3 = '#FFFFFF'
color4 = '#D00000'
color5 = '#adaeae'

# Fontsize
h1 = 24
h2 = 20
h3 = 16

fontname = 'monospace'

# Investment
fixed_costs = st.sidebar.number_input("Total investment (in Afl.)", value=150_000, step=10_000)
# Depreciation schedule
years = st.sidebar.number_input("Depreciation schedule (in years)", value=10)

# Price
sales_price = st.sidebar.number_input("Sales price (in Afl.)", step=0.01, value=1.3)
# COGS
cogs = st.sidebar.number_input("COGS per Liter (in Afl.)", step=0.01, value=.99)
# Liters
avg_tank = st.sidebar.number_input("Average fill up Week (in Liters)", step=1, value=60)

# Formulas
fixed_cost_per_year = fixed_costs / years
total_sales_price_per_year = sales_price * avg_tank * 52
cogs_per_year = cogs * avg_tank * 52

# Break Even
break_even = fixed_cost_per_year / (total_sales_price_per_year - cogs_per_year)

# Graph
def plot(break_even, cogs_per_year, fixed_cost_per_year, total_sales_price_per_year):
    fig, ax = plt.subplots(figsize=(16, 8))

    a = np.linspace(0, break_even + break_even)
    b = (cogs_per_year * a) + fixed_cost_per_year
    c = total_sales_price_per_year * a

    ax.fill_between(a,
                    b,
                    c,
                    where=b >= c,
                    color=color4,
                    interpolate=True)

    ax.fill_between(a,
                    b,
                    c,
                    where=b < c,
                    color=color5,
                    interpolate=True)


    # Titles
    fig.suptitle("LPG Fueling system, Yearly Break-Even",
                 fontsize=h1,
                 fontweight='bold',
                 x=0.125,
                 ha='left',
                 fontname='monospace'
                )

    ax.set_title("in Vehicles",
                 fontdict={
                     'fontsize': h2,
                     'verticalalignment': 'baseline',
                     'horizontalalignment': 'left'
                 },
                 loc='left',
                 fontname='monospace'
                )

    # Set Grid lines
    ax.yaxis.grid(linestyle='--')

    # Set Fontsize Labels
    ax.tick_params(labelsize=h3)

    # Hide Spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)


    ax.set_yticks(ax.get_yticks().tolist()[1:-1])
    ax.set_yticklabels([f"{y:,.0f}" for y in ax.get_yticks()])

    ax.set_ylabel('Total costs (Afl.)', size=h3)
    ax.set_xlabel('Vehicles', size=h3)

    ax.annotate(text=f"{break_even:,.1f} vehicles",
        xy=(break_even, (cogs_per_year * break_even) + fixed_cost_per_year),
        xytext=(-10, -50),
        xycoords='data',
        textcoords='offset points',
        color=color1,
        fontsize=h3,
        fontweight='bold',
        fontname=fontname,
        arrowprops= {'arrowstyle': '->', 'lw': 1.5, 'color': 'black'}
    )


    return fig

st.write("### Change the parameters in the sidebar to see how it affects the Break-even-point")
st.write('')
st.write('')
st.write('')
st.pyplot(plot(break_even, cogs_per_year, fixed_cost_per_year, total_sales_price_per_year))
