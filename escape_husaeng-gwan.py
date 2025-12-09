import pygame
import sys
import math
import random

# 초기화
pygame.init()

# 화면 설정
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("후생관 탈출기")
clock = pygame.time.Clock()

# --- 이미지 로드 ---
# (파일 경로가 정확해야 합니다)
gamecover_img = pygame.image.load("image/gamecover.png")
credit_img = pygame.image.load("image/credit.png")
floor_img = pygame.image.load("image/floor.png")
floor2_img = pygame.image.load("image/floor2.png")
desk_img = pygame.image.load("image/desk.png")
reddoor_img = pygame.image.load("image/reddoor.png")
bluedoor_img = pygame.image.load("image/bluedoor.png")
clock_img = pygame.image.load("image/clock1.png")
clock_flipped_img = pygame.image.load("image/clock_flipped.png")
locker_img = pygame.image.load("image/metal_locker1.png")
locker_opened_img = pygame.image.load("image/locker_opened.png")
locker_abnormal_img = pygame.image.load("image/locker_abnormal.png")
chair_img = pygame.image.load("image/chair.png")
chair2_img = pygame.image.load("image/chair2.png")
paper_img = pygame.image.load("image/paper.png")
trash_img = pygame.image.load("image/trash1.png")
trash_full_img = pygame.image.load("image/trash2.png")
blackboard_img = pygame.image.load("image/blackboard1.png")
blackboard2_img = pygame.image.load("image/blackboard2.png")
kyotak_img = pygame.image.load("image/kyotak.png")
hint_img = pygame.image.load("image/hint.png")
blood_img = pygame.image.load("image/blood1.png")
info_text_img = pygame.image.load("image/info_text.png")
reading_paper = pygame.image.load("image/reading_paper.png")
ending_bg_img = pygame.image.load("image/ending_bg.png")
ending_paper_img = pygame.image.load("image/ending_paper.png")

wall_imgs = [
    pygame.image.load("image/wall_top.png"),
    pygame.image.load("image/wall_bottom.png"),
    pygame.image.load("image/wall_left.png"),
    pygame.image.load("image/wall_right.png"),
    pygame.image.load("image/wall_corner.png"),
    pygame.image.load("image/wall_top_bottom.png")
]

player_imgs = {
    "up": [pygame.image.load("image/mychr0.png"), pygame.image.load("image/mychr1.png")],
    "down": [pygame.image.load("image/mychr2.png"), pygame.image.load("image/mychr3.png")],
    "left": [pygame.image.load("image/mychr4.png"), pygame.image.load("image/mychr5.png")],
    "right": [pygame.image.load("image/mychr6.png"), pygame.image.load("image/mychr7.png")]
}

player_idle_imgs = {
    "up": pygame.image.load("image/mychr8.png"),
    "down": pygame.image.load("image/mychr9.png"),
    "left": pygame.image.load("image/mychr10.png"),
    "right": pygame.image.load("image/mychr11.png")
}

# --- 사운드 로드 ---
footstep_sound = pygame.mixer.Sound("audio/Footstep_sound.ogg")
door_sound = pygame.mixer.Sound("audio/Open_door.ogg")
schoolbell_sound = pygame.mixer.Sound("audio/schoolbell.ogg")
schoolbell_horror_sound = pygame.mixer.Sound("audio/schoolbell_horror4.ogg")
Book_reading_sound = pygame.mixer.Sound("audio/Book_reading_sound.ogg")
main_sound = pygame.mixer.Sound("audio/main_sound4_23s.ogg")
last_door_sound = pygame.mixer.Sound("audio/last_door_open.ogg")
footstep_run_sound = pygame.mixer.Sound("audio/footstep_run.ogg")
night_sound = pygame.mixer.Sound("audio/night_sound.ogg")

schoolbell_horror_sound.set_volume(0.5)
last_door_sound.set_volume(0.8)
footstep_run_sound.set_volume(0.8)

# --- 이미지 크기 조정 ---
gamecover_img = pygame.transform.scale(gamecover_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
credit_img = pygame.transform.scale(credit_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
floor_img = pygame.transform.scale(floor_img, (64, 64))
floor2_img = pygame.transform.scale(floor2_img, (64, 64))
desk_img = pygame.transform.scale(desk_img, (100, 64))
reddoor_img = pygame.transform.scale(reddoor_img, (80, 128))
bluedoor_img = pygame.transform.scale(bluedoor_img, (80, 128))
clock_img = pygame.transform.scale(clock_img, (60, 60))
clock_flipped_img = pygame.transform.scale(clock_flipped_img, (60, 60))
locker_img = pygame.transform.scale(locker_img, (80, 128))
locker_opened_img = pygame.transform.scale(locker_opened_img, (80, 128))
locker_abnormal_img = pygame.transform.scale(locker_abnormal_img, (80, 128))
trash_img = pygame.transform.scale(trash_img, (64, 64))
trash_full_img = pygame.transform.scale(trash_full_img, (64, 64))
chair_img = pygame.transform.scale(chair_img, (150, 64))
chair2_img = pygame.transform.scale(chair2_img, (80, 64))
paper_img = pygame.transform.scale(paper_img, (30, 30))
blackboard_img = pygame.transform.scale(blackboard_img, (400, 120))
blackboard2_img = pygame.transform.scale(blackboard2_img, (400, 120))
kyotak_img = pygame.transform.scale(kyotak_img, (150, 80))
hint_img = pygame.transform.scale(hint_img, (40, 40))
blood_img = pygame.transform.scale(blood_img, (64, 64))
info_text_img = pygame.transform.scale(info_text_img, (140, 70))
reading_paper = pygame.transform.scale(reading_paper, (800, 800))
ending_bg_img = pygame.transform.scale(ending_bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
ending_paper_img = pygame.transform.scale(ending_paper_img, (500, 600))

for i in range(len(wall_imgs)):
    wall_imgs[i] = pygame.transform.scale(wall_imgs[i], (64, 64))

for direction in player_imgs:
    for i in range(2):
        player_imgs[direction][i] = pygame.transform.scale(player_imgs[direction][i], (48, 64))

for direction in player_idle_imgs:
    player_idle_imgs[direction] = pygame.transform.scale(player_idle_imgs[direction], (48, 64))

# --- 게임 변수 및 맵 설정 ---
target_chair_index = -1

# 맵 데이터 복구 (추정값)
game_map = (
    [[1] * 22] +
    [[1] * 22] +
    [[1] * 22] +
    [[1] + [0] * 20 + [1] for _ in range(15)] +
    [[1] * 22]
)

desk_pos = [
    (3, 6), (4.3, 6), (7, 6), (8.3, 6), (12, 6), (13.3, 6), (16, 6), (17.3, 6),
    (3, 9), (4.3, 9), (7, 9), (8.3, 9), (12, 9), (13.3, 9), (16, 9), (17.3, 9),
    (3, 12), (4.3, 12), (7, 12), (8.3, 12), (12, 12), (13.3, 12), (16, 12), (17.3, 12),
    (3, 15), (4.3, 15), (7, 15), (8.3, 15), (12, 15), (13.3, 15), (16, 15), (17.3, 15)
]

chair_pos = [
    (2.7, 6.5), (4.0, 6.5), (6.7, 6.5), (8.0, 6.5), (11.7, 6.5), (13.0, 6.5), (15.7, 6.5), (17.0, 6.5),
    (2.7, 9.5), (4.0, 9.5), (6.7, 9.5), (8.0, 9.5), (11.7, 9.5), (13.0, 9.5), (15.7, 9.5), (17.0, 9.5),
    (2.7, 12.5), (4.0, 12.5), (6.7, 12.5), (8.0, 12.5), (11.7, 12.5), (13.0, 12.5), (15.7, 12.5), (17.0, 12.5),
    (2.7, 15.5), (4.0, 15.5), (6.7, 15.5), (8.0, 15.5), (11.7, 15.5), (13.0, 15.5), (15.7, 15.5), (17.0, 15.5)
]

red_door_pos = [(5, 2)]
blue_door_pos = [(15, 2)]
hint_pos = (18, 2)
clock_pos = (10.2, 0)
locker_pos = [(1, 1.8), (2, 1.8)]
trash_pos = (3, 2.8)
trash_full_pos = (3, 2.8)
paper_pos = (3.2, 15.3)
paper_offset_x = 20
paper_offset_y = -10
blackboard_pos = (7.5, 1)
kyotak_pos = (9.7, 4)

# 충돌 영역 설정
paper_rect = pygame.Rect(int(paper_pos[0] * 64), int(paper_pos[1] * 64), 60, 60)
hint_rect = pygame.Rect(int(hint_pos[0] * 64), int(hint_pos[1] * 64), 40, 40)
trash_rect = pygame.Rect(int(trash_pos[0] * 64), int(trash_pos[1] * 64), 50, 17)
kyotak_rects = [pygame.Rect(int(kyotak_pos[0] * 64 + 10), int(kyotak_pos[1] * 64 + 10), 130, 35)]
desk_rects = [pygame.Rect(int(x * 64 + 20), int(y * 64 + 10), 55, 25) for (x, y) in desk_pos]
locker_rects = [pygame.Rect(int(x * 64), int(y * 64), 64, 80) for (x, y) in locker_pos]

wall_rects = []
for y, row in enumerate(game_map):
    for x, tile in enumerate(row):
        if tile == 1:
            wall_rects.append(pygame.Rect(x * 64, y * 64, 64, 30))

locker_states = [False] * len(locker_pos)

# 플레이어 변수
player_x = 220
player_y = 1000
player_speed = 4
player_dir = "up"
anim_frame = 0
anim_timer = 0
is_walking_sound = False
is_reading_paper = False
is_reading_hint = False

game_start_time = pygame.time.get_ticks()
hint_read_count = 0

# 조명/페이드 변수
LIGHT_RADIUS = 200
LIGHT_FADE = 100
DARKNESS_COLOR = (0, 0, 0, 230)
current_mask_radius = 0
start_delay_timer = 0

fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
fade_surface.fill((0, 0, 0))
timer_for_info = 0
fade_alpha = 0
fade_out = False
fade_in = False
count = 0
end_fade = False
show_ending = False
ending_timer = 0
ending_page = 0
last_door_timer = 0
last_door_played = False

font = pygame.font.Font("font/DOSIyagiBoldface.ttf", 22)
font2 = pygame.font.Font("font/DOSIyagiBoldface.ttf", 40)

ANOMALIES = {
    "paper_color": 20,
    "floor_change": 20,
    "blood": 20,
    "paper_run": 20,
    "clock_flipped": 20,
    "trash_full": 20,
    "schoolbell_horror": 20,
    "chair": 20,
    "locker_abnormal": 20,
    "timer_warp": 20,
    "count_error": 20,
    "blackboard": 20
}

total_anomaly = sum(ANOMALIES.values())
current_anomaly = "None"
is_anomaly_room = False
count_error = 0

def check_collision(new_x, new_y):
    player_rect_local = pygame.Rect(int(new_x), int(new_y), 48, 64)
    px = player_rect_local.centerx
    py = player_rect_local.centery
    max_check_dist = 512

    for w in wall_rects:
        if abs(w.centerx - px) > max_check_dist or abs(w.centery - py) > max_check_dist:
            continue
        if player_rect_local.colliderect(w):
            return True

    for d in desk_rects:
        if abs(d.centerx - px) > max_check_dist or abs(d.centery - py) > max_check_dist:
            continue
        if player_rect_local.colliderect(d):
            return True

    for l in locker_rects:
        if abs(l.centerx - px) > max_check_dist or abs(l.centery - py) > max_check_dist:
            continue
        if player_rect_local.colliderect(l):
            return True

    for l in kyotak_rects:
        if abs(l.centerx - px) > max_check_dist or abs(l.centery - py) > max_check_dist:
            continue
        if player_rect_local.colliderect(l):
            return True

    t = trash_rect
    if abs(t.centerx - px) <= max_check_dist and abs(t.centery - py) <= max_check_dist:
        if player_rect_local.colliderect(t):
            return True
            
    return False

def decide_next_room_state():
    global is_anomaly_room, current_anomaly, count, target_chair_index, count_error

    target_chair_index = -1
    if count == 0:
        is_anomaly_room = False
        current_anomaly = "None"
    else:
        if random.random() < 0.7:
            is_anomaly_room = True
            rand_val = random.randint(1, total_anomaly)
            cumulative_weight = 0

            for anomaly, weight in ANOMALIES.items():
                cumulative_weight += weight
                if rand_val <= cumulative_weight:
                    current_anomaly = anomaly
                    if current_anomaly == "chair":
                        target_chair_index = random.randint(0, len(chair_pos) - 1)
                    if current_anomaly == "count_error":
                        while True:
                            temp = random.randint(0, 10)
                            if temp != 7:
                                count_error = temp
                                break
                    break
        else:
            is_anomaly_room = False
            current_anomaly = "None"

cols = len(game_map[0])
rows = len(game_map)

def draw_map(camera_x, camera_y):
    tile_size = 64
    x0 = max(0, camera_x // tile_size)
    y0 = max(0, camera_y // tile_size)
    x1 = min(cols - 1, (camera_x + SCREEN_WIDTH) // tile_size + 1)
    y1 = min(rows - 1, (camera_y + SCREEN_HEIGHT) // tile_size + 1)

    for y in range(int(y0), int(y1) + 1):
        row = game_map[y]
        for x in range(int(x0), int(x1) + 1):
            tile = row[x]
            draw_x = x * tile_size - camera_x
            draw_y = y * tile_size - camera_y

            if tile == 0:
                if current_anomaly == "floor_change":
                    screen.blit(floor2_img, (draw_x, draw_y))
                else:
                    screen.blit(floor_img, (draw_x, draw_y))
            else:
                # 벽 그리기
                if x == 0 and y == rows - 1:
                    screen.blit(wall_imgs[4], (draw_x, draw_y))
                elif x == cols - 1 and y == rows - 1:
                    screen.blit(wall_imgs[4], (draw_x, draw_y))
                elif x == 0 and y == 0:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))
                elif x == 0 and y == 1:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))
                elif x == 0 and y == 2:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))
                elif x == cols - 1 and y == 0:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))
                elif x == cols - 1 and y == 1:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))
                elif x == cols - 1 and y == 2:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))
                elif y == 0:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))
                elif y == rows - 1:
                    screen.blit(wall_imgs[1], (draw_x, draw_y))
                elif x == 0:
                    screen.blit(wall_imgs[2], (draw_x, draw_y))
                elif x == cols - 1:
                    screen.blit(wall_imgs[3], (draw_x, draw_y))
                elif y == 2:
                    screen.blit(wall_imgs[5], (draw_x, draw_y))
                else:
                    screen.blit(wall_imgs[0], (draw_x, draw_y))

    # 칠판
    cb_x = blackboard_pos[0] * tile_size - camera_x
    cb_y = blackboard_pos[1] * tile_size - camera_y
    if -200 <= cb_x <= SCREEN_WIDTH + 200 and -200 <= cb_y <= SCREEN_HEIGHT + 200:
        if current_anomaly == "blackboard":
            screen.blit(blackboard2_img, (cb_x, cb_y))
        else:
            screen.blit(blackboard_img, (cb_x, cb_y))

    # 의자
    for i, cpos in enumerate(chair_pos):
        cx = cpos[0] * tile_size - camera_x
        cy = cpos[1] * tile_size - camera_y
        if -200 <= cx <= SCREEN_WIDTH + 200 and -200 <= cy <= SCREEN_HEIGHT + 200:
            if current_anomaly == "chair" and i == target_chair_index:
                screen.blit(chair2_img, (cx + 25, cy))
            else:
                screen.blit(chair_img, (cx, cy))

    # 피 (Blood)
    if current_anomaly == "blood":
        blood_x = 1248 - camera_x
        blood_y = 992 - camera_y
        screen.blit(blood_img, (blood_x, blood_y))

    # 책상
    for dpos in desk_pos:
        dx = dpos[0] * tile_size - camera_x
        dy = dpos[1] * tile_size - camera_y
        if -200 <= dx <= SCREEN_WIDTH + 200 and -200 <= dy <= SCREEN_HEIGHT + 200:
            screen.blit(desk_img, (dx, dy))

    # 교탁
    kb_x = kyotak_pos[0] * tile_size - camera_x
    kb_y = kyotak_pos[1] * tile_size - camera_y
    if -200 <= kb_x <= SCREEN_WIDTH + 200 and -200 <= kb_y <= SCREEN_HEIGHT + 200:
        screen.blit(kyotak_img, (kb_x, kb_y))

    # 쪽지
    px = paper_pos[0] * tile_size + paper_offset_x - camera_x
    py = paper_pos[1] * tile_size + paper_offset_y - camera_y
    if -200 <= px <= SCREEN_WIDTH + 200 and -200 <= py <= SCREEN_HEIGHT + 200:
        screen.blit(paper_img, (px, py))

    # 쓰레기통
    tx = trash_pos[0] * tile_size - camera_x
    ty = trash_pos[1] * tile_size - camera_y
    if -200 <= tx <= SCREEN_WIDTH + 200 and -200 <= ty <= SCREEN_HEIGHT + 200:
        if current_anomaly == "trash_full":
            screen.blit(trash_full_img, (tx, ty))
        else:
            screen.blit(trash_img, (tx, ty))

    # 문 (빨강/파랑)
    for pos in red_door_pos:
        dx = pos[0] * tile_size - camera_x
        dy = (pos[1] - 0.5) * tile_size - camera_y
        if -200 <= dx <= SCREEN_WIDTH + 200 and -200 <= dy <= SCREEN_HEIGHT + 200:
            screen.blit(reddoor_img, (dx, dy))
    
    for pos in blue_door_pos:
        dx = pos[0] * tile_size - camera_x
        dy = (pos[1] - 0.5) * tile_size - camera_y
        if -200 <= dx <= SCREEN_WIDTH + 200 and -200 <= dy <= SCREEN_HEIGHT + 200:
            screen.blit(bluedoor_img, (dx, dy))

    # 시계
    cx = clock_pos[0] * tile_size - camera_x
    cy = clock_pos[1] * tile_size - camera_y
    if -200 <= cx <= SCREEN_WIDTH + 200 and -200 <= cy <= SCREEN_HEIGHT + 200:
        if current_anomaly == "clock_flipped":
            screen.blit(clock_flipped_img, (cx, cy))
        else:
            screen.blit(clock_img, (cx, cy))

    # 사물함
    for l_index, lpos in enumerate(locker_pos):
        lx = lpos[0] * tile_size - camera_x
        ly = lpos[1] * tile_size - camera_y
        if -200 <= lx <= SCREEN_WIDTH + 200 and -200 <= ly <= SCREEN_HEIGHT + 200:
            if locker_states[l_index]:
                if current_anomaly == "locker_abnormal":
                    screen.blit(locker_abnormal_img, (lx, ly))
                else:
                    screen.blit(locker_opened_img, (lx, ly))
            else:
                screen.blit(locker_img, (lx, ly))

    # 힌트
    hx = hint_pos[0] * tile_size - camera_x
    hy = hint_pos[1] * tile_size - camera_y
    if -200 <= hx <= SCREEN_WIDTH + 200 and -200 <= hy <= SCREEN_HEIGHT + 200:
        screen.blit(hint_img, (hx, hy))


def draw_light_mask(center_x, center_y, radius):
    darkness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    darkness.fill(DARKNESS_COLOR)
    for r in range(radius + LIGHT_FADE, 0, -10):
        alpha = max(0, min(255, int(255 * (r - radius) / LIGHT_FADE)))
        if r < radius:
            alpha = 0
        color = (0, 0, 0, alpha)
        pygame.draw.circle(darkness, color, (center_x, center_y), r)
    screen.blit(darkness, (0, 0))

stage_timer = 0
is_bell_played = False

def show_credits():
    showing_credits = True
    while showing_credits:
        screen.blit(credit_img, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                showing_credits = False

def show_start_page():
    main_sound.play(loops=-1, fade_ms=3500)
    local_fade_alpha = 0
    is_fading = False
    waiting = True
    
    while waiting:
        clock.tick(60)
        screen.blit(gamecover_img, (0, 0))
        
        if is_fading:
            local_fade_alpha += 10
            if local_fade_alpha >= 255:
                local_fade_alpha = 255
                waiting = False
            fade_surface.set_alpha(local_fade_alpha)
            screen.blit(fade_surface, (0, 0))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    # 게임 시작
                    if 760 <= mx <= 935 and 370 <= my <= 435:
                        door_sound.play()
                        main_sound.fadeout(1800)
                        is_fading = True
                    # 제작진
                    elif 760 <= mx <= 935 and 475 <= my <= 545:
                        show_credits()
                    # 게임 종료
                    elif 760 <= mx <= 935 and 580 <= my <= 650:
                        pygame.quit()
                        sys.exit()

# --- 메인 실행 흐름 ---
show_start_page()

game_start_time = pygame.time.get_ticks()
current_mask_radius = 0
start_delay_timer = 0

while True:
    timer_for_info += clock.get_time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z and not fade_out and not fade_in:
            player_rect_check = pygame.Rect(int(player_x), int(player_y), 48, 64)
            interaction_happened = False
            
            # 쪽지 읽기
            if player_rect_check.colliderect(paper_rect.inflate(20, 20)):
                is_reading_paper = not is_reading_paper
                is_reading_hint = False
                interaction_happened = True
            
            # 힌트 읽기
            elif player_rect_check.colliderect(hint_rect.inflate(20, 20)):
                if not is_reading_hint:
                    hint_read_count += 1
                is_reading_hint = not is_reading_hint
                is_reading_paper = False
                interaction_happened = True
            
            # 사물함
            for l_index, lrect in enumerate(locker_rects):
                if player_rect_check.colliderect(lrect.inflate(-30, 30)):
                    locker_states[l_index] = not locker_states[l_index]
                    door_sound.play()
                    interaction_happened = True
                    break
            
            if interaction_happened and (is_reading_paper or is_reading_hint):
                Book_reading_sound.play()

            # 파란 문 (정상)
            for door_pos in blue_door_pos:
                door_rect = pygame.Rect(door_pos[0] * 64, (door_pos[1] - 0.5) * 64, 80, 130)
                if player_rect_check.colliderect(door_rect):
                    fade_out = True
                    if not is_anomaly_room:
                        count += 1
                        if count >= 7:
                            last_door_sound.play()
                            last_door_timer = pygame.time.get_ticks()
                            last_door_played = True
                        else:
                            door_sound.play()
                    else:
                        count = 0
                        door_sound.play()
                    break
            
            # 빨간 문 (변칙)
            for door_pos in red_door_pos:
                door_rect = pygame.Rect(door_pos[0] * 64, (door_pos[1] - 0.5) * 64, 80, 130)
                if player_rect_check.colliderect(door_rect):
                    fade_out = True
                    if is_anomaly_room:
                        count += 1
                        if count >= 7:
                            last_door_sound.play()
                            last_door_timer = pygame.time.get_ticks()
                            last_door_played = True
                        else:
                            door_sound.play()
                    else:
                        count = 0
                        door_sound.play()
                    break

    # --- 입력 및 이동 ---
    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    
    if is_reading_paper or is_reading_hint or end_fade or show_ending:
        moving = False
    else:
        moving = False
        current_speed = player_speed * (1.5 if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else 1)
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= current_speed
            player_dir = "left"
            moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += current_speed
            player_dir = "right"
            moving = True
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= current_speed
            player_dir = "up"
            moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += current_speed
            player_dir = "down"
            moving = True

    if moving and not check_collision(new_x, new_y):
        player_x, player_y = new_x, new_y

    # 애니메이션
    if moving:
        anim_timer += 1
        if anim_timer % 10 == 0:
            anim_frame = (anim_frame + 1) % 2
        if not is_walking_sound:
            footstep_sound.play(loops=-1)
            is_walking_sound = True
    else:
        anim_frame = 0
        if is_walking_sound:
            footstep_sound.stop()
            is_walking_sound = False

    # --- 카메라 ---
    map_width = len(game_map[0]) * 64
    map_height = len(game_map) * 64
    camera_x = int(player_x) - SCREEN_WIDTH // 2 + 24
    camera_y = int(player_y) - SCREEN_HEIGHT // 2 + 32
    camera_x = max(0, min(camera_x, map_width - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, map_height - SCREEN_HEIGHT))

    # --- 화면 그리기 ---
    screen.fill((0, 0, 0))

    if not show_ending:
        draw_map(camera_x, camera_y)
        
        # 플레이어 그리기
        if moving:
            screen.blit(player_imgs[player_dir][anim_frame], (player_x - camera_x, player_y - camera_y))
        else:
            screen.blit(player_idle_imgs[player_dir], (player_x - camera_x, player_y - camera_y))

        # 조명 마스크
        start_delay_timer += clock.get_time()
        if start_delay_timer > 100:
            if current_mask_radius < LIGHT_RADIUS:
                current_mask_radius += 3
            else:
                current_mask_radius = LIGHT_RADIUS
        else:
            current_mask_radius = -50
        
        draw_light_mask(int(player_x - camera_x + 24), int(player_y - camera_y + 32), current_mask_radius)

        # UI
        count_text = font.render(f"Count: {count}", True, (255, 255, 255))
        screen.blit(count_text, (SCREEN_WIDTH - 160, 30))

        # 시간 표시
        current_time = pygame.time.get_ticks()
        elapsed_time_ms = current_time - game_start_time
        total_time_seconds = elapsed_time_ms // 1000
        display_time_seconds = total_time_seconds

        if current_anomaly == "timer_warp":
            random_offset_seconds = random.randint(-7200, 7200)
            display_time_seconds = total_time_seconds + random_offset_seconds
            display_time_seconds = max(0, display_time_seconds)

        minutes = display_time_seconds // 60
        seconds = display_time_seconds % 60
        time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        screen.blit(time_text, (30, 30))

        hint_text = font.render(f" Hint: {hint_read_count}", True, (255, 255, 255))
        screen.blit(hint_text, (SCREEN_WIDTH - 160, 60))

    # --- 페이드 아웃/인 ---
    if end_fade:
        fade_alpha += 0.77
        if fade_alpha >= 255:
            fade_alpha = 255
            end_fade = False
            show_ending = True
            ending_page = 0
            ending_timer = 0
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

    elif fade_out:
        fade_alpha += 10
        if fade_alpha > 255:
            fade_alpha = 255
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        
        if fade_alpha >= 255:
            fade_out = False
            fade_in = True
            fade_alpha = 255
            player_x = 220
            player_y = 1000
            schoolbell_sound.stop()
            schoolbell_horror_sound.stop()
            locker_states = [False] * len(locker_pos)
            decide_next_room_state()

    elif fade_in:
        fade_alpha -= 10
        if fade_alpha < 0:
            fade_alpha = 0
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        
        if fade_alpha <= 0:
            fade_in = False
            fade_alpha = 0
            stage_timer = 0
            is_bell_played = False
    # --- 텍스트 오버레이 (튜토리얼/쪽지) ---
    if not show_ending:
        if 1500 < timer_for_info <= 5000:
            info_x = player_x - camera_x + 40
            info_y = player_y - camera_y + 50
            screen.blit(info_text_img, (info_x, info_y))

        if is_reading_paper or is_reading_hint:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(90)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            screen.blit(reading_paper, (110, -60))
            
            black_color = (0, 0, 0)
            
            text_lines = [
                ("This is a school classroom.", black_color),
                ("You must pass through exactly seven doors to escape.", black_color),
                ("If you encounter any anomalies, go through the red door.", (255, 0, 0)),
                ("If everything seems normal, proceed through the blue door.", (0, 0, 255)),
                ("The first room is always normal.", black_color),
                ("So, observe the first room carefully.", black_color),
                ("The loop exits when the count : 7", black_color)
            ]
            
            hint_lines = [("Memorize your surroundings well.", black_color)]

            if current_anomaly == "paper_run":
                text_lines = [
                    ("R U N R U N R U N R U N R U N", (255, 0, 0)),
                    ("R U N R U N R U N R U N R U N", (255, 0, 0)),
                    ("R U N R U N R U N R U N R U N", (255, 0, 0)),
                    ("R U N R U N R U N R U N R U N", (255, 0, 0)),
                    ("R U N R U N R U N R U N R U N", (255, 0, 0)),
                    ("R U N R U N R U N R U N R U N", (255, 0, 0)),
                ]
                hint_lines = [("Check the note again.", (255, 0, 0))]
            
            elif current_anomaly == "paper_color":
                text_lines = [
                    ("This is a school classroom.", black_color),
                    ("You must pass through exactly seven doors to escape.", black_color),
                    ("If you encounter any anomalies, go through the red door.", (0, 0, 255)),
                    ("If everything seems normal, proceed through the blue door.", (255, 0, 0)),
                    ("The first room is always normal.", black_color),
                    ("So, observe the first room carefully.", black_color),
                    ("The loop exits when the count : 7",black_color)
                ]
                hint_lines = [("Red and Blue", (255, 0, 0))]
            
            elif current_anomaly == "count_error":
                text_lines[-1] = (f"The loop exits when the count : {count_error}", black_color)
                hint_lines = [("Check the count in the notes", (255, 0, 0))]
            
            elif current_anomaly == "clock_flipped":
                hint_lines = [("The clock is strange.", (255, 0, 0))]
                
            elif current_anomaly == "trash_full":
                hint_lines = [("The trash can is strange.", (255, 0, 0))]
                
            elif current_anomaly == "schoolbell_horror":
                hint_lines = [("The bell sound is strange.", (255, 0, 0))]
                
            elif current_anomaly == "chair":
                hint_lines = [("Sitting strangely?", (255, 0, 0))]
                
            elif current_anomaly == "blood":
                hint_lines = [("blood", (255, 0, 0))]
                
            elif current_anomaly == "floor_change":
                hint_lines = [("floor pattern", (255, 0, 0))]
                
            elif current_anomaly == "locker_abnormal":
                hint_lines = [("DO NOT OPEN THE LOCKER", (255, 0, 0))]
                
            elif current_anomaly == "timer_warp":
                hint_lines = [("Check the timer", (255, 0, 0))]
                
            elif current_anomaly == "blackboard":
                hint_lines = [("Check the blackboard", (255, 0, 0))]

            lines_to_display = []
            if is_reading_hint:
                lines_to_display = hint_lines
            elif is_reading_paper:
                lines_to_display = text_lines
            
            y_offset = SCREEN_HEIGHT // 2 - 150
            for line_text, color in lines_to_display:
                txt_surface = font.render(line_text, True, color)
                screen.blit(txt_surface, (SCREEN_WIDTH // 2 - txt_surface.get_width() // 2, y_offset))
                y_offset += 50

    # 학교 종소리
    if not fade_in and not fade_out and not show_ending and not end_fade:
        stage_timer += clock.get_time()
        if stage_timer >= 2000 and not is_bell_played:
            if current_anomaly == "schoolbell_horror":
                schoolbell_horror_sound.play()
            else:
                schoolbell_sound.play()
            is_bell_played = True

    # 엔딩
    if count >= 7 and not show_ending and not end_fade:
        end_fade = True

    if last_door_played:
        last_door_current_time = pygame.time.get_ticks()
        if last_door_current_time - last_door_timer >= 7000:
            footstep_run_sound.play(fade_ms=2000, loops=1)
            night_sound.play(fade_ms=20000, loops=-1)
            last_door_played = False

    if show_ending:
        if ending_page == 0:
            screen.fill((0, 0, 0))
            end_text = font2.render("Game Clear", True, (255, 0, 0))
            screen.blit(end_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
            ending_timer += clock.get_time()
            
            if ending_timer > 4000:
                end_time = pygame.time.get_ticks()
                total_time_seconds = (end_time - game_start_time) // 1000
                base_time_seconds = 5 * 60
                time_penalty = 0
                
                if total_time_seconds > base_time_seconds:
                    exceeded_time_seconds = total_time_seconds - base_time_seconds
                    time_penalty = (exceeded_time_seconds // 60) * 5
                
                hint_penalty = hint_read_count * 5
                final_score = 100 - time_penalty - hint_penalty
                final_score = max(0, final_score)
                
                if final_score >= 95: final_grade = "A+"
                elif final_score >= 90: final_grade = "A"
                elif final_score >= 85: final_grade = "B+"
                elif final_score >= 80: final_grade = "B"
                elif final_score >= 70: final_grade = "C"
                else: final_grade = "F"
                
                minutes = total_time_seconds // 60
                seconds = total_time_seconds % 60
                formatted_time = f"{minutes:02d}minutes {seconds:02d}seconds"
                
                ending_score_data = [
                    (f"Escape Successful!", (43, 19, 5)),
                    (f"Time Taken: {formatted_time}", (43, 19, 5)),
                    (f"Hint Usage: {hint_read_count}times ({hint_penalty}points deducted)", (43, 19, 5)),
                    (f"Final Score: {final_score}", (0, 0, 0)),
                    (f"Final Grade: {final_grade}", (230, 0, 0) if final_grade in ["A+", "A"] else (43, 19, 5))
                ]
                
                ending_page = 1
                fade_alpha = 255
                ending_x = 400
                ending_y = 280
                player_dir = "down"
                anim_check = 0
                check_dir = 0
        
        elif ending_page == 1:
            screen.blit(ending_bg_img, (0, 0))
            anim_timer += 1
            if anim_timer % 20 == 0:
                anim_check = 1 - anim_check
            
            screen.blit(player_imgs[player_dir][anim_check], (ending_x, ending_y))
            
            if fade_alpha > 0:
                fade_alpha -= 5
            if fade_alpha < 0:
                fade_alpha = 0
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
            
            if ending_y < 630:
                player_dir = "down"
                ending_y += 0.8
                check_dir += 1
                if check_dir % 10 < 5:
                    ending_x -= 0.6
            elif ending_x >= -50:
                player_dir = "left"
                ending_x -= 0.8
                check_dir += 1
                if check_dir % 10 < 5:
                    ending_y += 0.3
            
            if ending_x <= -50:
                screen.blit(ending_paper_img, (260, 85))
                text_y = 170
                for text, color in ending_score_data:
                    print_text = font.render(text, True, color)
                    screen.blit(print_text, (SCREEN_WIDTH // 2 - print_text.get_width() // 2 + 10, text_y))
                    text_y += 80
                
                exit_text = font2.render("Click to Exit", True, (179, 123, 90))
                screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2 + 10, 550))
                
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pygame.quit()
                        sys.exit()

    pygame.display.update()
    clock.tick(60)