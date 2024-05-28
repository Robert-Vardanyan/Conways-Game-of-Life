from datetime import datetime
import time
import pygame
import webbrowser
import numpy as np
import pandas as pd

import colors as cl
import functions as fn
import options as opts


def menu():
    screen, photo = fn.py_init(back_photo = 'background')

    press_btn = pygame.image.load('./png/btn.png')
    press_info = pygame.image.load('./png/info_press.png')

    while True:
        screen.blit(photo, (0, 0))

        button_standard = pygame.Rect(356, 239, 268, 46)
        # button_reverse = pygame.Rect(356, 339, 268, 46)
        button_quit = pygame.Rect(356, 439, 268, 46)
        button_info = pygame.Rect(60, 495.6, 45, 45)
        

        mouse = pygame.mouse.get_pos()
        
        if button_standard.collidepoint(mouse):   screen.blit(press_btn, (356,239))
        # elif button_reverse.collidepoint(mouse):  screen.blit(press_btn, (60,339))
        elif button_quit.collidepoint(mouse):     screen.blit(press_btn, (356,439))
        elif button_info.collidepoint(mouse):     screen.blit(press_info, (60,495.6))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_standard.collidepoint(mouse):
                    pygame.quit()
                    start_cells = np.zeros((60, 120))
                    game(start_cells)
                # elif button_reverse.collidepoint(mouse): 
                #     pygame.quit()
                #     game()
                
                elif button_info.collidepoint(mouse):
                    pygame.quit()
                    info()                   

                elif button_quit.collidepoint(mouse):
                    pygame.quit()
                    return

        pygame.display.update()
    


def info():
    screen, photo = fn.py_init(back_photo = 'back_info')

    #URLs
    url_devs = 'https://www.linkedin.com/in/robert-vardanyan-0753532b6/'
    url_code = 'https://github.com/Robert-Vardanyan?tab=repositories'
    url_idea = 'https://www.codewars.com/kata/5ea6a8502186ab001427809e'

    devs = pygame.image.load('./png/devs.png')
    code = pygame.image.load('./png/code.png')
    idea = pygame.image.load('./png/idea.png')

    back_surf = pygame.Surface((93, 47), pygame.SRCALPHA)  
    back_surf.fill((255, 222, 89, 100))


    mouse = (0, 0)
    running = True 

    while running:
        screen.blit(photo, (0, 0))

        button_back = pygame.Rect(1107, 500, 93, 47)
        button_devs = pygame.Rect(60, 206, 272, 47)
        button_code = pygame.Rect(60, 276.5, 272, 47)
        button_idea = pygame.Rect(60, 346.8, 272, 47)


        if button_back.collidepoint(pygame.mouse.get_pos()):  
            screen.blit(back_surf, (1132, 500))
        if button_devs.collidepoint(pygame.mouse.get_pos()):  
            screen.blit(devs, (60, 206))
        if button_code.collidepoint(pygame.mouse.get_pos()):  
            screen.blit(code, (60, 276.5))
        if button_idea.collidepoint(pygame.mouse.get_pos()):  
            screen.blit(idea, (60, 346.8))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()  
                buttons = [(button_back, lambda: menu()), 
                        (button_devs, lambda: webbrowser.open(url_devs)), 
                        (button_code, lambda: webbrowser.open(url_code)), 
                        (button_idea, lambda: webbrowser.open(url_idea))]
                button_clicked = False
                for button, action in buttons:
                    if button.collidepoint(mouse):
                        action()  
                        button_clicked = True
                        break  
                if button_clicked:
                    break
                
        pygame.display.flip()

    pygame.quit()

send_key = True


def game(cells):
    global send_key
    screen = fn.py_init()
    
    # cells = np.zeros((60, 120))
    cells = cells
    screen.fill(cl.color_mesh)

    fn.update(screen, cells, 10)

    pygame.display.flip()

    running = False
    in_settings = False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    fn.update(screen, cells, 10)
                    pygame.display.update()
                elif event.key == pygame.K_ESCAPE:
                    fn.escape(screen, cells)
                    send_key = False
                    time.sleep(0.3)
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Pattern save -> Ctrl+S
                    now = datetime.now()
                    filename = f"cells_{now.strftime("%Y-%m-%d_%H-%M-%S_%f")}.csv"
                    df = pd.DataFrame(cells)
                    df.to_csv(f'./patterns/{filename}', index=False)
                    print(f"Saved pattern name: {filename}")

        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        if send_key:
            if not in_settings and mouse_pressed:
                while mouse_pressed:
                    if 0 < mouse_pos[0] < 1200 and 0 < mouse_pos[1] < 600:
                        cells[mouse_pos[1] // 10, mouse_pos[0] // 10] = 1
                        fn.update(screen, cells, 10)
                        pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            mouse_pressed = False
                            break
                        elif event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    mouse_pos = pygame.mouse.get_pos()
        else:
            send_key = True
            

        if running:
            screen.fill(cl.color_back)
            cells = fn.update(screen, cells, 10, with_progress=True)
            pygame.display.update()
            # Time speed
            time.sleep(opts.speeds[opts.speed_index])
        else:
            screen.fill(cl.color_mesh)
            fn.update(screen, cells, 10)
            pygame.display.flip()
