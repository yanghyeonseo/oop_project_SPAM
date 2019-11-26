import pygame,random 
from time import sleep

BLACK = (0, 0, 0)  # 게임 바탕화면의 색상
RED = (255, 0, 0)
pad_width = 480  # 게임화면의 가로 크기
pad_height = 640  # 게임화면의 세로 크기

class GameCharacter:
    def __init__(self, position):
        self.sheet = pygame.image.load('girlsheet.png')
        self.sheet.set_clip(pygame.Rect(13, 168, 30, 47))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.frame = 0
        self.dir = 'right'
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
        self.attack_motion_number = 0


    def update(self):
        # 현재 해당하는 event_name 에 맞추어 event를 실행하는 함수
        # 이동 이벤트
        if self.event_name == 'left':
            self.clip(self.left_states)
            self.rect.x -= 5
        if self.event_name == 'right':
            self.clip(self.right_states)
            self.rect.x += 5
        if self.event_name == 'up':
            self.clip(self.jump_states)
            self.rect.y -= 5
        if self.event_name == 'down':
            self.clip(self.jump_states)
            self.rect.y += 5
        if self.event_name == 'shoot' and self.dir == 'right':
            self.clip(self.shootr_states)
        if self.event_name == 'shoot' and self.dir == 'left':
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
        if self.event_name == 'stand_shoot' and self.dir == 'right':
            self.clip(self.shootr_stand)
        if self.event_name == 'stand_shoot' and self.dir == 'left':
            self.clip(self.shootl_stand)
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.event_name = 'left'
                self.dir = 'left'
            if event.key == pygame.K_RIGHT:
                self.event_name = 'right'
                self.dir = 'right'
            if event.key == pygame.K_UP:
                self.event_name = 'up'
            if event.key == pygame.K_DOWN:
                self.event_name = 'down'
            if event.key == pygame.K_COMMA:
                self.event_name = 'shoot'

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.event_name = 'stand_left'
            if event.key == pygame.K_RIGHT:
                self.event_name = 'stand_right'
            if event.key == pygame.K_UP:
                self.event_name = 'stand_up'
            if event.key == pygame.K_DOWN:
                self.event_name = 'stand_down'
            if event.key == pygame.K_COMMA:
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

class Princess(GameCharacter):
    def __init__(self, position):
        super().__init__(position)
        self.sheet = pygame.image.load('girlsheet.png')
        self.sheet.set_clip(pygame.Rect(13, 168, 30, 47))

class Prince(GameCharacter):
    def __init__(self, position):
        super().__init__(position)
        self.sheet = pygame.image.load('boysheet.png')
        self.sheet.set_clip(pygame.Rect(13, 168, 30, 47))

class Pinky(GameCharacter):
    def __init__(self, position):
        super().__init__(position)
        self.sheet = pygame.image.load('pinkysheet.png')
        self.sheet.set_clip(pygame.Rect(13, 168, 30, 47))

class Ninja(GameCharacter):
    def __init__(self, position):
        super().__init__(position)
        self.sheet = pygame.image.load('ninjasheet.png')
        self.sheet.set_clip(pygame.Rect(13, 168, 30, 47))

class Skeleton(GameCharacter):
    def __init__(self, position):
        super().__init__(position)
        self.sheet = pygame.image.load('skeletonsheet.png')
        self.sheet.set_clip(pygame.Rect(13, 168, 30, 47))

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Python/Pygame Animation")
clock = pygame.time.Clock()
player = Ninja((150, 150))

game_over = False

while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        player.handle_event(event)

    player.update()
    screen.fill(pygame.Color('white'))
    screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(10)

pygame.quit()
