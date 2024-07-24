#preshypily@gmail.com
import plotly.graph_objects as go
import numpy as np
import random

# Constants
radius = 80.47  # equivalent radius in meters

# Function to convert lat/lon to 3D coordinates
def lat_lon_to_xyz(lat, lon, radius):
    lat_rad = np.deg2rad(lat)
    lon_rad = np.deg2rad(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return x, y, z

# Given areas for each location
areas = {
    "Willow Creek": 7147.23,
    "Newcrest": 4712.58,
    "Oasis Springs": 7147.23,
    "Granite Falls": 2072.32,
    "Magnolia Promenade": 2725.63,
    "Windenburg": 11334.52,
    "San Myshuno": 8493.38,
    "Forgotten Hollow": 1648.66,
    "Brindleton Bay": 5297.26,
    "Selvadorada": 2067.63,
    "Del Sol Valley": 3962.18,
    "Strangerville": 2374.25,
    "Sulani": 3345.12,
    "Glimmerbrook": 1112.15,
    "Britechester": 1904.98,
    "Evergreen Harbor": 2145.89,
    "Mt. Komorebi": 1975.19,
    "Henford-On-Bagley": 2701.91,
    "Taratosa": 1680.15,
    "Moonwood Mill": 1657.63,
    "Copperdale": 2266.54,
    "San Sequoia": 2415.84,
    "Chesnut Ridge": 2125.98
}

# Calculate the dimensions (assuming square lots)
locations = []
for name, area in areas.items():
    side_length = np.sqrt(area)
    locations.append({"name": name, "width": side_length, "height": side_length})

# Distribute corresponding lat/lon values for each location more evenly across the globe
lat_lon_values = [
    (0, 0), (10, 30), (-10, 60), (-20, -30), (30, -60),
    (40, 120), (-30, 150), (-20, -120), (20, -150), (50, -90),
    (-40, 90), (0, -180), (-50, 60), (60, 30), (-60, 0),
    (20, 90), (30, -90), (-10, 120), (10, -120), (-30, -60),
    (40, 60), (-20, 180), (50, -150)
]

for i, (lat, lon) in enumerate(lat_lon_values):
    locations[i]["lat"] = lat
    locations[i]["lon"] = lon

# Generate random colors for each location
colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]) for _ in locations]

# Function to create interpolated points between two lat/lon points
def interpolate_points(lat1, lon1, lat2, lon2, num_points, radius):
    lats = np.linspace(lat1, lat2, num_points)
    lons = np.linspace(lon1, lon2, num_points)
    x_coords, y_coords, z_coords = [], [], []
    for lat, lon in zip(lats, lons):
        x, y, z = lat_lon_to_xyz(lat, lon, radius)
        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)
    return x_coords, y_coords, z_coords

# Create the 3D globe
fig = go.Figure()

# Generate data for a sphere with a gradient blue color
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)
x = radius * np.outer(np.cos(u), np.sin(v))
y = radius * np.outer(np.sin(u), np.sin(v))
z = radius * np.outer(np.ones(np.size(u)), np.cos(v))

# Create a gradient blue color for the globe
colorscale = [
    [0, 'rgb(135, 206, 250)'],  # Light blue
    [1, 'rgb(0, 0, 128)']       # Dark blue
]

# Add the globe surface with the gradient blue color
fig.add_trace(go.Surface(
    x=x, y=y, z=z,
    colorscale=colorscale,
    opacity=0.5,  # Make the globe slightly transparent for better visibility
    showscale=False
))

# Plot each location boundary as filled polygons and add borders
num_interp_points = 10  # Number of interpolation points to approximate curvature
for loc, color in zip(locations, colors):
    lat = loc["lat"]
    lon = loc["lon"]
    width = loc["width"]
    height = loc["height"]
    label = loc["name"]

    # Calculate the boundary coordinates
    lat_upper = lat + (height / 2)
    lat_lower = lat - (height / 2)
    lon_left = lon - (width / 2)
    lon_right = lon + (width / 2)

    # Interpolate the edges
    x_upper, y_upper, z_upper = interpolate_points(lat, lon_left, lat, lon_right, num_interp_points, radius)
    x_lower, y_lower, z_lower = interpolate_points(lat, lon_right, lat, lon_left, num_interp_points, radius)
    x_left, y_left, z_left = interpolate_points(lat_upper, lon, lat_lower, lon, num_interp_points, radius)
    x_right, y_right, z_right = interpolate_points(lat_lower, lon, lat_upper, lon, num_interp_points, radius)

    # Combine the coordinates to form the polygon
    x_coords = x_upper + x_right + x_lower[::-1] + x_left[::-1]
    y_coords = y_upper + y_right + y_lower[::-1] + y_left[::-1]
    z_coords = z_upper + z_right + z_lower[::-1] + z_left[::-1]

    # Plot the filled polygons
    fig.add_trace(go.Mesh3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        color=color,
        opacity=1
    ))

    # Plot the borders
    fig.add_trace(go.Scatter3d(
        x=x_coords,
        y=y_coords,
        z=z_coords,
        mode='lines',
        line=dict(color='white', width=2)
    ))

    # Plot the label at the center
    x_center, y_center, z_center = lat_lon_to_xyz(lat, lon, radius)
    fig.add_trace(go.Scatter3d(
        x=[x_center],
        y=[y_center],
        z=[z_center],
        mode='text',
        text=[label],
        textposition="top center",
        textfont=dict(size=12, color='white')
    ))

# Set plot limits, remove the legend, and make the background transparent
fig.update_layout(
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor='rgba(0,0,0,0)'  # Set the scene background to be transparent
    ),
    showlegend=False,  # Disable the legend
    paper_bgcolor='rgba(0,0,0,0)',  # Set the paper background to be transparent
    margin=dict(l=0, r=0, b=0, t=0),
    scene_camera=dict(
        eye=dict(x=0.8, y=0.8, z=0.8)  # Adjust these values to set the initial zoom level
    )
)

# Save the figure as an HTML file
fig.write_html("static/sims4_worlds_globe.html")


class Sims4Globe:
    def __init__(self):
        # Initialize globe data
        self.world_locations = {
            loc["name"]: {'x': loc["lat"], 'y': loc["lon"], 'z': loc["height"]} for loc in locations
        }


    def get_location(self, world_name, x, y, z):
        # Logic to find and map the coordinates to a location
        if world_name in self.world_locations:
            base_location = self.world_locations[world_name]
            # Example mapping logic, modify as needed
            mapped_location = {
                "latitude": base_location["x"],
                "longitude": base_location["y"],
                "altitude": base_location["z"]
            }
            return mapped_location
        else:
            raise ValueError(f"World '{world_name}' not found.")

