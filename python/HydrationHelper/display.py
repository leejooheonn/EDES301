import board
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time 

OLED_WIDTH = 128
OLED_HEIGHT = 64

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
        self.i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, self.i2c, addr=0x3C)

        # Fill with 0 and push to the screen 
    def clear_screen(self):
        self.oled.fill(0)
        self.oled.show()
    
    
    # def show_awake_pet(self):
        
    
    
    def show_happy_pet(self):
        for _ in range(6): 
            for frame in happy_frames: 
                self.oled.image(frame)
                self.oled.show()
                time.sleep(0.5)
        
        font = ImageFont.load_default()
        draw.text((35, 35), "Goal met! Meow!", font=font, fill=255)
        self.oled.image(image)
        self.oled.show()
        
        
    def show_sad_pet(self):
        for _ in range(11): 
            for frame in sad_frames:
                self.oled.image(frame)
                self.oled.show()
                time.sleep(0.5)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        draw.text((35, 35), "Goal not met :( ", font=font, fill=255)
        self.oled.image(image)
        self.oled.show()     
        
    
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
# newDisplay.write_text("hello")
# newDisplay.clear_screen()
# # newDisplay.show_sad_pet()

        
           