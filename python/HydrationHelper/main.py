import time
import datetime
import json
import keyboard 

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
    
    # Intialize config
    config = load_config()
    
    # Initialize our hardware modules
    my_display = display.PetDisplay()
    my_tracker = tracker.WaterTracker(
        fsr_pin=config['fsr_adc_pin'], 
        reading_empty=config['reading_empty'], 
        reading_full=config['reading_full'],
    )
    
    # Set our goal and timer
    timer = config['time_goal'] 
    session_active = True
    time_difference = 0 
    goal_met = False

    start_time = time.time()
    my_display.show_awake_pet()
    print(f"Goal: 1 bottle in {timer} minutes!")
    print("Press 'e' to end the timer early!")
    
    # exit_requested = False
    

    try:
        # While there is still time in the session 
        while session_active:
            
            # THE FAST LOOP
            my_display.continuous_running()
            # print("Loop tick")
            
            # if keyboard.is_pressed('e'):
            #     print("\n Ending timer early!")
            #     break 
            
            # # THE SLOW LOOP
            current_time = time.time()
            time_difference = current_time - start_time 
            
            if time_difference >= config['time_goal'] * 60:
                session_active = False
                break
        
        my_display.clear_screen()
        
        my_display.write_text("checking weight", 30, 30)
        my_display.write_text(f" will {my_display.pet_name} be :) or :(...", 10, 45)
        final_measure = my_tracker.get_stable_reading()
        goal_met = my_tracker.is_empty(final_measure)
        

        # Evaluate GoalMetOrNot
        if goal_met:
            print(f"Goal met!")
            my_display.clear_screen()
            my_display.show_happy_pet()
        else:
            print(f"Goal missed.")
            my_display.clear_screen()
            my_display.show_sad_pet()
            
        # Reset the timer and the session tracker for the next hour
    except KeyboardInterrupt:
        # exit the script by pressing Ctrl+C 
        print("\nShutting down gracefully...")
        my_display.clear_screen()
        
    # Reset the timer and the session tracker for the next hour
    my_tracker.reset_session_total()
    

if __name__ == "__main__":
    main()