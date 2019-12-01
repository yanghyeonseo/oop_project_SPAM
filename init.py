import pygame, random, sys

pygame.init()

screen_width, screen_height = 640, 480
player_width, player_height = 30, 47
bullet_width, bullet_height = 6, 3

item_heart_width, item_heart_height = 32, 29
item_magazine_width, item_magazine_height = 14, 12
item_shield_width, item_shield_height = 16, 16

screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 넓이 설정.
pygame.display.set_caption("Gun mayhem")    # 화면 이름 설정

FPS = 60
clock = pygame.time.Clock()  # 파이게임 모듈에 사용될 FPS 설정

key_dict = {1: [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LCTRL],
            2: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_COMMA]}

# 이미지 및 오디오 불러오기
try:
    font = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 30)

    background_img = pygame.image.load("./img/background1.png")
    bullet_img = pygame.image.load("./img/blackbullet.png")
    gold_bullet_img = pygame.image.load("./img/goldbullet.png")
    floor_img = pygame.image.load("./img/floor1.png")

    item_life_img = pygame.image.load("./img/heart1.png")
    item_bullet_img = pygame.image.load("./img/item_bullet1.png")
    item_shield_img = pygame.image.load("./img/item_shield.png")

    princess_img = pygame.image.load('./img/girlsheet.png')
    prince_img = pygame.image.load('./img/boysheet.png')
    pinky_img = pygame.image.load('./img/pinkysheet.png')
    ninja_img = pygame.image.load('./img/ninjasheet.png')
    skeleton_img = pygame.image.load('./img/skeletonsheet.png')
    special_bullet_img = pygame.image.load("./img/goldbullet.png")

    BASICFONT = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 18)  # 나눔 글씨체로 설정, 크기는 18
    BIGFONT = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 70)
    HINTFONT = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 60)
    bg = pygame.image.load("./img/startscreen.png")  # 시작 화면을 그림으로 가져옴
    mbg = pygame.image.load("./img/startscreen.png")

    pygame.mixer.music.load('./audio/bgm1.mp3')
    pygame.mixer.music.play(-1, 0.0)

except Exception as err:
    print('그림 또는 효과음 또는 글꼴 삽입에 문제가 있습니다.: ', err)
    # 에러가 발생하면 프로그램을 종료함.
    pygame.quit()
    exit(0)

player_dict = {1: prince_img, 2: princess_img, 3: pinky_img, 4: ninja_img, 5: skeleton_img}
