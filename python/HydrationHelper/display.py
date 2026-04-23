import board
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time 
import keyboard

OLED_WIDTH = 128
OLED_HEIGHT = 64
THRESHOLD = 215

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=0x3C)


#Get the frames for the happy and unhappy cats 
jumping_cat_files = [f'jumping_cat_{i}.jpeg' for i in range(1, 9)]
happy_frames = []

for name in jumping_cat_files:
    img = Image.open(name).resize((OLED_WIDTH, OLED_HEIGHT), Image.Resampling.NEAREST).convert('1')
    happy_frames.append(img)
    
crying_cat_files = [f'cat_tear_{i}.png' for i in range (1,4)]        
sad_frames = []

for name in crying_cat_files:
    img = Image.open(name).resize((OLED_WIDTH, OLED_HEIGHT), Image.Resampling.NEAREST).convert('1')
    sad_frames.append(img)
    
running_cat_files = [f'running_cat_{i}.jpeg' for i in range(1,8)]
running_frames = []

for name in running_cat_files:
    img = Image.open(name).resize((OLED_WIDTH, OLED_HEIGHT), Image.Resampling.LANCZOS)    
    img = img.point(lambda p: 255 if p > THRESHOLD else 0).convert('1')        
    running_frames.append(img)
    
# waking_cat_files =     
    
    
# lollipop_cat_image = Image.open('kid_cat.gif')
# lollipop_cat_image = lollipop_cat_image.resize((128,64), Image.Resampling.NEAREST)
# lollipop_cat_image = lollipop_cat_image.convert('1')

# oled.image(lollipop_cat_image)
# oled.show()


image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

class PetDisplay: 
    def __init__(self):
        self.pet_name = None 
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, self.i2c, addr=0x3C)

        # Fill with 0 and push to the screen 
    def clear_screen(self):
        self.oled.fill(0)
        self.oled.show()
    
    def continuous_running(self):
        #for _ in range(5):
        for frame in running_frames:
            if keyboard.is_pressed('e'):
                break
            self.oled.image(frame)
            self.oled.show()
            time.sleep(0.25)        
   
    
    def show_awake_pet(self):
        draw.text((10,32), "you woke up your pet!", font=font, fill=255)
        self.oled.image(image)
        self.oled.show()
        time.sleep(2)
        self.clear_screen()
        
        draw.text((10,32), "pet's name: ", font=font, fill=255)
        self.oled.image(image)
        self.oled.show()
        self.pet_name = input("pet's name: ")
        self.clear_screen()

        self.write_text(f"{self.pet_name} likes to run", 10, 30)
        self.write_text(f"keep {self.pet_name} hydrated!", 10, 40)
        time.sleep(3)
        self.clear_screen()

        for _ in range(3):
            self.continuous_running()    
           
   
    def show_happy_pet(self):
        for _ in range(5): 
            for frame in happy_frames: 
                self.oled.image(frame)
                self.oled.show()
                time.sleep(0.25)
        
        font = ImageFont.load_default()
        draw.text((35, 35), "Goal met! Meow!", font=font, fill=255)
        self.oled.image(image)
        self.oled.show()
        
        
    def show_sad_pet(self):
        for _ in range(5): 
            for frame in sad_frames:
                self.oled.image(frame)
                self.oled.show()
                time.sleep(0.25)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        draw.text((35, 35), "Goal not met :( ", font=font, fill=255)
        self.oled.image(image)
        self.oled.show()  
        time.sleep(5)
        self.clear_screen()
        
    
    def write_text(self, text, width, height):
        # draw = ImageDraw.Draw(image)
        # font = ImageFont.load_default()
        draw.text((width,height), text, font=font, fill=255)
        self.oled.image(image)
        self.oled.show()
    
    def clear_screen(self):
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        self.oled.image(image)
        self.oled.show()
        
    
# newDisplay = PetDisplay()
# newDisplay.show_happy_pet()
# newDisplay.show_awake_pet()

        
           