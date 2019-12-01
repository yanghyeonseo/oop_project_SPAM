import pygame, random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
text_color = white

screen_width, screen_height = 640, 480
player_width, player_height = 30, 47
bullet_width, bullet_height = 6, 3

item_heart_width, item_heart_height = 14, 12
item_magazine_width, item_magazine_height = 14, 12
item_shield_width, item_shield_height = 16, 16

FPS = 60
clock = pygame.time.Clock()  # 파이게임 모듈에 사용될 FPS 설정

key_dict = {1: [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LCTRL],
            2: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_COMMA]}

# 이미지 및 오디오 불러오기
try:
    font = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 30)
    font_basic = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 18)  # 나눔 글씨체로 설정, 크기는 18
    font_big = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 70)
    font_hint = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 60)

    background1 = pygame.image.load("./image/start_screen.png")  # 시작 화면을 그림으로 가져옴
    background2 = pygame.image.load("./image/instruction.png")
    background3 = pygame.image.load("./image/instruction2.png")
    background4 = pygame.image.load("./image/gamerule.png")
    character_background = pygame.image.load("./image/characters.png")
    map_background = pygame.image.load("./image/map_selection.png")

    sasa_morning_img = pygame.image.load("./image/sasa_morning.png")
    sasa_afternoon_img = pygame.image.load("./image/sasa_background.png")
    sasa_night_img = pygame.image.load("./image/sasa_night.png")

    bullet_img = pygame.image.load("./image/bullet_normal.png")
    gold_bullet_img = pygame.image.load("./image/bullet_gold.png")

    item_life_img = pygame.image.load("./image/item_heart.png")
    item_magazine_img = pygame.image.load("./image/item_magazine.png")
    item_shield_img = pygame.image.load("./image/item_shield.png")

    princess_img = pygame.image.load('./image/sheet_girl.png')
    princess_shield_img = pygame.image.load('./image/sheet_girl_shield.png')
    prince_img = pygame.image.load('./image/sheet_prince.png')
    prince_shield_img = pygame.image.load('./image/sheet_princess_shield.png')
    pinky_img = pygame.image.load('./image/sheet_pinky.png')
    pinky_shield_img = pygame.image.load('./image/sheet_pinky_shield.png')
    ninja_img = pygame.image.load('./image/sheet_ninja.png')
    ninja_shield_img = pygame.image.load('./image/sheet_ninjn_shield.png')
    skeleton_img = pygame.image.load('./image/sheet_skeleton.png')
    skeleton_shield_img = pygame.image.load('./image/sheet_skeleton_shield.png')

    gun_sound = pygame.mixer.Sound("./audio/sound_gun.wav")
    scream_sound = pygame.mixer.Sound("./audio/sound_scream.wav")
    pop_sound = pygame.mixer.Sound("./audio/sound_pop.wav")

    pygame.mixer.music.load('./audio/bgm1.mp3')
    pygame.mixer.music.play(-1, 0.0)

except Exception as err:
    print('그림 또는 효과음 또는 글꼴 삽입에 문제가 있습니다.: ', err)
    # 에러가 발생하면 프로그램을 종료함.
    pygame.quit()
    exit(0)

player_img_dict = {1: [prince_img, prince_shield_img], 2: [princess_img, princess_shield_img],
                   3: [pinky_img, pinky_shield_img], 4: [ninja_img, ninja_shield_img],
                   5: [skeleton_img, skeleton_shield_img]}
stage_img_list = [sasa_morning_img, sasa_afternoon_img , sasa_night_img]