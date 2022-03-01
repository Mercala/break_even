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


# Variables --------------------------------------------------------------------
variables = {
    "investment": {
        "text": "Total investment (in Afl.)",
        "value": 200_000,
    },
    "depreciation": {
        "text": "Depreciation schedule (in years)",
        "value": 10
    },
    "sales_price": {
        "text": "Sales price per Liter (in Afl.)",
        "value": 1.30,
    },
    "total_costs": {
        "text": "Total costs per Liter (in Afl.)",
        "value": 0.99,
    },
    "down_payment": {
        "text": "Down payment (in Afl.)",
        "value": 60_000,
        "help": "Usually 25% - 30%"
    },
    "interest_rate": {
        "text": "Interest rate (APR)",
        "value": 5.00,
        "help": "Enter the Annual Percentage Rate on the loan."
    },
    "unit_quantity": {
        "text": "Average quantity per week (in Liters)",
        "value": 60,
        "help": "Enter an estimate of how many liters a vehicle will tank per week."
    }
}

# Investment
variables['investment']['value']    = st.sidebar.number_input(variables['investment']['text'], value=variables['investment']['value'], step=25_000)
# Depreciation Schedule
variables['depreciation']['value']  = st.sidebar.number_input(variables['depreciation']['text'], value=variables['depreciation']['value'])
# Sales Price
variables['sales_price']['value']   = st.sidebar.number_input(variables['sales_price']['text'], value=variables['sales_price']['value'], step=0.01)
# Total Costs
variables['total_costs']['value']   = st.sidebar.number_input(variables['total_costs']['text'], value=variables['total_costs']['value'], step=0.01)
# Downpayment
variables['down_payment']['value']  = st.sidebar.number_input(variables['down_payment']['text'], value=variables['down_payment']['value'], step=5_000, help=variables['down_payment']['help'])
# Interest Rate
variables['interest_rate']['value'] = st.sidebar.number_input(variables['interest_rate']['text'], value=variables['interest_rate']['value'], step=0.01, help=variables['interest_rate']['help'])
# Units
variables['unit_quantity']['value'] = st.sidebar.number_input(variables['unit_quantity']['text'], value=variables['unit_quantity']['value'], step=1, help=variables['unit_quantity']['help'])





# Graph
def plot(dct):

    # Computations ----------------------------------------------------------- #
    # Total Principal
    principal = variables['investment']['value'] - variables['down_payment']['value']
    # Total Interest
    interest = (principal * (1 + variables['interest_rate']['value'] / 100 / 12) ** (variables['depreciation']['value'] * 12)) - principal
    # Total Depreciation per year
    total_depr_per_year = (principal + interest) / variables['depreciation']['value']
    # Quantity per year
    total_sales_per_year = variables['sales_price']['value'] * variables['unit_quantity']['value'] * 52
    # Total Cost per year
    total_cost_per_year = variables['total_costs']['value'] * variables['unit_quantity']['value'] * 52
    # Break Even
    break_even = total_depr_per_year / (total_sales_per_year - total_cost_per_year)
    # ------------------------------------------------------------------------ #

    fig, ax = plt.subplots(figsize=(16, 8))

    x = np.linspace(0, break_even + break_even)
    y1 = (total_cost_per_year * x) + total_depr_per_year
    y2 = total_sales_per_year * x

    ax.fill_between(x,
                    y1,
                    y2,
                    where=y1 >= y2,
                    color=color4,
                    interpolate=True)

    ax.fill_between(x,
                    y1,
                    y2,
                    where=y1 < y2,
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
        xy=(break_even, (total_cost_per_year * break_even) + total_depr_per_year),
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
st.pyplot(plot(variables))
