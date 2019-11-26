import pygame, random

pygame.init()  # 게임 초기화

screen_width, screen_height = 640, 480
player_width, player_height = 25, 50
bullet_width, bullet_height = 1, 1

item_life_width, item_life_height = 50, 50
item_bullet_width, item_bullet_height = 25, 25

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
    player_img = pygame.image.load("./img/player1.png")
    bullet_img = pygame.image.load("./img/bullet1.png")
    floor_img = pygame.image.load("./img/floor1.png")
    item_life_img = pygame.image.load("./img/heart1.png")
    item_bullet_img = pygame.image.load("./img/item_bullet1.png")

    pygame.mixer.music.load('./audio/bgm1.mp3')
    pygame.mixer.music.play(-1, 0.0)

except Exception as err:
    print('그림 또는 효과음 또는 글꼴 삽입에 문제가 있습니다.: ', err)
    # 에러가 발생하면 프로그램을 종료함.
    pygame.quit()
    exit(0)


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
                self.y = board.y - self.height / 2
                return True

        self.y += self.Vy
        self.Vy += g
        return False

    def update_x(self):
        self.x += self.Vx


class Player(Movement):
    def __init__(self, img, key_type):
        super().__init__(img, player_width, player_height, screen_width/2-player_width/2, player_height/2, 0, 0)
        self.key_type = key_type

        self.direction = "right"
        self.jump_cnt = 0

        self.life = 5
        self.special_bullet = 0

    def update(self, board_list, bullet_list, item_list):
        if self.update_y(0.5, board_list):
            self.jump_cnt = 0

        if self.y > 3 * screen_height:
            self.life -= 1
            self.Vx, self.Vy = 0, 0
            self.x = screen_width/2 - player_width/2
            self.y = -player_height/2

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
                    self.special_bullet += 30
                item.type = 'used'

    def choice_event(self, event):
        Vx_unit = 2
        Vy_unit = 8
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
                        stage.bullet_list.append(Bullet(bullet_img, self.x+player_width, self.y, 10, 0.5))
                    else:
                        stage.bullet_list.append(Bullet(bullet_img, self.x-player_width, self.y, -10, 0.5))

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

    def is_on(self, w, h, p_x, p_y, p_Vy):
        return self.x1-w/2 < p_x < self.x2+w/2 and self.y - p_Vy <= p_y + h/2 <= self.y


class Bullet(Movement):
    def __init__(self, img, x, y, Vx, power):
        super().__init__(img, bullet_width, bullet_height, x, y, Vx, 0)
        self.power = power

    def update(self):
        self.update_x()

    def is_hit(self, p_x, p_y):
        return p_x-player_width/2 < self.x < p_x+player_width/2 and p_y-player_height/2 < self.y < p_y+player_height/2


class Item(Movement):
    def __init__(self, img, type, width, height, x, y):
        super().__init__(img, width, height, x, y, 0, 0)
        self.type = type

    def update(self, board_list):
        self.update_y(0.05, board_list)

    def overlap(self, p_x, p_y):
        if p_x + player_width / 2 < self.x - self.width / 2 or p_x - player_width / 2 > self.x + self.width / 2 or p_y + player_height / 2 < self.y - self.height / 2 or p_y - player_height / 2 > self.y + self.height / 2:
            return False
        return True


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

    def make_player(self, num):
        for i in range(1, num+1):
            self.player_list.append(Player(player_img, key_dict[i]))

    def run_game(self):
        running = True

        while running:
            screen.fill((0, 0, 0))  # 화면을 색칠함.
            screen.blit(background_img, (0, 0))

            P1_life = font.render("생명: {}".format(self.player_list[0].life), True, (28, 0, 0))
            P2_life = font.render("생명: {}".format(self.player_list[1].life), True, (28, 0, 0))
            screen.blit(P1_life, (20, 20))
            screen.blit(P2_life, (530, 20))

            for board in self.board_list:
                board.draw()

            events = pygame.event.get()
            for player in self.player_list:
                if player.life <= 0:
                    running = False

                print(events)
                for event in events:
                    # 게임 종료조건, 우측 상단에 X 버튼 누르면 pygame 모듈과 프로그램이 종료되는 코드
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    player.choice_event(event)

                player.update(self.board_list, self.bullet_list, self.item_list)
                screen.blit(player.img_set, (player.x, player.y))

            for bullet in self.bullet_list:
                bullet.update()
                screen.blit(bullet.img, (bullet.x, bullet.y))

            item_num = random.randint(1, 1000)
            if item_num <= 1:
                self.item_list.append(Heart(item_life_img, random.randint(50, screen_width-50), 0))
            elif item_num <= 2:
                self.item_list.append(Special_bullet(item_bullet_img, random.randint(50, screen_width-50), 0))
            for item in self.item_list:
                if item.type != 'used':
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
                screen.blit(bullet.img, (bullet.x, bullet.y))

            for item in self.item_list:
                if item.type != 'used':
                    screen.blit(item.img, (item.x, item.y))

            clock.tick(FPS)  # 다음 와일문으로 넘어감. loop
            pygame.display.flip()


stage = Stage()
stage.make_board(267, 382, 135, (0, 115, 157, 220))
stage.make_board(268, 381, 210, (0, 115, 157, 220))
stage.make_board(123, 278, 310, (0, 115, 157, 220))
stage.make_board(368, 523, 310, (0, 115, 157, 220))
stage.make_board(23, 150, 357, (0, 115, 157, 220))
stage.make_board(490, 617, 357, (0, 115, 157, 220))
stage.make_player(2)
stage.run_game()
stage.game_over()

pygame.quit()

