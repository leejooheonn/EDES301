import time
import Adafruit_BBIO.ADC as ADC

# 1. SETUP
# Replace "P1_19" with whichever AIN pin you are actually using
fsr_pin = "P1_21" 

# Initialize the PocketBeagle's ADC hardware
ADC.setup()

print("Starting FSR Test... Press Ctrl+C to stop.")

# 2. THE LOOP
try:
    while True:
        # Read the analog value (Returns a float between 0.0 and 1.0)
        fsr_reading = ADC.read(fsr_pin)
        
        # Print the raw reading (formatted to 3 decimal places to keep it clean)
        print(f"Analog reading = {fsr_reading:.3f}", end="")
        
        # We'll have a few thresholds, qualitatively determined.
        # Scaled to match the PocketBeagle's 0.0 - 1.0 range.
        if fsr_reading < 0.01:   # Equivalent to Arduino < 10
            print(" - No pressure")
        elif fsr_reading < 0.20: # Equivalent to Arduino < 200
            print(" - Light touch")
        elif fsr_reading < 0.49: # Equivalent to Arduino < 500
            print(" - Light squeeze")
        elif fsr_reading < 0.78: # Equivalent to Arduino < 800
            print(" - Medium squeeze")
        else:
            print(" - Big squeeze")
            
        # Wait for 1 second before looping again (equivalent to delay(1000))
        time.sleep(1.0)
        
except KeyboardInterrupt:
    # This safely stops the program if you press Ctrl+C in the terminal
    print("\nTest stopped.")