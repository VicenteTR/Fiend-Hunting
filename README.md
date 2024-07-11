# FiendHunter

FiendHunter is a PyQt5 application designed finding fiends in Tibia by processing the input from the spell and narrowing down your search.
## Installation

1. **Ensure you have Python 3.x installed:**

2. **Install PyQt5 if you haven't already:**
```bash
pip install PyQt5
```

## Running the Application

1. **Within your downloaded directory run cmd and run:**
```bash
python main.py
```

## Installation

1. **Usage:**

Right click to create a marker. This represents the position where you are standing when casting Find Fiend. Scroll Wheel is used to zoom in or out. Left click to drag and navigate the map. + and - buttons to navigate floors.
Use the output from the spell to fill out the checkboxes on the left and press "Submit" when ready.
This will add a semi-transparent area in which your fiend is.
You can repeat this process to narrow down the location and stack multiple areas.
Keep in mind there may be multiple fiends active at a time, which means it's your job to recognize which casts are for which creature.

When you want to reset you can press the clear button to get rid of all markers and zones.

**Disclaimer:**

Very little testing has been done for this app. It is possible that a creature MAY be very close to the red area and not strictly inside it seeing as creatures can move when a player is nearby.
Also UI sucks. I know.

**Acknowledgements**

Thanks to Tibiamaps for having high resolution maps for Tibia so readily available online.