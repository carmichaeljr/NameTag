#Made by student Jack Carmichael
#All rights reserved ;D
"""===============================================================================================================
Object--------------------Parameters--------------Inheritance
Tkinter Wrapper
    -Window()             -name                   -object
    -WindowMenu()         -window                 -object
    -WindowMenuCascade()  -window                 -object
    -GroupWidgetActions() -none                   -object
    -WindowFrame()        -window                 -GroupWidgetActions
    -WindowButton()       -window,name,action     -GroupWidgetActions
    -WindowLabel()        -window,name            -GroupWidgetActions
    -WindowEntry()        -window                 -GroupWidgetActions
Window Instances
    -InformationWindow()  -name                          -Window
    -ConfigureWindow()    -window_name,label_name        -Window
    -NameTag()            -window_name,name,config_link  -Window
    -ColorWindow()        -window_name                   -Window
    -Bathroom()           -window_name                   -Window
Objects Used By Window Instances
    -UserErrorMessage()   -window, name           -object
    -DownloadEmulator()   -none                   -object
    -UserInformation()    -none                   -object
Main Program [FUNCTIONS]
    -retreve_user_information()  -none
    -save_uer_information()      -none
    -configure_link()            -none
    -change_name()               -none
    -change_nametag_color()      -none
    -bathroom_run()              -none
================================================================================================================="""
import os
import getpass
import linecache
import webbrowser
from tkinter import *
import tkinter as tk
from shutil import copy
from functools import partial

"""========================================== Tkinter Wrapper ======================================================="""
class Window(object):
    def __init__(self, name):
        self.window=Tk()
        self.window.title(name)

    def resize(self, x, y):
        size_string="{0}x{1}".format(x, y)
        self.window.geometry(size_string)

    def bind_action(self, key, action):
        self.window.bind(key, action)

    def start_mainloop(self):
        self.window.mainloop()

    def destroy_window(self):
        self.window.quit()
        self.window.destroy()


class WindowMenu(object):
    def __init__(self, window):
        self.menu_bar=Menu(window)
        window.config(menu=self.menu_bar)

    def add_cascade_to_menu(self, name, cascade):
        self.menu_bar.add_cascade(label=name, menu=cascade.cascade)


class WindowMenuCascade(object):
    def __init__(self, window):
        self.window=window
        self.menu_bar=Menu(self.window)
        self.cascade=Menu(self.window)

    def add_item_to_cascade(self, name, action):
        self.cascade.add_command(label=name, command=action)

    def add_separator(self):
        self.cascade.add_separator()

    def add_tearoff(self, yes_no):
        if yes_no==True:
            self.cascade=Menu(self.menu_bar, tearoff=1)
        else:
            self.cascade=Menu(self.menu_bar, tearoff=0)
        
        
class GroupWidgetActions(object):
    def __init__(self):
        pass

    def destroy_widget(self, widget):
        widget.destroy()

    def pack_widget(self, widget, position, pad_x, pad_y):
        if position=="LEFT":
            widget.pack(padx=pad_x, pady=pad_y,side=LEFT)
        elif position=="RIGHT":
            widget.pack(padx=pad_x, pady=pad_y,side=RIGHT)
        elif position=="TOP":
            widget.pack(padx=pad_x, pady=pad_y,side=TOP)
        elif position=="BOTTOM":
            widget.pack(padx=pad_x, pady=pad_y,side=BOTTOM)


class WindowFrame(GroupWidgetActions):
    def __init__(self, window):
        self.frame=Frame(window, relief=RIDGE)

    def pack_frame(self, position, pad_x, pad_y):
        super(WindowFrame, self).pack_widget(self.frame, position, pad_x, pad_y)

    def set_frame_fill(self, new_fill):
        self.frame.configure(fill=new_fill)

    def resize_frame(self, x, y):
        self.frame.configure(width=x)
        self.frame.configure(height=y)

    def destroy_frame(self):
        super(WindowFrame, self).destroy_widget(self.frame)

    def get_frame(self):
        return self.frame

        
class WindowButton(GroupWidgetActions):
    def __init__(self, window, name, action):
        self.button_text=StringVar()
        self.button_text.set(name)
        self.button=Button(window,text=name,command=action,font='times 10',cursor='hand2',bd=2, textvariable=self.button_text)

    def get_button(self):
            return self.button

    def set_position(self,row,column,pad_x,pad_y):
        self.button.grid(row=row,column=column, padx=pad_x, pady=pad_y)

    def change_text(self, new_text):
        self.button.text=new_text
        self.button_text.set(new_text)

    def change_action(self, new_action):
        self.button.configure(command=new_action)

    def change_color(self,foreground,background):
        self.button.configure(fg=foreground)
        self.button.configure(bg=background)

    def pack_button(self, position, pad_x, pad_y):
        super(WindowButton, self).pack_widget(self.button, position, pad_x, pad_y)

    def destroy_button(self):
        super(WindowButton, self).destroy_widget(self.button)


class WindowLabel(GroupWidgetActions):
    def __init__(self, window, name):
        self.label=Label(window,text=name,font="Times 10",fg="White",bg="Black")

    def set_colors(self, foreground, background, font):
        self.label.configure(foreground=foreground)
        self.label.configure(background=background)
        self.label.configure(font=font)

    def set_position(self,row,column,pad_x,pad_y):
        self.label.grid(row=row,column=column, padx=pad_x, pady=pad_y)

    def pack_label(self, position, pad_x, pad_y):
        super(WindowLabel, self).pack_widget(self.label, position, pad_x, pad_y)

    def destroy_label(self):
        super(WindowLabel, self).destroy_widget(self.label)

    def configure_text(self, text):
        self.label.configure(text=text)


class WindowEntry(GroupWidgetActions):
    def __init__(self, window):
        self.entry_text=StringVar()
        self.entry=Entry(window,font="Times 10",bd=2, textvariable=self.entry_text)
        self.entry.focus()

    def set_font(self,font,bd):
        self.entry.configure(font=font)
        self.entry.configure(bd=bd)

    def set_position(self,row,column,pad_x,pad_y):
        self.entry.grid(row=row,column=column, padx=pad_x, pady=pad_y)

    def set_entry_text(self, new_text):
        self.entry_text.set(new_text)

    def select_range(self, start, end):
        if end==END:
            end=len(self.entry_text.get())
        if start>=0 and end<=len(self.entry_text.get()):
            self.entry.select_range(start, end)

    def destroy_entry(self):
        super(WindowEntry, self).destroy_widget(self.entry)

    def get_entry(self):
        return self.entry.get()

"""========================================== Window Instances ======================================================"""
class InformationWindow(Window):
    def __init__(self, name):
        super(InformationWindow, self).__init__(name)
        self.__setup_menu()
        self.__add_name_entry()
        self.__add_display_button()
        self.__add_quit_button()
        self.bind_action("<Escape>",exit)
        self.bind_action("<Return>",self.display_name)
        self.resize(240,70)
        self.window.attributes("-toolwindow", 1)
        self.start_mainloop()

    def __setup_menu(self):
        file_cascade=WindowMenuCascade(self.window)
        file_cascade.add_tearoff(False)
        file_cascade.add_item_to_cascade("Config. Link", configure_link)
        file_cascade.add_separator()
        file_cascade.add_item_to_cascade("Quit", self.window.destroy)
        menu=WindowMenu(self.window)
        menu.add_cascade_to_menu("File", file_cascade)

    def __add_name_entry(self):
        name_entry=WindowLabel(self.window, "First Name:")
        name_entry.set_colors(user_info.get_foreground_color(),user_info.get_background_color(),'times 11 bold')
        name_entry.set_position(0,0,10,5)
        self.name=WindowEntry(self.window)
        self.name.set_font('times 10', 1)
        self.name.set_position(0,1,0,0)
        self.name.set_entry_text("name...")
        self.name.select_range(0,END)

    def __add_display_button(self):
        display_button=WindowButton(self.window, "Display", self.display_name)
        display_button.set_position(1,0,0,0)

    def __add_quit_button(self):
        quit_button=WindowButton(self.window, "Quit", self.window.destroy)
        quit_button.set_position(1,1,0,0)

    def display_name(self, *args):
        self.saved_name=self.name.get_entry()
        super(InformationWindow, self).destroy_window()

    def get_saved_info(self):
        return self.saved_name

    
class ConfigureWindow(Window):
    def __init__(self, window_name, label_name):
        super(ConfigureWindow, self).__init__(window_name)
        self.label_name=label_name
        self.__setup_menu()
        self.__add_link_entry()
        self.__add_insert_button()
        self.bind_action("<Escape>",exit)
        self.bind_action("<Return>",self.save_info_and_exit)
        self.window.call('wm', 'attributes', '.', '-topmost', '1')
        self.window.attributes("-toolwindow", 1)
        self.start_mainloop()

    def __setup_menu(self):
        file_cascade=WindowMenuCascade(self.window)
        file_cascade.add_tearoff(False)
        file_cascade.add_item_to_cascade("Quit", self.window.destroy)
        menu=WindowMenu(self.window)
        menu.add_cascade_to_menu("File", file_cascade)
        
    def __add_link_entry(self):
        link_label=WindowLabel(self.window, self.label_name)
        link_label.set_colors(user_info.get_foreground_color(),user_info.get_background_color(),'times 11 bold')
        link_label.set_position(0,0,10,20)
        self.info=WindowEntry(self.window)
        self.info.set_font('times 10',1)
        self.info.set_position(0,1,0,10)
        
    def __add_insert_button(self):
        insert_button=WindowButton(self.window, "Insert", self.save_info_and_exit)
        insert_button.set_position(0,2,5,0)

    def save_info_and_exit(self,*args):
        self.saved_info=self.info.get_entry()
        super(ConfigureWindow, self).destroy_window()

    def get_saved_info(self):
        return self.saved_info


class NameTag(Window):
    def __init__(self, window_name, name, config_link):
        super(NameTag, self).__init__(window_name)
        self.help_status="grey50"
        self.user_name=name
        self.config_link=config_link
        self.__setup_menu()
        self.__add_frames()
        self.__add_name()
        self.__add_buttons()
        self.__add_help_area()
        self.bind_action("<Escape>",exit)
        self.window.resizable(width=FALSE, height=FALSE)  #makes it so you cant resize it
        self.window.call('wm', 'attributes', '.', '-topmost', '1')  #Makes it always the top window
        self.window.attributes("-toolwindow", 1)    #Removes the minimise/maximise buttons
        self.start_mainloop()

    def __setup_menu(self):
        file_cascade=WindowMenuCascade(self.window)
        file_cascade.add_tearoff(False)
        file_cascade.add_item_to_cascade("Config. Link", self.configure_and_update_link)
        file_cascade.add_item_to_cascade("Change Color", self.change_and_update_color)
        file_cascade.add_item_to_cascade("Change Name", self.change_and_update_name)
        file_cascade.add_separator()
        file_cascade.add_item_to_cascade("Quit", self.window.destroy)
        menu=WindowMenu(self.window)
        menu.add_cascade_to_menu("File", file_cascade)

    def __add_frames(self):
        self.name_frame=WindowFrame(self.window)
        self.top_frame=WindowFrame(self.window)
        self.error_frame=WindowFrame(self.window)
        self.help_frame=WindowFrame(self.window)
        self.name_frame.pack_frame("TOP",0,0)
        self.top_frame.pack_frame("TOP",0,0)
        self.error_frame.pack_frame("TOP",0,0)
        self.help_frame.pack_frame("TOP",0,0)
        
    def __add_name(self):
        self.name_label=WindowLabel(self.name_frame.get_frame(), self.user_name)
        self.name_label.set_colors(user_info.get_foreground_color(),user_info.get_background_color(),'times 72 bold')
        self.name_label.pack_label("TOP",5,5)

    def __add_buttons(self):
        self.__add_edmodo_link()
        self.__add_infinite_campus_link()
        self.__add_google_drive_link()
        self.__add_bathroom()
        self.__add_help_button()
        self.__add_configure_link()

    def __add_edmodo_link(self):
        edmodo_link=WindowButton(self.top_frame.get_frame(), "Edmodo", self.open_edmodo)
        edmodo_link.pack_button("LEFT",2,2)

    def __add_infinite_campus_link(self):
        recordXP_link=WindowButton(self.top_frame.get_frame(), "Infinite Campus", self.open_infinite_campus)
        recordXP_link.pack_button("LEFT",0,2)

    def __add_google_drive_link(self):
        server_link=WindowButton(self.top_frame.get_frame(), "GDrive", self.open_google_drive)
        server_link.pack_button("LEFT",2,2)

    def __add_bathroom(self):
        bathroom=WindowButton(self.top_frame.get_frame(), "Bathroom!", bathroom_run)
        bathroom.pack_button("LEFT",0,2)

    def __add_configure_link(self):
        if self.config_link!="":
            self.config_button_name()
            self.config_link_button=WindowButton(self.top_frame.get_frame(), "{0}".format(self.config_link), self.open_config_link)
            self.config_link_button.pack_button("LEFT",5,5)
        else:
            self.config_link_button=WindowButton(self.top_frame.get_frame(), "Config. Link", self.configure_and_update_link)
            self.config_link_button.pack_button("LEFT",5,5)

    def __add_help_button(self):
        self.help_toggle=WindowButton(self.top_frame.get_frame(),"Help Me!",self.toggle_help_display)
        self.help_toggle.pack_button("LEFT",0,2)

    def __add_help_area(self):
        self.help_canvas=Canvas(self.help_frame.get_frame(), width=500,height=50)
        self.help_canvas.config(bg=self.help_status)
        self.help_canvas.pack(padx=0, pady=0,side=LEFT)

    def config_button_name(self):
        if len(self.config_link)>=10:
            self.config_link=self.config_link[0:9]+"..."

    def configure_and_update_link(self):
        configure_link()
        self.config_link=user_info.config_link
        self.config_button_name()
        self.config_link_button.change_text(self.config_link)
        self.config_link_button.change_action(self.open_config_link)

    def change_and_update_color(self):
        change_nametag_color()
        self.name_label.set_colors(user_info.get_foreground_color(),user_info.get_background_color(),'times 72 bold')

    def change_and_update_name(self):
        change_name()
        self.name_label.configure_text(user_info.get_user_name())

    def open_edmodo(self):
        webbrowser.open("www.edmodo.com",new=0,autoraise=True)
    def open_infinite_campus(self):
        webbrowser.open("https://campus.dcsdk12.org/icprod/portal/icprod.jsp",new=0,autoraise=True)
    def open_config_link(self):
        webbrowser.open("{0}".format(user_info.config_link),new=0, autoraise=True)
    def open_google_drive(self):
        webbrowser.open("https://drive.google.com/drive/my-drive",new=0,autoraise=True)
    def toggle_help_display(self):
        colors=["grey50","red","green"]
        names=["Help Me!","Can Help!","Learning!"]
        index=colors.index(self.help_status)
        index=(index+1)%len(colors)
        self.help_status=colors[index]
        self.help_canvas.config(bg=self.help_status)
        self.help_toggle.change_text(names[index])


class ColorWindow(Window):
    def __init__(self, window_name):
        super(ColorWindow, self).__init__(window_name)
        self.foreground=user_info.get_foreground_color()
        self.background=user_info.get_background_color()
        self.colors=["hotpink1","firebrick","darkorange1","yellow2","chartreuse3","dodgerblue2","purple3", "grey95","grey1"]
        self.__add_frames()
        self.__setup_name_frame()
        self.__setup_foreground_frame()
        self.__setup_background_frame()
        self.__setup_bottom_frame()
        self.window.resizable(width=FALSE, height=FALSE)  #makes it so you cant resize it
        self.window.call('wm', 'attributes', '.', '-topmost', '1')  #Makes it always the top window
        self.window.attributes("-toolwindow", 1)    #Removes the minimise/maximise buttons
        self.start_mainloop()
        
    def __add_frames(self):
        self.name_frame=WindowFrame(self.window)
        self.name_frame.pack_frame("LEFT",5,0)
        color_selection_frame=WindowFrame(self.window)
        color_selection_frame.pack_frame("LEFT",0,0)
        self.foreground_frame=WindowFrame(color_selection_frame.get_frame())
        self.background_frame=WindowFrame(color_selection_frame.get_frame())
        self.bottom_frame=WindowFrame(color_selection_frame.get_frame())
        self.foreground_frame.pack_frame("TOP",0,0)
        self.background_frame.pack_frame("TOP",0,0)
        self.bottom_frame.pack_frame("TOP",0,0)        

    def __setup_name_frame(self):
        self.name_label=WindowLabel(self.name_frame.get_frame(), user_info.get_user_name())
        self.name_label.set_colors(self.foreground,self.background,'times 72 bold')
        self.name_label.pack_label("TOP",5,5)

    def __setup_foreground_frame(self):
        foreground_label=WindowLabel(self.foreground_frame.get_frame(), "Text color:")
        foreground_label.set_colors('black','grey94','times 9')
        foreground_label.pack_label("TOP",0,0)
        counter=0
        for color in self.colors:
            button=WindowButton(self.foreground_frame.get_frame(),"   ",partial(self.change_foreground_color,color))
            button.change_color(color,color)
            button.pack_button("LEFT",2.5,0)
            counter+=1

    def __setup_background_frame(self):
        foreground_label=WindowLabel(self.background_frame.get_frame(), "Background color:")
        foreground_label.set_colors('black','grey94','times 9')
        foreground_label.pack_label("TOP",0,0)
        counter=0
        for color in self.colors:
            button=WindowButton(self.background_frame.get_frame(),"   ",partial(self.change_background_color,color))
            button.change_color(color,color)
            button.pack_button("LEFT",2.5,0)
            counter+=1

    def __setup_bottom_frame(self):
        done_button=WindowButton(self.bottom_frame.get_frame(), "Done!", self.save_colors_and_exit)
        done_button.pack_button("TOP",0,5)

    def change_foreground_color(self, color):
        self.foreground=color
        self.name_label.set_colors(self.foreground,self.background,'times 72 bold')

    def change_background_color(self, color):
        self.background=color
        self.name_label.set_colors(self.foreground,self.background,'times 72 bold')

    def save_colors_and_exit(self):
        self.saved_foreground=self.foreground
        self.saved_background=self.background
        super(ColorWindow, self).destroy_window()
        
    def get_foreground(self):
        return self.saved_foreground
    def get_background(self):
        return self.saved_background


class Bathroom(Window):
    def __init__(self, window_name):
        super(Bathroom, self).__init__(window_name)
        self.window.configure(background="dark grey")
        self.time_remaining=270
        self.minute=0
        self.second=0
        self.__setup_menu()
        self.__add_time()
        self.__add_back_button()
        self.window.call('wm', 'attributes', '.', '-topmost', '1')  #Makes it always the top window
        self.resize(self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.overrideredirect(True)
        self.start_countdown()

    def __setup_menu(self):
        file_cascade=WindowMenuCascade(self.window)
        file_cascade.add_tearoff(False)
        file_cascade.add_item_to_cascade("Quit", self.window.destroy)
        menu=WindowMenu(self.window)
        menu.add_cascade_to_menu("File", file_cascade)

    def __add_time(self):
        self.time_label=WindowLabel(self.window, "Time!")
        self.time_label.set_colors('Dodgerblue2','dark grey', 'times 100')
        self.time_label.pack_label("TOP",0,0)

    def __add_back_button(self):
        back_from_bathroom=WindowButton(self.window, "Back from Bathroom!",self.window.destroy)
        back_from_bathroom.pack_button("TOP",0,0)

    def start_countdown(self):
        if self.time_remaining<=0:
            self.time_label.configure_text("Time's up!\nSubtract 10 XP!")
        else:
            self.calculate_minute_and_second()
            self.time_label.configure_text("BRB in {0}:{1}".format(self.minute,self.second))
            self.time_remaining-=1
            self.window.after(1000,self.start_countdown)

    def calculate_minute_and_second(self):
        self.minute=int(self.time_remaining/60)
        self.second=self.time_remaining%60
        if self.second<=9:
            self.second="0{0}".format(self.second)

"""================================= Objects Used By Window Instances ==============================================="""
class UserErrorMessage(object):
    def __init__(self, window, name):
        self.counter=0
        self.window=window
        self.gradient_array=[]
        self.error_message=WindowLabel(self.window, name)
        self.error_message.pack_label("TOP",0,0)
        self.setup_gradient_array()
        self.display_error()

    def setup_gradient_array(self):
        for x in range(0,99):
            if x%2==0:
                self.gradient_array.append("grey{0}".format(x))

    def display_error(self):
        self.error_message.set_colors('white',self.gradient_array[self.counter],'times 10')
        self.counter+=1
        if self.counter<len(self.gradient_array):
            self.window.after(50, self.display_error)
        else:
            self.error_message.destroy_label()


class DownloadEmulator(object):
    def __init__(self):
        self.atari_original_path=r"\\hrhs-files\HRHS\Department\Mr. DeBolt\Video Game Design\Emulators\Stella-Atari Emulator.zip"
        self.nintendo_original_path=r"\\hrhs-files\HRHS\Department\Mr. DeBolt\Video Game Design\Emulators\NES Emulator and 758 Roms (Kingdom-games by KloWn).zip"
        self.sega_original_path=r"\\hrhs-files\HRHS\Department\Mr. DeBolt\Video Game Design\Emulators\Sega Genesis.zip"
        self.copy_path="C:\\Users\\"+getpass.getuser()+"\Downloads"
        
    def atari(self):
        copy(self.atari_original_path, self.copy_path)
        os.startfile(self.copy_path)
    def nintendo(self):
        copy(self.nintendo_original_path, self.copy_path)
        os.startfile(self.copy_path)
    def sega(self):
        copy(self.sega_original_path, self.copy_path)
        os.startfile(self.copy_path)


class File(object):
    def __init__(self, file_location):
        self.file_location=file_location
        self.__open_file()
        

    def __open_file(self):
        try:
            self.file=open(self.file_location,"r")
        except:
            self.file=open(self.file_location,"w")
            self.open_file_mode("r")

    def open_file_mode(self, mode):
        self.file.close()
        if mode.upper()=='W':
            self.file=open(self.file_location, "w")
        elif mode.upper()=='R':
            self.file=open(self.file_location,"r")

    def read_line(self, line):
        print("Line {0}: {1}".format(line, linecache.getline(self.file_location, line)))
        return linecache.getline(self.file_location, line).rstrip()

    def write_line(self,info):
        self.file.write(info+'\n')

    def delete_all(self):
        self.file.seek(0)
        self.file.truncate()

    def close_file(self):
        self.file.close()

        
class UserInformation(object):
    def __init__(self):
        self.name=""
        self.config_link=""
        self.foreground="DodgerBlue2"
        self.background="grey95"
        
    def set_user_name(self, name):
        self.name=name
    def get_user_name(self):
        return self.name

    def set_config_link(self, config_link):
        self.config_link=config_link
    def get_config_link(self):
        return self.config_link

    def set_color(self, foreground, background):
        self.foreground=foreground
        self.background=background
    def get_foreground_color(self):
            return self.foreground
    def get_background_color(self):
            return self.background

    def print_information(self):
        print("User Info: [Name: {0}][Grade: {1}][Link: {2}][Color:: FG:{3} BG:{4}]".format(
            self.name, self.grade, self.config_link, self.foreground, self.background))


"""============================================== Main Program ======================================================"""
def retreve_user_information():
    user_file.open_file_mode("r")
    if user_file.read_line(1)!="":
        user_info.set_user_name(user_file.read_line(1))
        user_info.set_config_link(user_file.read_line(2))
        user_info.set_color(user_file.read_line(3),user_file.read_line(4))
    else:
        information_window=InformationWindow("Nametag")
        user_info.set_user_name(information_window.get_saved_info())

def save_user_information():
    user_file.open_file_mode("w")
    user_file.delete_all()
    user_file.write_line(user_info.get_user_name())
    user_file.write_line(user_info.get_config_link())
    user_file.write_line(user_info.get_foreground_color())
    user_file.write_line(user_info.get_background_color())
    user_file.close_file()

def configure_link():        
    config_window=ConfigureWindow("Configure Custom Link","Enter link:")    
    user_info.set_config_link(config_window.get_saved_info())

def change_name():
    change_name_window=ConfigureWindow("Change Name:", "Re-enter Name:")
    user_info.set_user_name(change_name_window.get_saved_info())

def change_nametag_color():
    color_window=ColorWindow("Chose your color:")
    user_info.set_color(color_window.get_foreground(), color_window.get_background())
    
def bathroom_run():
    bathroom_window=Bathroom("Bathroom")
    

def main():
    retreve_user_information()
    name_tag=NameTag("Presenting: ", user_info.get_user_name(), user_info.config_link)
    save_user_information()
user_file=File("C:\\Users\\"+getpass.getuser()+"\\My Documents\\Name Tag User Info.txt")
download_emulators=DownloadEmulator()
user_info=UserInformation()
main()
