def plot_doughnut_chart(data, inner_radius=0.3, outer_radius=0.7, title=None):
    import numpy as np
    import matplotlib.pyplot as plt

    # Prepare data
    labels = data['labels']
    sizes = data['sizes']
    colors = data.get('colors', None)

    # Create a figure and a set of subplots
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(aspect="equal"))

    # Create the doughnut chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, startangle=90,
                                       counterclock=False, wedgeprops=dict(width=outer_radius-inner_radius))

    # Draw a circle at the center of the doughnut
    centre_circle = plt.Circle((0, 0), inner_radius, color='white', fc='white', linewidth=0)
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    # Title
    if title:
        plt.title(title, fontsize=16)

    # Show percentage on the wedges
    plt.setp(autotexts, size=10, weight="bold", color="white")
    
    # Display the chart
    plt.tight_layout()
    plt.show()

    return fig, ax

def save_doughnut_chart(data, save_path, inner_radius=0.3, outer_radius=0.7, title=None):
    fig, ax = plot_doughnut_chart(data, inner_radius, outer_radius, title)
    fig.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close(fig)