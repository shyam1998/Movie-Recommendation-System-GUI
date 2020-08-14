import tkinter.messagebox
import webbrowser
import pygame
import time
from functools import partial
from tkinter import ttk
import imdb_recommendation_system as ims
from tkHyperlinkManager import *


def play_menu_sound(option):
    """
    :type option: str
    :return: None

    Plays a sound based on the 'option' argument
    """
    if option == 'menu_bar':
        pygame.mixer.music.load('music/button-11.wav')
        pygame.mixer.music.play()
    elif option == 'quit':
        pygame.mixer.music.load('music/quit.wav')
        pygame.mixer.music.play()
        time.sleep(0.3)
        root.destroy()


def open_popup():
    tkinter.messagebox.showinfo('How it Works?', 'Using Cosine Similarity on IMDb dataset!')


def update_values():
    """

    :return: None

    Updates the content in the dropdown menu based on the keyword entered in the text field.

    """
    pygame.mixer.music.load('music/button-3.wav')
    pygame.mixer.music.play()
    filter_str = combo1.get().lower()
    filter_str = ' '.join([word for word in re.split(r'\s+', filter_str) if word != ''])  # handling white space
    # if no input is provided show the entire database
    if filter_str == '':
        combo1['values'] = movie_data
    # else filter based on the input
    else:
        filtered_list_1 = []  # holds values that starts with the input string
        filtered_list_2 = []  # holds values that matches the input pattern in the database
        for value in movie_data:
            if value.lower().startswith(filter_str):
                filtered_list_1.append(value)
            elif filter_str in value.lower():
                filtered_list_2.append(value)
        combo1['values'] = filtered_list_1 + filtered_list_2  # so that values of filtered_list_1 appear first


def open_link(my_url):
    """

    :param my_url: URL
    :type my_url: str
    :return: None

    Opens the provided URL in your default browser.
    """
    pygame.mixer.music.load('music/open_browser.wav')
    pygame.mixer.music.play()
    webbrowser.open_new(url=my_url)


def get_text(event=None):
    """

    :param event: None
    :return: None

    Gets the recommendations and shows it in a text widget.
    """
    pygame.mixer.music.load('music/button-3.wav')
    pygame.mixer.music.play()
    text_widget = Text(frame, font='Courier 13 italic', cursor='arrow', bg='yellow', height=11, width=60)
    hyperlink = HyperlinkManager(text_widget)
    text_widget.tag_configure('tag-center', justify='center')
    text_widget.tag_configure('tag-left', justify='left')
    query = combo1.get()  # get input from combo widget
    query = ' '.join([word for word in re.split(r'\s+', query) if word != ''])  # handling white space
    text = ims.get_recommendations(query)
    if text is None:  # if the movie/tv show not found print some tips
        text = "Item not found!\n"
        text_widget.insert(1.0, text, 'tag-center')
        text_widget.insert(END, '\nYou can try the following:\n\n 1. Enter keywords and choose from dropdown menu.\n '
                                '2. Check for typos.', 'tag-left')
    else:  # if found iterate over the DataFrame to create hyperlinks in the text widget
        text_widget.delete(1.0, END)  # clear previous entries
        for idx, title, imdb_url in text.itertuples():  # iterating over the DataFrame as tuples
            text_widget.insert(END, title, hyperlink.add(partial(open_link, imdb_url)))  # insert hyperlinks in the
            # widget
            if idx != 9:  # if not the last index, insert a new line after the previous entry
                text_widget.insert(END, '\n')
                text_widget.insert(END, '\n')
    text_widget.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
    text_widget.place(x=185, y=310)
    # adding scrollbar to the text widget
    scroll_y = Scrollbar(frame, orient='vertical', command=text_widget.yview)
    scroll_y.place(x=773, y=313, relheight=0.31)
    text_widget.configure(state='disabled', yscrollcommand=scroll_y.set)  # making the text widget un-editable


# initialize master window
root = Tk()  # creates a window in which we work our gui
root.title("MRS v0.1.0")
root.geometry('960x720')  # width x height
root.resizable(width=False, height=False)  # restricts window size

# creating menu widget
menu = Menu(root)
helpMenu = Menu(menu, tearoff=0, postcommand=partial(play_menu_sound, 'menu_bar'), font='Courier 11', bg='yellow',
                activebackground='black', activeforeground='white')
menu.add_cascade(label='Menu', menu=helpMenu)
helpMenu.add_command(label='How it Works?', command=open_popup)
helpMenu.add_separator()
helpMenu.add_command(label='See project in GitHub...', command=lambda: webbrowser.open_new("https://git.io/JJwnU"))
helpMenu.add_separator()
helpMenu.add_command(label='Donate via PayPal...', command=lambda: webbrowser.open_new("https://bit.ly/30oJqAt"))
helpMenu.add_separator()
helpMenu.add_command(label='Exit', command=partial(play_menu_sound, 'quit'))

# setting background image for our app
bg_image = PhotoImage(file=r'images/new_bg_image.png')
bg_label = Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# creating a frame to place the widgets
frame = Frame(root, height=500, width=750, bg='black').place(x=150, y=75)
frame_bg_image = PhotoImage(file=r'images/new_bg_image.png')
frame_label = Label(frame, image=bg_image)
frame_label.pack()

# creating widgets
label1 = Label(frame, font='Courier 13 italic', text='Select a Movie/TV Show/Documentary!', height=2, width=65,
               bg='yellow', highlightthickness=2, highlightbackground="black")
movie_data = ims.get_movie_data()  # get the database of all the movies/tv shows
combo1 = ttk.Combobox(frame, width=55, font=("Courier", 13), postcommand=update_values, values=movie_data)
button1 = Button(frame, text='GO!', font='Arial 13 bold italic', bg='#e50914', width=35, command=get_text)
instructions_text = Text(frame, font='Courier 13 italic', cursor='arrow', bg='yellow', height=11, width=60)

# print instructions in the text widget
instructions_text.tag_configure('tag-center', justify='center')
instructions_text.tag_configure('tag-center-underline', justify='center', underline=1)
instructions_text.tag_configure('tag-left', justify='left')
instructions_text.insert(1.0, 'Welcome to my recommendation system!\n', 'tag-center')
instructions_text.insert(END, "\nInstructions\n", 'tag-center-underline')
instructions_text.insert(END, "\n 1. Enter the keywords of a TV Show/Movie/Documentary. \n 2. Select from the "
                              "dropdown menu. \n 3. Press ENTER or 'GO!' to search. \n 4. Click on the Hyperlink to "
                              "take you to the IMDb website.", 'tag-left')
# placing widgets
instructions_text.config(highlightcolor='black', highlightbackground="black", highlightthickness=2)
instructions_text.place(x=185, y=310)
instructions_text.configure(state='disabled')
label1.place(x=150, y=150)
root.option_add('*TCombobox*Listbox.font', ("Courier", 13))
root.config(menu=menu)
combo1.place(x=200, y=213, height=32)
button1.place(x=300, y=260)
combo1.bind('<Return>', get_text)

# main loop
if __name__ == '__main__':
    pygame.mixer.init()
    root.mainloop()
