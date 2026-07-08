# PROJECT HEADER
"""
==========================================
🏎️ F1 REACTION CHALLENGE v1.0
------------------------------------------
Developer : Thamindu Fernando
Language  : Python
Library   : Tkinter

A Formula 1 inspired reaction time game
featuring realistic five-light starts,
false start detection, best time tracking,
and replay functionality.

Version : 1.0
==========================================
"""

# ==========================================
# IMPORTS
# ==========================================
import tkinter as tk
import random
import time

# ==========================================
# GAME VARIABLES
# ==========================================
best_time = None
start_time=None
waiting=False
after_id = None
light_count=0
game_state="idle"

# ==========================================
# MAIN WINDOW
# ==========================================
root =tk.Tk()
root.title("🏎️F1 Reaction Time Challenge v1.0")
root.geometry("900x800")
root.configure(bg="#111111")

# ==========================================
# TITLE
# ==========================================
title = tk.Label(
    root,
    text="F1 REACTION CHALLENGE",
    font=("Segoe UI",20,"bold"),
    bg="#111111",
    fg="#E10600"
)
title.pack(pady=20)

# ==========================================
# START LIGHTS (Canvas)
# ==========================================
canvas=tk.Canvas(
    root,
    width=420,
    height=90,
    bg="#111111",
    highlightthickness=0
)
canvas.pack(pady=20)

lights=[]
for i in range(5):
    light = canvas.create_oval(
        30 + i*75,
        20,
        80+i*75,
        70,
        fill="#222222",
        outline="#555555",
        width=2
    )
    lights.append(light)

# ==========================================
# MAIN LABEL
# ==========================================
label = tk.Label(
    root,
    text="Press START",
    font=("Segoe UI",30,"bold"),
    bg="#111111",
    fg="white"
)
label.pack(pady=35)

# ==========================================
# GAME FUNCTIONS
# ==========================================
def start_game(): 
    global waiting,light_count,game_state,after_id,start_time

    waiting=True
    game_state="waiting"
    light_count=0

    button.config(
        text="START",
        state="disabled"
        )

    label.config(
        text="WAIT...",
        bg="#111111",
        fg="white"
    )
    for light in lights:
        canvas.itemconfig(light, fill="#222222")
    root.configure(bg="#111111")
    show_lights()

   

def show_lights():
    global light_count,after_id,game_state
    if game_state != "waiting":
        return

    canvas.itemconfig(
        lights[light_count],
        fill="#E10600"
    )

    light_count+=1

    #lights = "🔴" * light_count
    #lights += "⚫" *(5-light_count)

    #label.config(text=lights)

    if light_count<5:
        after_id = root.after(700, show_lights)
    else:
        delay = random.randint(500,2500)
        after_id = root.after(delay,turn_green)

def turn_green():
    global start_time,waiting,game_state

    waiting=False
    game_state="green"

    for light in lights:
        canvas.itemconfig(light, fill="#222222")
    
    #root.configure(bg="#00C853")
    
    label.config(text="🏁GO!",fg="#00C853",bg="#111111")
    start_time=time.time()

def click(event):
    global best_time,waiting,after_id,game_state,light_count
    if game_state=="idle":
        return
    
    if game_state=="waiting":
        game_state="idle"
        waiting=False

        if after_id is not None:
            root.after_cancel(after_id)
            after_id=None
        light_count=0
        
        for light in lights:
            canvas.itemconfig(light, fill="#222222")
       

        root.configure(bg="darkred")

        label.config(
            text="FALSE START!\nPress START",
            bg="darkred",
            fg="white"
        )

        button.config(state="normal")
        return


    if game_state=="green":
        
        #game_state="idle"

        reaction=time.time()-start_time
        #milliseconds = int(reaction*1000)

        if best_time is None or reaction < best_time:
            best_time=reaction

        label.config(
            #text=f"Reaction:{milliseconds} ms\nBest: {best_time}ms"
            text=(
                f"REACTION\n"
                f"{reaction:.3f}s\n\n"
                f"🏆 BEST\n"
                f"{best_time:.3f}s"
            )
        )
        button.config(
            text="PLAY AGAIN",
            state="normal"
            )
        game_state="idle"

# ==========================================
# BUTTONS
# ==========================================
button = tk.Button(
    root,
    text="START",
    font=("Segoe UI", 18,"bold"),
    bg="#E10600",
    fg="white",
    activebackground="#C00000",
    activeforeground="white",
    bd=0,
    padx=25,
    pady=10,
    command=start_game
)
button.pack(pady=20)

def go_mainmenu():
    global game_state
    game_state="idle"
    root.configure(bg="#111111")

    label.config(
        text="Press START",
        bg="#111111",
        fg="white"
         )
    
    for light in lights:
        canvas.itemconfig(light, fill="#222222")
    button.config(
        text="START",
        state="normal"
    )

mainmenu_button=tk.Button(
    root,
    text="MAIN MENU",
    font=("Segoe UI",14,"bold"),
    bg="#333333",
    fg="white",
    command=go_mainmenu
)
mainmenu_button.pack(pady=10)

# ==========================================
# EVENT BINDINGS
# ==========================================
root.bind_all("<Button-1>", click)

# ==========================================
# START APPLICATION
# ==========================================
root.mainloop()