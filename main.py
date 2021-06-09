from tkinter import *
from TkinterDnD2 import *
import os
from functools import partial
from pynput.keyboard import Key, Listener
import time
import tkinter.messagebox


if __name__ == '__main__':
    code = []
    name = []
    boxes = []
    codes = []
    path = []
    pressed_numbers = [10]*4
    x = 0
    t1 = time.time()


    def on_enter(e, button):
        e['background'] = '#282c2e'


    def on_leave(e, button):
        e['background'] = '#212526'

    def drop(index, boxes_i,event):

        if len(path) == index:
            path.append(event.data.replace("{", "").replace("}", ""))

        else:
            path[index] = event.data.replace("{", "").replace("}", "")

        print(event.data.replace("{", "").replace("}", ""))
        sch_name = path[index].split("/")[-1].split(".")[0]
        boxes_i.delete(0, 20)
        boxes_i.insert(0, sch_name) #insert formated  argument

    def create_new_row(boxes, codes):
        i = len(codes)
        print(i)
        codes.append(Entry(root, font=("Times", 20), bg="#212526", fg="white", bd=0))
        codes[i].place(x=10, y=30 + 50 * i, height=40, width=60)

        boxes.append(Entry(root, font=("Courier", 20), bg="#212526", fg="white", bd=0))
        boxes[i].place(x=85, y=30 + 50 * i, height=40, width=180)
        boxes[i].drop_target_register(DND_FILES)
        boxes[i].dnd_bind('<<Drop>>', partial(drop, i, boxes[i]))
        add_button.place(x=Window_width/10*6, y=i*50+80)
        save_button.place(x=Window_width/6, y=i*50+80)
        root.geometry(str(Window_width)+"x"+str(50*i+130))

    def save(codes, names):
        new_names = []
        new_path = []
        with open("data.txt", "w") as f:
            for index, _ in enumerate(codes):
                try:
                    new_names.append(names[index].get().replace(" ", "_"))
                    new_path.append(path[index].replace(" ", "_"))
                except Exception:
                    pass
                if len(codes[index].get()) > 4:
                    tkinter.messagebox.showinfo("Warning", "Please use 4 or less digits in your code")
                f.write(codes[index].get()+" "+new_names[index]+" "+new_path[index]+"\n")
        pass


    def on_press(key):
        global t1
        try:
            if 96 <= key.vk <= 105:
                t2 = time.time()
                print(key.vk-96)
                if t2-t1 > 3:
                    for index, _ in enumerate(pressed_numbers):

                        pressed_numbers[index] = 10
                    find_code(key.vk - 96)

                else:
                    find_code(key.vk-96)
                t1 = t2
        except Exception:
            pass

    def on_release(key):
        if key == Key.esc:
            # Stop listener
            return False

    def find_code(pressed):
        global pressed_numbers
        for index, _ in enumerate(pressed_numbers):
            try:
                pressed_numbers[-index-1] = pressed_numbers[-index-2]
            except Exception:
                pressed_numbers[0] = pressed
        pressed_numbers1 = list(pressed_numbers[::-1])
        full = []
        for index, new in enumerate(codes):
            full.append(new.get())
        ready_codes = full
        for ind, full_code in enumerate(ready_codes):
            list_of_splitted_codes = list(full_code)
            try:
                if int(list_of_splitted_codes[0]) == pressed_numbers1[0] and int(list_of_splitted_codes[1]) == pressed_numbers1[1] and int(list_of_splitted_codes[2]) == pressed_numbers1[2] and int(list_of_splitted_codes[3]) == pressed_numbers1[3]:
                    print('Launch app: ', path[ind])
                    os.startfile(path[ind])
                    pressed_numbers = [10 for _ in pressed_numbers]
            except:
                pass


    #reading the file
    if os.path.isfile("data.txt"):
        with open("data.txt") as f:
            for e, line in enumerate(f.readlines()):

                code.append(line.split()[0])
                try:
                    name.append(line.split()[1].replace("_", " "))
                except:
                    name.append(line.split()[1])
                try:
                    path.append(line.split()[2].replace("_", " "))
                except:
                    path.append(line.split()[2])
    else:
        with open("data.txt", "w+") as f:
            pass

    root = TkinterDnD.Tk()
    var = StringVar()
    root.title('Fast pick')
    Window_width = 270
    Window_high = 45 * len(code) + 120
    root.geometry(str(Window_width)+"x"+str(Window_high))
    root.configure(background='#363636')

    # codes boxes
    for i, entry in enumerate(code):
        codes.append(Entry(root, font=("Times", 20), bg="#212526", fg="white", bd=0))
        codes[i].insert(0, code[i])
        codes[i].place(x=10, y=30 + 50*i, height=40, width=60)

    # file paths drop places
    for i, box in enumerate(name):
        boxes.append(Entry(root, font=("Courier", 20), bg="#212526", fg="white", bd=0))
        boxes[i].place(x=85, y=30+50*i, height=40, width=180)
        boxes[i].drop_target_register(DND_FILES)
        boxes[i].dnd_bind('<<Drop>>', partial(drop, i, boxes[i]))
        boxes[i].insert(0, name[i])

    #add button
    pixelVirtual = PhotoImage(width=1, height=1)
    add_button = Button(
        root, command=partial(create_new_row, boxes, codes), image=pixelVirtual,
        compound="c", text="+", font=("Times", 30), height=40, width=40, bg="#212526", fg="white", bd=0, activebackground='#1b1e1f')

    add_button.place(x=Window_width/10*6, y=len(name)*50+30)
    add_button.bind("<Enter>", partial(on_enter, add_button))
    add_button.bind("<Leave>", partial(on_leave, add_button))



    #save button
    save_button = Button(root, command=partial(save, codes, boxes), image=pixelVirtual,
        compound="c", text="save", font=("Times", 16), height=40, width=40, bg="#212526", fg="white", bd=0, activebackground='#1b1e1f')
    save_button.place(x=Window_width / 6, y=len(name) * 50 + 30)

    save_button.bind("<Enter>", partial(on_enter, save_button))
    save_button.bind("<Leave>", partial(on_leave, save_button))

    #Top labels
    code_label = Label(root, font=("Courier", 15), bg="#212526", fg="white", bd=0, text="Code")
    code_label.place(x=15, y=5)

    path_label = Label(root, font=("Courier", 15), bg="#212526", fg="white", bd=0, text="Drop file")
    path_label.place(x=120, y=5)

    # Collect events until released
    listener = Listener(on_press=on_press, on_release=on_release)

    listener.start()

    root.mainloop()

    listener.stop()




