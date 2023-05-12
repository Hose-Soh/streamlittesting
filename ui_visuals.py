import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

'''
    Contains  set of functions that generate visualisations used in the applicaiton
'''

# Definition of a function to attach a label to each bar.
def autolabel_soil_prop(ax, rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate(
            "{}".format(height) + "%",
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # 3 points vertical offset.
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
        )

def generate_pr_pet_rech_graph(recharge_df):
    '''
    Generates a line graph comparing Precipitation, Potential Evapotranspiration and Groundwater Recharge over time from a dataframe
    The recharge_df must contain the columns "pr", "pet", "rech" 
    '''
    # Data visualization in the form of line.
    fig, ax = plt.subplots(figsize=(15, 6))

    # Title of the plot.
    ax.set_title(
        "Comparison of Precipitation, Potential Evapotranspiration, Groundwater Recharge",
        fontsize=14,
    )

    # Barplot associated with precipitation.
    recharge_df["pr"].plot(kind="line", ax=ax, label="precipitation")

    # Barplot associated with potential evapotranspiration.
    recharge_df["pet"].plot(
        kind="line", ax=ax, label="potential evapotranspiration", color="orange"
    )

    # Barplot associated with groundwater recharge
    recharge_df["rech"].plot(kind="line", ax=ax, label="recharge", color="green")

    # Add a legend.
    ax.legend(loc='upper right')

    # Define x/y-labels properties.
    ax.set_ylabel("Intensity [mm]")
    ax.set_xlabel(None)

    # Define the date format and shape of x-labels.
    x_labels = recharge_df.index.strftime("%m-%Y")
    ax.set_xticklabels(x_labels, rotation=90, fontsize=10)

    return fig


def generate_pr_pet_graph(meteo_df):
    # Data visualization
    fig, ax = plt.subplots(figsize=(15, 6))

    # Title of the plot.
    ax.set_title(
        "Comparison of Precipitation and Potential Evapotranspiration", fontsize=14
    )

    # Barplot associated with precipitations.
    meteo_df["pr"].plot(kind="line", ax=ax, label="precipitation")

    # Barplot associated with potential evapotranspiration.
    meteo_df["pet"].plot(
        kind="line", ax=ax, label="potential evapotranspiration", color="orange", alpha=0.5
    )

    # Add a legend.
    ax.legend(loc='upper right')

    # Add some x/y-labels properties.
    ax.set_ylabel("Intensity [mm]")
    ax.set_xlabel(None)

    # Define the date format and shape of x-labels.
    x_labels = meteo_df.index.strftime("%m-%Y")
    ax.set_xticklabels(x_labels, rotation=90, fontsize=10)

    return fig

def generate_hydraulic_props_chart(profile_wp, profile_fc, olm_bands, olm_depths):
    fig, ax = plt.subplots(figsize=(15, 6))
    ax.axes.get_yaxis().set_visible(False)

    # Definition of the label locations.
    x = np.arange(len(olm_bands))

    # Width of the bar of the barplot.
    width = 0.25

    # Barplot associated with the water content at the wilting point.
    rect1 = ax.bar(
        x - width / 2,
        [round(profile_wp[b] * 100, 2) for b in olm_bands],
        width,
        label="Water content at wilting point",
        color="red",
        alpha=0.5,
    )

    # Barplot associated with the water content at the field capacity.
    rect2 = ax.bar(
        x + width / 2,
        [round(profile_fc[b] * 100, 2) for b in olm_bands],
        width,
        label="Water content at field capacity",
        color="blue",
        alpha=0.5,
    )

    # Add Labels on top of bars.
    autolabel_soil_prop(ax, rect1)
    autolabel_soil_prop(ax, rect2)

    # Title of the plot.
    ax.set_title("Hydraulic properties of the soil at different depths", fontsize=14)

    # Properties of x/y labels and ticks.
    ax.set_xticks(x)
    x_labels = [str(d) + " cm" for d in olm_depths]
    ax.set_xticklabels(x_labels, rotation=45, fontsize=10)

    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)

    # Shrink current axis's height by 10% on the bottom.
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

    # Put a legend below current axis.
    ax.legend(
        loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=2
    )

    return fig

def generate(profile_sand, profile_clay, profile_orgc, olm_bands, olm_depths):
    # Create the plot
    fig = go

    # Bar plot representing the sand content profile
    fig.add_trace(go.Bar(
        x=list(profile_sand.keys()),
        y=[round(100 * s, 2) for s in profile_sand.values()],
        name='Sand',
        marker_color='#ecebbd'
    ))

    # Bar plot representing the clay content profile
    fig.add_trace(go.Bar(
        x=list(profile_clay.keys()),
        y=[round(100 * c, 2) for c in profile_clay.values()],
        name='Clay',
        marker_color='#6f6c5d'
    ))

    # Bar plot representing the organic carbon content profile
    fig.add_trace(go.Bar(
        x=list(profile_orgc.keys()),
        y=[round(100 * o, 2) for o in profile_orgc.values()],
        name='Organic Carbon',
        marker_color='black',
        opacity=0.75
    ))

    # Update layout
    fig.update_layout(
        title="Properties of the soil at different depths (mass content)",
        xaxis_title="Depth",
        yaxis_title="Content (%)",
        xaxis_tickangle=-45,
        showlegend=True,
        legend=dict(x=0.5, y=-0.15, xanchor='center', yanchor='top', orientation='h'),
        barmode='group'
    )


    return fig