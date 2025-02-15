import pygame, sys, random

# Khởi tạo pygame
pygame.init()
pygame.mixer.init()

# Tạo cửa sổ game
screen = pygame.display.set_mode((432,700))
clock = pygame.time.Clock()

# Tạo các biến cho game
gravity = 0.25
plane_movement = 0
game_active = True
score = 0
high_score = 0

# Tạo font chữ
game_font = pygame.font.Font('assets/04B_19.ttf', 40)

# Tạo âm thanh
cross = pygame.mixer.Sound('sound/vine-boom.wav')

# Tạo nổ
boom = pygame.image.load('assets/boom.png').convert_alpha()

# Tạo tháp 
tower_surface = pygame.image.load('assets/tower.png').convert()
tower_surface = pygame.transform.scale(tower_surface, (tower_surface.get_width(), tower_surface.get_height() * 1.5))  # Kéo dài tháp thêm 50%
tower_list = []
SPAWNTOWER = pygame.USEREVENT
pygame.time.set_timer(SPAWNTOWER,1200)

# Tạo background 
backgound = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
floor_base = pygame.image.load('assets/floor.png').convert()

# Tạo máy bay 
plane_down = pygame.transform.scale2x(pygame.image.load('assets/yellowplane-downflap.png').convert_alpha())
plane_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowplane-midflap.png').convert_alpha())
plane_up = pygame.transform.scale2x(pygame.image.load('assets/yellowplane-upflap.png').convert_alpha())
plane_list = [plane_down,plane_mid,plane_up]
plane_index = 0
plane_surface = plane_list[plane_index]
plane_rect = plane_surface.get_rect(center = (100,512))

# Tạo timer cho máy bay
PLANEFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PLANEFLAP,200)

# Chèn âm thanh 
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')

# Thêm biến game_state và load hình ảnh cho màn hình chính
game_state = 'start_screen'  # Thêm trạng thái mới: 'start_screen', 'main_game', 'game_over'

def create_tower():
    random_tower_pos = random.randint(400, 700)
    bottom_tower = tower_surface.get_rect(midtop = (700,random_tower_pos))
    top_tower = tower_surface.get_rect(midbottom = (700,random_tower_pos - 300))  # Giảm khoảng cách xuống 300
    return bottom_tower, top_tower

def move_tower(towers):
    # Di chuyển tháp
    for tower in towers:
        tower.centerx -= 5
    return towers

def draw_tower(towers):
    # Vẽ tháp
    for tower in towers:
        screen.blit(tower_surface,tower)

def check_collision(towers):
    # Kiểm tra va chạm
    for tower in towers:
        if plane_rect.colliderect(tower):
            cross.play()
            return False
    if plane_rect.top <= -100 or plane_rect.bottom >= 900:
        cross.play()
        return False
    return True

def rotate_plane(plane):
    # Xoay máy bay
    new_plane = pygame.transform.rotozoom(plane,-plane_movement * 3,1)
    return new_plane

def plane_animation():
    # Hoạt ảnh máy bay
    new_plane = plane_list[plane_index]
    new_plane_rect = new_plane.get_rect(center = (100,plane_rect.centery))
    return new_plane, new_plane_rect

def score_display(game_state):
    # Hiển thị điểm
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,850))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    # Cập nhật điểm cao
    if score > high_score:
        high_score = score
    return high_score

def update_plane():
    # Cập nhật trạng thái máy bay
    global plane_movement, game_active
    plane_movement += gravity
    rotated_plane = rotate_plane(plane_list[plane_index])
    plane_rect.centery += plane_movement
    screen.blit(rotated_plane, plane_rect)
    return True

def draw_start_screen():
    screen.blit(backgound, (0,0))
    # Vẽ tiêu đề game
    title_text = game_font.render('FLAPPY PLANE', True, (255,255,255))
    title_rect = title_text.get_rect(center=(216, 200))
    screen.blit(title_text, title_rect)
    
    # Vẽ hướng dẫn
    start_text = game_font.render('Press SPACE', True, (255,255,255))
    start_rect = start_text.get_rect(center=(216, 350))
    screen.blit(start_text, start_rect)
    
    # Vẽ máy bay ở màn hình chính
    screen.blit(plane_surface, plane_rect)
    
    pygame.display.update()

# Vòng lặp game chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == 'start_screen':
                    game_state = 'main_game'
                    game_active = True
                    tower_list.clear()
                    plane_rect.center = (100,512)
                    plane_movement = 0
                    score = 0
                elif game_state == 'main_game' and game_active:
                    plane_movement = 0
                    plane_movement -= 8
                    flap_sound.play()
                elif game_state == 'game_over':
                    game_state = 'main_game'
                    game_active = True
                    tower_list.clear()
                    plane_rect.center = (100,512)
                    plane_movement = 0
                    score = 0
        
        if event.type == SPAWNTOWER:
            tower_list.extend(create_tower())
        
        if event.type == PLANEFLAP:
            if plane_index < 2:
                plane_index += 1
            else:
                plane_index = 0
            plane_surface, plane_rect = plane_animation()
            
    if game_state == 'start_screen':
        draw_start_screen()
    elif game_state == 'main_game':
        screen.blit(backgound,(0,0))
        if game_active:
            # Cập nhật trạng thái máy bay
            game_active = update_plane()
            
            # Di chuyển tháp
            tower_list = move_tower(tower_list)
            draw_tower(tower_list)
            
            # Kiểm tra va chạm
            game_active = check_collision(tower_list)
            
            # Tính điểm
            score += 0.01
            score_display('main_game')
            high_score = update_score(score, high_score)
        else:
            game_state = 'game_over'
            score_display('game_over')
    
    pygame.display.update()
    clock.tick(120)