from initing import *

pygame.init()  # 게임 초기화

screen = pygame.display.set_mode((screen_width, screen_height))  # 화면 넓이 설정.
pygame.display.set_caption("Gun mayhem")    # 화면 이름 설정


class Movement:
    def __init__(self, img, width, height, x, y, Vx, Vy):
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
    def __init__(self, num, key_type):
        super().__init__(player_img_dict[num][0], player_width, player_height, screen_width / 2 - player_width / 2, -player_height, 0, 0)
        self.player_num = num
        self.key_type = key_type

        self.direction = "right"
        self.jump_cnt = 0

        self.life = 5
        self.special_bullet = 0
        self.shield = 0

        self.img_set = player_img_dict[self.player_num][0]
        self.img_set.set_clip(pygame.Rect(13, 168, 30, 47))
        self.img = self.img_set.subsurface(self.img_set.get_clip())
        self.rect = self.img.get_rect()
        self.frame = 0

        # 이동 모션 (꼭짓점, 넓이, 높이)
        self.right_states = {0: (13, 598, 30, 47), 1: (67, 598, 30, 47), 2: (120, 598, 30, 47),
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
        self.jump_states = {0: (67, 1078, 30, 47), 1: (120, 1078, 30, 47),
                            2: (175, 1078, 30, 47), 3: (120, 1078, 30, 47), 4: (67, 1078, 30, 47)}

        # 총 쏘는 모션
        self.shootl_states = {0: (8, 703, 33, 47), 1: (63, 703, 33, 47), 2: (115, 703, 33, 47),
                              3: (165, 703, 35, 47), 4: (216, 703, 37, 47), 5: (265, 703, 40, 47)}
        self.shootr_states = {0: (5, 809, 40, 48), 1: (60, 809, 40, 48), 2: (115, 809, 40, 48),
                              3: (170, 809, 40, 48), 4: (225, 809, 40, 48), 5: (280, 809, 40, 48)}
        self.action_name = ''

    def update(self, board_list, bullet_list, item_list):
        if self.shield == 0:
            self.img_set = player_img_dict[self.player_num][0]
        else:
            self.img_set = player_img_dict[self.player_num][1]

        if self.update_y(0.5, board_list):
            self.jump_cnt = 0

        if self.y > 3 * screen_height:
            scream_sound.play()
            self.life -= 1
            self.Vx, self.Vy = 0, 0
            self.x = screen_width/2 - player_width/2
            self.y = -player_height

        for bullet in bullet_list:
            if bullet.is_hit(self.x, self.y):
                if self.shield == 0:
                    self.Vx += bullet.power

        self.update_x()

        if self.shield > 0:
            self.shield -= 1
        for item in item_list:
            if item.overlap(self.x, self.y):
                pop_sound.play()
                if item.type == 'heart':
                    self.life += 1
                if item.type == 'bullet':
                    self.special_bullet += 10
                if item.type == 'shield':
                    self.shield += 600
                item.type = 'used'

    def update_sprite(self):
        if self.action_name == 'left':
            self.clip(self.left_states)
        if self.action_name == 'right':
            self.clip(self.right_states)
        if self.action_name == 'up':
            self.clip(self.jump_states)
        if self.action_name == 'down':
            self.clip(self.jump_states)
        if self.action_name == 'shoot' and self.direction == 'right':
            self.clip(self.shootr_states)
        if self.action_name == 'shoot' and self.direction == 'left':
            self.clip(self.shootl_states)

            # 정지 이벤트
        if self.action_name == 'stand_left':
            self.clip(self.left_stand)
        if self.action_name == 'stand_right':
            self.clip(self.right_stand)
        if self.action_name == 'stand_up':
            self.clip(self.jump_stand)
        if self.action_name == 'stand_down':
            self.clip(self.jump_stand)
        if self.action_name == 'stand_shoot' and self.direction == 'right':
            self.clip(self.shootr_stand)
        if self.action_name == 'stand_shoot' and self.direction == 'left':
            self.clip(self.shootl_stand)

        self.img = self.img_set.subsurface(self.img_set.get_clip())

    def choice_event(self, event):
        Vx_unit = 2
        Vy_unit = 8
        # print(event)

        if event.type == pygame.KEYDOWN:
            # 왼쪽 오른쪽
            if event.key == self.key_type[0]:
                self.direction = "left"
                self.action_name = 'left'
                self.Vx = -Vx_unit
            if event.key == self.key_type[1]:
                self.direction = "right"
                self.action_name = 'right'
                self.Vx = Vx_unit
            # 점프, 아래 통과
            if event.key == self.key_type[2]:
                if self.jump_cnt < 2:
                    self.Vy = -Vy_unit
                    self.action_name = 'up'
                    self.jump_cnt += 1
            if event.key == self.key_type[3]:
                self.action_name = 'down'
                self.y += 1
            # 총알 쏘기
            gun_sound.play()
            if event.key == self.key_type[4]:
                self.action_name = 'shoot'
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
                self.action_name = 'stand_left'
                self.Vx = 0
            if event.key == self.key_type[1]:
                self.action_name = 'stand_right'
                self.Vx = 0
            if event.key == self.key_type[2]:
                self.action_name = 'stand_up'
            if event.key == self.key_type[3]:
                self.action_name = 'stand_down'
            if event.key == self.key_type[4]:
                self.action_name = 'stand_shoot'

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
            self.img_set.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.img_set.set_clip(pygame.Rect(clipped_rect))
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


class Heart(Item):
    def __init__(self, x, y):
        super().__init__(item_life_img, 'heart', item_heart_width, item_heart_height, x, y)


class Magazine(Item):
    def __init__(self, x, y):
        super().__init__(item_magazine_img, 'bullet', item_magazine_width, item_magazine_height, x, y)


class Shield(Item):
    def __init__(self, x, y):
        super().__init__(item_shield_img, 'shield', item_shield_width, item_shield_height, x, y)


class Stage:
    def __init__(self):
        self.img = []
        self.board_list = []
        self.player_list = []
        self.bullet_list = []
        self.item_list = []

    def make_board(self, x1, x2, y, color):
        self.board_list.append(Board(x1, x2, y, color))

    def make_player(self, player1, player2):
        self.player_list.append(Player(player1+1, key_dict[1]))
        self.player_list.append(Player(player2-4, key_dict[2]))

    def run_game(self, background):
        running = True

        while running:
            screen.fill((0, 0, 0))  # 화면을 색칠함.
            screen.blit(stage_img_list[background], (0, 0))

            info1_life = font.render("생명: {}".format(self.player_list[0].life), True, (28, 0, 0))
            info2_life = font.render("생명: {}".format(self.player_list[1].life), True, (28, 0, 0))
            screen.blit(info1_life, (20, 20))
            screen.blit(info2_life, (530, 20))

            info1_bullet = font.render("총알: {}".format(self.player_list[0].special_bullet), True, (28, 0, 0))
            info2_bullet = font.render("총알: {}".format(self.player_list[1].special_bullet), True, (28, 0, 0))
            screen.blit(info1_bullet, (20, 60))
            screen.blit(info2_bullet, (530, 60))

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
                player.update_sprite()
                screen.blit(player.img, (player.x, player.y))

            for bullet in self.bullet_list:
                bullet.update()
                screen.blit(bullet.img, (bullet.x, bullet.y))
                if not bullet.in_screen():
                    self.bullet_list.remove(bullet)

            item_num = random.randint(1, 1000)
            if item_num <= 1:
                self.item_list.append(Heart(random.randint(50, screen_width-50), 0))
            elif item_num <= 2:
                self.item_list.append(Magazine(random.randint(50, screen_width - 50), 0))
            elif item_num <= 3:
                self.item_list.append(Shield(random.randint(50, screen_width - 50), 0))
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
                winner = 'Player {}'.format(i + 1)

        running = True
        text1 = font.render("Game Over".format(self.player_list[0].life), True, (28, 0, 0))
        text2 = font.render("{} WIN!!".format(winner), True, (28, 0, 0))
        screen.blit(text1, (225, 150))
        screen.blit(text2, (205, 200))
        pygame.display.flip()

        while running:
            events = pygame.event.get()
            for event in events:
                # 게임 종료조건, 우측 상단에 X 버튼 누르면 pygame 모듈과 프로그램이 종료되는 코드
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(FPS)  # 다음 와일문으로 넘어감. loop


stage = Stage()
