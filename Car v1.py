import sys
import pygame
import random
from time import sleep

# 게임 화면 크기
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800

# 색상
RED = (255,0,0)
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (150, 150, 150)

# 이미지 파일이 들어있는 경로를 변수로 초기화

DIRCARS = "cars/"

DIRSOUND = "sound/"

# 기본 변수
STAGE = 1
OIL_CK = 2
CAR_COUNT = 5
SCORE = 0
BESTSCORE = 0
STAGESCORE = 0
STAGESTAIR = 300

# 플레이어 Life 갯수

PNUMBER = 5

# 자동차 오브젝트를 저장할 List

CARS = []

# 오일 오브젝트를 저장할 List
OILS = []


class Car:
    # 이미지 파일명을 저장해놓은 List
    car_image = ['Car01.png', 'Car02.png', 'Car03.png', 'Car04.png', 'Car05.png',
                 'Car06.png', 'Car07.png', 'Car08.png', 'Car09.png', 'Car10.png',
                 'Car11.png', 'Car12.png', 'Car13.png', 'Car14.png', 'Car15.png',
                 'Car16.png', 'Car17.png', 'Car18.png', 'Car19.png', 'Car20.png',
                 'Car21.png', 'Car22.png', 'Car23.png', 'Car24.png', 'Car25.png',
                 'Car26.png', 'Car27.png', 'Car28.png', 'Car29.png', 'Car30.png',
                 'Car31.png', 'Car32.png', 'Car33.png', 'Car34.png', 'Car35.png',
                 'Car36.png', 'Car37.png', 'Car38.png', 'Car39.png', 'Car40.png']

    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.rect = ""

    def load_car(self, p = ""):
        if p == "p":
            # 플레이어 차량
            self.image = pygame.image.load(DIRCARS + "Player.png")
            # 크기 조정
            self.image = pygame.transform.scale(self.image, (40, 102))
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
        else:
            # 상대방 자동차

            # 40개의 이미지중에서 랜덤으로 선택한다.
            self.image = pygame.image.load(DIRCARS + random.choice(self.car_image))
            self.rect = self.image.get_rect()


            # 이미지 크기 조절 - 이미지마다 크기가 다 다르므로 가로 세로 비율 유지하면서 변경
            if self.rect.width <= 55:
                carwidth = self.rect.width - 15
                carheight = round((self.rect.height * carwidth) / self.rect.width)
            else:
                carwidth = self.rect.width
                carheight = self.rect.height

            self.image = pygame.transform.scale(self.image, (carwidth, carheight))
            self.rect.width = carwidth
            self.rect.height = carheight

            # 생성 위치 - 스크린 크기 안에서 랜덤으로 x 좌표 생성. y 좌표는 스크린 밖 위에 생성
            self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -50)


            # STAGE에 따른 속도 변화, STAGE가 높아짐에 따라 자동차의 속도도 빨라진다.

            # 다양한 속도차이를 위해 5 ~ speed 사이에세 랜덤으로 속도를 선택하게 한다.
            speed = STAGE + 15
            if speed > 30:
                speed = 15
            self.dy = random.randint(5, speed)

     # 오일 이미지 및 생성위치, 오일 떨어지는 속도 지정하는 함수       
    def load_oil(self):
        self.image = pygame.image.load(DIRCARS + "oil.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -50)
        self.dy = 5

    # 자동차를 스크린에 그리기

    def draw_car(self):
        SCREEN.blit(self.image, [self.rect.x, self.rect.y])
        
        
    # x 좌표 이동 - 플레이어 자동차의 움직임 제어할 때 필요

    def move_x(self):
        self.rect.x += self.dx
        

    # y 좌표 이동 - 플레이어 자동차의 움직임 제어할 때 필요,

    def move_y(self):
        self.rect.y += self.dy

    # 화면 밖으로 못 나가게 방지

    def check_screen(self):
        if self.rect.right > WINDOW_WIDTH or self.rect.x < 0:
            self.rect.x -= self.dx
        if self.rect.bottom > WINDOW_HEIGHT or self.rect.y < 0:
            self.rect.y -= self.dy

    # 차량 충돌 감지
    # distance : 오른쪽, 왼쪽, 아래쪽, 위쪽 이미지의 간격 설정

    def check_collision(self, car, distance = 0):
        if (self.rect.top + distance < car.rect.bottom) and (car.rect.top < self.rect.bottom - distance) and (self.rect.left + distance < car.rect.right) and (car.rect.left < self.rect.right - distance):
            return True
        else:
            return False
        
    
def draw_main_menu():
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_intro = pygame.image.load('PyCar.png')
    SCREEN.blit(image_intro, [draw_x, draw_y - 280])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render("PyCar: Racing Car Game",True, BLACK)
    SCREEN.blit(text_title,[draw_x, draw_y])
    score_text = font_40.render("Score:" + str(SCORE), True, WHITE)
    SCREEN.blit(score_text,[draw_x,draw_y + 70])
    bestscore_text = font_40.render("Best Score : " + str(BESTSCORE), True, WHITE)
    SCREEN.blit(bestscore_text,[draw_x,draw_y + 105])
    text_start = font_30.render("Press Space Key to Start!", True, RED)
    SCREEN.blit(text_start, [draw_x, draw_y + 140])
    pygame.display.flip()
    
def draw_score():
    # SCORE 기록
    font_01 = pygame.font.SysFont("FixedSsy", 30, True, False)
    text_score = font_01.render("Score : " + str(SCORE), True, BLACK)
    SCREEN.blit(text_score, [15, 15])

    # STAGE 기록
    text_stage = font_01.render("STAGE : " + str(STAGE), True, BLACK)
    # 화면 가운데 위치
    text_stage_rect = text_stage.get_rect()
    text_stage_rect.centerx = round(WINDOW_WIDTH / 2)
    SCREEN.blit(text_stage, [text_stage_rect.x, 15])

    # 플레이어 Life 기록
    for i in range(PNUMBER):
        # 5개는 그림으로
        if i < 5:
            pimage = pygame.image.load(DIRCARS + 'Player.png')
            pimage = pygame.transform.scale(pimage, (15, 38))
            px = WINDOW_WIDTH - 20 - (i * 30)
            SCREEN.blit(pimage, [px, 15])
        # 5개가 넘으면 숫자로 표현해준다.
        else:
            text_pnumber = font_01.render("+" + str(PNUMBER - 5), True, WHITE)
            text_pnumber_x = WINDOW_WIDTH - 30 - (5 * 30)
            SCREEN.blit(text_pnumber, [text_pnumber_x, 25])

def increase_score():
    global SCORE, STAGE, STAGESCORE, BESTSCORE

    # 점수 10점 추가

    SCORE += 10
    
    # 베스트 스코어를 설정
    if SCORE >= BESTSCORE:
        BESTSCORE = SCORE

    # STAGE별 증가율을 위한 stair 값 설정
    if STAGE == 1:
        stair = STAGESTAIR
    else:
        stair = (STAGE - 1) * STAGESTAIR

    # 스테이지 별 증가율에 따른 STAGE 증가
    if SCORE >= STAGESCORE + stair:
        STAGE += 1
        STAGESCORE = STAGESCORE + stair

def main():
    global SCREEN, CAR_COUNT, WINDOW_WIDTH, WINDOW_HEIGHT, PNUMBER, SCORE, BESTSCORE, OIL_CK, STAGE, STAGESCORE, STAGESTAIR

    # pygame 초기화 및 스크린 생성

    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                     pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
    pygame.display.set_caption("Racing Car Game")
    # 투명 아이콘은 32 x 32 로 해야 적용 됨
    windowicon = pygame.image.load(DIRCARS + 'icon.png').convert_alpha()
    pygame.display.set_icon(windowicon)

    clock = pygame.time.Clock()

    #게임 사운드
    pygame.mixer.music.load(DIRSOUND + 'background.ogg')
    sound_crash = pygame.mixer.Sound(DIRSOUND + 'crash.ogg')
    sound_engine = pygame.mixer.Sound(DIRSOUND + 'engine.ogg')
    sound_oil = pygame.mixer.Sound(DIRSOUND + 'oil.ogg')

    # 플레이어 자동차 생성
    player = Car(round(WINDOW_WIDTH / 2), round(WINDOW_HEIGHT - 150), 0, 0)
    player.load_car("p")

    # 1번째 도로 차선 생성
    lanes_1 = []
    lane_width = 10
    lane_height = 80
    lane_margin = 20
    lane_count = 10
    lane_x = (WINDOW_WIDTH - lane_width) / 3
    lane_y = -10
    for i in range(lane_count):
        lanes_1.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    # 2번째 도로 차선 생성   
    lanes_2 = []
    lane_width = 10
    lane_height = 80
    lane_margin = 20
    lane_count = 10
    lane_x = WINDOW_WIDTH - (WINDOW_WIDTH - lane_width) / 3
    lane_y = -10
    for i in range(lane_count):
        lanes_2.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    # 설정한 수 만큼 자동차 오브젝트 생성하여 CARS 리스트에 넣기

    for i in range(CAR_COUNT):
        car = Car(0, 0, 0, 0)
        car.load_car()
        CARS.append(car)
    # 오일 오브젝트 생성하여 OILS 리스트에 넣기
    oil = Car()
    oil.load_oil()
    OILS.append(oil)
    

    playing = True
    score = 0
    collision = True
    PNUMBER = 5

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
                pygame.quit()
                sys.exit()

            #게임 다시 시작
            if collision:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    collision = False
                    for i in range(CAR_COUNT):
                        CARS[i].x = random.randrange(0, WINDOW_WIDTH-CARS[i].rect.width)
                        CARS[i].y = random.randrange(-150, -50)
                        CARS[i].load_car()
                    #게임 재시작시 초기 설정으로 돌리기위한 변수 초기화
                    player.x = 175
                    player.y = -150
                    player.dx = 0
                    SCORE = 0
                    STAGESCORE = 0
                    STAGESTAIR = 300
                    STAGE = 1
                    OIL_CK = 2
                    PNUMBER = 5
                    pygame.mouse.set_visible(False)
                    sound_engine.play()
                    sleep(1)
                    pygame.mixer.music.play(-1)

             # 화살표 키를 이용해서 플레이어의 움직임 거리를 조정해준다.
             # 키를 떼면 움직임 거리를 0으로 한다.

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.dx = 5
                elif event.key == pygame.K_LEFT:
                    player.dx = -5

                if event.key == pygame.K_DOWN:
                    player.dy = 5
                elif event.key == pygame.K_UP:
                    player.dy = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.dx = 0
                elif event.key == pygame.K_LEFT:
                    player.dx = 0

                if event.key == pygame.K_DOWN:
                    player.dy = 0
                elif event.key == pygame.K_UP:
                    player.dy = 0

        # 배경색을 회색으로
        SCREEN.fill(GRAY)

        ''' 게임 코드 작성 '''
        #게임 화면 출력
        if not collision:
            # 도로 차선 그리는 부분
            for i in range(lane_count):
                pygame.draw.rect(SCREEN, WHITE, [lanes_1[i][0], lanes_1[i][1], lane_width, lane_height])
                lanes_1[i][1] += 10  # 도로 차선 속도
                if lanes_1[i][1] > WINDOW_HEIGHT:
                    lanes_1[i][1] = -40 - lane_height
                    
            for i in range(lane_count):
                pygame.draw.rect(SCREEN, WHITE, [lanes_2[i][0], lanes_2[i][1], lane_width, lane_height])
                lanes_2[i][1] += 10  # 도로 차선 속도
                if lanes_2[i][1] > WINDOW_HEIGHT:
                    lanes_2[i][1] = -40 - lane_height
            # 플레이어를 스크린에 표시 및 화면 밖으로 못 벗어나게 하기
            player.draw_car()
            player.move_x()
            player.move_y()
            player.check_screen()  

            # 스테이지 가 올라갈 때마다 오일 하나씩 생성
            if STAGE == OIL_CK: # 현재 스테이지와 OIL_CK 값이 같을경우
                OILS[0].draw_car() # 오일을 그린다.
                OILS[0].rect.y += OILS[0].dy # 오일이 떨어질수 있게 오일의 y좌표값을 점점추가하여 떨어지듯 표현
                
                if player.check_collision(OILS[0]): # 오일이 플레이어와 충돌할시
                    PNUMBER += 1 # 플레이어 목숨 +1
                    OIL_CK += 1 # OIL_CK를 +1 하여 다음스테이지 에 오일이 나올수 있도록 값 초기화
                    OILS[0].load_oil() # 오일 load
                if OILS[0].rect.y > WINDOW_HEIGHT: # 오일이 화면 아래로 지나갔을경우
                    OIL_CK += 1 # OIL_CK를 +1 하여 다음스테이지 에 오일이 나올수 있도록 값 초기화
                    OILS[0].load_oil() # 오일 load
            # 다른 자동차들 도로위에 움직이기
            for i in range(CAR_COUNT):
                CARS[i].draw_car()
                CARS[i].rect.y += CARS[i].dy

                # 화면 아래로 내려가면 자동차를 다시 로드한다.
                # 로드시 자동차의 이미지가 랜덤으로 바뀌므로 새로운 자동차가 생긴 듯한 효과가 있다.
                if CARS[i].rect.y > WINDOW_HEIGHT:
                    increase_score()
                    CARS[i].load_car()

                    # 플레이어와 다른 차량 충돌 감지
            for i in range(CAR_COUNT):
                if player.check_collision(CARS[i], 5):
                    PNUMBER -= 1
                    # 부딪쳤을 경우 상대방 차량 튕겨나게 함. 좌우 튕김
                    if player.rect.x > CARS[i].rect.x:
                        CARS[i].rect.x -= CARS[i].rect.width + 10
                    else:
                        CARS[i].rect.x += CARS[i].rect.width + 10

                    # 위 아래 튕김
                    if player.rect.y > CARS[i].rect.y:
                        CARS[i].rect.y -= 30
                    else:
                        CARS[i].rect.y += 30

            # 상대 자동차들끼리 충돌 감지, 각 자동차들을 순서대로 서로 비교
            for i in range(CAR_COUNT):
                for j in range(i + 1, CAR_COUNT):
                    # 충돌 후 서로 팅겨 나가게 함.
                    if CARS[i].check_collision(CARS[j]):
                        # 왼쪽에 있는 차는 왼쪽으로 오른쪽 차는 오른쪽으로 튕김
                        if CARS[i].rect.x > CARS[j].rect.x:
                            CARS[i].rect.x += 4
                            CARS[j].rect.x -= 4
                        else:
                            CARS[i].rect.x -= 4
                            CARS[j].rect.x += 4

                        # 위쪽 차는 위로, 아래쪽차는 아래로 튕김
                        if CARS[i].rect.y > CARS[j].rect.y:
                            CARS[i].rect.y += CARS[i].dy
                            CARS[j].rect.y -= CARS[j].dy
                        else:
                            CARS[i].rect.y -= CARS[i].dy
                            CARS[j].rect.y += CARS[j].dy

            # 레이싱 카 충돌사고 체크
            for i in range(CAR_COUNT):
                if PNUMBER <= 0:
                    collision = True
                    pygame.mixer.music.stop()
                    sound_crash.play()
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break

            ''' 게임 코드 끝 '''

            draw_score()
            pygame.display.flip()
        else:
            draw_main_menu()

        # 초당 프레임 설정
        clock.tick(60)
        
pygame.quit()


if __name__ == '__main__':
    main()
