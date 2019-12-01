import random, pygame, sys
from pygame.locals import *

WINDOWWIDTH = 640 # 화면의 넓이는 640 픽셀
WINDOWHEIGHT = 480  # 화면의 높이는 480 픽셀

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXTCOLOR = WHITE


def main():  # 시작 화면
    global DISPLAYSURF, BASICFONT, BIGFONT, HINTFONT
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('nanum.ttf', 18)  # 나눔 글씨체로 설정, 크기는 18
    BIGFONT = pygame.font.Font('nanum.ttf', 70)
    HINTFONT = pygame.font.Font('nanum.ttf', 60)
    bg = pygame.image.load("startscreen.png")  # 시작 화면을 그림으로 가져옴
    pygame.display.set_caption('Candy Baseball')  # 창의 제목 설정
    DISPLAYSURF.blit(bg, (0, 0))  # 그림의 왼쪽 위 모서리가 (0,0)에 있음
    while checkForKeyPress() == None:
        pygame.display.update()  # 키보드를 누르면 다음 화면으로 넘어감
    while True:
        mainScreen()

def mainScreen():  # 시작 화면
    bg = pygame.image.load("instruction.png")
    DISPLAYSURF.blit(bg, (0, 0))
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', HINTFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 200)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)  # press a key to play를 화면 중앙 아래에 띄움
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        instruction()

def instruction():  # 시작 화면
    bg = pygame.image.load("instruction2.png")
    DISPLAYSURF.blit(bg, (0, 0))
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        a,b = characterSelectScreen()
    print(a,b)


def characterSelectScreen():
    bg = pygame.image.load("character.png")
    DISPLAYSURF.blit(bg, (0, 0))
    pygame.display.update()
    p1 = None
    p2 = None
    while p1 is None or p2 is None:
        for event in pygame.event.get():
            if event.type  == pygame.KEYDOWN:
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


