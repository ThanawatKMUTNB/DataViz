import csv
import tkinter as tk
import csvManager

#creating window
window=tk.Tk()
width= window.winfo_screenwidth() 
height= window.winfo_screenheight()
window.geometry("%dx%d" % (width, height))
window.title("Tableau")

sec = tk.Frame(window)
sec.pack(fill=tk.X,side=tk.TOP)
main_frame = tk.Frame(window)
main_frame.pack(fill=tk.BOTH,expand=1)

my_canvas = tk.Canvas(main_frame)
my_canvas.pack(side=tk.LEFT,fill=tk.BOTH,expand=1)

y_scrollbar = tk.Scrollbar(main_frame,orient=tk.VERTICAL,command=my_canvas.yview)
y_scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
x_scrollbar = tk.Scrollbar(sec,orient=tk.HORIZONTAL,command=my_canvas.xview)
x_scrollbar.pack(side=tk.TOP,fill=tk.X)

my_canvas.configure(yscrollcommand=y_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))

second_frame = tk.Frame(my_canvas)
my_canvas.create_window((0,0), window=second_frame, anchor="nw")

colum = csvManager.getHeader()
for thing,i in zip(colum,range(len(colum))):
    tk.Label(second_frame, text=str(thing),bg = "white").grid(row=0, column=i, pady=20, padx=20)
    row = csvManager.getValueByHead(thing)
    j = 1
    for k in row:
        tk.Label(second_frame, text=str(k),bg = "white").grid(row=j, column=i, pady=20, padx=20)
        j+=1

window.mainloop()
