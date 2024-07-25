#preshypily@gmail.com
from flask import Flask, request, render_template, Response, url_for, send_from_directory
from dash import Dash, dcc, html, Input, Output
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = "browser"
from main import CreateLegacyChallenge, SimNatalChart
from sims4_globe import Sims4Globe

app = Flask(__name__)

# Create the Dash app instance
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Define the Dash app's layout (includes the chart)
dash_app.layout = html.Div([
    dcc.Graph(id='natal-chart'),
])

chart_data = None
results_data = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global chart_data, results_data
    if request.method == 'POST':
        sim_age = int(request.form['sim_age'])
        sim_year_days = int(request.form['sim_year_days'])
        sim_season_days = int(request.form['sim_season_days'])
        birth_location = request.form['birth_location']
        coordinates = request.form['coordinates']
        if coordinates:
            try:
                x, y, z = map(float, coordinates.split(','))
            except ValueError:
                x, y, z = 0.0, 0.0, 0.0  # Default coordinates if not provided or invalid
        else:
            x, y, z = 0.0, 0.0, 0.0  # Default coordinates if not provided
        
        current_sim_day = int(request.form['current_sim_day'])
        
        sims4_globe = Sims4Globe()
        location = sims4_globe.get_location(birth_location, x, y, z)

        natal_chart = SimNatalChart(sim_age, location, current_sim_day, sim_year_days, sim_season_days)
        generated_chart = natal_chart.generate_natal_chart()

        #print(generated_chart['planetary_positions'])
        
        legacychallenge = CreateLegacyChallenge(generated_chart['planetary_positions'])
        traits_set, aspirations_set, careers_set, final_best_skills, final_worst_skills, seen_rules = legacychallenge.filter_natal_chart()

        # Prepare data for the dashboard
        chart_data = create_natal_chart(generated_chart['planetary_positions'])
        results_data = {
            "Traits": traits_set,
            "Aspirations": aspirations_set,
            "Careers": careers_set,
            "Best_Skills": final_best_skills,
            "Worst_Skills": final_worst_skills,
            "Rules": seen_rules,
            "Natal_Chart": {
                    "formatted_birthdate": generated_chart["formatted_birthdate"]
                }
            }
        return render_template('index.html', results=results_data)
    else:
        chart_data = None
        results_data = None
    return render_template('index.html')

@app.route('/health')
def health():
    return 'OK', 200

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml dynamically."""
    pages = []
    ten_days_ago = (datetime.now() - timedelta(days=10)).date().isoformat()

    # Static pages
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            url = url_for(rule.endpoint, _external=True)
            pages.append([url, ten_days_ago])

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = Response(sitemap_xml, mimetype='application/xml')
    return response

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')

@dash_app.callback(
    Output('natal-chart', 'figure'),
    Input('natal-chart', 'id')
)

def update_chart(_):
    return chart_data if chart_data else go.Figure()

def create_natal_chart(natal_chart):
    #print(natal_chart)
    # Element colors
    element_colors = {
        "Wood": "burlywood",
        "Fire": "red",
        "Earth": "green",
        "Metal": "lavender",
        "Water": "mediumaquamarine",
        "Air": "darkslategrey"
    }

    # Zodiac to element mapping
    zodiac_elements = {
        "Aries": "Wood",
        "Taurus": "Earth",
        "Gemini": "Air",
        "Cancer": "Water",
        "Leo": "Fire",
        "Virgo": "Earth",
        "Libra": "Air",
        "Scorpio": "Metal",
        "Sagittarius": "Fire",
        "Capricorn": "Earth",
        "Aquarius": "Air",
        "Pisces": "Water"
    }

    planets = list(natal_chart.keys())

    exclude_planets = ["midheaven", "ic", "ascendant", "descendant"]
    planets = [planet for planet in planets if planet not in exclude_planets]

    # Calculate the angles based on the house number and sign position
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
        "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    angles = []
    for planet in planets:
        house = natal_chart[planet]['house']
        sign_index = zodiac_signs.index(natal_chart[planet]['sign'])
        angle = ((house - 1) * 30 + sign_index * 30 / 12) % 360
        angles.append(angle)

    # Correcting specific planets based on observed errors
    def correct_angle(planet, correction):
        index = planets.index(planet)
        angles[index] = (angles[index] + correction) % 360

    # Apply corrections for specific planets
    correct_angle('jupiter', -15)
    correct_angle('saturn', -15)
    correct_angle('neptune', -15)
    correct_angle('north_node', -15)
    correct_angle('fortune', -15)
    correct_angle('vertex', -20)
    correct_angle('pluto', -15)

    fig = go.Figure()



    # Offset for overlapping planets
    offset_radius = 0.04
    adjusted_angles = []
    seen_angles = {}

    for angle in angles:
        if angle in seen_angles:
            seen_angles[angle] += 1
            adjusted_angle = angle + seen_angles[angle] * (360 / len(planets))
        else:
            seen_angles[angle] = 0
            adjusted_angle = angle
        adjusted_angles.append(adjusted_angle)

    adjusted_radii = [1 + seen_angles[angle] * offset_radius for angle in angles]


    # Matching colors for each planet
    planet_colors_map = {
        "pluto": "black",
        "moon": "white",
        "mars": "red",
        "sun": "yellow",
        "uranus": "blue",
        "venus": "green",
        "jupiter": "orange",
        "neptune": "violet",
        "saturn": "grey",
        "mercury": "brown",
        "north_node": "darkslateblue",
        "south_node": "darksalmon",
        "vertex": "mediumaquamarine",
        "chiron": "darkgrey",
        "lilith": "hotpink",
        "fortune": "mintcream"
    }
    planet_colors = [planet_colors_map[planet] for planet in planets]

    # Adding the planets
    for planet, angle, radius in zip(planets, adjusted_angles, adjusted_radii):
        if planet not in ["mc", "ic", "ascendant", "descendant"]:
            sign = natal_chart[planet]['sign']
            element = zodiac_elements[sign]
            border_color = element_colors[element]

            fig.add_trace(go.Scatterpolar(
                r=[radius],
                theta=[angle],
                mode='markers',
                marker=dict(size=15, color=planet_colors_map[planet], line=dict(color=border_color, width=2)),
                hoverinfo='text',
                text=[f"{planet.capitalize()}: {sign} {natal_chart[planet]['house']}"],
                showlegend=True,
                name=f"{planet.capitalize()} ({sign} {natal_chart[planet]['house']})"
            ))

    fig.add_trace(go.Scatterpolar(
        r=adjusted_radii,
        theta=adjusted_angles,
        mode='text',
        text=planets,
        textposition='top center',
        textfont=dict(color='rgba(0,0,0,0)'),
        hoverinfo='none',
        showlegend=False
    ))

    # Adding the zodiac signs
    zodiac_signs = [
        "Pisces", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius"
    ]

    for i, sign in enumerate(zodiac_signs):
        angle = (i * 30 + 15) % 360
        fig.add_trace(go.Scatterpolar(
            r=[1.2],
            theta=[angle],
            mode='text',
            text=sign,
            textposition='middle center',
            hoverinfo='none',
            showlegend=False
        ))

    # Adding the house numbers
    house_angles = [(i * 30 + 15) % 360 for i in range(12)]
    house_numbers = list(range(1, 13))

    for angle, house in zip(house_angles, house_numbers):
        fig.add_trace(go.Scatterpolar(
            r=[0.3],
            theta=[angle],
            mode='text',
            text=[f"{house}"],
            textposition='middle center',
            hoverinfo='none',
            showlegend=False
        ))

    # Adding MC, IC, Ascendant, and Descendant lines and legends
    mc_sign = natal_chart["midheaven"]['sign']
    ic_sign = natal_chart["ic"]['sign']
    asc_sign = natal_chart["ascendant"]['sign']
    dc_sign = natal_chart["descendant"]['sign']

    mc_color = element_colors[zodiac_elements[mc_sign]]
    ic_color = element_colors[zodiac_elements[ic_sign]]
    asc_color = element_colors[zodiac_elements[asc_sign]]
    dc_color = element_colors[zodiac_elements[dc_sign]]

    mc_angle = (natal_chart["midheaven"]['house'] - 1) * 30 + (zodiac_signs.index(mc_sign) * 30) / 12
    ic_angle = (natal_chart["ic"]['house'] - 1) * 30 + (zodiac_signs.index(ic_sign) * 30) / 12
    asc_angle = (natal_chart["ascendant"]['house'] - 1) * 30 + (zodiac_signs.index(asc_sign) * 30) / 12
    dc_angle = (natal_chart["descendant"]['house'] - 1) * 30 + (zodiac_signs.index(dc_sign) * 30) / 12

    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[mc_angle, mc_angle],
        mode='lines',
        line=dict(color=mc_color, dash='dash', width=2),
        opacity=0.5,
        showlegend=True,
        name="MC"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[ic_angle, ic_angle],
        mode='lines',
        line=dict(color=ic_color, dash='dash', width=2),
        opacity=0.5,
        showlegend=True,
        name="IC"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[asc_angle, asc_angle],
        mode='lines',
        line=dict(color=asc_color, dash='dash', width=2),
        opacity=0.5,
        showlegend=True,
        name="Asc"
    ))

    fig.add_trace(go.Scatterpolar(
        r=[0, 1],
        theta=[dc_angle, dc_angle],
        mode='lines',
        line=dict(color=dc_color, dash='dash', width=2),
        opacity=0.5,
        showlegend=True,
        name="Dsc"
    ))


    # Adding labels for MC, IC, Ascendant, and Descendant
    fig.add_trace(go.Scatterpolar(
        r=[1.05],
        theta=[mc_angle],
        mode='text',
        text=["MC"],
        textposition='middle right',
        hoverinfo='none',
        showlegend=False
    ))

    fig.add_trace(go.Scatterpolar(
        r=[1.05],
        theta=[ic_angle],
        mode='text',
        text=["IC"],
        textposition='middle left',
        hoverinfo='none',
        showlegend=False
    ))

    fig.add_trace(go.Scatterpolar(
        r=[1.05],
        theta=[asc_angle],
        mode='text',
        text=["   Asc"],
        textposition='middle left',
        hoverinfo='none',
        showlegend=False
    ))

    fig.add_trace(go.Scatterpolar(
        r=[1.05],
        theta=[dc_angle],
        mode='text',
        text=["Dsc"],
        textposition='middle right',
        hoverinfo='none',
        showlegend=False
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1.25]),
            angularaxis=dict(visible=True, tickmode='array', tickvals=[i * 30 for i in range(12)], ticktext=zodiac_signs, showticklabels=False)
        ),
        showlegend=True,
        margin=dict(l=40, r=40, b=40, t=40)
    )

    return fig



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
