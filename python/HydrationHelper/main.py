import time
import datetime
import json

import tracker
import display

def load_config():
    """Loads your settings like calibration factors and goals."""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("No config.json found. Please run calibration.py first!")
        exit()

def main():

    # Initializing the configuration
    config = load_config()
    
    # Initialize our hardware modules
    my_display = display.PetDisplay()
    my_tracker = tracker.WaterTracker(
        fsr_pin=config['fsr_adc_pin'], 
        reading_empty=config['reading_empty'], 
        reading_full=config['reading_full'],
        goal_input=config['hourly_goal_percent'],
        reading_coaster=config['reading_coaster']
    )
    
    # Set our goals and timers from the flowchart
    hourly_goal_percent = config.get('hourly_goal_percent') 
    check_interval_seconds = 60 # 1 hour (3600 seconds) CHANGE THIS LATER 
    last_time_check = time.time()
    
    
    
    # my_display.show_awake_pet()
    print(f"System Ready. Goal: {hourly_goal_percent}oz every {check_interval_seconds/60} minutes.")

    try:
        # THE MAIN CONTINUOUS LOOP 
        while True:
            
            my_tracker.get_stable_reading()
            
            # THE FAST LOOP
            # This quickly reads the FSR sensor. If the weight dropped, it adds 
            # to the running total. If it went up massively, it registers a refill.
            # my_tracker.poll_sensor() 
            
            # # THE SLOW LOOP
            # current_time = time.time()
            # if (current_time - last_time_check) >= check_interval_seconds:
            #     print("Hourly check time!")
                
            #     # GetWeightChange: How much was drank since the last check?
            #     drank_this_session = my_tracker.session_drank_percent

            #     # Evaluate GoalMetOrNot
            #     if drank_this_session >= hourly_goal_oz:
            #         print(f"Drank {drank_this_session}%. Goal met!")
            #         my_display.show_happy_pet()
            #     else:
            #         print(f"Only drank {drank_this_session}%. Goal missed.")
            #         my_display.show_sad_pet()
                    
            #     # Reset the timer and the session tracker for the next hour
            #     last_time_check = current_time
            #     my_tracker.reset_session_total()

            # # END OF DAY CHECK
            # now = datetime.datetime.now()
            # if now.hour == 23 and now.minute == 59:
            #     print("End of day. Resetting daily totals...")
            #     my_display.show_sleeping_pet()
            #     my_tracker.reset_daily_total()
            #     time.sleep(60) # Sleep for a minute to prevent multiple triggers
            #     my_display.show_awake_pet()

            # time.sleep(0.5)

    except KeyboardInterrupt:
        # exit the script by pressing Ctrl+C 
        print("\nShutting down gracefully...")
        my_display.clear_screen()
        # sensor cleanup code here

if __name__ == "__main__":
    main()