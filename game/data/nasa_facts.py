"""NASA facts and educational content database"""

PLANET_FACTS = {
    'Earth': [
        "Earth is the only known planet with life in the universe.",
        "71% of Earth's surface is covered by water.",
        "Earth's atmosphere is 78% nitrogen and 21% oxygen.",
        "The International Space Station orbits Earth every 90 minutes.",
        "Earth's magnetic field protects us from harmful solar radiation."
    ],
    'Mars': [
        "Mars has the largest volcano in the solar system - Olympus Mons.",
        "A day on Mars is 24 hours and 37 minutes long.",
        "Mars has two small moons: Phobos and Deimos.",
        "The first successful Mars rover was Sojourner in 1997.",
        "Mars appears red due to iron oxide (rust) on its surface."
    ],
    'Moon': [
        "The Moon is moving away from Earth at 3.8 cm per year.",
        "The Moon's gravity causes Earth's ocean tides.",
        "Apollo 11 was the first crewed mission to land on the Moon in 1969.",
        "The Moon has no atmosphere, so there's no weather or wind.",
        "The same side of the Moon always faces Earth due to tidal locking."
    ],
    'Jupiter': [
        "Jupiter is the largest planet in our solar system.",
        "Jupiter has over 80 known moons, including the four Galilean moons.",
        "The Great Red Spot is a storm larger than Earth that has raged for centuries.",
        "Jupiter acts as a 'cosmic vacuum cleaner' protecting inner planets from asteroids.",
        "Jupiter is mostly made of hydrogen and helium, like a star."
    ]
}

MISSION_FACTS = {
    'exploration': [
        "NASA's Perseverance rover is searching for signs of ancient life on Mars.",
        "The Voyager probes have traveled beyond our solar system into interstellar space.",
        "The Hubble Space Telescope has been observing the universe for over 30 years.",
        "NASA's New Horizons mission gave us the first close-up images of Pluto."
    ],
    'research': [
        "The Kepler Space Telescope discovered over 2,600 confirmed exoplanets.",
        "NASA studies climate change using satellites that monitor Earth's atmosphere.",
        "The James Webb Space Telescope can see the first galaxies formed after the Big Bang.",
        "Microgravity research on the ISS helps develop new medicines and materials."
    ],
    'collaboration': [
        "The ISS is a partnership between NASA, Roscosmos, ESA, JAXA, and CSA.",
        "International cooperation is essential for future Mars missions.",
        "NASA shares data openly to benefit scientists worldwide.",
        "The Artemis program aims to return humans to the Moon with international partners."
    ],
    'problem_solving': [
        "NASA's DART mission successfully changed an asteroid's trajectory in 2022.",
        "Engineers use creative problem-solving to fix spacecraft millions of miles away.",
        "NASA develops technologies that benefit life on Earth, like water purification systems.",
        "Mission control teams work 24/7 to solve problems in real-time during space missions."
    ]
}

SPACE_CHALLENGES = [
    "Radiation exposure is a major challenge for long-duration space missions.",
    "Microgravity causes bone and muscle loss in astronauts.",
    "Space debris poses a growing threat to satellites and spacecraft.",
    "Communication delays make real-time control of Mars missions impossible.",
    "Psychological challenges of isolation affect astronaut mental health.",
    "Dust storms on Mars can last for months and block solar panels.",
    "Extreme temperatures in space range from -250°F to 250°F.",
    "Spacecraft must be designed to work perfectly for years without maintenance."
]

def get_random_fact(category=None):
    """Get a random educational fact"""
    import random
    
    if category and category in PLANET_FACTS:
        return random.choice(PLANET_FACTS[category])
    elif category and category in MISSION_FACTS:
        return random.choice(MISSION_FACTS[category])
    else:
        all_facts = []
        for facts_list in PLANET_FACTS.values():
            all_facts.extend(facts_list)
        for facts_list in MISSION_FACTS.values():
            all_facts.extend(facts_list)
        all_facts.extend(SPACE_CHALLENGES)
        return random.choice(all_facts)