import math
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sims4_globe import Sims4Globe


class SimNatalChart:
    ZODIAC_SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
        "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    HOUSES = range(1, 13)
    SIM_YEAR_DAYS = 28

    def __init__(self, sim_age, birth_location, current_sim_day):
        self.sim_age = sim_age
        self.birth_location = birth_location
        self.current_sim_day = current_sim_day
        self.birthdate = self.calculate_birthdate()
        self.jd = self.julian_date(self.birthdate)

    def calculate_birthdate(self):
        total_days_current_year = self.current_sim_day
        full_years_passed = self.sim_age // self.SIM_YEAR_DAYS
        remaining_days = self.sim_age % self.SIM_YEAR_DAYS
        birth_year = 0 - full_years_passed
        birth_day_of_year = total_days_current_year - remaining_days

        if birth_year <= 0:
            return (birth_year, birth_day_of_year)
        return datetime(year=birth_year, month=1,
                        day=1) + timedelta(days=birth_day_of_year)

    def convert_birthdate_to_days(self, birthdate):
        if isinstance(birthdate, tuple):
            year, day_of_year = birthdate
            return year * self.SIM_YEAR_DAYS + day_of_year
        days_from_start = (birthdate -
                           datetime(year=birthdate.year, month=1, day=1)).days
        return birthdate.year * self.SIM_YEAR_DAYS + days_from_start

    def julian_date(self, date):
        if isinstance(date, tuple):
            year, day_of_year = date
            return self.bce_to_julian_date(year, day_of_year)
        a = (14 - date.month) // 12
        y = date.year + 4800 - a
        m = date.month + 12 * a - 3
        jdn = date.day + ((153 * m + 2) //
                          5) + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        return jdn + (date.hour -
                      12) / 24 + date.minute / 1440 + date.second / 86400

    def bce_to_julian_date(self, year, day_of_year):
        jd_start_of_year = self.julian_date(datetime(year=1, month=1,
                                                     day=1)) - (year * 365.25)
        return jd_start_of_year + day_of_year

    def calculate_planetary_positions(self, jd):

        def calc_position(L, g, n):
            L = (L + 1.915 * math.sin(math.radians(g)) +
                 0.020 * math.sin(math.radians(2 * g))) % 360
            return L

        def planet_position(jd, L0, g0, rate):
            n = jd - 2451545.0
            L = (L0 + rate * n) % 360
            g = (g0 + rate * n) % 360
            return calc_position(L, g, n)

        positions = {
            "sun": planet_position(jd, 280.460, 357.528, 0.9856474),
            "moon": planet_position(jd, 218.316, 134.963, 13.176396),
            "mercury": planet_position(jd, 252.250, 77.456, 4.0923388),
            "venus": planet_position(jd, 181.979, 131.563, 1.6021303),
            "mars": planet_position(jd, 355.433, 336.040, 0.5240208),
            "jupiter": planet_position(jd, 34.351, 14.331, 0.083091),
            "saturn": planet_position(jd, 50.077, 93.056, 0.033459),
            "uranus": planet_position(jd, 314.055, 173.005, 0.011733),
            "neptune": planet_position(jd, 304.348, 48.123, 0.006021),
            "pluto": planet_position(jd, 238.929, 224.066, 0.003963),
            "north_node": planet_position(jd, 174.873, 123.448, 0.001479),
            "south_node": planet_position(jd, 354.873, 243.448, 0.001479),
            "lilith": planet_position(jd, 120.982, 142.102, 0.004925),
            "chiron": planet_position(jd, 209.515, 172.439, 0.007166),
            "fortune": planet_position(jd, 238.929, 224.066, 0.003963),
            "vertex": planet_position(jd, 238.929, 224.066, 0.003963)
        }

        E, w, A = 90, 23.44, self.birth_location['latitude']
        ascendant = math.degrees(
            math.atan(
                math.sin(math.radians(E)) /
                (math.cos(math.radians(E)) * math.cos(math.radians(w)) -
                 math.sin(math.radians(w)) * math.tan(math.radians(A)))))
        mc = math.degrees(
            math.atan(math.tan(math.radians(90)) / math.cos(math.radians(w))))

        positions.update({
            "midheaven": mc,
            "ascendant": ascendant,
            "descendant": (ascendant + 180) % 360,
            "ic": (mc + 180) % 360
        })
        return positions

    def generate_natal_chart(self):
        planetary_positions = self.calculate_planetary_positions(self.jd)
        zodiac_chart = self.assign_to_zodiac_and_houses(planetary_positions)
        return zodiac_chart

    def assign_to_zodiac_and_houses(self, planetary_positions):
        zodiac_chart = {}
        for planet, position in planetary_positions.items():
            sign_index = int(position // 30)
            house = (sign_index + 1) % 12 + 1
            zodiac_chart[planet] = {
                "sign": self.ZODIAC_SIGNS[sign_index],
                "house": house
            }
        return zodiac_chart


class CreateLegacyChallenge:

    def __init__(self, natal_chart):
        self.natal_chart = natal_chart

    def filter_natal_chart(self):

        result_text = ""
        file_path = 'static/natal_planets_houses_allzodiacs.xlsx'
        df = pd.read_excel(file_path, engine='openpyxl')

        # Filter the DataFrame based on the natal chart
        matching_rows = []
        natal_chart = self.natal_chart

        for planet, info in natal_chart.items():
            matches = df[(df['Planet'] == planet.title())
                         & (df['Zodiac'] == info['sign']) &
                         (df['House'] == info['house'])]
            matching_rows.append(matches)

        # Combine the matching rows into a single DataFrame
        result_df = pd.concat(matching_rows)

        # Extract the specified columns
        columns_of_interest = [
            'Trait(s)', 'Aspiration(s)', 'Career', 'Best Skill(s)',
            'Worst Skill(s)', 'Rule(s)'
        ]
        result_df = result_df[columns_of_interest]

        # Initialize sets for unique values
        traits_set, aspirations_set, careers_set = set(), set(), set()
        best_skills_set, worst_skills_set, rules_list = set(), set(), []

        # Define separators
        separators = [',', '.']

        # Populate sets with unique, cleaned values
        for _, row in result_df.iterrows():
            traits = row['Trait(s)'].split(', ')
            aspirations = row['Aspiration(s)'].split(', ')
            careers = row['Career'].split(', ')
            best_skills = row['Best Skill(s)'].split(', ')
            worst_skills = row['Worst Skill(s)'].split(', ')
            rules = row['Rule(s)'].split('. ')

            for trait in traits:
                traits_set.add(clean_split(trait, separators))

            for aspiration in aspirations:
                aspirations_set.add(clean_split(aspiration, separators))

            for career in careers:
                careers_set.add(clean_split(career, separators))

            for skill in best_skills:
                best_skills_set.add(clean_split(skill, separators))

            for skill in worst_skills:
                worst_skills_set.add(clean_split(skill, separators))

            for rule in rules:
                if "Must master" in rule:
                    rule_parts = rule.split(" and ")
                    for part in rule_parts:
                        part_cleaned = part.replace("Must master",
                                                    "").strip().capitalize()
                        rules_list.append(f"Must master {part_cleaned}")
                else:
                    rule_parts = rule.split(", ")
                    for part in rule_parts:
                        rules_list.append(part.capitalize().strip())

        # Remove duplicates from the rules list
        rules_set = set(rules_list)
        rules_list = sorted(rules_set)
        final_rules = []
        seen_rules = set()

        for rule in rules_list:
            if rule not in seen_rules:
                if ", " in rule:
                    rule_parts = rule.split(", ")
                    for part in rule_parts:
                        part_cleaned = part.capitalize().strip()
                        if part_cleaned not in seen_rules:
                            final_rules.append(part_cleaned)
                            seen_rules.add(part_cleaned)
                else:
                    final_rules.append(rule)
                    seen_rules.add(rule.capitalize().strip())

        # Resolve skills conflicts between best and worst skills
        best_skills_counts = {skill: 0 for skill in best_skills_set}
        worst_skills_counts = {skill: 0 for skill in worst_skills_set}

        for _, row in result_df.iterrows():
            best_skills = row['Best Skill(s)'].split(', ')
            worst_skills = row['Worst Skill(s)'].split(', ')

            for skill in best_skills:
                skill_cleaned = clean_split(skill, separators)
                if skill_cleaned in best_skills_counts:
                    best_skills_counts[skill_cleaned] += 1

            for skill in worst_skills:
                skill_cleaned = clean_split(skill, separators)
                if skill_cleaned in worst_skills_counts:
                    worst_skills_counts[skill_cleaned] += 1

        # Ensure all keys are present in the counts dictionaries
        all_skills = best_skills_set.union(worst_skills_set)
        for skill in all_skills:
            if skill not in best_skills_counts:
                best_skills_counts[skill] = 0
            if skill not in worst_skills_counts:
                worst_skills_counts[skill] = 0

        final_best_skills = {
            skill
            for skill in best_skills_set
            if best_skills_counts[skill] > worst_skills_counts[skill]
        }
        final_worst_skills = {
            skill
            for skill in worst_skills_set
            if worst_skills_counts[skill] > best_skills_counts[skill]
        }

        # Prepare formatted result
        result_text += "\nTraits:\n" + "\n".join(sorted(traits_set)) + "\n\n"
        result_text += "Aspirations:\n" + "\n".join(
            sorted(aspirations_set)) + "\n\n"
        result_text += "Careers:\n" + "\n".join(sorted(careers_set)) + "\n\n"
        result_text += "Best Skills:\n" + "\n".join(
            sorted(final_best_skills)) + "\n\n"
        result_text += "Worst Skills:\n" + "\n".join(
            sorted(final_worst_skills)) + "\n\n"
        result_text += "Rules:\n" + "\n".join(sorted(seen_rules)) + "\n"

        # Define the path to the output text file
        output_file_path = 'cleaned_natal_chart_results.txt'

        # Write the result_text to the text file
        with open(output_file_path, 'w') as file:
            file.write(result_text)

        return traits_set, aspirations_set, careers_set, final_best_skills, final_worst_skills, seen_rules




def lat_lon_to_xyz(lat, lon, radius=80.47):
    lat_rad = np.deg2rad(lat)
    lon_rad = np.deg2rad(lon)
    x = radius * np.cos(lat_rad) * np.cos(lon_rad)
    y = radius * np.cos(lat_rad) * np.sin(lon_rad)
    z = radius * np.sin(lat_rad)
    return x, y, z


def calculate_natal_chart(world_name, x, y, z):
    globe = Sims4Globe()
    location = globe.get_location(world_name, x, y, z)
    print(f"\nCalculating natal chart for location: {location}\n")
    return location


def pretty_print_natal_chart(natal_chart):
    print("\nNatal Chart:")
    for planet, details in natal_chart.items():
        print(
            f"{planet.capitalize()}: {details['sign']}, House {details['house']}"
        )


def clean_split(entry, separators):
    for sep in separators:
        entry = entry.split(sep)[0]
    return entry.strip()
