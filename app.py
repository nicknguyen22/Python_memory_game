from ast import If
import pygame
from pygame import display, event, image
import sys
import os.path
import game_config as gc
from animal import Animal
import button

pygame.init()
display.set_caption("My Game")
screen = display.set_mode((1024, 1124))

#other image
matched = image.load('other_assets/matched.png').convert_alpha()
start_screen_bg = image.load('other_assets/start_screen.png').convert_alpha()
game_bg = image.load('other_assets/game_bg.png').convert_alpha()
s_clear = image.load('other_assets/stage_clear.png').convert_alpha()
ldboard_bg = image.load('other_assets/ldboard_bg.png').convert_alpha()
g_quit = image.load('other_assets/quit.png').convert_alpha()

#button image
start_img = image.load("button_images/start.png").convert_alpha()
leaderboard_img = image.load("button_images/leaderboard.png").convert_alpha()
quit_img = image.load("button_images/quit.png").convert_alpha()
back_img = image.load('button_images/back.png').convert_alpha()
replay_img = image.load('button_images/replay.png').convert_alpha()
easy_img = image.load('button_images/easy.png').convert_alpha()
medium_img = image.load('button_images/medium.png').convert_alpha()
hard_img = image.load('button_images/hard.png').convert_alpha()

#create button instances
start_button = button.Button(387, 672, start_img, 1)
leaderboard_button = button.Button(372, 915, leaderboard_img, 1)
quit_button = button.Button(402, 995, quit_img, 1)
easy_button = button.Button(272, 752, easy_img, 1)
medium_button = button.Button(420, 752, medium_img, 1)
hard_button = button.Button(628, 752, hard_img, 1)
replay_button = button.Button(441, 510, replay_img, 1)
back_button = button.Button(367, 844, back_img, 1)

#default variables
GRAY = (64, 64, 64)
BLUE = (0, 0, 255)
ORANGE = (255, 128, 0)
running = True
menu_state = 'main_menu'
current_images = []
no_of_moves = 0
player_name = 'GUEST'



class EventAction():
    """Quit even check"""
    def __init__(self):
        global running
        current_events = event.get()

        for e in current_events:
            if e.type == pygame.QUIT:
                game_quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    game_quit()



class Menu():
    """ Menu class """
    def main_menu():
        """ Main menu """

        global menu_state
        EventAction()
        if menu_state == 'main_menu':
            if start_button.draw(screen):
                menu_state = 'start_menu'
            if leaderboard_button.draw(screen):
                leaderboard()
            if quit_button.draw(screen):
                game_quit()
                
        if menu_state == 'start_menu':
            if easy_button.draw(screen):
                gc.load_setting('easy')
                game_loop()
            if medium_button.draw(screen):
                gc.load_setting('medium')
                game_loop()
            if hard_button.draw(screen):
                gc.load_setting('hard')
                game_loop()
            if back_button.draw(screen):
                menu_state = 'main_menu'

            display.update()


    def end_menu():
        """ Menu after game completed """
        global menu_state
        #EventAction()
        menu_state = 'end_menu'
        if menu_state == 'end_menu':
            if replay_button.draw(screen):
                record_moves(player_name,no_of_moves,gc.NUM_TITLES_SIDE)
                game_loop()
            if back_button.draw(screen):
                menu_state = 'main_menu'
                record_moves(player_name,no_of_moves,gc.NUM_TITLES_SIDE)
                intro()
            display.update()
    
    def ldb_menu():
        """ Menu for leaderboard """
        global menu_state
        EventAction()
        menu_state = 'ldb_menu'
        if menu_state == 'ldb_menu':
            if back_button.draw(screen):
                menu_state = 'main_menu'
                intro()
            display.update()


def draw_text(surface, text, size, x, y, color):
    """ Draw text to screen """

    font = pygame.font.Font(pygame.font.match_font('arialblack'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)

    surface.blit(text_surface, text_rect)


def text_input(surface,text,size,x,y,color,color_current):
    """Get text input from keyboard"""

    input_rect = pygame.Rect(x-5, y-1, 200, 40)
    font = pygame.font.Font(pygame.font.match_font('arialblack'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect = (x, y)
    pygame.draw.rect(surface,color_current,input_rect,2)
    surface.blit(text_surface, text_rect)


                
def find_index(x,y):
    """ Title index lookup """

    row = (y - gc.SCREEN_START_Y) // gc.IMAGE_SIZE_H
    col = (x - gc.SCREEN_START_X)  // gc.IMAGE_SIZE_W
    return row * gc.NUM_TITLES_SIDE + col

def record_moves(player_name,no_of_moves,no_of_titles):
    """ Write the record to leaderboard file """

    if os.path.exists('leaderboard.txt'):
        leaderboard_file = open('leaderboard.txt','a')
    else: 
        leaderboard_file = open('leaderboard.txt','w')

    leaderboard_file.write(f'\n{player_name},{no_of_moves},{no_of_titles}')
    leaderboard_file.close()

def leaderboard():
    """ Leaderboard screen """
    easy_lv = []
    medium_lv = []
    hard_lv = []
    
    leaderboard_file = open('leaderboard.txt')
    lines = leaderboard_file.readlines()
    leaderboard_file.close()
    for line in lines:
        line = line.strip()
        line = line.split(',')
        name,moves,level = line
        if level == '4':
            easy_lv.append((name,moves))
        if level == '6':
            medium_lv.append((name,moves))
        if level == '8':
            hard_lv.append((name,moves))
    
    easy_lv = sorted(easy_lv, key=lambda x: x[1])
    medium_lv = sorted(medium_lv, key=lambda x: x[1])
    hard_lv = sorted(hard_lv, key=lambda x: x[1])

    easy_surface = pygame.Surface((290, 250))
    medium_surface = pygame.Surface((290, 250))
    hard_surface = pygame.Surface((290, 250))


    board_font = pygame.font.SysFont('arialblack', 25)

    highscores_visible = True
    running = True
    while running:
        screen.blit(ldboard_bg, (0,0))
        if highscores_visible:
            easy_surface.fill((255,255,255,255))
            for i, (name, score) in enumerate(easy_lv):
                if i < 5:
                    text = board_font.render('{}'.format(name), True, (0, 128, 255))
                    score = board_font.render('{}'.format(score), True, (0, 76, 153))
                    easy_surface.blit(text, (3, 50*i+5))
                    easy_surface.blit(score, (220, 50*i+5))
            
            medium_surface.fill((255,255,255,255))
            for i1, (name1, score1) in enumerate(medium_lv):
                if i1 < 5:
                    text1 = board_font.render('{}'.format(name1), True, (255, 128, 0))
                    score1 = board_font.render('{}'.format(score1), True, (204, 102, 0))
                    medium_surface.blit(text1, (3, 50*i1+5))
                    medium_surface.blit(score1, (220, 50*i1+5))

            hard_surface.fill((255,255,255,255))
            for i2, (name2, score2) in enumerate(hard_lv):
                if i2 < 5:
                    text2 = board_font.render('{}'.format(name2), True, (255, 0, 0))
                    score2 = board_font.render('{}'.format(score2), True, (204, 0, 0))
                    hard_surface.blit(text2, (3, 50*i2+5))
                    hard_surface.blit(score2, (220, 50*i2+5))

            screen.blit(easy_surface, (27, 403))
            screen.blit(medium_surface, (367, 403))
            screen.blit(hard_surface, (708, 403))

        Menu.ldb_menu()
        display.flip()


def intro():
    """ Intro screen with menu """

    running = True
    while running:
        screen.blit(start_screen_bg, (0,0))

        Menu.main_menu()
        display.update()


def game_loop():
    """ Game main loop """

    global running, current_images,no_of_moves
    no_of_moves = 0
    ignored_idxs = list()
    animals_count = dict((a,0) for a in gc.ASSET_FILES)
    tiles = [Animal(i,animals_count) for i in range(0, gc.NUM_TITLES_TOTAL)]
    screen_end_x = gc.SCREEN_START_X + gc.NUM_TITLES_SIDE * gc.IMAGE_SIZE_W
    screen_end_y = gc.SCREEN_START_Y + gc.NUM_TITLES_SIDE * gc.IMAGE_SIZE_H

    while running:
        current_events = event.get()

        for e in current_events:
            if e.type == pygame.QUIT:
                game_quit()
            
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    game_quit()
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if gc.SCREEN_START_X <= mouse_x <= screen_end_x and gc.SCREEN_START_Y <= mouse_y <= screen_end_y:
                    index = find_index(mouse_x, mouse_y)
                    if index not in current_images and index not in ignored_idxs:
                        current_images.append(index)
                        no_of_moves += 1
                    if len(current_images) >2:
                        current_images = current_images[1:]
        
        screen.fill((255,255,255))
        screen.blit(game_bg, (0,0))

        total_skipped = 0

        for _, tile in enumerate(tiles):
            image_i = tile.image if tile.index in current_images else tile.back
            if not tile.skip:
                screen.blit(image_i, (tile.col * gc.IMAGE_SIZE_W + gc.MARGIN + gc.SCREEN_START_X, tile.row * gc.IMAGE_SIZE_H + gc.MARGIN + gc.SCREEN_START_Y))
            else: total_skipped += 1
        
        if len(current_images) == 2:
            idx1, idx2 = current_images
            if tiles[idx1].name == tiles[idx2].name:
                tiles[idx1].skip = True
                tiles[idx2].skip = True
                ignored_idxs.append(idx1)
                ignored_idxs.append(idx2)
                display.flip()
                pygame.time.wait(400)
                screen.blit(matched, (363,487))
                display.flip()
                pygame.time.wait(500)
                current_images = []
        
        if total_skipped == len(tiles):
            completed_screen(no_of_moves)
        
        draw_text(screen, "NUMBER OF MOVES: ", 25, 780, 14, GRAY)
        draw_text(screen, str(no_of_moves), 25, 970 , 14, BLUE)

        display.flip()

def completed_screen(no_of_moves):
    """ Stage clear screen """
    global player_name
    running = True
    input_active = False
    input_rect = pygame.Rect(645, 429, 200, 40)
    color_active = pygame.Color('green')
    color_passive = pygame.Color('orange')
    color_current = color_passive

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                record_moves(player_name,no_of_moves,gc.NUM_TITLES_SIDE)
                game_quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    if len(player_name) <= 9:
                        input_active = True
                    else:
                        player_name = player_name[:-1]
                        input_active = True
                else:
                    input_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    record_moves(player_name,no_of_moves,gc.NUM_TITLES_SIDE)
                    game_quit()
                if input_active == True:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
            
    
        if input_active:
            color_current = color_active
        else:
            color_current = color_passive

        if len(player_name) > 9:
            input_active = False
            color_current = color_passive

        screen.blit(s_clear, (0,0))
        draw_text(screen, "YOU HAVE FINISHED THE STAGE IN : ", 25, 415, 380, GRAY)
        draw_text(screen, str(no_of_moves), 25, 720 , 380, BLUE)
        draw_text(screen, "MOVES", 25, 815, 380, GRAY)
        draw_text(screen, "PLEASE ENTER PLAYER NAME :", 25, 415, 430, GRAY)
        text_input(screen, player_name, 25, 650, 430, ORANGE,color_current)
        Menu.end_menu()

        display.flip()

def game_quit ():
    """ Quit screen """
    running = True
    while running:
        screen.blit(g_quit, (0,0))
        display.flip()
        pygame.time.wait(400)
        running = False
    pygame.quit()
    sys.exit()


intro()