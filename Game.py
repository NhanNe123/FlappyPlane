import pygame, sys, random, os
#Khai báo
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((432,700))
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/04B_19.ttf', 40)
gravity = 0.25
game_active = True
plane_movement = 0
score = 0
high_score = 0  
used_images = set() 
fading_images = []  
cross = pygame.mixer.Sound('sound/vine-boom.wav')

#Tạo hàm        
def create_tower():
    random_tower_pos = random.choice(tower_height)
    top_tower = tower_surface.get_rect(midtop = (500,random_tower_pos-680))
    bot_tower = tower_surface.get_rect(midtop = (500,random_tower_pos))
    return bot_tower,top_tower
def move_tower(towers):
    for tower in towers :
        tower.centerx -= 3
    return towers
def draw_tower(towers):
    for tower in towers:
        if tower.bottom > 400:
            screen.blit(tower_surface,tower)
        else :
            flip_tower = pygame.transform.flip(tower_surface,False,True)
            screen.blit(flip_tower,tower)
def random_position():
    x = random.randint(0, 432)
    y = random.randint(0, 700)
    return (x, y)
def check_collision(towers):
    global score
    for tower in towers:
        if plane_rect.colliderect(tower):
            win_sound.play()
            return False
        if tower.centerx + 3 >= plane_rect.centerx >= tower.centerx - 3:
            cross.play()
            random_img = load_random_image('assets/random_images')
            if random_img:
                pos = random_position()
                rect = random_img.get_rect(topleft=pos)
                start_time = pygame.time.get_ticks()
                fading_images.append((random_img, rect, 255, start_time))
        if plane_rect.top <= -75 or plane_rect.bottom >= 600:
            win_sound.play()
            return False 
    return True      
def rotate_plane(plane1):
    new_plane = pygame.transform.rotozoom(plane1,-plane_movement*3,1)
    return new_plane
def plane_animation():
    new_plane = plane_list[plane_index]
    new_plane_rect = new_plane.get_rect(center = (100,plane_rect.centery))
    return new_plane, new_plane_rect
def score_display(game_state):
    if game_state == "Mission success":
        success_text = game_font.render("Mission Success!", True, (255, 255, 255))
        success_rect = success_text.get_rect(center = (200, 300))
        screen.blit(success_text, success_rect)
        space_text = game_font.render("Space to continue", True, (255, 255, 255))
        space_rect = space_text.get_rect(center = (200, 150))
        screen.blit(space_text,space_rect)
        score_surface = game_font.render(f"Good job",True,(255,255,255))
        score_rect = score_surface.get_rect(center = (200,100))
        screen.blit(score_surface,score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
def load_random_image(folder_path):
    global used_images
    valid_extensions = ['.png', '.jpg', '.jpeg']
    
    try:
        if not os.path.exists(folder_path):
            return None
            
        files = os.listdir(folder_path)
        available_images = [f for f in files 
                          if os.path.splitext(f)[1].lower() in valid_extensions 
                          and f not in used_images]
        
        if not available_images:
            used_images.clear()
            available_images = [f for f in files 
                               if os.path.splitext(f)[1].lower() in valid_extensions]
        
        if not available_images:
            return None
            
        random_image = random.choice(available_images)
        used_images.add(random_image)
        
        image_path = os.path.join(folder_path, random_image)
        return pygame.image.load(image_path).convert_alpha()
        
    except Exception as e:
        return None
def update_fading_images():
    current_time = pygame.time.get_ticks()
    fade_duration = 500  # 500ms = 0.5 giây
    
    i = 0
    while i < len(fading_images):
        img, rect, alpha, start_time = fading_images[i]
        elapsed_time = current_time - start_time
        
        if elapsed_time >= fade_duration:
            fading_images.pop(i)
        else:
            new_alpha = 255 * (1 - elapsed_time / fade_duration)
            temp_surface = img.copy()
            temp_surface.set_alpha(new_alpha)
            screen.blit(temp_surface, rect)
            fading_images[i] = (img, rect, new_alpha, start_time)
            i += 1

#Tạo nổ
boom = pygame.image.load('assets/boom.png').convert_alpha()
boom = pygame.transform.scale2x(boom)  # Scale cho phù hợp với kích thước máy bay
#Tạo tháp 
tower_surface = pygame.image.load('assets/tower.png').convert()
tower_surface = pygame.transform.scale2x(tower_surface)
tower_list = [] 
tower_height = [200, 250, 300, 350, 400, 450]
#Tạo backgound 
backgound = pygame.transform.scale2x(pygame.image.load('assets/background-night.png').convert())
#Tạo May_bay 
plane_down = pygame.transform.scale2x(pygame.image.load('assets/yellowplane-downflap.png').convert_alpha())
plane_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowplane-midflap.png').convert_alpha())
plane_up = pygame.transform.scale2x(pygame.image.load('assets/yellowplane-upflap.png').convert_alpha())
plane_list = [plane_down,plane_mid,plane_up]
plane_index = 2
plane = plane_list[plane_index]
plane_rect = plane.get_rect(center = (100,384))
#Tạo timer 
#Máy bay
plane_flap = pygame.USEREVENT + 1
pygame.time.set_timer(plane_flap,200)
#Tháp 
spawntower = pygame.USEREVENT
pygame.time.set_timer(spawntower,1200)
#Chèn âm thanh 
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
#Âm thanh thắng
win_sound = pygame.mixer.Sound('sound/tbc.wav')


#Chạy
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                plane_movement = 0
                plane_movement = -7
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                tower_list.clear()
                plane_rect.center = (100,384)
                plane_movement = 0
                win_sound.stop()
        if event.type == spawntower:
            tower_list.extend(create_tower())
        if event.type == plane_flap:
            if plane_index < 2:
                plane_index += 1
            else:
                plane_index = 0 
            plane, plane_rect = plane_animation()

    screen.blit(backgound,(0,0))
    
    draw_tower(tower_list)      
    rotated_plane = rotate_plane(plane)
    screen.blit(rotated_plane,plane_rect)
    
    if game_active:
        game_active = check_collision(tower_list)
        plane_movement += gravity
        plane_rect.centery += plane_movement
        tower_list = move_tower(tower_list)
        update_fading_images()
    else:
        score_display1("")
        score_display("Mission success")
        screen.blit(boom, plane_rect)
    pygame.display.update()
    clock.tick(120)
pygame.quit()