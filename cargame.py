import pygame
import random
import io
import cv2
import os
import time
from threading import Thread

start_time = time.time()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
carState = 2
score1 = 0

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set the height and width of the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

player_img = pygame.image.load('rszcarPack.png').convert()
block_img = pygame.image.load('game_obstacle.png').convert()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/kenan/Documents/packHacks.json"

camera_port = 0


def get_image():
    camera = cv2.VideoCapture(camera_port)
    # time.sleep(0.01)
    return_value, image = camera.read()
    cv2.imwrite("face.png", image)


def text_objects(text, font):
    screen = font.render(text, True, WHITE)
    return screen, screen.get_rect()


def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 20)
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
    while (True):
        global carState
        faceDegree = get_angle()
        if faceDegree != None:
            if (faceDegree < -20):
                if carState < 3:
                    car.rect.x += screen_width / 3
                    carState += 1
            elif (faceDegree > 20):
                if carState > 1:
                    car.rect.x -= screen_width / 3
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

        self.image = block_img
        self.rect = self.image.get_rect()

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

block_list = pygame.sprite.Group()

# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

objectW = 100
objectH = 50

state1x = screen_width / 6 - objectW / 2
state2x = screen_width / 2 - objectW / 2
state3x = 5 * screen_width / 6 - objectW / 2

stateArr = [state1x, state2x, state3x]

block = Block(GREEN, objectW, objectH)

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

    BackGround = Background('rszroad.png', [0, 0])
    screen.fill([255, 255, 255])
    screen.blit(BackGround.image, BackGround.rect)
    # screen.fill(GREEN)

    pygame.draw.rect(screen, BLACK, ((screen_width / 3) - 5, 0, 10, screen_height))
    pygame.draw.rect(screen, BLACK, ((2 * screen_width / 3) - 5, 0, 10, screen_height))

    if (pygame.sprite.collide_rect(car, block)):
        print("Collision has occurred!")
        done = True

    block.rect.y += 8.5

    if (block.rect.y >= screen_height):
        currentState = random.randint(0, 2)
        state = stateArr[currentState]
        block.rect.y = -objectH
        block.rect.x = state
        score1 = score1 + 1

    print(score)
    message_display("Score: " + str(score1))
    # pygame.display.update()

    all_sprites_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
quit()
