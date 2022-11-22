# import thư viện
from glob import glob
import threading
import pygame
import sys
import random
import time
from pygame.locals import *
# thư viện tự viết
import controller.img as IMAGE
import controller.button as button
import controller.soundButton as sbutton
import constants.obstacle as obstacle
import constants.car as car
import constants.window as window


# icon app
IMAGE.setIconApp()


# window app
WINDOW_WIDTH = window.WINDOW_WIDTH
WINDOW_HEIGHT = window.WINDOW_HEIGHT
X_MARGIN = window.X_MARGIN
LANE_WIDTH = window.LANE_WIDTH
DISTANCE = window.DISTANCE
FPS = window.FPS


# tốc độ car
CAR_WIDTH = car.CAR_WIDTH
CAR_HEIGHT = car.CAR_HEIGHT
CAR_SPEED = car.CAR_SPEED


# init OBSTACLES
# OBSTACLES_IMG = IMAGE.obstacle.redCar()
OBSTACLES_SPEED = obstacle.obstacleSpeed
CHANGE_SPEED = obstacle.changeSpeed
BG_SPEED = obstacle.backgroundSpeed


# list OBSTACLES
carListObstacle = car.carListObstacle


# list car user
carListUser =  car.carListUser
carListUserStart = car.carListUserStart


# img
BG_POSTER = IMAGE.POSTER() # Background trước ghi vào game
BG_IMG = IMAGE.BACKGROUND()
PLAY_BUTTON = IMAGE.PLAY_BUTTON()
HELP_BUTTON = IMAGE.HELP_BUTTON()
SOUND_BUTTON = IMAGE.SOUND_BUTTON()
RETURN_BUTTON = IMAGE.RETURN_BUTTON()
RELOAD_BUTTON = IMAGE.RELOAD_BUTTON()
BACK_BUTTON= IMAGE.BACK_BUTTON()
INSTRUCTION = IMAGE.INSTRUCTION()
LEFT_BUTTON = IMAGE.LEFT_BUTTON()
RIGHT_BUTTON = IMAGE.RIGHT_BUTTON()
FRAMES = IMAGE.FRAMES()  # khung chứa chọn các xe
CHOOSE_CAR = IMAGE.CHOOSE_CAR()
ONE_PLAYER = IMAGE.ONE_PLAYER()  
TWO_PLAYER = IMAGE.TWO_PLAYER()


# init app game
pygame.init()
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('HORIZON CHASE Tunbo')
fpsClock = pygame.time.Clock()


# music
pygame.mixer.music.load('./sounds/background.wav')
pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound('./sounds/explosion.wav')


# button
soundButton = sbutton.soundButton(WINDOW_WIDTH - 60, 3, SOUND_BUTTON)


# global variable
option = 0
idx1 = idx2 = 0
choosedCar1 = choosedCar2 = False
carPlayer1 = carPlayer2 = carListUserStart[0]
x1 = x2 = 0.02
playing = sleep = False
P1moveLeft = P1moveRight = P1moveUp = P1moveDown = False
P2moveLeft = P2moveRight = P2moveUp = P2moveDown = False


class Background():
    def __init__(self, img):
        self.x = 0
        self.y = 0
        self.speed = BG_SPEED
        self.img = img
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self):
        DISPLAY_SURF.blit(self.img, (int(self.x), int(self.y)))
        DISPLAY_SURF.blit(self.img, (int(self.x), int(self.y-self.height)))

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y -= self.height


class Obstacles():
    def __init__(self):
        # self.width = CAR_WIDTH
        # self.height = CAR_HEIGHT
        self.distance = DISTANCE
        self.speed = OBSTACLES_SPEED
        self.changeSpeed = CHANGE_SPEED
        self.ls = []
        for i in range(5):
            carObstacleImg = carListObstacle[random.randint(0, len(carListObstacle) - 1)]
            obstacle_width = carObstacleImg.get_width()
            obstacle_height = carObstacleImg.get_height()
            y = - obstacle_height - i * self.distance
            lane = random.randint(55, 300)
            self.ls.append([lane, y, carObstacleImg, obstacle_width, obstacle_height]) 

    def draw(self):
        for i in range(5):
            # x = int(X_MARGIN + self.ls[i][0] *
            #         LANE_WIDTH + (LANE_WIDTH-self.width)/2)
            x = int(self.ls[i][0])
            y = int(self.ls[i][1])
            # rect = [x, y, self.ls[i][3], self.ls[i][4]]
            # pygame.draw.rect(DISPLAY_SURF, (255,0,0), rect, 2)
            DISPLAY_SURF.blit(self.ls[i][2], (x, y))

    def update(self):
        for i in range(5):
            self.ls[i][1] += self.speed
        self.speed += self.changeSpeed
        if self.ls[0][1] > WINDOW_HEIGHT:
            self.ls.pop(0)
            carObstacleImg = carListObstacle[random.randint(0, len(carListObstacle) - 1)] # random xe
            obstacle_width = carObstacleImg.get_width()
            obstacle_height = carObstacleImg.get_height()
            y = self.ls[3][1] - self.distance
            lane = random.randint(55, 300)
            self.ls.append([lane, y, carObstacleImg, obstacle_width, obstacle_height]) 


class Car():
    def __init__(self, img):
        self.isAlive = True
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.img = img 
        self.x = (WINDOW_WIDTH-self.width)/2
        self.y = (WINDOW_HEIGHT-self.height)/2
        self.speed = CAR_SPEED
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))

    def draw(self):
        DISPLAY_SURF.blit(self.img, (int(self.x), int(self.y)))

    def update(self, moveLeft, moveRight, moveUp, moveDown):
        if moveLeft == True:
            self.x -= self.speed
        if moveRight == True:
            self.x += self.speed
        if moveUp == True:
            self.y -= self.speed
        if moveDown == True:
            self.y += self.speed

        if self.x < X_MARGIN:
            self.x = X_MARGIN
        if self.x + self.width > WINDOW_WIDTH - X_MARGIN:
            self.x = WINDOW_WIDTH - X_MARGIN - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.height


class Score():
    def __init__(self):
        self.score1 = 0
        self.score2 = 0

    def draw(self, option):
        font = pygame.font.SysFont('consolas', 30)
            
        scoreSuface1 = font.render(
            'Score1: '+str(int(self.score1)), True, (255, 255, 255))
        scoreSuface2 = font.render(
            'Score2: '+str(int(self.score2)), True, (255, 255, 255))            
        DISPLAY_SURF.blit(scoreSuface1, (10, 10))
        if option == 2: DISPLAY_SURF.blit(scoreSuface2, (10, 50))

    def update1(self, x1):
        self.score1 += x1

    def update2(self, x2):
        self.score2 += x2

    def getScore1(self):
        return self.score1

    def getScore2(self):
        return self.score2


def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False


def isGameOver(car, obstacles):
    carRect = [car.x, car.y, car.width - 14, car.height - 10]
    for i in range(5):
        # x = int(X_MARGIN + obstacles.ls[i][0] *
        #         LANE_WIDTH + (LANE_WIDTH-obstacles.width)/2)
        x = int(obstacles.ls[i][0])
        y = int(obstacles.ls[i][1])
        obstaclesRect = [x, y, obstacles.ls[i][3] - 10, obstacles.ls[i][4] - 10]
        if rectCollision(carRect, obstaclesRect) == True:
            if soundButton.mute == False: explosion_sound.play()
            return True
    return False


def chooseOpitons(bg):
    global option

    DISPLAY_SURF.blit(bg, (0, 0))

    option1 = button.Button(WINDOW_WIDTH / 2 - 60, WINDOW_HEIGHT / 2 - 70, ONE_PLAYER)
    option2 = button.Button(WINDOW_WIDTH / 2 - 60, WINDOW_HEIGHT / 2 - 0, TWO_PLAYER)
    option1.draw(DISPLAY_SURF)
    option2.draw(DISPLAY_SURF)

    if option1.isClicked:
        option = 1

    if option2.isClicked:
        option = 2


def chooseCar1(bg):
    global idx1
    global choosedCar1
    
    car = carListUserStart[idx1]
    playButton = button.Button(WINDOW_WIDTH/2 - 90, WINDOW_HEIGHT - 250, PLAY_BUTTON)
    leftButton = button.Button(40, 280, LEFT_BUTTON)
    rightButton = button.Button(300, 280, RIGHT_BUTTON)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    DISPLAY_SURF.blit(bg, (0, 0))
    DISPLAY_SURF.blit(FRAMES, (80, 150))
    DISPLAY_SURF.blit(carListUser[idx1], (170, 260))
    playButton.draw(DISPLAY_SURF) 
    leftButton.draw(DISPLAY_SURF)
    rightButton.draw(DISPLAY_SURF)

    if leftButton.isClicked:
        time.sleep(0.3)
        if idx1 == 0:
            idx1 = len(carListUser) - 1
        else:
            idx1 -= 1

    if rightButton.isClicked:
        time.sleep(0.3)
        if idx1 == len(carListUser) - 1:
            idx1 = 0
        else:
            idx1 += 1
    
    if playButton.isClicked:
        choosedCar1 = True
        car = carListUserStart[idx1]
    return car


def chooseCar2(bg):
    global idx2
    global choosedCar2
    
    car = carListUserStart[idx2]
    playButton = button.Button(WINDOW_WIDTH/2 - 90, WINDOW_HEIGHT - 250, PLAY_BUTTON)
    leftButton = button.Button(40, 280, LEFT_BUTTON)
    rightButton = button.Button(300, 280, RIGHT_BUTTON)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    DISPLAY_SURF.blit(bg, (0, 0))
    DISPLAY_SURF.blit(FRAMES, (80, 150))
    DISPLAY_SURF.blit(carListUser[idx2], (170, 260))
    playButton.draw(DISPLAY_SURF) 
    leftButton.draw(DISPLAY_SURF)
    rightButton.draw(DISPLAY_SURF)

    if leftButton.isClicked:
        time.sleep(0.3)
        if idx2 == 0:
            idx2 = len(carListUser) - 1
        else:
            idx2 -= 1

    if rightButton.isClicked:
        time.sleep(0.3)
        if idx2 == len(carListUser) - 1:
            idx2 = 0
        else:
            idx2 += 1
    
    if playButton.isClicked:
        choosedCar2 = True
        car = carListUserStart[idx2]
    return car


def gameStart(bg):
    global sleep
    global playing
    global carPlayer1
    global carPlayer2

    font = pygame.font.SysFont('consolas', 30)
    commentSuface = font.render('Press "space" to play', True, (0, 0, 0))
    commentSize = commentSuface.get_size()

    helpButton = button.Button(WINDOW_WIDTH - 110, 0, HELP_BUTTON)

    returnButton = button.Button(20, 160, RETURN_BUTTON)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYUP:
                if event.key == K_SPACE:   
                    playing = True
        
        DISPLAY_SURF.blit(bg, (0, 0))
      
        helpButton.draw(DISPLAY_SURF)
        soundButton.draw(DISPLAY_SURF)
        DISPLAY_SURF.blit(commentSuface, (int((WINDOW_WIDTH - commentSize[0])/2), 300))

        if helpButton.isClicked:
            DISPLAY_SURF.blit(INSTRUCTION, (-94, 40))
            returnButton.draw(DISPLAY_SURF)
            if returnButton.isClicked:
                gameStart(bg)

        if playing:
            chooseOpitons(bg)
            if option == 1:
                carPlayer1 = chooseCar1(bg)
            if option == 2:
                if choosedCar1 == False:
                    carPlayer1 = chooseCar1(bg)
                if choosedCar1 == True and sleep == False:
                    sleep = True
                    time.sleep(0.3)
                if choosedCar1 == True and sleep == True:
                    carPlayer2 = chooseCar2(bg)
                
        if choosedCar1 == True and option == 1:
            return

        if choosedCar2 == True and option == 2:
            return

        pygame.display.update()
        fpsClock.tick(FPS)


def P1Movement(events, car):
    global P1moveLeft, P1moveRight, P1moveUp, P1moveDown

    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                P1moveLeft = True
            if event.key == K_RIGHT:
                P1moveRight = True
            if event.key == K_UP:
                P1moveUp = True
            if event.key == K_DOWN:
                P1moveDown = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                P1moveLeft = False
            if event.key == K_RIGHT:
                P1moveRight = False
            if event.key == K_UP:
                P1moveUp = False
            if event.key == K_DOWN:
                P1moveDown = False
    
    car.draw()
    car.update(P1moveLeft, P1moveRight, P1moveUp, P1moveDown)


def P2Movement(events, car):
    global P2moveLeft, P2moveRight, P2moveUp, P2moveDown

    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_a:
                P2moveLeft = True
            if event.key == K_d:
                P2moveRight = True
            if event.key == K_w:
                P2moveUp = True
            if event.key == K_s:
                P2moveDown = True
        if event.type == KEYUP:
            if event.key == K_a:
                P2moveLeft = False
            if event.key == K_d:
                P2moveRight = False
            if event.key == K_w:
                P2moveUp = False
            if event.key == K_s:
                P2moveDown = False

    car.draw()
    car.update(P2moveLeft, P2moveRight, P2moveUp, P2moveDown)


def gamePlay2P(bg, car1, car2, obstacles, score):
    global P1moveLeft, P1moveRight, P1moveUp, P1moveDown
    global P2moveLeft, P2moveRight, P2moveUp, P2moveDown
    global x1, x2

    car1.__init__(carPlayer1)
    car2.__init__(carPlayer2)
    obstacles.__init__()
    bg.__init__(BG_IMG)
    score.__init__()

    P1moveLeft = P1moveRight = P1moveUp = P1moveDown = False
    P2moveLeft = P2moveRight = P2moveUp = P2moveDown = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bg.draw()
        bg.update()

        P1_thread = threading.Thread(target=P1Movement, args=(events, car1))
        P2_thread = threading.Thread(target=P2Movement, args=(events, car2))

        if car1.isAlive: 
            P1_thread.start()
            if isGameOver(car1, obstacles): 
                x1 = 0
                car1.isAlive = False

        if car2.isAlive: 
            P2_thread.start()
            if isGameOver(car2, obstacles): 
                x2 = 0
                car2.isAlive = False

        if car1.isAlive == False and car2.isAlive == False:
            return

        soundButton.draw(DISPLAY_SURF)
        obstacles.draw()
        obstacles.update()
        score.draw(option)
        score.update1(x1)
        score.update2(x2)

        pygame.display.update()
        fpsClock.tick(FPS)


def gamePlay1P(bg, car, obstacles, score):
    global P1moveLeft, P1moveRight, P1moveUp, P1moveDown
    global BG_IMG

    car.__init__(carPlayer1)
    obstacles.__init__()
    bg.__init__(BG_IMG)
    score.__init__()

    P1moveLeft = P1moveRight = P1moveUp = P1moveDown = False

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        bg.draw()
        bg.update()

        P1_thread = threading.Thread(target=P1Movement, args=(events, car))
        P1_thread.start()

        if isGameOver(car, obstacles):
            return

        soundButton.draw(DISPLAY_SURF)
        obstacles.draw()
        obstacles.update()
        score.draw(option)
        score.update1(x1)

        pygame.display.update()
        fpsClock.tick(FPS)


def gameOver(bg, score):
    global option
    global sleep
    global choosedCar1, choosedCar2
    global x1, x2

    reloadButton = button.Button(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 30, RELOAD_BUTTON)
    backButton = button.Button(WINDOW_WIDTH/2 + 5, WINDOW_HEIGHT/2 - 30, BACK_BUTTON) 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        bg.draw()
        score.draw(option)
        reloadButton.draw(DISPLAY_SURF)
        backButton.draw(DISPLAY_SURF) 

        if option == 1: DISPLAY_SURF.blit(IMAGE.GAME_OVER(), (35, 150))
        else: 
            font = pygame.font.SysFont('consolas', 30)
            if score.getScore1() > score.getScore2(): 
                win = font.render(
                'Player 1 win', True, (0, 0, 0))
            else:
                win = font.render(
                'Player 2 win ', True, (0, 0, 0))
            DISPLAY_SURF.blit(win, (100, 290))
            DISPLAY_SURF.blit(IMAGE.CUP(), (80, 80))

        # for event in pygame.event.get():
        #     if event.type == pygame.KEYUP:
        #         if event.key == K_SPACE:     
        #             return   

        if reloadButton.isClicked:
            x1 = x2 = 0.02
            return

        if backButton.isClicked:
            time.sleep(0.3)
            option = 0
            sleep = choosedCar1 = choosedCar2 = False
            x1 = x2 = 0.02
            gameStart(BG_POSTER)
            return

        pygame.display.update()
        fpsClock.tick(FPS)


def main():
    gameStart(BG_POSTER)
    bg = Background(BG_IMG)
    car1 = Car(carPlayer1)
    car2 = Car(carPlayer2)
    obstacles = Obstacles()
    score = Score()
    while True:
        if option == 1:
            gamePlay1P(bg, car1, obstacles, score)
            gameOver(bg, score)
        elif option == 2:
            gamePlay2P(bg, car1, car2, obstacles, score)
            gameOver(bg, score)

if __name__ == '__main__':
    main()