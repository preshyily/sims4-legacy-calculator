#preshypily@gmail.com
from flask import Flask, request, render_template
from dash import Dash, dcc, html, Input, Output
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
        x, y, z = map(float, request.form['coordinates'].split(','))
        current_sim_day = int(request.form['current_sim_day'])
        
        sims4_globe = Sims4Globe()
        location = sims4_globe.get_location(birth_location, x, y, z)

        natal_chart = SimNatalChart(sim_age, location, current_sim_day, sim_year_days, sim_season_days)
        generated_chart = natal_chart.generate_natal_chart()

        print(generated_chart['planetary_positions'])
        
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

@dash_app.callback(
    Output('natal-chart', 'figure'),
    Input('natal-chart', 'id')
)

def update_chart(_):
    return chart_data if chart_data else go.Figure()

def create_natal_chart(natal_chart):
    planets = list(natal_chart.keys())
    angles = [natal_chart[planet]['house'] * 30 for planet in planets]
    signs = [natal_chart[planet]['sign'] for planet in planets]

    fig = go.Figure()

    # Offset for overlapping planets
    offset_radius = 0.05  # Distance from the original position
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

    # Different colors for each planet
    planet_colors = [
        "red", "blue", "green", "orange", "purple", "brown", "pink",
        "cyan", "magenta", "lime", "yellow", "navy", "gold", "grey"
    ]

    # Adding the planets
    fig.add_trace(go.Scatterpolar(
        r=adjusted_radii,
        theta=adjusted_angles,
        mode='markers+text',
        marker=dict(size=15, color=planet_colors[:len(planets)]),
        text=planets,
        textposition='top center',
        hoverinfo='text',
        showlegend=False
    ))

    # Adding the zodiac signs
    zodiac_signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
        "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    for i, sign in enumerate(zodiac_signs):
        angle = i * 30 + 15
        fig.add_trace(go.Scatterpolar(
            r=[1.1],
            theta=[angle],
            mode='text',
            text='',
            textposition='middle center',
            hoverinfo='none',
            showlegend=False
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=False, range=[0, 1.2]),
            angularaxis=dict(visible=True, tickmode='array', tickvals=[i * 30 for i in range(12)], ticktext=zodiac_signs)
        ),
        showlegend=False,
        margin=dict(l=40, r=40, b=40, t=40),
    )

    return fig

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
