##Title: GameCollectionBuilder
##By: Collin McClendon
##Used with: Python 3.10.2 and sqlite3
##March 2023

##Python imports.
import math
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import *

##Connect to Sqlite with Python.
with sqlite3.connect("gcb.db") as connection: ##Helps create a sqlite table to store the data.
    c = connection.cursor() ##Cursor for SQL commands.

    current_page = 1 ##For representing the current page of a Game list.
    sort1 = True ##For sorting by game title.
    sort2 = True ##For sorting by platform name.
    max_games = 512 ##Maximum number of games you can have on the list.

    ##c.execute("""DROP TABLE IF EXISTS games""")
    c.execute("""CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            video_game text NOT NULL,
            platform text NOT NULL,
            regional_version text NOT NULL,
            play_status text NOT NULL
        )""") ##Creates an SQLite Table with id and four different text values.

    def main_program(): ##The contents of the program.
        ##Different Functions for the App.
        def next_page(): ##Function to flip the next page of Games.
            total_pages = get_page_total() ##Get total number of pages.
            global current_page
            if total_pages == 0 or current_page >= total_pages: ##Do nothing if on the last page.
                return;
            else: ##Turn to the next page.
                current_page += 1 ##Next page.
                page_label["text"] = f"Page: {current_page}/{total_pages}" ##Change the page number display.
                change_page() ##Function to change the page layout.
 
        def prev_page(): ##Function to flip the previous page of Games
            total_pages = get_page_total()
            global current_page
            if total_pages == 0 or current_page == 1: ##Do nothing if on the first page.
                return;
            else: ##Turn to the previous page.
                current_page -= 1 ##Previous page.
                page_label["text"] = f"Page: {current_page}/{total_pages}" ##Change the page number display.
                change_page() ##Function to change the page layout.

        def change_page(): ##Function to change the page layout.
            upper_limit = (current_page)*16 ##Number for the last item on the page.
            lower_limit = (current_page - 1)*16 ##Number for the first item on the page.
            page_display = c.execute(f"SELECT * FROM games LIMIT {lower_limit},{upper_limit}").fetchall();
            ##Select a range of Games in a set of 16 to be displayed
            display_games(page_display) ##Function to display the games on the current page.

        def display_games(sql): ##Function to display the games on the current page.
            for row in games_frame.get_children(): ##The Games onscreen disappear.
                games_frame.delete(row)
            for i in range(16):
                if i < len(sql): ##Inserts the corresponding Games.
                    games_frame.insert(parent = '', index = 'end', iid = sql[i][0], text = sql[i][0],
                                    values = (sql[i][1], sql[i][2], sql[i][3], sql[i][4]))
                else:
                    break; ##Breaks loop if there are less then 16 Games on a page.

        def get_page_total(): ##Function to get the total number of pages of your Game collection.
            c.execute("""SELECT COUNT(*) FROM games""") ##Get the number of Games from the table.
            count = c.fetchone()
            total_pages = math.ceil((count[0])/16) ##Counts the number of pages (16 Games or less each).
            if total_pages <= 0:
                return 1; ##The minimum total number of pages will always be 1.
            else:
                return total_pages; ##Returns the total number of pages based on the number of Games.

        def sort_games(change1): ##Function to sort the list by game title alphabetically (ascending or descending).
            global sort1
            if change1 == True: ##This is for sorting the Games alphabetically by title ascending.
                sort1 = False ##Arrange Games alphabetically by title descending next time.
                default1 = c.execute("""SELECT video_game, platform, regional_version, play_status
                                    FROM games ORDER BY video_game ASC""").fetchall()
                rearrange_data(default1) ##Function to change the table based on an action.
            else: ##This is for sorting the Games alphabetically by title descending.
                sort1 = True ##Arrange Games alphabetically by title ascending next time.
                default2 = c.execute("""SELECT video_game, platform, regional_version, play_status
                                    FROM games ORDER BY video_game DESC""").fetchall()
                rearrange_data(default2) ##Function to change the table based on an action.
            change_page()

        def sort_platform(change2):
            global sort2
            if change2 == True: ##This is for sorting the Games alphabetically by platform ascending.
                sort2 = False ##Arrange Games alphabetically by platform descending next time.
                default1 = c.execute("""SELECT video_game, platform, regional_version, play_status
                                    FROM games ORDER BY platform ASC""").fetchall()
                rearrange_data(default1) ##Function to change the table based on an action.
            else: ##This is for sorting the Games alphabetically by platform descending.
                sort2 = True ##Arrange Games alphabetically by platform ascending next time.
                default2 = c.execute("""SELECT video_game, platform, regional_version, play_status
                                    FROM games ORDER BY platform DESC""").fetchall()
                rearrange_data(default2) ##Function to change the table based on an action.
            change_page()

        def rearrange_data(new_data): ##Function to change the table based on an action.
            c.execute("""DROP TABLE IF EXISTS games""") ##Drop the old table.
            c.execute("""CREATE TABLE IF NOT EXISTS games ( 
                    id INTEGER PRIMARY KEY,
                    video_game text NOT NULL,
                    platform text NOT NULL,
                    regional_version text NOT NULL,
                    play_status text NOT NULL
                )""") ##Create a new table to use.
            c.executemany("""INSERT INTO games(video_game, platform, regional_version, play_status)
                            VALUES (?,?,?,?)""", new_data) ##Insert the data based on the input.
            
        def add_game(): ##Function for adding a Game to the list.
            ge = game_entry.get().strip() ##Get the Game name entry.
            pe = platform_entry.get().strip() ##Get the Platform name entry.
            re = region_entry.get().strip() ##Get the Region selection.
            se = status_entry.get().strip() ##Get the Status selection.
            c.execute("""SELECT COUNT(*) FROM games""") ##Count the number of Games on the table.
            count_max = c.fetchone()
            if ge == "" or len(ge) > 80 or '"' in ge: ##Warning messages if you do not meet the requirements.
                tk.messagebox.showwarning("Notice", "The Video Game Title Entry must not: be blank, " \
                                          "exceed 80 characters, or contain double qoutation marks.")
            elif pe == "" or len(pe) > 20 or '"' in pe:
                tk.messagebox.showwarning("Notice", "The Platform Entry must not: be blank, " \
                                          "exceed 20 characters, or contain double qoutation marks.")
            elif re == "":
                tk.messagebox.showwarning("Notice",
                                          "You need to select one of the Region choices.")
            elif se == "":
                tk.messagebox.showwarning("Notice",
                                          "You need to select one of the Play Status choices.")
            elif count_max[0] >= max_games: ##There is a limit of having 512 Games on the list.
                tk.messagebox.showwarning("Notice",
                                          "You reached the limit of 512 games. Delete an entry to make room.")
            else:
                duplicate = c.execute(f"""SELECT * FROM games WHERE video_game = "{ge}" AND platform = "{pe}"
                            AND regional_version = "{re}" AND play_status = "{se}" """).fetchall()
                if len(duplicate) > 0: ##You cannot have two of the exact Games on the list.
                    tk.messagebox.showwarning("Notice", "This entry is already in the list.")
                else:
                    total_before = get_page_total() ##Get total
                    c.execute(f"""INSERT INTO games(video_game, platform, regional_version, play_status)
                                VALUES ("{ge}","{pe}","{re}","{se}")""")
                    reorder = c.execute("""SELECT video_game, platform, regional_version, play_status
                                    FROM games""").fetchall()
                    rearrange_data(reorder) ##Function to change the table based on an action.
                    total_after = get_page_total()
                    if total_before < total_after and total_before != 0:
                        page_label["text"] = f"Page: {current_page}/{total_after}"
                        ##Increase the total number of pages
                    change_page() ##Alter the table based on the addition of a Game.
            
        def delete_game(): ##Function to delete a Game from the list.
            total_before = get_page_total() ##Get total number of pages from the function.
            selected_game = games_frame.selection()[0]
            games_frame.delete(selected_game) ##Delete Game from the list.
            c.execute(f"DELETE from games WHERE id = {selected_game}")
            reorder = c.execute("""SELECT video_game, platform, regional_version, play_status
                                    FROM games""").fetchall()
            rearrange_data(reorder)
            change_page()
            total_after = get_page_total()
            if total_before > total_after and total_before > 1:
                page_label["text"] = f"Page: {current_page}/{total_after}"
            if current_page > total_after and current_page != 1:
                prev_page()

        def confirm_delete(): ##Function to display a message before deleting a Game.
            if len(games_frame.selection()) == 0: ##Warning message for not selecting a Game.
                tk.messagebox.showwarning("Notice",
                                          "You need to select a game first in order to delete it.")
            else:
                choice = tk.messagebox.askquestion("Confirm",
                                                   "Are you sure you want to delete this entry?",
                                      icon= 'question')
                ##Asks if you a sure about deleting the selected Game.
                if choice == "yes":
                    delete_game() ##Function to delete a Game from the list.

        window = tk.Tk()
        window.title("Gaming Collection Builder") ##Sets the title of the program.
        window.geometry("960x640") ##Sets window size to 960x640 at the start.
        window.minsize(960,640) ##Cannot adjust the window size smaller than 960x640.
        window.resizable(width=True, height=True) ##Can change the window size.

        pages = tk.Frame(window) ##For displaying the current page/total pages.
        prev_button = tk.Button(pages, text="Previous Page") ##Prevous page Button
        prev_button.grid(row = 0, column = 0)
        pop = c.execute("""SELECT COUNT(*) FROM games""").fetchall()
        if math.ceil((pop[0][0])/16) > 0:
            page_of_page = math.ceil((pop[0][0])/16)
        else:
            page_of_page = 1 ##Total number of pages is always at least 1.
        page_label = tk.Label(pages, text = f"Page: {current_page}/{page_of_page}")
        page_label.grid(row = 0, column = 1)
        next_button = tk.Button(pages, text="Next Page") ##Next Page Button
        next_button.grid(row = 0, column = 2)
        pages.pack(pady= 3)
        prev_button["command"] = prev_page ##Button that calls the function to go to previous page.
        next_button["command"] = next_page ##Button that calls the function to go to next page.

        main_frame = tk.Frame(window) ##Main frame for listing the games.
        main_frame.pack(pady = 3)

        list_frame = tk.LabelFrame(main_frame, text = "Game List Information")
        list_frame.pack(pady = 3) ##List that displays the Games.

        games_frame = ttk.Treeview(list_frame, height = 16, selectmode = "browse")
        ##Up to 16 Games for each page and can only select one at a time
        games_frame['columns'] = ("Video Game Title", "Platform", "Region", "Status")
        ##Column names to display.
        games_frame.bind('<Motion>', 'break') ##Cannot adjust the columns width.

        games_frame.column("#0", width = 50, minwidth = 50) ##Columns with Game information.
        games_frame.column("Video Game Title", anchor = W, width = 650)
        games_frame.column("Platform", anchor = W, width = 130)
        games_frame.column("Region", anchor = W, width = 45)
        games_frame.column("Status", anchor = W, width = 80)

        ##Set up the headings for the information.
        games_frame.heading("#0", text = "Number", anchor = W)
        games_frame.heading("Video Game Title", text = "Video Game Title", anchor = W)
        games_frame.heading("Platform", text = "Platform", anchor = W)
        games_frame.heading("Region", text = "Region", anchor = W)
        games_frame.heading("Status", text = "Status", anchor = W)

        game_list = c.execute("""SELECT *
                            FROM games
                            LIMIT 0,16""").fetchall();
        ##Get the first 16 Games from the table.

        for i in range(16): ##Insert the first 16 Games from the table on the list.
            if i < len(game_list):
                games_frame.insert(parent = '', index = 'end', iid = game_list[i][0],
                                   text = game_list[i][0], values = (game_list[i][1],
                                   game_list[i][2], game_list[i][3], game_list[i][4]))
            else:
                break; ##Stop if there are less than 16 Games.
        games_frame.pack(pady = 3)


        selection = tk.Frame(master=window) ##Frame to display some buttons.
        add_button = tk.Button(selection, text="Add Entry", command = add_game)
        add_button.grid(row = 0, column = 0)
        ##Button to add a Game with the function add_game.
        delete_button = tk.Button(selection, text="Delete Entry", command = confirm_delete)
        delete_button.grid(row = 0, column = 1)
        ##Button to delete a Game with the function confirm_delete.
        sort1_button = tk.Button(selection, text="Sort by Game Title",
                                 command = lambda:sort_games(sort1))
        sort1_button.grid(row = 0, column = 2)
        ##Button to sort games by title alphabetically.
        sort2_button = tk.Button(selection, text="Sort by Platform",
                                 command = lambda:sort_platform(sort2))
        sort2_button.grid(row = 0, column = 3)
        ##Button to sort games by platform alphabetically.
        quit_button = tk.Button(selection, text="Exit Out", command = window.destroy)
        quit_button.grid(row = 0, column = 4)
        ##Button to exit out the app.
        selection.pack(pady = 3)


        entry_frame = tk.Frame(window) ##Frame for Game entry information input.
        entry_frame.pack(pady = 3)

        add_frame = tk.LabelFrame(entry_frame, text = "Add Entry Information") 
        add_frame.pack(pady = 3) 

        game_name_label = tk.Label(add_frame, text = "Video Game Title")
        game_name_label.grid(row = 0, column = 0) ##For labeling the Game entry.
        platform_name_label = tk.Label(add_frame, text = "Platform")
        platform_name_label.grid(row = 0, column = 1) ##For labling the Platform entry.
        region_name_label = tk.Label(add_frame, text = "Region")
        region_name_label.grid(row = 0, column = 2) ##For labeling the Region selection.
        status_name_label = tk.Label(add_frame, text = "Status")
        status_name_label.grid(row = 0, column = 3) ##For labeling the Status selection.
        game_entry = tk.Entry(add_frame, width = 71)
        game_entry.grid(row = 1, column = 0)  ##For typing the name of the Game.
        platform_entry = tk.Entry(add_frame, width = 14)
        platform_entry.grid(row = 1, column = 1) ##For typing the name of the Platform.
        region_entry = ttk.Combobox(add_frame, state = "readonly",
                                    values = ["", "NA", "EU", "JP", "Other"], width = 4)
        region_entry.grid(row = 1, column = 2) ##For selecting a Region from the options offered.
        status_entry = ttk.Combobox(add_frame, state = "readonly",
                                    values = ["", "Not Played", "Unfinished",
                                              "Completed", "100% Clear"], width = 8)
        status_entry.grid(row = 1, column = 3) ##For selecting a Status from the options offered.
        

        text_frame = tk.Frame(window) ##Frame for displaying some information.
        text_frame.pack(pady = 3)

        box_frame = tk.LabelFrame(text_frame, text = "Instructions and Tips")
        ##Label for the information box.
        box_frame.pack(pady = 3, side=tk.LEFT)

        dialogue1 = tk.Label(box_frame, ##Displays some useful information for this app.
                           text = "-You can add a Game on this list; first you will need to input the entry information on the " \
                           "'Add Entry Information' section, then press the 'Add Entry' Button.", width = 105)
        dialogue1.pack(pady = 2) 
        dialogue2 = tk.Label(box_frame,
                           text =  "-You can delete a Game from this list; first select a game from the list that can be found " \
                           "in the 'Game List Information', then press the 'Delete Entry' Button.", width = 105)
        dialogue2.pack(pady = 2) 
        dialogue3 = tk.Label(box_frame,
                           text =  "-You can use the sort buttons to rearrange the list of entries by game title or platform " \
                           "alphabetically, alternating between ascending and descending orders." , width = 105)
        dialogue3.pack(pady = 2) 
        dialogue4 = tk.Label(box_frame,
                           text = "-Remember, each Game entry must have no more than 80 characters for the Game title and 20 characters " \
                           "for the platform; use abbreviations if you need to.", width = 105)
        dialogue4.pack(pady = 2)


        sort_platform(sort2) ##Sort the Games with both functions at the start of the app.
        sort_games(sort1)

        window.mainloop() ##Infinite loop that allows the program to stay on the screen.

    main_program() ##The function to start the app program.
