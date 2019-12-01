from init import *
from game_module import *


pygame.init()  # 게임 초기화

screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 넓이 설정.
pygame.display.set_caption("Gun mayhem")    # 화면 이름 설정


def make_text(text, font, color):  # 텍스트 생성 함수
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def make_screen(img, str = None):
    while True:
        screen.blit(img, (0, 0))  # 그림의 왼쪽 위 모서리가 (0,0)에 있음
        pressKeySurf, pressKeyRect = make_text(str, font_hint, text_color)
        pressKeyRect.center = (int(screen_width / 2), int(screen_height / 2) + 200)
        screen.blit(pressKeySurf, pressKeyRect)  # press a key to play를 화면 중앙 아래에 띄움
        pygame.display.update()
        flag = key_press()
        if flag is True:
            break
        elif flag is False:
            pygame.quit()


def key_press():  # 키를 눌렀는지 확인하는 함수
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return True
        if event.type == pygame.QUIT:
            return False
    return None


def screen_start():  # 시작 화면
    global screen

    make_screen(background1)
    make_screen(background2, 'Press a key to play.')
    make_screen(background3)
    make_screen(background4)


def character_select():
    screen.blit(character_background, (0, 0))
    pygame.display.update()
    player1_num = None
    player2_num = None
    while player1_num is None or player2_num is None:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    player1_num = 0
                if event.key == pygame.K_1:
                    player1_num = 1
                if event.key == pygame.K_2:
                    player1_num = 2
                if event.key == pygame.K_3:
                    player1_num = 3
                if event.key == pygame.K_4:
                    player1_num = 4
                if event.key == pygame.K_5:
                    player2_num = 5
                if event.key == pygame.K_6:
                    player2_num = 6
                if event.key == pygame.K_7:
                    player2_num = 7
                if event.key == pygame.K_8:
                    player2_num = 8
                if event.key == pygame.K_9:
                    player2_num = 9
    return player1_num, player2_num


def map_select():
    screen.blit(map_background, (0, 0))
    pygame.display.update()
    background_num = None
    while background_num is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    background_num = 0
                if event.key == pygame.K_2:
                    background_num = 1
                if event.key == pygame.K_3:
                    background_num = 2
    return background_num


def game_screen(player1, player2, background):
    stage.make_board(267, 382, 135, (0, 115, 157, 220))
    stage.make_board(268, 381, 210, (0, 115, 157, 220))
    stage.make_board(123, 278, 310, (0, 115, 157, 220))
    stage.make_board(368, 523, 310, (0, 115, 157, 220))
    stage.make_board(23, 150, 357, (0, 115, 157, 220))
    stage.make_board(490, 617, 357, (0, 115, 157, 220))
    stage.make_player(player1, player2)
    stage.run_game(background)
    stage.game_over()
    pygame.quit()

