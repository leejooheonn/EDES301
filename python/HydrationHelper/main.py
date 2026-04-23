import time
import datetime
import json
import button 

import tracker
import display
import buzzer

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
    
    my_buzzer = buzzer.Buzzer("P2_1")
    my_display.show_awake_pet()
    my_buzzer.alert_tone()
    my_button = button.Button("P2_8")
    
    try: 
        # This lets the program keep running until the user wants to stop 
        while True: 
            
            # make sure the water bottle is full before proceeding
            while True: 
                start_bottle = my_tracker.get_stable_reading()
            
                # the bottle is full, the 0.2 may need to be changed  !
                if start_bottle >= config['reading_full'] - 0.2: 
                    break 
                
                # if the full bottle isn't on, prompt them to 
                my_display.clear_screen()
                my_display.write_text("put on full weight!", 0, 30)

                time.sleep(0.5)
            
            # the full bottle is now on at this point
            my_display.clear_screen()
     
            session_active = True
            time_difference = 0 
            goal_met = False
            exit_requested = False

            
            start_time = time.time()
            print(f"Goal: 1 bottle in {config['time_goal']} minutes!")
            print("Press button to end the timer early!")
            
            # exit_requested = False
            
            my_display.write_text(f"time starts now!", 15, 30)
            my_display.write_text(f"you have {config['time_goal']} min(s)", 10, 40)
        
            # start the timer
            start_time = time.time()
            time.sleep(3)
            my_display.clear_screen()
            
                # While there is still time in the session 
            while session_active:
                
                keep_running = my_display.continuous_running()
                
                if my_button.is_pressed():
                    print("\n Ending timer early!")
                    session_active = False
                    break 
                
                current_time = time.time()
                time_difference = current_time - start_time 
                
                # see if the time is up yet 
                if time_difference >= config['time_goal'] * 60:
                    session_active = False
                    break
            
            
            # when the timer is up, prompt user to place bottle back on 
            my_display.write_text("put bottle on", 30, 30)
            my_buzzer.alert_tone()
            time.sleep(3)
            my_display.clear_screen()
            
            my_display.write_text("checking weight", 15, 30)
            my_display.write_text(f" will {my_display.pet_name} be :) or :(...", 0, 45)
            # takes a while to stabilize... 
            time.sleep(8)
            
            final_measure = my_tracker.get_stable_reading()
            goal_met = my_tracker.is_empty(final_measure)
            
    
            # see if goal has been met 
            if goal_met:
                print(f"Goal met!")
                my_display.clear_screen()
                my_display.show_happy_pet()
                

            else:
                print(f"Goal missed.")
                my_display.clear_screen()
                my_display.show_sad_pet()

            # see if the user wants to keep going
            my_display.clear_screen()
            my_display.write_text("restart? (y/n)", 30, 30)
            play_again = input("\n Would you like to start the timer again? (y/n): ").strip()
            time.sleep(2)
            my_display.clear_screen()
            
            # when they want to leave 
            if play_again == 'n':
                my_display.write_text("bye bye", 0, 15)
                my_display.write_text("thanks for hydrating!", 0, 30)
                my_display.write_text("meow", 25, 45)
                print("Thanks for hydrating!")
                time.sleep(5)
                break 
            
            # if they want to keep going, ask if they want to change goal
            my_display.write_text("new goal?", 15, 25)
            my_display.write_text("to skip, press Enter", 0, 40)
            
            new_goal = input("Enter a new goal (in minutes) or press Enter to keep current: ")
            time.sleep(5)
            my_display.clear_screen()

            if new_goal != "": 
                try: 
                    config['time_goal'] = float(new_goal) 
                    print(f"Goal updated to {config['time_goal']} minutes!")
                except ValueError:
                    my_display.write_text("invalid. enter a number!", 15, 25)
                    print("That wasn't a valid number grrrr.")
                    time.sleep(3)
                    my_display.clear_screen()
                            
            
    except KeyboardInterrupt:
        # exit the script by pressing Ctrl+C 
        print("\nShutting down...")
    finally:
        my_display.clear_screen()
        my_buzzer.cleanup()
        my_button.cleanup()

if __name__ == "__main__":
    main()