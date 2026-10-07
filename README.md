
# Hydra-Gotchi | Embedded Smart Scale

[![Platform](https://img.shields.io/badge/Platform-BeagleBone%20Black-orange.svg)](https://beagleboard.org/black)
[![Language](https://img.shields.io/badge/Language-Python%203-blue.svg)](https://www.python.org/)
[![Protocols](https://img.shields.io/badge/Protocols-I2C%20%7C%20ADC%20%7C%20GPIO-green.svg)](#hardware-architecture)
[![Documentation](https://img.shields.io/badge/Hackster.io-Project%20Build-blueviolet.svg)](YOUR_HACKSTER_IO_URL_HERE)

**Hydra-Gotchi** is an ARM-based Linux embedded smart scale built on the BeagleBone Black. The system integrates analog force sensing, custom signal calibration software, and interactive user feedback via an I2C OLED display, GPIO digital inputs, and a piezo audio signal.

---

## 📖 Full Build Log & Hardware Schematics

For detailed hardware schematics, wiring diagrams, laser-cut enclosure vectors, and physical build photographs, check out the full project writeup on **Hackster.io**:

👉 **[View the Hydra-Gotchi Project on Hackster.io](https://www.hackster.io/jl587/hydrationhelper-0f8108) 

---

## 🛠️ Hardware & System Architecture

The hardware architecture combines a custom circuit assembly with a laser-cut, stress-tested enclosure designed to standardize physical load distribution across the Force Sensitive Resistor (FSR) to eliminate mechanical measurement noise.

### Hardware Components
* **SBC (Single-Board Computer):** BeagleBone Black (AM335x ARM Cortex-A8)
* **Weight Sensing:** Force Sensitive Resistor (FSR) connected via Analog-to-Digital Converter (ADC)
* **Visual Display:** SSD1306 OLED Display interfaced via **I2C**
* **Inputs & Audio:** Digital push button (**GPIO**) and Piezoelectric Buzzer (**GPIO**)
* **Physical Assembly:** Custom soldered PCB assembly housed in a laser-cut acrylic enclosure

### Block Diagram

```text
  +--------------------------------------------------------------+
  |                      BeagleBone Black                        |
  |                                                              |
  |   +-------------+      +-------------+      +------------+   |
  |   |   ADC Pin   |      |  I2C Bus    |      | GPIO Pins  |   |
  |   +------+------+      +------+------+      +-----+------+   |
  +----------|--------------------|-------------------|----------+
             |                    |                   |
             v                    v                   v
     [ FSR Sensor ]        [ OLED Display ]     [ Push Button / ]
    (Analog Weight)         (128x64 I2C)        [ Piezo Buzzer  ]
