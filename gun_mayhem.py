import pygame, random
from init import *

pygame.init()  # 게임 초기화


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
        self.sheild = 0

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
                if self.sheild == 0:
                    self.Vx += bullet.power

        self.update_x()

        for item in item_list:
            if item.overlap(self.x, self.y):
                if item.type == 'heart':
                    self.life += 1
                if item.type == 'bullet':
                    self.special_bullet += 10
                if item.type == 'shield':
                    self.shield += 60
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
                bullet_image = bullet_img
                power = 1
                if self.special_bullet > 0:
                    bullet_image = gold_bullet_img
                    power = 2
                    self.special_bullet -= 1

                if self.direction == "right":
                    stage.bullet_list.append(Bullet(bullet_image, self.x+player_width, self.y+player_height/2, 10, power))
                else:
                    stage.bullet_list.append(Bullet(bullet_image, self.x-bullet_width, self.y+player_height/2, -10, -power))

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


class Heart(Item):
    def __init__(self, img, x, y):
        super().__init__(img, 'heart', item_heart_width, item_heart_height, x, y)


class Magazine(Item):
    def __init__(self, img, x, y):
        super().__init__(img, 'bullet', item_magazine_width, item_magazine_height, x, y)


class Shield(Item):
    def __init__(self, img, x, y):
        super().__init__(img, 'shield', item_shield_width, item_shield_height, x, y)


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
                if not bullet.in_screen():
                    self.bullet_list.remove(bullet)

            item_num = random.randint(1, 1000)
            if item_num <= 1:
                self.item_list.append(Heart(item_life_img, random.randint(50, screen_width-50), 0))
            elif item_num <= 2:
                self.item_list.append(Magazine(item_bullet_img, random.randint(50, screen_width - 50), 0))
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


stage = Stage()
stage.make_board(100, 150, 310, (0, 0, 0, 0))
stage.make_board(100, 500, 400, (0, 255, 0, 0))
stage.make_board(300, 500, 350, (0, 0, 255, 0))
stage.make_board(320, 450, 320, (0, 100, 255, 40))
stage.make_player(2)
stage.run_game()
stage.game_over()

pygame.quit()

