# CSináljunk egy számológépet
# Legyen entry mező
# Gombok 1-9
# Műveleti jelek (+, -, *, /)
# Egyenlőségjel


import tkinter as tk
import sys

print("Innen jön:", sys.argv)


### Gombkreáló metódus ############################################################

def gombkreálás(x):
    gomb=tk.Button(Gomb_frame, text= f"{x}", command= lambda b=x: gombnyomás(b) )
    gomb.grid(row=f"{sorszám}", column=f"{oszlopszám}", sticky="nsew")
    Gomb_frame.grid_columnconfigure(oszlopszám, weight=1)
    Gomb_frame.grid_rowconfigure(sorszám, weight=1)

### Gombnyomás metódus ############################################################

def gombnyomás(gomb):
    if gomb=="=":
        kiszámolás()
    elif gomb=="<-":
        karaktertörlés()
    elif gomb=="C":
        entrytörlés()
    else:
        entry_mezo.insert(tk.END, gomb)


### kiszámolás metódus ###########################################################

def kiszámolás():
    feladat=entry_mezo.get()
    végeredmény=eval(feladat)
    entry_mezo.delete(0,tk.END)
    entry_mezo.insert(0, végeredmény)

### egy karakter törlése metódus ################################################

def karaktertörlés():
    karakterek=entry_mezo.get()
    entry_mezo.delete(len(karakterek)-1)

### "C" billentyű parancsa#######################################################

def entrytörlés():
    entry_mezo.delete(0, "end")


### Program ######################################################################

root=tk.Tk()
root.title("Első számológépem")

width=400
height=500

elhelyezés_width=root.winfo_screenwidth()
elhelyezés_height=root.winfo_screenheight()

ballfelso_width=(elhelyezés_width//2)-(width//2)
ballfelso_height=(elhelyezés_height//2)-(height//2)

root.geometry(f"{width}x{height}+{ballfelso_width}+{ballfelso_height}")

# ENtry Frame + entry mező ###################################################

Entry_frame=tk.Frame(root, width= 30)
Entry_frame.pack(side="top", pady=10, padx=4, fill="y", expand=True)

entry_mezo=tk.Entry(Entry_frame, text=f" ")
entry_mezo.pack()


lst_szamok=[1,2,3,4,5,6,7,8,9]
lst_muveletijelek=["+",0, "-", "/", "*", "=", "C","<-", "."]


# Gombframe + gombok##########################################################

Gomb_frame=tk.Frame(root, bg="lightblue")
Gomb_frame.pack(expand=True, fill= "both")

sorszám= 0
oszlopszám=0
for x in lst_szamok+lst_muveletijelek:
    gombkreálás(x)
    oszlopszám+=1
    if oszlopszám==3:
        sorszám+=1
        oszlopszám=0
    
        
    
    

root.mainloop()
