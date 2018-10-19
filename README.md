# Pyghack2018
Our project tackles the Urbana Fleet Fuel Management problem, which tries to find trends in gas station prices and vehicle fueling behaviors. In addition to answering these questions, we built a dynamic route recommendation system. The system calculates the route between a start point and a destination, looks at all of the gas stations that are reachable along the route, and then recommends a gas station to go to. This recommendation can be optimized for cost (i.e., it will recommend the gas station with the cheapest prices while taking into account the fuel lost by making a detour to the station) or for time (i.e., it will recommend the gas station that is fastest and cheapest to get to). 

The dynamic route recommendation system can be found at: https://lynnnyn.pythonanywhere.com

The layout for our website:
![alt text](https://github.com/lynnnyn/Pyghack2018/blob/master/screencapture-lynnnyn-pythonanywhere-2018-10-19-11_46_24.png)

The search result:
![alt text](https://github.com/lynnnyn/Pyghack2018/blob/master/Screen%20Shot%202018-10-19%20at%2011.49.54%20AM.png)

We visualized some of the insights we gained from the dataset on Tableau: 
https://public.tableau.com/views/FinalProduct/Story1?:embed=y&:display_count=yes&publish=yes

Powerpoint slides discussing our results can be found in Deliverable.pdf
# About our website
## Technology stack
* Python 3.6
* Flask
* jQuery
* ES6
## Installation
1. Get the code. Clone this git repository and check out the latest release:
git clone https://github.com/lynnnyn/Pyghack2018.git
    cd Pyghack2018
    git checkout latest

2. run flask_app.py

3. website will run on http://0.0.0.0:5000

# Setting up the environment 
Run 
conda env create -f environment.yml

