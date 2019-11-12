import pygame
# import random

pygame.init()  # 게임 초기화

screen_width, screen_height = 640, 480
player_width, player_height = 25, 50
bullet_width, bullet_height = 1, 1

screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 넓이 설정.
pygame.display.set_caption("Gun mayhem")    # 화면 이름 설정

FPS = 60
clock = pygame.time.Clock()  # 파이게임 모듈에 사용될 FPS 설정

key_dict = {1: [pygame.K_d, pygame.K_g, pygame.K_r, pygame.K_f, pygame.K_LSHIFT],
            2: [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_COMMA]}

# 이미지 및 오디오 불러오기
try:
    background_img = pygame.image.load("./img/background1.png")
    player_img = pygame.image.load("./img/player1.png")
    bullet_img = pygame.image.load("./img/bullet1.png")
    floor_img = pygame.image.load("./img/floor1.png")

    pygame.mixer.music.load('./audio/bgm1.mp3')
    pygame.mixer.music.play(-1, 0.0)

except Exception as err:
    print('그림 또는 효과음 삽입에 문제가 있습니다.: ', err)
    # 에러가 발생하면 프로그램을 종료함.
    pygame.quit()
    exit(0)


class Player:
    def __init__(self, key_type):
        self.img_set = player_img
        self.key_type = key_type

        self.x = screen_width/2-player_width/2      # 중심 기준
        self.y = player_height/2                    # 중심 기준
        self.Vx = 0
        self.Vy = 0
        self.direction = "right"
        self.jump_cnt = 0

    def update(self, board_list, bullet_list):
        g = 0.5
        on_board = False
        for board in board_list:
            if board.is_on(self.x, self.y, self.Vy):
                self.Vy = 0
                self.y = board.y - player_height/2
                on_board = True
                self.jump_cnt = 0
        if on_board is False:
            self.y += self.Vy
            self.Vy += g

        for bullet in bullet_list:
            if bullet.is_hit(self.x, self.y):
                if bullet.Vx > 0:
                    self.Vx += bullet.power
                else:
                    self.Vx -= bullet.power

        self.x += self.Vx

    def choice_event(self, event):
        Vx_unit = 2
        Vy_unit = 10
        # print(event)

        if event.type == pygame.KEYDOWN:
            # 왼쪽 오른쪽
            if event.key == self.key_type[0]:
                self.direction = "left"
                self.Vx = -Vx_unit
            if event.key == self.key_type[1]:
                self.direction = "right"
                self.Vx = Vx_unit
            # 점프, 아래 통과
            if event.key == self.key_type[2]:
                if self.jump_cnt < 2:
                    self.Vy = -Vy_unit
                    self.jump_cnt += 1
            if event.key == self.key_type[3]:
                self.y += 1
            # 총알 쏘기
            if event.key == self.key_type[4]:
                if True:
                    if self.direction == "right":
                        stage.bullet_list.append(Bullet(self.x+player_width, self.y, 10, 1))
                    else:
                        stage.bullet_list.append(Bullet(self.x-player_width, self.y, -10, 1))

        if event.type == pygame.KEYUP:
            if event.key == self.key_type[0]:
                self.Vx = 0
            if event.key == self.key_type[1]:
                self.Vx = 0


class Board:
    def __init__(self, x1, x2, y, color):
        self.x1 = x1
        self.x2 = x2
        self.y = y
        self.color = color

    def draw(self):
        d = 5
        pygame.draw.rect(screen, self.color, [self.x1, self.y, self.x2-self.x1, d])

    def is_on(self, p_x, p_y, p_Vy):
        return self.x1-player_width/2 < p_x < self.x2+player_width/2 and self.y - p_Vy <= p_y + player_height/2 <= self.y


class Bullet:
    def __init__(self, x, y, Vx, power):
        self.img = bullet_img
        self.x = x
        self.y = y
        self.Vx = Vx
        self.power = power

    def update(self):
        self.x += self.Vx

    def is_hit(self, p_x, p_y):
        return p_x-player_width/2 < self.x < p_x+player_width/2 and p_y-player_height/2 < self.y < p_y+player_height/2


class Stage:
    def __init__(self):
        self.img = background_img
        self.board_list = []
        self.player_list = []
        self.bullet_list = []

    def make_board(self, x1, x2, y, color):
        self.board_list.append(Board(x1, x2, y, color))

    def make_player(self, num):
        for i in range(1, num+1):
            self.player_list.append(Player(key_dict[i]))

    def run_game(self):
        running = True

        while running:
            screen.fill((0, 0, 0))  # 화면을 색칠함.
            screen.blit(background_img, (0, 0))

            for board in self.board_list:
                board.draw()

            events = pygame.event.get()
            for player in self.player_list:
                print(events)
                for event in events:
                    # 게임 종료조건, 우측 상단에 X 버튼 누르면 pygame 모듈과 프로그램이 종료되는 코드
                    if event.type == pygame.QUIT:
                        running = False
                    player.choice_event(event)

                player.update(self.board_list, self.bullet_list)
                screen.blit(player.img_set, (player.x, player.y))

            for bullet in self.bullet_list:
                bullet.update()
                screen.blit(bullet.img, (bullet.x, bullet.y))

            clock.tick(FPS)  # 다음 와일문으로 넘어감. loop
            pygame.display.flip()


stage = Stage()
stage.make_board(100, 150, 50, (0, 0, 0, 0))
stage.make_board(100, 500, 400, (0, 255, 0, 0))
stage.make_board(300, 500, 350, (0, 0, 255, 0))
stage.make_board(320, 450, 200, (0, 100, 255, 40))
stage.make_player(2)
stage.run_game()

pygame.quit()

