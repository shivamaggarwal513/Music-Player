from tkinter import *
from pygame import mixer
from tkinter import filedialog
import threading
import os
from mutagen.mp3 import MP3
import time

#defining the main window of application
root = Tk()
mixer.init()

theme = "black"

root.geometry("680x350")
root.config(background = "black")
root.title("RS Music")

#bottom frame
statusbar = Label(root, fg = "white", background = "black")
statusbar.pack(side = BOTTOM, fill = X)

#default file to be played if no file is selected
filename = "My Life is Going On.mp3"

#function to exit the application
def exitroot():
    mixer.music.stop()
    root.destroy()

#function to browse a file stored in storage
def browsefile():
    global filename
    filename = filedialog.askopenfilename()

def changeTheme():
    global theme

    if theme == "black":
        theme = "white"
        root.config(background = "white")
        statusbar.config(fg = "black", background = "white")
        welcome_txt.config(fg = "black", background = "white")
        right.config(background = "white")
        left.config(background = "white")
        music_img.config(file = "ProjectImages\\LightTheme\\music.png")
        total_len.config(fg = "black", background = "white")
        current_len.config(fg = "black", background = "white")
        middle.config(background = "white")
        play_img.config(file = "ProjectImages\\LightTheme\\play.png")
        pause_img.config(file = "ProjectImages\\LightTheme\\pause.png")
        stop_img.config(file = "ProjectImages\\LightTheme\\stop.png")
        bottom.config(background = "white")
        mute_img.config(file = "ProjectImages\\LightTheme\\mute.png")
        rewind_img.config(file = "ProjectImages\\LightTheme\\replay.png")
        unmute_img.config(file = "ProjectImages\\LightTheme\\volume.png")
        vol_scale.config(fg = "black", background = "white")
    
    else:
        theme = "black"
        root.config(background = "black")
        statusbar.config(fg = "white", background = "black")
        welcome_txt.config(fg = "white", background = "black")
        right.config(background = "black")
        left.config(background = "black")
        music_img.config(file = "ProjectImages\\DarkTheme\\music.png")
        total_len.config(fg = "white", background = "black")
        current_len.config(fg = "white", background = "black")
        middle.config(background = "black")
        play_img.config(file = "ProjectImages\\DarkTheme\\play.png")
        pause_img.config(file = "ProjectImages\\DarkTheme\\pause.png")
        stop_img.config(file = "ProjectImages\\DarkTheme\\stop.png")
        bottom.config(background = "black")
        mute_img.config(file = "ProjectImages\\DarkTheme\\mute.png")
        rewind_img.config(file = "ProjectImages\\DarkTheme\\replay.png")
        unmute_img.config(file = "ProjectImages\\DarkTheme\\volume.png")
        vol_scale.config(fg = "white", background = "black")

def about():
    about_window = Tk()
    about_window.title("About")
    about_window.geometry("210x85")
    about_labelf = LabelFrame(about_window, text = "RS Music", font = {'Segoe UI', 14, 'bold'})
    about_labelf.pack(padx = 10, pady = 10)
    about_text = Label(about_labelf, text = "© Shivam Aggarwal \nDelhi Technological University", font = 'Ariel 10')
    about_text.pack(padx = 2, pady = 2)
    about_window.mainloop()


#top frame, menu and submenu of File options
menubar = Menu(root, tearoff = 0)
root.config(menu = menubar)

submenu1 = Menu(menubar, tearoff = 0)
submenu2 = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = submenu1)
submenu1.add_command(label = "Open", command = browsefile)
submenu1.add_command(label = "Exit", command = exitroot)
menubar.add_command(label = "About", command = about)

#top heading
welcome_txt = Label(root, text = 'UI Media Player', fg = "white", background = "black", font = 'Ariel 16')
welcome_txt.pack()

#right frame
right = Frame(root)
right.config(background = "black")
right.pack(side = RIGHT, padx = 10)

#left frame
left = Frame(root)
left.config(background = "black")
left.pack(side = LEFT, padx = 10)

music_img = PhotoImage(file = "ProjectImages\\DarkTheme\\music.png")
music_btn = Button(left, image = music_img, command = changeTheme)
music_btn.grid(row = 0, column = 0, padx = 5)

top = Frame(right)
top.pack(side = TOP)

#function to show total time of media being played
def total(song_time):
    timing = MP3(song_time).info.length #using mutagen module extracting song length
    mints, scnds = divmod(timing, 60) #dividing timing into minutes and seconds
    mints = round(mints)
    scnds = round(scnds)
    if scnds == 60:
        mints +=1
        scnds = 0
    total_len['text'] = "  Total length : {:02}:{:02}  ".format(mints, scnds)
    thread = threading.Thread(target=current, args = (timing, )) #calling the second thread to show current time left which is updating every second
    thread.start()

#function to show realtime timing status of media being played
def current(clength):
    global rew
    t = clength
    while clength and mixer.music.get_busy():
        if paused:
            continue
        elif rew == True:
            rew = False
            break
        else:
            mints, scnds = divmod(clength, 60)
            mints = round(mints)
            scnds = round(scnds)
            if scnds == 60:
                mints +=1
                scnds = 0
            current_len['text'] = "Current length : {:02}:{:02}".format(mints, scnds)
            time.sleep(1)
            clength -= 1
    if mixer.music.get_busy() == False:
        mints, scnds = divmod(t, 60)
        mints = round(mints)
        scnds = round(scnds)
        if scnds == 60:
            mints +=1
            scnds = 0
        current_len['text'] = "Current length : {:02}:{:02}".format(mints, scnds)

#default timings when no media is selected
total_len = Label(top, text = "  Total length : --:--  ", fg = "white", background = "black")
total_len.pack()

current_len = Label(top, text = "Current length : --:--", fg = "white", background = "black")
current_len.pack()

#middle frame
middle = Frame(right) 
middle.config(background = "black")
middle.pack()

#function to play and show play status of media in bottom frame
def playfunc():
    global paused
    global filename
    if paused:
        mixer.music.unpause()
        paused = False
        statusbar['text'] = "Playing" + " : " + os.path.basename(filename) #extracting the basename from file path
    else:
        mixer.music.load(filename)
        mixer.music.play()
        total(filename)
        statusbar['text'] = "Playing" + " : " + os.path.basename(filename)

paused = False

#function to pause and show pause status of media in bottom frame
def pausefunc():
    global paused
    mixer.music.pause()
    paused = True
    statusbar['text'] = "Music Paused"

#function to stop and show stop status of media in bottom frame
def stopfunc():
    global paused
    mixer.music.stop()
    paused = False
    statusbar['text'] = "Music Stopped"

rew = False

#function to rewind the media
def rewindfunc():
    global rew
    playfunc()
    rew = True

#function to control volume
def volume(value):
    vol = float(value)/100
    mixer.music.set_volume(vol)

muted = False

#function to mute media or to set volume back to 50
def mutefunc():
    global muted
    if muted:
        mute_btn.config(image = mute_img)
        mixer.music.set_volume(0.5)
        vol_scale.set(50)
        muted = False
    else:
        mute_btn.config(image = unmute_img)
        mixer.music.set_volume(0)
        vol_scale.set(0)
        muted = True

#play button
play_img = PhotoImage(file = "ProjectImages\\DarkTheme\\play.png")
play_btn = Button(middle, image = play_img, command = playfunc)
play_btn.grid(row = 0, column = 0, padx = 5)

#pause button
pause_img = PhotoImage(file = "ProjectImages\\DarkTheme\\pause.png")
pause_btn = Button(middle, image = pause_img, command = pausefunc)
pause_btn.grid(row = 0, column = 1, pady =5)

#stop button
stop_img = PhotoImage(file = "ProjectImages\\DarkTheme\\stop.png")
stop_btn = Button(middle, image = stop_img, command = stopfunc)
stop_btn.grid(row = 0, column = 2, padx = 5, pady =5)

#bottom frame
bottom = Frame(right)
bottom.config(background = "black")
bottom.pack(side = BOTTOM) 

#mute button
mute_img = PhotoImage(file = "ProjectImages\\DarkTheme\\mute.png")
mute_btn = Button(bottom, image = mute_img, command = mutefunc)
mute_btn.grid(row = 0, column = 0,padx = 5, pady =5)

#rewind button
rewind_img = PhotoImage(file = "ProjectImages\\DarkTheme\\replay.png")
rewind_btn = Button(bottom, image = rewind_img, command = rewindfunc)
rewind_btn.grid(row = 0, column = 1,padx = 5, pady = 5)

#volume button
unmute_img = PhotoImage(file = "ProjectImages\\DarkTheme\\volume.png")

#volume slider
vol_scale = Scale(bottom, from_ = 0, to = 100, orient = HORIZONTAL, command = volume, fg = "white", background = "black")
vol_scale.grid(row = 0, column = 2, padx = 10)
vol_scale.set(50)

#marking the end of the tkinter infinite loop
root.mainloop()
