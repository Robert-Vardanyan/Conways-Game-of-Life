import pygame
import numpy as np
import os
import random
import pandas as pd
import time


import colors as cl
import options as opts
import windows as wd

# Windows init
def py_init(back_photo=False):
    
    pygame.init()


    icon = pygame.image.load('./png/icon.png')
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((opts.width, opts.height))

    pygame.display.set_caption("'Conway's Game of Life' by Rova")

    if back_photo:

        photo = pygame.image.load(f'./png/{back_photo}.png')
        photo = pygame.transform.scale(photo, (opts.width, opts.height))
        return screen, photo
    
    else:
        return screen
    

def escape(screen, cells):
    time.sleep(0.3)
    in_settings = True
    if not settings(screen, in_settings,cells):
        in_settings = False
    screen.fill(cl.color_mesh)  # Settings pakeluc heto tazuc nkaruma dashty
    update(screen, cells, 10)
    pygame.display.flip()
    in_settings = False


# Windows settings
def settings(screen, in_settings, cells):

    running = True
    settings_back = pygame.image.load('./png/settings.png')

    press_pattern = pygame.image.load('./png/btn.png')
    press_speed = pygame.image.load('./png/speed.png')
    press_other = pygame.image.load('./png/other.png')

    normal = pygame.image.load('./png/normal.png')
    x_2 = pygame.image.load('./png/2x.png')
    x_5 = pygame.image.load('./png/5x.png')
    
    back_surf = pygame.Surface((93, 47), pygame.SRCALPHA)  
    back_surf.fill((255, 222, 89, 100))        
    
    while running:
        screen.blit(settings_back,(0, 0))  

        button_back = pygame.Rect(1107, 500, 93, 47)
        button_pattern = pygame.Rect(99.7, 199.5, 268, 47)

        button_slower_5x = pygame.Rect(60, 306, 63, 47)
        button_slower_2x = pygame.Rect(131, 306, 63, 47)
        button_normal = pygame.Rect(202, 306, 63, 47)
        button_faster_2x = pygame.Rect(273, 306, 63, 47)
        button_faster_5x = pygame.Rect(344, 306, 63, 47)

        button_home = pygame.Rect(60, 414.4, 134, 47)
        button_restart = pygame.Rect(273.3, 414.4, 134, 47)

        if opts.speed_index == 0:
            screen.blit(x_5,(60, 306))
        elif opts.speed_index == 1:
            screen.blit(x_2,(131, 306))
        elif opts.speed_index == 2:
            screen.blit(normal,(202, 306))
        elif opts.speed_index == 3:
            screen.blit(x_2,(273, 306))
        elif opts.speed_index == 4:
            screen.blit(x_5,(344, 306))


        if button_back.collidepoint(pygame.mouse.get_pos()):  
            screen.blit(back_surf, (1132, 500))
        elif button_pattern.collidepoint(pygame.mouse.get_pos()):
            screen.blit(press_pattern, (99.7, 199.5))

        elif button_slower_5x.collidepoint(pygame.mouse.get_pos()): 
            screen.blit(press_speed, (60, 306))     
        elif button_slower_2x.collidepoint(pygame.mouse.get_pos()): 
            screen.blit(press_speed, (131, 306)) 
        elif button_normal.collidepoint(pygame.mouse.get_pos()): 
            screen.blit(press_speed, (202, 306)) 
        elif button_faster_2x.collidepoint(pygame.mouse.get_pos()): 
            screen.blit(press_speed, (273, 306)) 
        elif button_faster_5x.collidepoint(pygame.mouse.get_pos()): 
            screen.blit(press_speed, (344, 306)) 

        elif button_home.collidepoint(pygame.mouse.get_pos()): 
            screen.blit(press_other, (60, 414.4))
        elif button_restart.collidepoint(pygame.mouse.get_pos()): 
            screen.blit(press_other, (273.3, 414.4))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Settings-i pakum krknake ESC-i sexmeluc
                    in_settings = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    in_settings = False
                elif button_pattern.collidepoint(pygame.mouse.get_pos()):
                    csv_files = os.listdir('patterns')
                    my_csv_name = random.choice(csv_files)
                    open_file_path = f'patterns/{my_csv_name}'
                    cell_csv = pd.read_csv(open_file_path)
                    time.sleep(0.3)
                    wd.game(cell_csv.values)
                elif button_slower_5x.collidepoint(pygame.mouse.get_pos()):
                    opts.speed_index = 0
                elif button_slower_2x.collidepoint(pygame.mouse.get_pos()):
                    opts.speed_index = 1
                elif button_normal.collidepoint(pygame.mouse.get_pos()):
                    opts.speed_index = 2
                elif button_faster_2x.collidepoint(pygame.mouse.get_pos()):
                    opts.speed_index = 3
                elif button_faster_5x.collidepoint(pygame.mouse.get_pos()):
                    opts.speed_index = 4
                elif button_home.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    wd.menu()
                elif button_restart.collidepoint(pygame.mouse.get_pos()):
                    cells.fill(0)


        pygame.display.flip()
    
    return True


# Update game
def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))
    
    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        
        if cells[row, col] == 0:
            color = cl.color_back
        else:
            color = cl.color_alive_next

        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = cl.color_die_next
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = cl.color_alive_next
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = cl.color_alive_next

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


