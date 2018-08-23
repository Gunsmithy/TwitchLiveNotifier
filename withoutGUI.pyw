import twitchlivenotifier as tln
import tkinter as tk

def popUp():
    root = tk.Tk()
    tk.Label(root, text="Your streamer is live", fg="Red", font="Arial 20 bold").pack()
    root.mainloop()

tln.config()
tln.lock()

root = tk.Tk()
tk.Label(root, text="Twitch Live Notivier is active, now you can close window", fg="Green", font="Arial 15").pack()
root.mainloop()

tln.main()
popUp()
