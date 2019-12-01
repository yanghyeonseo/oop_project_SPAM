import pygame, random, sys
from pygame.locals import *

pygame.init()  # 게임 초기화

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXTCOLOR = WHITE

screen_width, screen_height = 640, 480
player_width, player_height = 40, 48
bullet_width, bullet_height = 6, 5

item_life_width, item_life_height = 32, 29
item_bullet_width, item_bullet_height = 15, 15

screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 넓이 설정.
pygame.display.set_caption("Gun mayhem")    # 화면 이름 설정

FPS = 60
clock = pygame.time.Clock()  # 파이게임 모듈에 사용될 FPS 설정

key_dict = {1: [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LCTRL],
            2: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_COMMA]}

# 이미지 및 오디오 불러오기
try:
    font = pygame.font.Font('./font/NanumSquareRoundEB.ttf', 30)

    background_img = pygame.image.load("./img/sasabackground.png")
    bullet_img = pygame.image.load("./img/bullet1.png")
    floor_img = pygame.image.load("./img/floor1.png")
    item_life_img = pygame.image.load("./img/heart1.png")
    item_bullet_img = pygame.image.load("./img/item_bullet1.png")
    
    princess_img = pygame.image.load('./img/girlsheet.png')
    prince_img = pygame.image.load('./img/boysheet.png')
    pinky_img = pygame.image.load('./img/pinkysheet.png')
    ninja_img = pygame.image.load('./img/ninjasheet.png')
    skeleton_img = pygame.image.load('./img/skeletonsheet.png')

    pygame.mixer.music.load('./audio/bgm1.mp3')
    pygame.mixer.music.play(-1, 0.0)

except Exception as err:
    print('그림 또는 효과음 또는 글꼴 삽입에 문제가 있습니다.: ', err)
    # 에러가 발생하면 프로그램을 종료함.
    pygame.quit()
    exit(0)

player_dict = {1: prince_img, 2: princess_img, 3: pinky_img, 4: ninja_img, 5: skeleton_img}

class Movement:
    def __init__(self, img, width, height, x, y, Vx, Vy):
        self.img_set = img
        self.img = img
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.Vx = Vx
        self.Vy = Vy

    def update_y(self, g, board_list):
        for board in board_list:
            if board.is_on(self.width, self.height, self.x, self.y, self.Vy):
                self.Vy = 0
                self.y = board.y - self.height
                return True

        self.y += self.Vy
        self.Vy += g
        return False

    def update_x(self):
        self.x += self.Vx

    def in_screen(self):
        return -self.width < self.x < screen_width and -self.height < self.y < screen_height


class Player(Movement):
    def __init__(self, img, key_type):
        super().__init__(img, player_width, player_height, screen_width/2-player_width/2, -player_height, 0, 0)
        self.key_type = key_type

        self.direction = "right"
        self.jump_cnt = 0

        self.life = 5
        self.special_bullet = 0

        self.sheet = img
        self.sheet.set_clip(pygame.Rect(13, 168, 30, 47))
        self.img = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.img.get_rect()
        self.frame = 0

        # 이동 모션 (꼭짓점, 넓이, 높이)
        self.right_states ={0: (13, 598, 30, 47), 1: (67, 598, 30, 47), 2: (120, 598, 30, 47),
                            3: (175, 598, 30, 47), 4: (229, 598, 30, 47), 5: (281, 598, 30, 47),
                            6: (335, 598, 30, 47), 7: (387, 598, 30, 47), 8: (439, 598, 30, 47)}

        self.left_states = {0: (10, 490, 30, 47), 1: (64, 490, 30, 47), 2: (117, 490, 30, 47),
                            3: (172, 490, 30, 47), 4: (226, 490, 30, 47), 5: (278, 490, 30, 47),
                            6: (332, 490, 30, 47), 7: (384, 490, 30, 47), 8: (436, 490, 30, 47)}
        
        # 정지 모션
        self.right_stand = (13, 598, 30, 47)
        self.left_stand = (17, 62, 30, 47)
        self.jump_stand = (13, 1078, 30, 47)
        self.shootl_stand = (8, 703, 33, 47)
        self.shootr_stand = (5, 809, 40, 48)

        # 뛰는 모션
        self.jump_states = {0:(67, 1078, 30, 47), 1:(120, 1078, 30, 47),
                            2:(175, 1078, 30, 47), 3:(120, 1078, 30, 47), 4:(67, 1078, 30, 47)}

        # 총 쏘는 모션
        self.shootl_states ={0: (8, 703, 33, 47), 1: (63, 703, 33, 47), 2: (115, 703, 33, 47),
                            3: (165, 703, 35, 47), 4: (216, 703, 37, 47), 5: (265, 703, 40, 47)}
        self.shootr_states ={0: (5, 809, 40, 48), 1: (60, 809, 40, 48), 2: (115, 809, 40, 48),
                            3: (170, 809, 40, 48), 4: (225, 809, 40, 48), 5: (280, 809, 40, 48)}
        self.event_name = ''
        
    def update(self, board_list, bullet_list, item_list):
        if self.update_y(0.5, board_list):
            self.jump_cnt = 0

        if self.y > 3 * screen_height:
            self.life -= 1
            self.Vx, self.Vy = 0, 0
            self.x = screen_width/2 - player_width/2
            self.y = -player_height

        for bullet in bullet_list:
            if bullet.is_hit(self.x, self.y):
                if bullet.Vx > 0:
                    self.Vx += bullet.power
                else:
                    self.Vx -= bullet.power

        self.update_x()

        for item in item_list:
            if item.overlap(self.x, self.y):
                if item.type == 'heart':
                    self.life += 1
                if item.type == 'bullet':
                    self.special_bullet += 10
                item.type = 'used'

        if self.event_name == 'left':
            self.clip(self.left_states)
        if self.event_name == 'right':
            self.clip(self.right_states)
        if self.event_name == 'up':
            self.clip(self.jump_states)
        if self.event_name == 'down':
            self.clip(self.jump_states)
        if self.event_name == 'shoot' and self.direction == 'right':
            self.clip(self.shootr_states)
        if self.event_name == 'shoot' and self.direction == 'left':
            self.clip(self.shootl_states)
        
            # 정지 이벤트
        if self.event_name == 'stand_left':
            self.clip(self.left_stand)
        if self.event_name == 'stand_right':
            self.clip(self.right_stand)
        if self.event_name == 'stand_up':
            self.clip(self.jump_stand)
        if self.event_name == 'stand_down':
            self.clip(self.jump_stand)
        if self.event_name == 'stand_shoot' and self.direction == 'right':
            self.clip(self.shootr_stand)
        if self.event_name == 'stand_shoot' and self.direction == 'left':
            self.clip(self.shootl_stand)
        
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        
    def choice_event(self, event):
        Vx_unit = 2
        Vy_unit = 8

        if event.type == pygame.KEYDOWN:
            # 왼쪽 오른쪽
            if event.key == self.key_type[0]:
                self.direction = "left"
                self.event_name = 'left'
                self.Vx = -Vx_unit
            if event.key == self.key_type[1]:
                self.direction = "right"
                self.event_name = 'right'
                self.Vx = Vx_unit
            # 점프, 아래 통과
            if event.key == self.key_type[2]:
                if self.jump_cnt < 2:
                    self.Vy = -Vy_unit
                    self.event_name = 'up'
                    self.jump_cnt += 1
            if event.key == self.key_type[3]:
                self.event_name = 'down'
                self.y += 1
            # 총알 쏘기
            if event.key == self.key_type[4]:
                self.event_name = 'shoot'
                power = 1
                if self.special_bullet > 0:
                    power = 2
                    self.special_bullet -= 1

                if self.direction == "right":
                    stage.bullet_list.append(Bullet(bullet_img, self.x+player_width, self.y+5, 10, power))
                else:
                    stage.bullet_list.append(Bullet(bullet_img, self.x-bullet_width, self.y+5, -10, power))

        if event.type == pygame.KEYUP:
            if event.key == self.key_type[0]:
                self.event_name = 'stand_left'
                self.Vx = 0
            if event.key == self.key_type[1]:
                self.event_name = 'stand_right'
                self.Vx = 0
            if event.key == self.key_type[2]:
                self.event_name = 'stand_up'
            if event.key == self.key_type[3]:
                self.event_name = 'stand_down'
            if event.key == self.key_type[4]:
                self.event_name = 'stand_shoot'

    def get_frame(self, frame_set):
        # frame_set : 스프래드의 위치를 받아놓은 dict
        # 스프레드의 프레임에 해당하는 위치를 준 다음
        # 프레임을 업데이트 해주는 함수
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        # clipped_rect : 잘라낼 위치를 저장한 데이터
        # 스프레드로 주어진 이미지에서 지금 사용할 이미지를 잘라내주는 함수
        # clipped_rect 가 위치데이터의 dict면 get_frame으로
        # 알맞은 위치를 가져온다.
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
    
class Board:
    def __init__(self, x1, x2, y, color):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.color = color

    def draw(self):
        d = 5
        pygame.draw.rect(screen, self.color, [self.x1, self.y, self.x2-self.x1, d])

    def is_on(self, w, h, p_x, p_y, p_Vy):
        return self.x1-w < p_x < self.x2 and self.y - p_Vy <= p_y + h <= self.y


class Bullet(Movement):
    def __init__(self, img, x, y, Vx, power):
        super().__init__(img, bullet_width, bullet_height, x, y, Vx, 0)
        self.power = power

    def update(self):
        self.update_x()

    def is_hit(self, p_x, p_y):
        return self.x+self.width-player_width < p_x < self.x+self.width and self.y - player_height < p_y < self.y + self.height


class Item(Movement):
    def __init__(self, img, type, width, height, x, y):
        super().__init__(img, width, height, x, y, 0, 0)
        self.type = type

    def update(self, board_list):
        self.update_y(0.05, board_list)

    def overlap(self, p_x, p_y):
        return self.x - self.width - player_width < p_x < self.x + self.width and self.y - player_height < p_y < self.y + self.height
        # if p_x + player_width / 2 < self.x - self.width / 2 or p_x - player_width / 2 > self.x + self.width / 2 or p_y + player_height / 2 < self.y - self.height / 2 or p_y - player_height / 2 > self.y + self.height / 2:
        #     return False
        # return True


class Heart(Item):
    def __init__(self, img, x, y):
        super().__init__(img, 'heart', item_life_width, item_life_height, x, y)


class Special_bullet(Item):
    def __init__(self, img, x, y):
        super().__init__(img, 'bullet', item_bullet_width, item_bullet_height, x, y)


class Stage:
    def __init__(self):
        self.img = background_img
        self.board_list = []
        self.player_list = []
        self.bullet_list = []
        self.item_list = []

    def make_board(self, x1, x2, y, color):
        self.board_list.append(Board(x1, x2, y, color))

    def make_player(self, player1, player2):
        self.player_list.append(Player(player_dict[player1+1], key_dict[1]))
        self.player_list.append(Player(player_dict[player2-4], key_dict[2]))

    def run_game(self):
        running = True

        while running:
            screen.fill((0, 0, 0))  # 화면을 색칠함.
            screen.blit(background_img, (0, 0))

            P1_life = font.render("생명: {}".format(self.player_list[0].life), True, (28, 0, 0))
            P2_life = font.render("생명: {}".format(self.player_list[1].life), True, (28, 0, 0))
            screen.blit(P1_life, (20, 20))
            screen.blit(P2_life, (530, 20))

            P1_bullet = font.render("총알: {}".format(self.player_list[0].special_bullet), True, (28, 0, 0))
            P2_bullet = font.render("총알: {}".format(self.player_list[1].special_bullet), True, (28, 0, 0))
            screen.blit(P1_bullet, (20, 60))
            screen.blit(P2_bullet, (530, 60))

            for board in self.board_list:
                board.draw()

            events = pygame.event.get()
            for player in self.player_list:
                if player.life <= 0:
                    running = False

                for event in events:
                    # 게임 종료조건, 우측 상단에 X 버튼 누르면 pygame 모듈과 프로그램이 종료되는 코드
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    player.choice_event(event)

                player.update(self.board_list, self.bullet_list, self.item_list)
                screen.blit(player.image, (player.x, player.y))

            for bullet in self.bullet_list:
                bullet.update()
                screen.blit(bullet.img, (bullet.x, bullet.y))
                if not bullet.in_screen():
                    self.bullet_list.remove(bullet)

            item_num = random.randint(1, 1000)
            if item_num <= 1:
                self.item_list.append(Heart(item_life_img, random.randint(50, screen_width-50), 0))
            elif item_num <= 2:
                self.item_list.append(Special_bullet(item_bullet_img, random.randint(50, screen_width-50), 0))
            for item in self.item_list:
                if item.type == 'used' or not item.in_screen():
                    self.item_list.remove(item)
                else:
                    item.update(self.board_list)
                    screen.blit(item.img, (item.x, item.y))

            clock.tick(FPS)  # 다음 와일문으로 넘어감. loop
            pygame.display.flip()

    def game_over(self):
        winner = ''
        for i in range(len(self.player_list)):
            if self.player_list[i].life > 0:
                winner = 'Player {}'.format(i+1)

        running = True
        while running:
            screen.fill((0, 0, 0))  # 화면을 색칠함.
            screen.blit(background_img, (0, 0))

            text1 = font.render("Game Over".format(self.player_list[0].life), True, (28, 0, 0))
            text2 = font.render("{} WIN!!".format(winner), True, (28, 0, 0))
            screen.blit(text1, (225, 150))
            screen.blit(text2, (205, 200))

            P1_life = font.render("생명: {}".format(self.player_list[0].life), True, (28, 0, 0))
            P2_life = font.render("생명: {}".format(self.player_list[1].life), True, (28, 0, 0))
            screen.blit(P1_life, (20, 20))
            screen.blit(P2_life, (530, 20))

            P1_bullet = font.render("총알: {}".format(self.player_list[0].special_bullet), True, (28, 0, 0))
            P2_bullet = font.render("총알: {}".format(self.player_list[1].special_bullet), True, (28, 0, 0))
            screen.blit(P1_bullet, (20, 60))
            screen.blit(P2_bullet, (530, 60))

            events = pygame.event.get()
            for event in events:
                # 게임 종료조건, 우측 상단에 X 버튼 누르면 pygame 모듈과 프로그램이 종료되는 코드
                if event.type == pygame.QUIT:
                    running = False

            for board in self.board_list:
                board.draw()

            for player in self.player_list:
                screen.blit(player.img_set, (player.x, player.y))

            for bullet in self.bullet_list:
                if bullet.in_screen():
                    screen.blit(bullet.img, (bullet.x, bullet.y))

            for item in self.item_list:
                if item.type != 'used':
                    screen.blit(item.img, (item.x, item.y))

            clock.tick(FPS)  # 다음 와일문으로 넘어감. loop
            pygame.display.flip()
            
def main():  # 시작 화면
    global DISPLAYSURF, BASICFONT, BIGFONT, HINTFONT
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((screen_width, screen_height))
    BASICFONT = pygame.font.Font('./font/nanum.ttf', 18)  # 나눔 글씨체로 설정, 크기는 18
    BIGFONT = pygame.font.Font('./font/nanum.ttf', 70)
    HINTFONT = pygame.font.Font('./font/nanum.ttf', 60)
    bg = pygame.image.load("./img/startscreen.png")  # 시작 화면을 그림으로 가져옴
    pygame.display.set_caption('Gun Mayhem')  # 창의 제목 설정
    DISPLAYSURF.blit(bg, (0, 0))  # 그림의 왼쪽 위 모서리가 (0,0)에 있음
    while checkForKeyPress() == None:
        pygame.display.update()  # 키보드를 누르면 다음 화면으로 넘어감
    while True:
        mainScreen()

def mainScreen():  # 시작 화면
    bg = pygame.image.load("./img/instruction.png")
    DISPLAYSURF.blit(bg, (0, 0))
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', HINTFONT, TEXTCOLOR)
    pressKeyRect.center = (int(screen_width / 2), int(screen_height / 2) + 200)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)  # press a key to play를 화면 중앙 아래에 띄움
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        instruction()

def instruction():  # 시작 화면
    bg = pygame.image.load("./img/instruction2.png")
    DISPLAYSURF.blit(bg, (0, 0))
    while checkForKeyPress() == None:
        pygame.display.update()
    while True:
        p1,p2 = characterSelectScreen()
        GameScreen(p1,p2)


def characterSelectScreen():
    bg = pygame.image.load("./img/character.png")
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

def GameScreen(player1,player2):
    stage = Stage()
    stage.make_board(267, 382, 135, (0, 115, 157, 220))
    stage.make_board(268, 381, 210, (0, 115, 157, 220))
    stage.make_board(123, 278, 310, (0, 115, 157, 220))
    stage.make_board(368, 523, 310, (0, 115, 157, 220))
    stage.make_board(23, 150, 357, (0, 115, 157, 220))
    stage.make_board(490, 617, 357, (0, 115, 157, 220))
    stage.make_player(player1, player2)
    stage.run_game()
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
