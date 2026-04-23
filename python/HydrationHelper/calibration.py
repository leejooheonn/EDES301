import time
import json
import Adafruit_BBIO.ADC as ADC
import display 
import sys

def get_stable_reading(pin, samples=10, delay=0.1):
    """Takes multiple readings and averages them to smooth out FSR noise."""
    print("Reading sensor data", end="")
    readings = []
    for _ in range(samples):
        readings.append(ADC.read(pin))
        time.sleep(delay)
    
    print(" Done!")
    return sum(readings) / len(readings)

def main():
    my_display = display.PetDisplay()
    
    my_display.write_text("HydraGotchi", 20, 32) 
    time.sleep(3)
    
    my_display.clear_screen()
        
    my_display.write_text("Enter your FSR's pin", 5, 30)
    # setup the Pin
    fsr_pin = input("Which ADC pin is your FSR connected to? (e.g., P2_35 or P1_19): ").strip()
    
    try:
        setup_successful = ADC.setup()
        test_val = ADC.read(fsr_pin)
        
        if setup_successful is False or test_val is None:
            raise Exception("ADC responded with invalid data")
        my_display.clear_screen()
        
        my_display.write_text("ADC initialized", 5, 30)
        time.sleep(3)
        my_display.clear_screen()
    
    except Exception as e:
        print(f"\nERROR: Could not initialize ADC")
        my_display.clear_screen()
        my_display.write_text("ADC not set up", 5, 30)
        sys.exit(1)
    

    # record the "Empty" baseline (0%
    my_display.write_text("weigh empty", 2, 30)
    print("\n--- STEP 1: Weigh The Empty Bottle ---")
    input("Place your EMPTY bottle on the coaster. Press ENTER when ready...")
    reading_empty = get_stable_reading(fsr_pin)
    my_display.clear_screen()
    my_display.write_text("empty remembered", 2, 30)
    print(f"Empty baseline recorded: {reading_empty:.4f}")
    time.sleep(3)
    my_display.clear_screen()

    my_display.write_text("weigh full", 2, 30)
    print("\n--- STEP 2: Weigh The Full Bottle ---")
    input("Fill your bottle up and place it on the coaster. Press ENTER when ready...")
    reading_full = get_stable_reading(fsr_pin)
    my_display.clear_screen()
    my_display.write_text("full remembered", 2, 30)
    print(f"Full baseline recorded: {reading_full:.4f}")    
    time.sleep(3)
    my_display.clear_screen()    

    # check that the readings make sense
    if reading_empty >= reading_full:
        print("\nWARNING: Your empty reading is higher than or equal to your full reading!")
        print("Run calibration again.")
        my_display.write_text("calibration error", 2, 30)
        my_display.write_text("try again", 2, 45)

        time.sleep(4)
        my_display.clear_screen()
        return
    


    my_display.write_text("set timer", 2, 30)
    # set the goal
    print("\n--- STEP 3: Goal Setting ---")
    while True:
        try:
            time_goal = input("Input timer (mins): ")
            time_goal = float(time_goal)
            break
        except (ValueError, TypeError):
            my_display.clear_screen()
            my_display.write_text("enter valid #", 2, 30)
            time.sleep(3)
            my_display.clear_screen()
            print("Please input a valid number! ")

    # save the configuration
    config = {
        "fsr_adc_pin": fsr_pin,
        "reading_empty": reading_empty,
        "reading_full": reading_full,
        "time_goal": time_goal, 
        # "reading_coaster": reading_coaster
    }
    
    my_display.clear_screen()
    my_display.write_text("sucessfully calibrated!", 2, 30)
    time.sleep(3)
    my_display.clear_screen()
    
    print("\nSaving your custom profile to config.json...")
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    print("\n Calibration Complete! ")
    print("Your PocketBeagle remembers your bottle's weight. You can now run main.py!")
    my_display.write_text("run main.py!", 2, 30)
    time.sleep(3)
    my_display.clear_screen()

if __name__ == "__main__":
    main()