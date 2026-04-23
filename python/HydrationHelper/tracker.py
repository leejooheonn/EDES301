import time
import Adafruit_BBIO.ADC as ADC

class WaterTracker:
        # Gets a stable reading by averaging multiple samples and converting to percentage
    
    def __init__(self, fsr_pin, reading_empty, reading_full):
        """Initializes the tracker"""
        self.fsr_pin = fsr_pin
        self.reading_empty = reading_empty
        self.reading_full = reading_full

        # Initializes the ADC converter and sets up the sensor 
        ADC.setup()
        ADC.read(self.fsr_pin)  
        time.sleep(0.2)  # Let the sensor stabilize 

        # Set the initial baseline reading
        self.last_known_raw_avg = self.get_stable_reading()

    def get_stable_reading(self):

        """Reads the ADC 5 times, and averages it."""
        readings = []
        for _ in range(5):
            readings.append(ADC.read(self.fsr_pin))
            time.sleep(0.5)
        
        avg_raw = sum(readings) / len(readings)
        
        print(f"the current avg_raw is {avg_raw}")
        return avg_raw

    # def poll_sensor(self):
    #     """Checks for sips, refills, and liftoffs using percentages."""
    #     """ Returns the last known raw value of the bottle, discounting when it's lifted"""
    #     current_raw = self.get_stable_reading()
    #     print(f"the current_raw is {current_raw}")
        
    #     # Wait until the bottle is placed back down
    #     if current_raw == 0.0:
    #         return 

    #     # If it was lifted off the sensor earlier, record the weight now that it's down
    #     if current_raw != 0.0 :
    #         time.sleep(3.0)
            
    #         current_raw = self.get_stable_reading()
    #         if current_raw != 0.0:
    #             self.last_known_avg_raw = current_raw
        
    #     return self.last_known_avg_raw         
    
    def is_empty(self, raw_val):
        """ Ret #urns true if the bottle is empty, false otherwise """
        # somewhat arbritrary buffer of 0.1 
        if raw_val < self.reading_empty + 0.1:
            return True
            
        return False    
    
    # def get_session_total(self):
    #     """Returns the raw difference in FSR reading since last hourly check."""
    #     return round(self.session_drank, 1)

    # def reset_session_total(self):
    #     """Resets the session tracker """
    #     self.session_drank = 0.0

    # def get_daily_total(self):
    #     """Returns the total raw difference in FSR reading for the whole day."""
    #     return round(self.daily_drank_percent, 1)
        

# test_tracker = WaterTracker("P1_21", 0.0047, 0.96)
# for _ in range(10): 
#     test_tracker.get_stable_reading()