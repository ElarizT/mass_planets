import streamlit as st

MERCURY_GRAVITY = 0.376
VENUS_GRAVITY = 0.889
MARS_GRAVITY = 0.378
JUPITER_GRAVITY = 2.36
SATURN_GRAVITY = 1.081
URANUS_GRAVITY = 0.815
NEPTUNE_GRAVITY = 1.14
EARTH_GRAVITY = 1.0

def calculate_weight(earth_mass, planet_name):
    gravity_constants = {
        'mercury': MERCURY_GRAVITY,
        'venus': VENUS_GRAVITY,
        'mars': MARS_GRAVITY,
        'jupiter': JUPITER_GRAVITY,
        'saturn': SATURN_GRAVITY,
        'uranus': URANUS_GRAVITY,
        'neptune': NEPTUNE_GRAVITY
    }

    if planet_name.lower() in gravity_constants:
        gravity_const = gravity_constants[planet_name.lower()]
        planets_weight = earth_mass * gravity_const
        return round(planets_weight, 2)
    else:
        return None

st.title('Gravity Calculator')

earth_mass = st.number_input('What is the mass on the Earth:')
planet_name = st.text_input('What is the name of the Planet:').lower()

if st.button('Calculate'):
    weight = calculate_weight(earth_mass, planet_name)
    if weight is not None:
        st.success(f'The weight on {planet_name.capitalize()} is {weight}')
    else:
        st.error('Sorry, we don\'t have gravity information for the planet you entered.')
