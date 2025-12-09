from tkinter import Tk, Canvas, Label
from PIL import Image, ImageTk
import os
import pygame
import random

pygame.mixer.init()

meow_sound = pygame.mixer.Sound("assets/sounds/007_meow.wav")
hit_sound = pygame.mixer.Sound("assets/sounds/001_jump.wav")
win_sound = pygame.mixer.Sound("assets/sounds/003_congratulations.wav")
lose_sound = pygame.mixer.Sound("assets/sounds/002_we-lost.wav")

WIDTH = 500
HEIGHT = 500

root = Tk()
root.title("CS101-COLLECT GAME-FINAL PROJECT")
canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

bg_img = Image.open("assets/orig.png").resize((WIDTH, HEIGHT), Image.NEAREST)
root.bg_photo = ImageTk.PhotoImage(bg_img)

def load_player_frames(spritesheet, row, num_frames=4):
    frames = []
    for i in range(num_frames):
        left = i * 16
        top = row * 16
        right = left + 16
        bottom = top + 16
        frame = spritesheet.crop((left, top, right, bottom))
        frame = frame.resize((32, 32), Image.NEAREST)
        frames.append(ImageTk.PhotoImage(frame))
    return frames

spritesheet = Image.open("assets/player_front.png")
root.player_down = load_player_frames(spritesheet, 0)
root.player_right = load_player_frames(spritesheet, 2)
root.player_left = load_player_frames(spritesheet, 3)

item_img = Image.open("assets/PinkCloud.png").resize((16, 16), Image.NEAREST)
root.item_sprite = ImageTk.PhotoImage(item_img)

fake_item_img = Image.open("assets/002 - Edited.png").resize((18, 18), Image.NEAREST)
root.fake_item_sprite = ImageTk.PhotoImage(fake_item_img)

enemy_frames = []
for fname in sorted(os.listdir("assets/enemy")): 
    if fname.endswith(".png"):
        img = Image.open(f"assets/enemy/{fname}").resize((40, 40), Image.NEAREST)
        enemy_frames.append(ImageTk.PhotoImage(img))
root.enemy_frames = enemy_frames

score_label = Label(root, text="Score: 0", fg="white", bg="black")
canvas.create_window(60, 15, window=score_label)

time_label = Label(root, text="Time: 60", fg="white", bg="black")
canvas.create_window(200, 15, window=time_label)

win_label = Label(root, text="Win: 5 items", fg="yellow", bg="black")
canvas.create_window(320, 15, window=win_label)

canvas.create_line(0, 30, WIDTH, 30, fill="white")
canvas.create_image(0, 0, anchor="nw", image=root.bg_photo)

# Game state
data = {
    "player": [20, 40],
    "items": [
        [100, 100],
        [120, 100],
        [200, 150],
        [250, 300],
        [300, 400]
    ],
    "score": 0,
    "real_items_collected": 0
}

# Initialize player
px, py = data["player"]
player = canvas.create_image(px, py, image=root.player_down[0])
player_dir = "down"
player_frame_index = 0

game_running = True
timer = 60
lives = 2
hit_cooldown = 0

items = []
item_timers = {}
item_metadata = {}
real_items_count = 0
fake_items_count = 0
TARGET_FAKE_ITEMS = 5
TARGET_REAL_ITEMS = 3

def get_random_position():
    margin = 30
    return (random.randint(margin, WIDTH - margin),
            random.randint(margin + 30, HEIGHT - margin))

def create_item_at_position(x, y, is_real):
    if not game_running:
        return
    
    sprite = root.item_sprite if is_real else root.fake_item_sprite
    item = canvas.create_image(x, y, image=sprite)
    items.append(item)
    item_metadata[item] = "real" if is_real else "fake"
    
    global real_items_count, fake_items_count
    if is_real:
        real_items_count += 1
    else:
        fake_items_count += 1
    
    outline_color = "green" if is_real else "gray"
    width = 3 if is_real else 2
    countdown_circle = canvas.create_oval(x - 20, y - 20, x + 20, y + 20,
                                          outline=outline_color, width=width, fill="")
    
    item_timers[item] = {
        "time_left": 5,
        "timer_id": None,
        "countdown_circle": countdown_circle
    }
    
    item_countdown(item)

def remove_item(item):
    cancel_item_timer(item)
    canvas.delete(item)
    if item in items:
        items.remove(item)
    if item in item_metadata:
        item_type = item_metadata[item]
        del item_metadata[item]
        return item_type
    return None

def touch():
    px_center, py_center = canvas.coords(player)
    x1, y1 = px_center - 16, py_center - 16
    x2, y2 = px_center + 16, py_center + 16
    found_items = canvas.find_overlapping(x1, y1, x2, y2)

    for item in found_items:
        if item not in items or item not in item_metadata:
            continue
            
        item_type = item_metadata[item]
        item_x, item_y = canvas.coords(item)
        remove_item(item)
        
        if item_type == "fake":
            global fake_items_count
            fake_items_count -= 1
            update_lives(-1)
            maintain_fake_items()
        else:
            global real_items_count
            real_items_count -= 1
            data["score"] += 1
            data["real_items_collected"] += 1
            score_label.config(text=f"Score: {data['score']}")
            meow_sound.play()
            flash_player()
            popup_plus_one(item_x, item_y)
            
            if data["real_items_collected"] >= 5:
                global game_running
                game_running = False
                win_sound.play()
                canvas.create_text(WIDTH / 2, HEIGHT / 2, text="🎉 YOU WIN! 🎉",
                                   fill="yellow", font=("Arial", 20, "bold"))
                return
            
            maintain_real_items()
            maintain_fake_items()  

def move_player(dx, dy, direction):
    if not game_running:
        return
    global player_dir
    canvas.move(player, dx, dy)
    player_dir = direction
    touch()

def up_handler(event):
    move_player(0, -10, "down")

def down_handler(event):
    move_player(0, 10, "down")

def left_handler(event):
    move_player(-10, 0, "left")

def right_handler(event):
    move_player(10, 0, "right")

for key, handler in [("<Up>", up_handler), ("w", up_handler),
                     ("<Down>", down_handler), ("s", down_handler),
                     ("<Left>", left_handler), ("a", left_handler),
                     ("<Right>", right_handler), ("d", right_handler)]:
    root.bind(key, handler)


def clamp_position(x, y, margin=30):
    return (max(margin, min(WIDTH - margin, x)),
            max(margin + 30, min(HEIGHT - margin, y)))

def move_items():
    if not game_running:
        return
    
    px, py = canvas.coords(player)
    margin = 30
    
    for item in items:
        if item not in item_timers:
            continue
        
        try:
            item_x, item_y = canvas.coords(item)
        except:
            continue
        
        dx = random.randint(-15, 15)
        dy = random.randint(-15, 15)
        new_x, new_y = clamp_position(item_x + dx, item_y + dy, margin)
        
        distance = ((new_x - px) ** 2 + (new_y - py) ** 2) ** 0.5
        if distance < 50:
            new_x += 20 if new_x < px else -20
            new_y += 20 if new_y < py else -20
            new_x, new_y = clamp_position(new_x, new_y, margin)
        
        canvas.coords(item, new_x, new_y)
        
        if item in item_timers and item_timers[item]["countdown_circle"]:
            circle = item_timers[item]["countdown_circle"]
            canvas.coords(circle, new_x - 20, new_y - 20, new_x + 20, new_y + 20)
    
    root.after(500, move_items)

def maintain_real_items():
    global real_items_count
    real_items_count = sum(1 for item in items 
                          if item in item_metadata and item_metadata[item] == "real")
    while real_items_count < TARGET_REAL_ITEMS:
        spawn_item_with_timer(real_only=True)

def maintain_fake_items():
    global fake_items_count
    fake_items_count = sum(1 for item in items 
                          if item in item_metadata and item_metadata[item] == "fake")
    while fake_items_count < TARGET_FAKE_ITEMS:
        spawn_item_with_timer(real_only=False)

def spawn_item_with_timer(real_only=False):
    x, y = get_random_position()
    create_item_at_position(x, y, real_only)

def get_countdown_color(time_left, is_real):
    if is_real:
        return "green" if time_left > 3 else ("yellow" if time_left > 1.5 else "red")
    else:
        return "gray" if time_left > 3 else ("light gray" if time_left > 1.5 else "dark gray")

def item_countdown(item_id):
    if not game_running or item_id not in items or item_id not in item_timers:
        return
    
    timer_info = item_timers[item_id]
    timer_info["time_left"] -= 0.1
    is_real = item_id in item_metadata and item_metadata[item_id] == "real"
    
    if timer_info["countdown_circle"]:
        x, y = canvas.coords(item_id)
        color = get_countdown_color(timer_info["time_left"], is_real)
        canvas.coords(timer_info["countdown_circle"], x - 20, y - 20, x + 20, y + 20)
        canvas.itemconfig(timer_info["countdown_circle"], outline=color)
    
    if timer_info["time_left"] <= 0:
        if item_id in items:
            items.remove(item_id)
        canvas.delete(item_id)
        if timer_info["countdown_circle"]:
            canvas.delete(timer_info["countdown_circle"])
        if item_id in item_timers:
            del item_timers[item_id]
        if item_id in item_metadata:
            del item_metadata[item_id]
        
        global real_items_count, fake_items_count
        if is_real:
            real_items_count -= 1
            maintain_real_items()
        else:
            fake_items_count -= 1
            maintain_fake_items()
    else:
        timer_info["timer_id"] = root.after(100, lambda: item_countdown(item_id))

def cancel_item_timer(item_id):
    if item_id not in item_timers:
        return
    
    timer_info = item_timers[item_id]
    if timer_info["timer_id"]:
        root.after_cancel(timer_info["timer_id"])
    if timer_info["countdown_circle"]:
        canvas.delete(timer_info["countdown_circle"])
    del item_timers[item_id]

def countdown():
    global timer, game_running
    if not game_running:
        return
    
    if timer > 0:
        timer -= 1
        time_label.config(text=f"Time: {timer}")
        root.after(1000, countdown)
    else:
        game_over()

def draw_lives_bar():
    global lives
    canvas.delete("lives_bar")
    bar_x, bar_y = 350, 15
    
    for i in range(2):
        heart_x = bar_x + i * 25
        heart = "❤️" if i < lives else "🤍"
        canvas.create_text(heart_x, bar_y, text=heart, 
                          font=("Arial", 16), tags="lives_bar")

def update_lives(change):
    global lives
    lives = max(0, min(2, lives + change))
    draw_lives_bar()
    if lives == 0:
        game_over()

def get_player_frames_for_direction():
    direction_map = {
        "down": root.player_down,
        "left": root.player_left,
        "right": root.player_right
    }
    return direction_map.get(player_dir, root.player_down)

def get_direction_row():
    row_map = {"down": 0, "left": 3, "right": 2}
    return row_map.get(player_dir, 0)

def flash_player():
    grow_count = [0]
    frames = get_player_frames_for_direction()
    current_frame = frames[player_frame_index % len(frames)]
    
    img = Image.open("assets/player_front.png")
    row = get_direction_row()
    frame_idx = player_frame_index % 4
    base_frame = img.crop((frame_idx * 16, row * 16, (frame_idx + 1) * 16, (row + 1) * 16))
    
    sizes = [32, 38, 44, 48, 44, 38, 32]
    scaled_frames = [ImageTk.PhotoImage(base_frame.resize((s, s), Image.NEAREST)) 
                     for s in sizes]
    
    def grow_animation():
        if grow_count[0] < len(scaled_frames):
            canvas.itemconfig(player, image=scaled_frames[grow_count[0]])
            root._temp_grow_frame = scaled_frames[grow_count[0]]
            grow_count[0] += 1
            root.after(40, grow_animation)
        else:
            canvas.itemconfig(player, image=current_frame)
    
    grow_animation()

def popup_plus_one(x, y):
    popup_text = canvas.create_text(x, y, text="+1", fill="yellow", 
                                   font=("Arial", 16, "bold"))
    popup_count = [0]
    fade_colors = ["yellow", "#FFD700", "#FFA500", "#FF8C00", "orange"]
    
    def popup_animation():
        if popup_count[0] < 12:
            canvas.move(popup_text, 0, -4)
            if popup_count[0] < len(fade_colors):
                canvas.itemconfig(popup_text, fill=fade_colors[popup_count[0] - 1])
            popup_count[0] += 1
            root.after(40, popup_animation)
        else:
            canvas.delete(popup_text)
    
    popup_animation()

def animate_player():
    global player_frame_index
    if not game_running:
        return
    
    frames = get_player_frames_for_direction()
    player_frame_index = (player_frame_index + 1) % len(frames)
    canvas.itemconfig(player, image=frames[player_frame_index])
    root.after(120, animate_player)

def animate_enemy():
    global enemy_frame_index
    if not game_running:
        return
    enemy_frame_index = (enemy_frame_index + 1) % len(root.enemy_frames)
    canvas.itemconfig(enemy, image=root.enemy_frames[enemy_frame_index])
    root.after(120, animate_enemy)

def game_over():
    global game_running
    game_running = False
    lose_sound.play()
    canvas.create_text(WIDTH / 2, HEIGHT / 2, text="GAME OVER!",
                       fill="red", font=("Arial", 24, "bold"))

def chase_player():
    global chasing_active, lives, hit_cooldown
    if not game_running or not chasing_active:
        return
    
    px, py = canvas.coords(player)
    ex, ey = canvas.coords(enemy)
    distance = ((px - ex) ** 2 + (py - ey) ** 2) ** 0.5
    
    if distance < 25:
        if hit_cooldown <= 0:
            lives -= 1
            hit_sound.play()
            draw_lives_bar()
            hit_cooldown = 60
            if lives <= 0:
                chasing_active = False
                game_over()
                return
        else:
            hit_cooldown -= 1
    elif hit_cooldown > 0:
        hit_cooldown -= 1
    
    dx = (px - ex) * 0.02
    dy = (py - ey) * 0.02
    canvas.move(enemy, dx, dy)
    root.after(60, chase_player)

animate_player()

enemy = canvas.create_image(400, 400, image=root.enemy_frames[0])
enemy_frame_index = 0
chasing_active = True
animate_enemy()
chase_player()

draw_lives_bar()
countdown()

for item in items:
    if item in item_timers:
        item_countdown(item)

maintain_real_items()
maintain_fake_items()
move_items()

root.mainloop()



