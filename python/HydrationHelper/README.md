<h1>HydrationHelper</h1>

## About the Project 
HydrationHelper is a tool to help people reach their daily water goals. It works to motivate users to drink water by having a virtual pet track the weight of the water bottle and setting a time period for the water bottle to be finished by. The sensor then checks the water bottle at the end of the time period and depending on if the water is full or empty, the virtual pet acts accordingly. 

## Features
* Goal setting: the users can set their time goal for finishing their water bottle
* Calibration: tracks the weight of the full water bottle and the empty water bottle to calibrate the program
* Project presentation: the project proposal can be found in the `docs/` folder

## Repository Structure
* `docs/` - Contains the project presentation and other documentation.
* `HydrationHelper/` - *Contains source code, and images used for the virtual pet*

## Installation and Set-up 
To run this project locally, ensure you have Python3 installed. 
1) Clone the repository
2) Install the required dependencies
   `pip install Adafruit-BBIO`
   `pip install Pillow`
   `pip install Adafruit-Blinka`
   `pip install adafruit-circuitpython-ssd1306`
3) Run the application by entering the HydrationHelper directory and run `python3 calibration.py` to calibrate and then `python3 main.py` to start the HydrationHelper

> **Troubleshooting:** If you receive a "Permission Denied" error regarding hardware access (ADC or I2C), your user may not have the correct permissions. In that case, you can run the program with administrator privileges: `sudo python3 main.py` (Note: If you need to run it with sudo, you may need to install the requirements globally using `sudo pip3 install -r {dependency}`).

## Built With
* Python, BeagleBoard

# Author
* Jooheon Lee EDES301
