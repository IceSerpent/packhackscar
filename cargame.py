import pygame
import random
import io
import cv2
import os
import time
import math
from threading import Thread

start_time = time.time()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
carState = 2

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set the height and width of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])


player_img = pygame.image.load('rszcar.png').convert()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/Pranav/Desktop/Vision API Test/car.json"

camera_port = 0

def get_image():
    camera = cv2.VideoCapture(camera_port)
    # time.sleep(0.01)
    return_value, image = camera.read()
    cv2.imwrite("face.png", image)

def text_objects(text, font):
    screen = font.render(text, True, BLACK)
    return screen, screen.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (65, 65)
    screen.blit(TextSurf, TextRect)
    # pygame.display.update()


def roll(path):
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    for face in faces:
        return face.roll_angle


def get_angle():
    get_image()
    return roll("face.png")

def faceUpdate():
    while(True):
        global carState
        faceDegree = get_angle()
        if faceDegree != None:
            if(faceDegree < -20):
                if carState < 3:
                    car.rect.x += screen_width/3
                    carState += 1
            elif(faceDegree > 20):
                if carState > 1:
                    car.rect.x -= screen_width/3
                    carState -= 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)


class Block(pygame.sprite.Sprite):

    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its size. """

        super().__init__()
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

objectW = 100
objectH = 50

state1x = screen_width/6 - objectW/2
state2x = screen_width/2 - objectW/2
state3x = 5*screen_width/6 - objectW/2

stateArr = [state1x, state2x, state3x]

block = Block(BLACK, objectW, objectH)

currentState = random.randint(0, 2)
state = stateArr[currentState]
block.rect.y = -objectH
block.rect.x = state

# block.rect.x = state1x
# block.rect.y = -objectH

block_list.add(block)
all_sprites_list.add(block)

# Test

car = Player()
car.rect.x = 365
car.rect.y = 450
all_sprites_list.add(car)

done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

score = 0

t1 = Thread(target=faceUpdate)
t1.start()

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_LEFT:
        #         if carState > 1:
        #             if get_angle()
        #             car.rect.x -= screen_width/3
        #             carState -= 1
        #     if event.key == pygame.K_RIGHT:
        #         if carState < 3:
        #             car.rect.x += screen_width/3
        #             carState += 1


    # faceUpdate()
    score = time.time() - start_time
    print("Score: " + str(score))
    
    screen.fill(GREEN)

    pygame.draw.rect(screen, BLACK, ((screen_width / 3) - 5, 0, 10, screen_height))
    pygame.draw.rect(screen, BLACK, ((2 * screen_width / 3) - 5, 0, 10, screen_height))

    if(pygame.sprite.collide_rect(car,block)):
        print("Collision has occurred!")
        done = True

    block.rect.y += 3.5

    if(block.rect.y >= screen_height):
        currentState = random.randint(0,2)
        state = stateArr[currentState]
        block.rect.y = -objectH
        block.rect.x = state
        score = score + 1

    print(score)
    message_display(str(math.floor(score)))
    # pygame.display.update()

    all_sprites_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
quit()
