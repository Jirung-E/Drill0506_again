from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024


def load_resources():
    global TUK_ground, character
    global arrow
    
    TUK_ground = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')
    arrow = load_image('hand_arrow.png')


def handle_events():
    global running
    global mx, my

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, TUK_HEIGHT - 1 - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass


def reset_world():
    global running
    global frame
    global action
    global cx, cy
    global mx, my
    global points

    mx, my = 0, 0
    running = True
    frame = 0
    action = 3
    cx, cy = TUK_WIDTH // 2, TUK_HEIGHT // 2

    points = [(100, 900), (1200, 800), (500, 100)]

    set_new_target_arrow()


def set_new_target_arrow():
    global sx, sy
    global hx, hy
    global t
    global action
    global frame
    global target_exists

    if points:
        sx, sy = cx, cy
        hx, hy = points[0]
        t = 0.0
        action = 1 if cx < hx else 0
        frame = 0
        target_exists = True
    else:
        action = 3 if action == 1 else 2
        frame = 0
        target_exists = False


def render_world():
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    for p in points:
        arrow.draw(p[0], p[1])
    arrow.draw(mx, my)
    character.clip_draw(frame * 100, 100 * action, 100, 100, cx, cy)
    update_canvas()


def update_world():
    global frame
    global cx, cy
    global t

    frame = (frame + 1) % 8

    if target_exists:
        if t <= 1.0:
            cx = (1-t)*sx + t*hx
            cy = (1-t)*sy + t*hy
            t += 0.001
        else:
            cx, cy = hx, hy
            del points[0]
            set_new_target_arrow()


open_canvas(TUK_WIDTH, TUK_HEIGHT)
hide_cursor()
load_resources()
reset_world()

while running:
    render_world()  # 월드의 현재 내용을 그린다.
    handle_events() # 사용자 입력을 받아들인다. 
    update_world()  # 월드 안의 객체들의 상호작용을 계산하고 그 내용을 업데이트한다.


close_canvas()
