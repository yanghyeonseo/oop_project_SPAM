from initing import *
from game_module import *
from pygame.locals import *

pygame.init()  # 게임 초기화


def main():  # 시작 화면
    global DISPLAYSURF, BASICFONT, BIGFONT, HINTFONT
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Gun Mayhem')  # 창의 제목 설정
    DISPLAYSURF.blit(bg, (0, 0))  # 그림의 왼쪽 위 모서리가 (0,0)에 있음
    while checkForKeyPress() == None:
        pygame.display.update()  # 키보드를 누르면 다음 화면으로 넘어감
    while True:
        mainScreen()


def mainScreen():  # 시작 화면
    bg = pygame.image.load("./image/instruction.png")
    DISPLAYSURF.blit(bg, (0, 0))
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', font_hint, text_color)
    pressKeyRect.center = (int(screen_width / 2), int(screen_height / 2) + 200)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)  # press a key to play를 화면 중앙 아래에 띄움
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        instruction()


def instruction():  # 시작 화면
    bg = pygame.image.load("./image/instruction2.png")
    DISPLAYSURF.blit(bg, (0, 0))
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        gameRule()
        
def gameRule():  # 시작 화면
    bg = pygame.image.load("./image/gamerule.png")
    DISPLAYSURF.blit(bg, (0, 0))
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        p1, p2 = characterSelectScreen()
        background = mapSelectScreen()
        GameScreen(p1, p2, background)


def gameRule():  # 시작 화면
    bg = pygame.image.load("./image/gamerule.png")
    DISPLAYSURF.blit(bg, (0, 0))
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        p1, p2 = characterSelectScreen()
        background = mapSelectScreen()
        GameScreen(p1, p2, background)


def characterSelectScreen():
    bg = pygame.image.load("./image/characters.png")
    DISPLAYSURF.blit(bg, (0, 0))
    pygame.display.update()
    p1 = None
    p2 = None
    while p1 is None or p2 is None:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == K_0:
                    p1 = 0
                if event.key == K_1:
                    p1 = 1
                if event.key == K_2:
                    p1 = 2
                if event.key == K_3:
                    p1 = 3
                if event.key == K_4:
                    p1 = 4
                if event.key == K_5:
                    p2 = 5
                if event.key == K_6:
                    p2 = 6
                if event.key == K_7:
                    p2 = 7
                if event.key == K_8:
                    p2 = 8
                if event.key == K_9:
                    p2 = 9
    return p1, p2


def mapSelectScreen():
    DISPLAYSURF.blit(mbg, (0, 0))
    pygame.display.update()
    background = None
    while background is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_1:
                    background = 0
                if event.key == K_2:
                    background = 1
                if event.key == K_3:
                    background = 2
    return background


def GameScreen(player1, player2, background):
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


def makeTextObjs(text, font, color):  # 텍스트 생성 함수
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def checkForKeyPress():  # 키를 눌렀는지 확인하는 함수
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


if __name__ == '__main__':
    main()
