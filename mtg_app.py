#Tashi Sherpa
#Comp Sci IA
#Feb 25 2021

from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from mtg_cards_settings import *
import requests
from mtgtools.MtgDB import MtgDB
from pathlib import Path

#GUI Class
#Used as the "main class"
#calls other classes
class GUI(Tk):
    #constructor method
    #pre: GUI is called
    #post: everything necessary for the app is set up
    def __init__(self):
        Tk.__init__(self)
        self.title_text = "Your MTG Collection"
        self.geometry("1200x800")
        self.title(self.title_text)
        self.cards = []
        self.filtered_cards = []
        self.searching_options = {
            "name": {},
            "text": {},
            "color_identity": {},
            "cmc": {},
            "mana_cost": {},
        }
        self.mtg_db = MtgDB("my_db.fs")
        # self.get_mtg_cards()
        self.cards_db = self.mtg_db.root.mtgio_cards
        self.draw_gui()
        self.shown_buttons = []
        self.page = 0
        self.file_path = Path("~/Documents/MTGCollection.txt").expanduser()
        self.read_from_file(self.file_path)
        self.draw_cards()
        self.protocol("WM_DELETE_WINDOW", self.close)

    #closing method
    #pre: the window is closed
    #post: it updates the file with new cards and amounts
    def close(self):
        print("Writing file...")
        try:
            with open(self.file_path, "w") as f:
                for card in self.cards:
                    f.write(f"{card.amount} {card.name}\n")
                f.close()
        except Exception as e:
            print("The Text file isn't in the right place.")
        finally:
            self.destroy()

    #reading from file method
    #pre: none
    #post: when the app is opened, this reads from the text file, telling the app which cards are in the database
    def read_from_file(self, filename):
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if "\n" in line:
                        line = line[:-1].split()
                    else:
                        line = line.split()
                    amount = line[0]
                    name = " ".join(line[1:])
                    self.cards.append(Cards(int(amount), name, self))
                    self.searching_options["name"][name] = [self.cards[-1]]
        except Exception as e:
            print(f"{e}\nThis means the file isn't in your Documents folder")

    #makes buttons for all the cards
    #pre: the card objects are made
    #post: all the buttons for the cards are made and put into place
    def draw_cards(self):
        if len(self.search_entry.get().strip()) == 0:
            self.filtered_cards = self.cards.copy()
        if len(self.shown_buttons):
            for i in range(len(self.shown_buttons)):
                button = self.shown_buttons.pop(0)
                button.pack_forget()

        for card in self.filtered_cards[self.page * 16: self.page * 16 + 16]:
            self.shown_buttons.append(card.button)
            self.shown_buttons[-1].pack()

    #moves to the next page of cards
    #pre: the card buttons are made
    #post: it goes to the next set of cards
    def next_page(self):
        if self.page < len(self.filtered_cards) // 16:
            self.page += 1
            self.draw_cards()

    #moves to the previous page of cards
    #pre: the card buttons are made
    #post: it goes to the previous set of cards
    def prev_page(self):
        if self.page > 0:
            self.page -= 1
            self.draw_cards()

    #updates the mtgio database
    #pre: none
    #post: the database is up to date
    def get_mtg_cards(self):
        self.mtg_db.mtgio_update()

    #searches through the cards
    #pre: a searching option is set (there is a default one in case the user doesn't select one)
    #post: the cards shown are the ones filtered with the user's inputed parameters
    def search_cards(self):
        option = self.option.get()
        self.page = 0
        keys = self.searching_options[option].keys()
        result_search = []
        for data in keys:
            if self.search_entry.get().lower() in data.lower():
                result_search.extend(self.searching_options[option][data])
        self.filtered_cards = result_search.copy()
        if option == "name":
            if len(self.filtered_cards) == 0:
                ask = messagebox.askyesno("Add card", f"No cards was found.\nDo you want to search for {self.search_entry.get()}?")
                if ask:
                    card = Cards(1, self.search_entry.get(), self)
                    ask_new = messagebox.askyesno("Confirm to add", f"{card.name} was found.\nDo you want to add this card to your collection?")
                    if ask_new:
                        self.cards.append(card)

        self.draw_cards()

    #opens a webcam window
    #pre: none
    #post: the webcam window is open with full functionality
    def get_card(self):
        from read_from_image import GetImage, ReadImage
        image = GetImage()
        image.run_capture()
        cap_text = ""
        if len(image.images) > 0:
            for item in image.images:
                text_from_image = ReadImage(item)
                text = text_from_image.get_text().strip()
                if len(text) > 0:
                    cap_text = text
        if len(cap_text) > 0:
            message = messagebox.askyesnocancel("Get Image", f"Do you want to add {cap_text} to your collection?")
            if message:
                self.cards.append(1, cap_text, self)
                self.searching_options["name"][self.cards.name] = [self.cards[-1]]

    #makes all the GUI components, save for the card-specific ones
    #pre: none
    #post: the GUI is setup
    def draw_gui(self):
        self.title_frame = Frame(self)
        self.title_label = Label(self.title_frame, text=self.title_text)

        self.content_frame = Frame(self, width=CONTENT_FRAME_SIZE[0], height=CONTENT_FRAME_SIZE[1])
        self.left_button_frame = Frame(self.content_frame)
        self.cards_frame = Frame(self.content_frame)
        self.search_frame = Frame(self.cards_frame)
        self.right_button_fram = Frame(self.content_frame)

        self.prev_button = Button(self.left_button_frame, text="prev", command=self.prev_page, width=BUTTONS_SIZE[0], height=BUTTONS_SIZE[1], font=MID_FONT)
        self.next_button = Button(self.right_button_fram, text="next", command=self.next_page, width=BUTTONS_SIZE[0], height=BUTTONS_SIZE[1], font=MID_FONT)
        self.search_entry = Entry(self.search_frame)

        self.options = ["name", "text", "cmc", "color_identity", "mana_cost"]
        self.option = StringVar()
        self.option.set(self.options[0])
        self.search_option_menu = OptionMenu(self.search_frame, self.option, *self.options)

        self.search_button = Button(self.search_frame, text="Search", command=self.search_cards)
        self.capture_image = Button(self.search_frame, text="Get Card", command=self.get_card)

        self.title_frame.pack()
        self.title_label.pack()

        self.content_frame.pack()
        self.left_button_frame.pack(side=LEFT)
        self.cards_frame.pack(side=LEFT)
        self.search_frame.pack()
        self.right_button_fram.pack(side=LEFT)

        self.prev_button.pack()
        self.search_entry.pack(side=LEFT)
        self.search_option_menu.pack(side=LEFT)
        self.search_button.pack(side=LEFT)
        self.capture_image.pack(side=LEFT)
        self.next_button.pack()

#Cards class
#subclass of GUI
#has an instance for each card in the file
class Cards:
    #constructor method
    #pre: cards is called
    #post: a card is setup, including a name, attributes, a button, and a card-specific menu
    def __init__(self, amount, name, master: GUI):
        self.master = master
        self.amount = amount
        self.name = name
        self.button = Button(self.master.cards_frame, text=self.name, command=self.clicked, width=BUTTONS_CARDS_SIZE[0], font=MID_FONT)
        self.mana_cost = ""
        self.cmc = ""
        self.color_identity = ""
        self.text = ""
        self.card_data = None
        self.get_card_data()
        self.card_frame = Frame(self.master)
        self.buttons_frame = Frame(self.card_frame)
        self.content_frame = Frame(self.card_frame)
        self.image_frame = Frame(self.content_frame)
        self.data_frame = Frame(self.content_frame)
        self.image_frame.pack(side=LEFT)
        self.data_frame.pack(side=LEFT)
        self.buttons_frame.pack()
        self.content_frame.pack()
        self.back_button = Button(self.buttons_frame, text="Back", command=self.back_button_command)
        self.increase_amount = Button(self.buttons_frame, text="Add copy", command=self.increase_cards)
        self.decrease_amount = Button(self.buttons_frame, text="Remove copy", command=self.decrease_cards)

        self.normalize_text()
        self.name_label = Label(self.data_frame, text=self.name)
        self.amount_label = Label(self.data_frame, text=f"Amount: {self.amount}")
        self.mana_cost_label = Label(self.data_frame, text=f"Mana cost: {self.mana_cost}")
        self.text_label = Label(self.data_frame, text=self.text)
        self.color_identity = Label(self.data_frame, text=f"Colors: {self.color_identity}")

        self.back_button.pack(side=LEFT)
        self.increase_amount.pack(side=LEFT)
        self.decrease_amount.pack(side=LEFT)

        self.name_label.pack()
        self.amount_label.pack()
        self.mana_cost_label.pack()
        self.color_identity.pack()
        self.text_label.pack()

    #returns a string representing the card
    #pre: card object is created
    #post: returns the name of the card
    def __str__(self):
        return self.name

    #a button command for the card-specific menu
    #pre: the card is setup and it's menu opened
    #post: increases the number of copies of that card
    def increase_cards(self):
        self.amount += 1
        self.amount_label.config(text=f"Amount: {self.amount}")

    #a button command for the card-specific menu
    #pre: the card is setup and it's menu opened
    #post: decreases the number of copies of that card. If it's 0, then it deletes this card object
    def decrease_cards(self):
        if self.amount == 1:
            data = messagebox.askyesno(title="Warning", message="This card will be deleted from your collection.\nAre you sure want to continue?")
            if data:
                self.amount -= 1
                self.master.cards.remove(self)
                self.back_button_command()
        else:
            self.amount -= 1
            self.amount_label.config(text=f"Amount: {self.amount}")

    #setting up text for the card-specific menu
    #pre: the card is setup and it's menu opened
    #post: the text is put in such a way, so that it doesn't go beyond the frame
    def normalize_text(self):
        self.text = self.text.replace("\n", " ").split()
        for i in range(6, len(self.text), 7):
            self.text[i] += '\n'
        self.text = " ".join(self.text)

    #gets card data
    #pre: none
    #post: collects the cards data from the mtg database
    def get_card_data(self):
        try:
            self.card_data = self.master.cards_db.where(name=self.name)[-1]
            print(self.card_data.name)
            self.name = self.card_data.name
            self.button.config(text=self.name)
            self.mana_cost = self.card_data.mana_cost
            self.cmc = self.card_data.cmc
            self.text = self.card_data.text
            self.color_identity = self.card_data.colors

        except Exception as e:
            print(e)

        self.add_to_search_option("text", self.text)
        self.add_to_search_option("cmc", self.cmc)
        self.add_to_search_option("color_identity", self.color_identity)
        self.add_to_search_option("mana_cost", self.mana_cost)

    def add_to_search_option(self, search_option, val):
        if type(val) is not list:
            val = [val]
        for i in val:
            if i not in self.master.searching_options[search_option]:
                self.master.searching_options[search_option][str(i)] = [self]
            else:
                self.master.searching_options[search_option][str(i)].append(self)

    #a button command for each card
    #pre: the card is setup
    #post: opens up the card-specific menu for this object
    def clicked(self):
        self.master.content_frame.pack_forget()
        try:
            image = Image.open(requests.get(self.card_data.image_url, stream=True).raw)
        except:
            image = Image.open(requests.get("https://i.imgur.com/8VeJwKZ_d.webp?maxwidth=760&fidelity=grand", stream = True).raw)
        self.tk_image = ImageTk.PhotoImage(image)
        self.image_label = Label(self.image_frame, image=self.tk_image)
        self.image_label.pack()
        self.card_frame.pack()

    #a button command for the card-specific menu
    #pre: the card is setup and it's menu opened
    #post: goes back to the main menu
    def back_button_command(self):
        self.card_frame.pack_forget()
        self.image_label.pack_forget()
        self.master.content_frame.pack()
        self.master.draw_cards()


app = GUI()
app.mainloop()