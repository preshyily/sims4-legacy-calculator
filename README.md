# Sims 4 Legacy Calculator

## Overview
The Sims 4 Legacy Calculator is a web application designed to help Sims 4 players generate and analyze natal charts for their Sims. Based on the input data, it provides insights into traits, aspirations, careers, skills, and legacy rules for a Sim. You can access the web application [here](https://sims4-legacy-calculator.onrender.com/).

If you enjoy this tool, please consider buying me a taco here @ https://ko-fi.com/preshy

Please credit and tag my socials if you use my program for a Let's Play or any content. I would love to see it <3

## Features
- Generate natal charts for Sims based on age, birth location, and current Sim day.
- Analyze and filter natal charts to provide traits, aspirations, careers, best and worst skills, and legacy rules.
- Visualize the natal chart with a polar chart.

## Installation
You can either use the web application directly or install and run it locally.

### Option 1: Use the Web Application
Simply visit [Sims 4 Legacy Calculator](https://sims4-legacy-calculator.onrender.com/) and start using the tool.

### Option 2: Install Locally
To run the application locally, follow these steps:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/your-repository/sims4-legacy-calculator.git
    cd sims4-legacy-calculator
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application:**
    ```bash
    python app.py
    ```

    The application will be accessible at `http://localhost:5000`.

## Usage
### Inputs
- **Sim Age:** The age of the Sim in Sim days.
- **Birth Location:** The location where the Sim was born. Select from a list of available locations.
- **Coordinates (x, y, z):** The coordinates of the birth location in the Sim world.
- **Current Sim Day:** The current day in the Sim world beginning from the creation of the save.
- **Sim Year Days:** The number of Sim days in a year. Default is 28.
- **Sim Season Days:** The number of Sim days in a season. Default is 7.

### Outputs
- **Traits:** The traits assigned to the Sim based on their natal chart.
- **Aspirations:** The aspirations the Sim should pursue.
- **Careers:** Suggested careers for the Sim.
- **Best Skills:** The skills the Sim excels at.
- **Worst Skills:** The skills the Sim struggles with.
- **Legacy Rules:** Rules for the Sim based on their natal chart.
- **Birth Date:** The formatted birth date of the Sim.

## Sources

### Liisims
- **Zodiac Legacy Challenge**
- [Tumblr: liisims](https://liisims.tumblr.com)
- Mentioned for creating the Zodiac Legacy Challenge with inspiration from the internet and people around.

### Legacy Challenge Rules
- **The Sims 4 Legacy Challenge Rules**
- [Legacy Challenge Official Site](https://www.simslegacychallenge.com/the-sims-4-legacy-challenge-rules/)
- General rules for the Legacy Challenge, specifying the guidelines for starting and maintaining a legacy in The Sims 4.

### Leaflysims & Tropiccoconut
- **Astrology Legacy Challenge**
- [Tumblr: Leaflysims](https://leaflysims.tumblr.com)
- [Tumblr: Tropiccoconut](https://tropiccoconut.tumblr.com)
- Co-authored the Astrology Legacy Challenge along with the user.
- Mentioned for their involvement in creating this challenge.

### Spacesuitsims (me)
- **Ascendant Legacy Challenge Rules**
- [Spacesuitsims Tumblr](https://spacesuitsims.tumblr.com)
- A detailed challenge focusing on the Ascendant/Rising sign in astrology.
- Mentioned for providing in-depth astrology-based Sims challenges.

### Ginovasims
- **Star Sign Legacy Challenge**
- [Tumblr: ginovasims](https://ginovasims.tumblr.com)
- Created a twelve-generation legacy challenge based on the twelve signs of the zodiac.
- Mentioned for providing specific rules and guidelines for each zodiac sign in the challenge.

### Natal Chart Mathematical Formulas
1. **Astrology: A Cosmic Science by Isabel Hickey**
   - This book is a classic in the field of astrology and offers detailed explanations of the calculations involved in creating natal charts.
   - **Link**: [Amazon - Astrology: A Cosmic Science](https://www.amazon.com/Astrology-Cosmic-Science-Isabel-Hickey/dp/0877283188)

2. **Compendium of Astrology by Rose Lineman and Rose Popelka**
   - Another comprehensive guide, this book provides in-depth methods for calculating planetary positions and interpreting natal charts.
   - **Link**: [Amazon - Compendium of Astrology](https://www.amazon.com/Compendium-Astrology-Rose-Lineman/dp/0877285970)

3. **The American Ephemeris for the 21st Century (2000-2050) at Midnight**
   - An ephemeris is essential for looking up the positions of the planets at given times. This specific ephemeris provides data for the 21st century.
   - **Link**: [Amazon - The American Ephemeris for the 21st Century](https://www.amazon.com/American-Ephemeris-Century-2000-2050-Midnight/dp/1934976287)

4. **Placidus Houses and Koch Houses**
   - Books on house systems are necessary for calculating the positions of the planets within the houses of a natal chart.
   - **Link**: [Amazon - Placidus Houses](https://www.amazon.com/Placidus-House-Tables-Astrology/dp/1934976236)
   - **Link**: [Amazon - Koch Houses](https://www.amazon.com/Koch-House-Tables-Michelsen-Memorial/dp/193497621X)

### Globe Formulas
1. **Latitude and Longitude to Cartesian Coordinates Conversion**
   - This formula is used to convert geographical coordinates into 3D Cartesian coordinates.
   - **Link**: [Wikipedia - Geographic coordinate conversion](https://en.wikipedia.org/wiki/Geographic_coordinate_conversion)

2. **Spherical to Cartesian Coordinate Transformation**
   - Additional resources for transforming spherical coordinates to Cartesian coordinates.
   - **Link**: [MathWorks - Spherical to Cartesian Coordinates](https://www.mathworks.com/help/matlab/ref/sph2cart.html)

### Additional Resources
1. **Julian Date Calculation**
   - The method for converting calendar dates to Julian dates is essential for astronomical calculations.
   - **Link**: [NASA - Julian Date Converter](https://ssd.jpl.nasa.gov/tools/jdc/)

### Mathematical Formulas and Algorithms
1. **Spherical Geometry Basics**
   - Understanding spherical geometry to map 2D coordinates onto a 3D globe.
   - Source: [Wikipedia - Spherical Geometry](https://en.wikipedia.org/wiki/Spherical_geometry)

2. **Plotly for 3D Visualization**
   - Using Plotly for visualizing 3D plots and integrating geographic data.
   - Documentation: [Plotly 3D Charts](https://plotly.com/python/3d-charts/)

3. **Mapping 2D Grids to 3D Spheres**
   - Techniques for transforming 2D grid data to fit onto a 3D spherical surface.
   - Source: [Stack Overflow - Mapping 2D Grid to 3D Sphere](https://stackoverflow.com/questions/25869428/convert-2d-grid-to-3d-sphere)

### Sims 4 Specific Data
4. **Sims 4 Lot Sizes and Locations**
   - Detailed information about the lot sizes and locations in various Sims 4 worlds.
   - Sources:
     - [Snooty Sims](https://snootysims.com/wiki/sims-4/sims-4-lot-sizes-list/)
     - [Teoalida - Sims 4 Worlds and Lots](https://www.teoalida.com/thesims/sims-4-worlds/)

5. **Sims 4 Forums and Discussions**
   - Discussions and forums for insights and examples on accessing and utilizing Sim data.
   - Sources:
     - [Mod The Sims Forums](https://modthesims.info/wiki.php?title=Tutorials:TS4_General_Modding)
     - [Sims 4 Studio Forums](http://sims4studio.com/)

### Other Relevant Mathematical and Coding Resources
6. **Geographic Coordinate Systems**
   - Concepts and calculations for geographic coordinate systems and conversions.
   - Source: [Geographic Coordinate System - Wikipedia](https://en.wikipedia.org/wiki/Geographic_coordinate_system)

7. **NumPy and SciPy for Scientific Computing**
   - Utilizing NumPy and SciPy libraries for scientific computations and transformations.
   - Documentation: [NumPy Documentation](https://numpy.org/doc/stable/)
   - [SciPy Documentation](https://www.scipy.org/docs.html)

These resources provide the mathematical foundations and detailed methods for accurately calculating natal charts and converting geographical coordinates for the simulated globe.


## Contact
For any queries or support, please contact:
- **Email:** preshypily@gmail.com
- **TikTok:** @preshyp.ily
- **Instagram:** @preshy.ily

## Contributing
Contributions are welcome! If you have suggestions or improvements, please create a submit request using the Google Form:

### Viewing The Sims 4 Natal Legacy Matrix

To view the `natal_planets_houses_allzodiacs` sheet with filters:

1. **Access the Sheet**:
   - Click on the following link to access the Google Sheet: [Google Sheet Link](https://docs.google.com/spreadsheets/d/1JHIMzBUyrXWUYKNXl-Enkrqp79z1kHR1Jx55_dCdun4/edit?usp=sharing)

2. **Use the Filter View**:
   - Use the filter view options provided in the Google Sheet to find the row you want to review or request an update for. This allows you to filter by specific columns without modifying the sheet.

### Submitting an Update Request

To submit an update request for a specific row in the `natal_planets_houses_allzodiacs` sheet:

1. **Identify the Row**:
   - Note down the Row ID or any other unique identifier for the row you want to request an update for. Ensure you have the relevant details about the row you wish to update.

2. **Access the Update Request Form**:
   - Click on the following link to open the update request form: [Google Form Link](https://forms.gle/5PTvZA96EHXVq1C58)

3. **Fill Out the Form**:
   - Complete the form with the necessary information, including the Row ID and the details of the update request.
   - Provide as much detail as possible to ensure accurate updates.

4. **Submit the Form**:
   - Once you have filled out the form with the necessary details, submit the form.

Thank you for helping us keep the data accurate and up-to-date!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
``` &#8203;:citation[oaicite:0]{index=0}&#8203;
