import time
import Adafruit_BBIO.ADC as ADC

class WaterTracker:
        # Gets a stable reading by averaging multiple samples and converting to percentage
    
    
    def __init__(self, fsr_pin, reading_empty, reading_full, goal_input, reading_coaster):
        """Initializes the tracker for FSR percentages."""
        self.fsr_pin = fsr_pin
        self.reading_empty = reading_empty
        self.reading_full = reading_full
        self.is_lifted = False
        
        # Initializes the ADC converter and sets up the sensor 
        ADC.setup()
        ADC.read(self.fsr_pin)  # Initial read to stabilize

        time.sleep(0.5)  # Allow some time for the sensor to stabilize


        # Variables to track progress in percentage terms
        self.session_drank_percent = 0.0  
        self.daily_drank_percent = 0.0   
        
        # Thresholds for the FSR to account for noise 
        self.SIP_THRESHOLD = 10       # Min drop (%) to count as a real sip
        # self.REFILL_THRESHOLD = 15.0   # Min jump (%) to count as a refill
        self.LIFT_OFF_RAW = reading_coaster  # Raw ADC value indicating bottle is lifted
        
        # Set the initial baseline reading
        self.last_known_percent = self.get_stable_reading()
        

    # def get_stable_reading(self):
        
    #     """Reads the ADC 5 times, averages it, and converts to a percentage."""
    #     readings = []
    #     for _ in range(5):
    #         readings.append(ADC.read(self.fsr_pin))
    #         time.sleep(0.05)
        
    #     avg_raw = sum(readings) / len(readings)
        
    #     # # This accounts for the case where the bottle is lifted off the sensor
    #     # #THIS IS LOWKEY ARBRITRARY CHANGE LATER 
    #     # if avg_raw <= self.LIFT_OFF_RAW: 
    #     #     return -1  # -1 is a flag to mean that the bottle is "lifted off"

    #     # Conversion of the raw value to a percentage 
    #     percent = ((avg_raw - self.reading_empty) / (self.reading_full - self.reading_empty)) * 100
        
    #     # Restrict the percentage to be between 0 and 100 in response to results from noise
    #     percent = max(0.0, min(100.0, percent))
    #     print(f"the current stable_reading percent is {percent}")
    #     return percent

    def get_stable_reading(self):

        
        """Reads the ADC 5 times, and averages it."""
        readings = []
        for _ in range(5):
            readings.append(ADC.read(self.fsr_pin))
            time.sleep(0.05)
        
        avg_raw = sum(readings) / len(readings)
        
        print (f'the avg_raw value is: {avg_raw}')
        print (f'the LIFT_OFF_RAW value is {self.LIFT_OFF_RAW}')
        
        # kind of an arbritrary 0.02 value but 
        if avg_raw <= self.LIFT_OFF_RAW + 0.08:
            return "N/A"

        elif avg_raw <= self.reading_empty + 0.1:
            return "empty"
        
        if avg_raw == self.reading_full:
            return "full"
        percent = max(0.0, min(100.0, percent))
        print(f"the current stable reading percent is {percent}")
        return avg_raw


    def poll_sensor(self):
        """Checks for sips, refills, and liftoffs using percentages."""
        current_percent = self.get_stable_reading()
        print(f"the current_percent is {current_percent}")
        
        # Wait until the bottle is placed back down
        if current_percent == 0.0:
            return 

        # If it was lifted off the sensor earlier, initialize it now that it's down
        if current_percent != 0.0 :
            #self.is_lifted = False  # ← Exit lifted state FIRST
            time.sleep(5.0)
            
            current_percent = self.get_stable_reading()
            if current_percent != 0.0:
                self.last_known_percent = current_percent
                print(f"Bottle down at {current_percent:.1f}%")
        
        # Only when the bottle isn't lifted do we want to take the difference 

                time.sleep(5.0)
                percent_difference = self.last_known_percent - current_percent
        
                # If there was a percent drop greater than the SIP_THRESHOLD, we count it as a sip
                if percent_difference > self.SIP_THRESHOLD:
                    self.session_drank_percent += percent_difference
                    self.daily_drank_percent += percent_difference
                    self.last_known_percent = current_percent
                    print(f"Sip detected! Drank ~{percent_difference:.1f}% of bottle.")
                print(f"the last_known_percent is {self.last_known_percent} but it should be {current_percent}")        

    
    def get_session_total(self):
        """Returns percentage drank since last hourly check."""
        return round(self.session_drank_percent, 1)

    def reset_session_total(self):
        """Resets the hourly tracker (called by main.py)."""
        self.session_drank_percent = 0.0

    def get_daily_total(self):
        """Returns the total percentage drank for the whole day."""
        return round(self.daily_drank_percent, 1)

    def reset_daily_total(self):
        """Resets the daily tracker at midnight."""
        self.daily_drank_percent = 0.0