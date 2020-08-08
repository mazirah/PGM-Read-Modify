import numpy
from tkinter import *
from PIL import Image, ImageTk

#Reading of the original file
def get_pgm_data():
    try:
        global filename
        filename = e.get()
        with open(filename, "r") as f:
            content = f.readlines()
            global size
            size=[]
            global Lmax 
            Lmax=0
            global data
            data=[]
            global comments
            comments=[]
            for line in list(content):
                if line[0] == "#":
                    comments.append(line)
                    content.remove(line)
            if content[0].strip() != "P2":
                e.delete(0, END)
                status['text'] = "Това не е PGM файл"
            else:
                size = [int(el) for el in content[1].strip().split()]
                Lmax = int(content[2].strip())
                for line in content[3:]:
                     for el in line.split():
                         data.append(int(el))
                #get_file_button['state'] = DISABLED #if you remove the comment the program will work only with 1 file 
                status['text'] = "Файлът беше успешно зареден"
                open_file['state'] = ACTIVE
    except OSError:
        status['text'] = "Файлът не е намерен"
   
#Showing the original image on the screen
def open_original_pgm():
    original_image = Toplevel(root)
    original_image.iconbitmap("img\\icona.ico")
    original_image.title(filename)
    original_image.resizable(0,0)
    original_image.transient(root)
    #using nympy array to get the image information
    new_data = numpy.array(data).reshape(size[1], size[0])
    #creating and displaying of the image on the screen
    img = ImageTk.PhotoImage(image = Image.fromarray(new_data))
    c = Canvas(original_image, width=size[0], height=size[1])
    c.pack()
    c.create_image(0,0, anchor="nw", image = img)
    #right click mouse event for showing the additional field on the screen
    c.bind("<Button-3>", enable_mod)
    koef_text = Label(original_image, text="коефициент:")
    koef_text.pack(side=LEFT)

    k_v = Entry(original_image, width=15)
    k_v.pack(side=LEFT)

    stepen_text = Label(original_image,text="степен:")
    stepen_text.pack(side=LEFT)

    img4 = PhotoImage(file="img\\adjust.png")

    s_v = Entry(original_image, width=15)
    s_v.pack(side=LEFT)
    #calling the input validation function for both fields to ensure only numerals are entered
    reg = original_image.register(only_numbers)
    k_v.config(validate="key", validatecommand=(reg, '%S'))
    s_v.config(validate="key", validatecommand=(reg, '%S'))
    #lambda function to use the inputs from the fields otherwise tkinter can't use them
    x = lambda:open_modified_pgm(float(k_v.get()), float(s_v.get()))

    global modify
    modify = Button(original_image, image=img4, compound="left", text= "Промени", state=DISABLED, command=x)
    modify.pack(side=RIGHT)

    #positioning of the image according to the main window
    original_image.update_idletasks()
    windowWidth = original_image.winfo_reqwidth()
    windowHeight = original_image.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(original_image.winfo_screenwidth()/2 -  windowWidth/2-(windowHeight/2))
    positionDown = int(original_image.winfo_screenheight()/2 - windowHeight/2)
    # Positions the window in the center of the page.
    original_image.geometry("+{}+{}".format(positionRight, positionDown))

    original_image.mainloop()
    
#Showing the moified image on the screen
def open_modified_pgm(k,s):
    modified_image = Toplevel(root)
    modified_image.iconbitmap("img\\icona.ico")
    modified_image.title(filename.rstrip(".pgm")+"_mod.pgm")
    modified_image.resizable(0,0)
    modified_image.transient(root)
    global data1
    #creating and modifying of the new image 
    data1 = numpy.array(data).reshape(size[1], size[0])
    with numpy.nditer(data1, op_flags=['readwrite']) as it:
        for x in it:
            x[...] = Lmax*(x/Lmax)**(k/s)
    img = ImageTk.PhotoImage(image = Image.fromarray(data1))
    c = Canvas(modified_image, width=size[0], height=size[1])
    c.pack()
    c.create_image(0,0, anchor="nw", image = img)
    img5 = PhotoImage(file="img\\sd-card.png")
    open_file = Button(modified_image, image=img5, compound="left", text= "Запази", command=save_new_pgm, state=ACTIVE)
    open_file.pack(side=BOTTOM)
    modify['state'] = DISABLED
    status['text'] = "Модификация на файла..."
    #positioning of the image according to the main window
    modified_image.update_idletasks()
    windowWidth = modified_image.winfo_reqwidth()
    windowHeight = modified_image.winfo_reqheight()
    # Gets both half the screen width/height and window width/height
    positionRight = int(modified_image.winfo_screenwidth()/2 - windowWidth/2+(windowHeight/2))
    positionDown = int(modified_image.winfo_screenheight()/2 - windowHeight/2)
    # Positions the window in the center of the page.
    modified_image.geometry("+{}+{}".format(positionRight, positionDown))

    modified_image.mainloop()
    
#saving the modified mage as a file
def save_new_pgm():
    with open(filename.rstrip(".pgm")+"_mod.pgm", "w") as f:
        f.writelines("P2\n")
        f.writelines("# modified by PGM Read&Modify\n")
        for line in list(comments):
            #if the file was aleady modified by the program, making sure to remove the comment
            if line.strip() == "# modified by PGM Read&Modify":
                comments.remove(line)
            else:
                f.writelines(line)
        f.writelines(str(size[0])+" "+str(size[1])+"\n")
        f.writelines(str(Lmax)+"\n")
        #formating the image information so it can be dispalyed properly by any app
        for line in data1.tolist():
            f.writelines(str(line)[str(line).find("[")+1 : str(line).find("]")].replace(",", "")+"\n")    
    status['text'] = "Файлът беше записан успешно като "+filename.rstrip(".pgm")+"mod.pgm"

#input validation to make sure the iput is either a number, a space or a dot f0r floatng numbers
def only_numbers(inp):
    if inp.isdigit():
        return True
    elif inp == "":
        return True
    elif inp == ".":
        return True
    else:
        return False

#changing the state of "Change" button("Промени")
def enable_mod(event):
    modify['state'] = ACTIVE

#using this to be able to call get_pgm_data via enter button
def call_get_pgm(event):
    get_pgm_data()

#function to use in event to create a popup menu
def popup(event):
    try:
        popup_menu.tk_popup(event.x_root, event.y_root,0)
    finally:
         popup_menu.grab_release()



#Creating of the main window
root = Tk()
root.iconbitmap("img\\icona.ico")
root.title("PGM Read&Modify")
root.resizable(0,0) #this disables rezising of the window
#root.attributes("-toolwindow",1) #hides the window control button under windows. As a side effect it also hides the program icon.
#root.overrideredirect(1) #hides all the elements of the window control manager. Bad idea to use under winodws, works on linux or mac though.

#Creating the top frame where the buttons and path to file elements reside
top_frame = Frame(root)
top_frame.pack(side=TOP, fill=X)

#Creating of the bottom frame to hold the status bar element
bottom_frame = Frame(root)
bottom_frame.pack(side=BOTTOM, fill=X)
filename = Label(top_frame, text="Файл:")
filename.pack(side=LEFT, anchor=W)
e = Entry(top_frame, width=67)
e.pack(side=LEFT)
e.focus()
e.bind("<Return>", call_get_pgm)

#Creates the popup menu with an option to exit the program
popup_menu = Menu(root, tearoff=0)
popup_menu.add_command(label="Exit", command=root.destroy)

#Creating the images for the buttons
img = ImageTk.PhotoImage(Image.open("img\\pgm.jpg"))
img1 = PhotoImage(file = "img\\file.png")
img2  = PhotoImage(file ="img\\display.png")
background = Label(bottom_frame,image=img)
background.pack(side=TOP)

status_text = Label(bottom_frame, text="статус:", bd=1, relief=SUNKEN)
status_text.pack(side=LEFT)

status = Label(bottom_frame, text="Изчакване", bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

root.bind("<Button-3>", popup)

get_file_button = Button(top_frame, image=img1, text="Отвори", command=get_pgm_data, state=ACTIVE, compound="left")
get_file_button.pack(side=RIGHT)

open_file = Button(top_frame, image=img2, text= "Покажи", command=open_original_pgm, state=DISABLED, compound="left")
open_file.pack(side=LEFT)

#Centering of the main window according to screen resolution
root.withdraw()
root.update_idletasks()
x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.geometry("+%d+%d" % (x, y))
root.deiconify()

root.mainloop()
