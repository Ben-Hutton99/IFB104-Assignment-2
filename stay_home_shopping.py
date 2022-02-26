#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N10534598
#    Student name: Ben Hutton
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Stay at Home Shopping
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these functions
# only.  You can import other functions provided they are standard
# ones that come with the default Python/IDLE implementation and NOT
# functions from modules that need to be downloaded and installed
# separately.  Note that not all of the imported functions below are
# needed to successfully complete this assignment.

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import some standard Tkinter functions. (You WILL need to use
# some of these functions in your solution.)  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to download and save a web document. If the
# attempted download fails, an error message is written to
# the shell window and the special value None is returned.
#
# Parameters:
# * url - The address of the web page you want to download.
# * target_filename - Name of the file to be saved (if any).
# * filename_extension - Extension for the target file, usually
#      "html" for an HTML document or "xhtml" for an XML
#      document.
# * save_file - A file is saved only if this is True. WARNING:
#      The function will silently overwrite the target file
#      if it already exists!
# * char_set - The character set used by the web page, which is
#      usually Unicode UTF-8, although some web pages use other
#      character sets.
# * lying - If True the Python function will try to hide its
#      identity from the web server. This can sometimes be used
#      to prevent the server from blocking access to Python
#      programs. However we do NOT encourage using this option
#      as it is both unreliable and unethical!
# * got_the_message - Set this to True once you've absorbed the
#      message above about Internet ethics.
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html',
             save_file = True,
             char_set = 'UTF-8',
             lying = False,
             got_the_message = False):

    # Import the function for opening online documents and
    # the class for creating requests
    from urllib.request import urlopen, Request

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        if lying:
            # Pretend to be something other than a Python
            # script (NOT RELIABLE OR RECOMMENDED!)
            request = Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            if not got_the_message:
                print("Warning - Request does not reveal client's true identity.")
                print("          This is both unreliable and unethical!")
                print("          Proceed at your own risk!\n")
        else:
            # Behave ethically
            request = url
        web_page = urlopen(request)
    except ValueError:
        print("Download error - Cannot find document at URL '" + url + "'\n")
        return None
    except HTTPError:
        print("Download error - Access denied to document at URL '" + url + "'\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to download " + \
              "the document at URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Read the contents as a character string
    try:
        web_page_contents = web_page.read().decode(char_set)
    except UnicodeDecodeError:
        print("Download error - Unable to decode document from URL '" + \
              url + "' as '" + char_set + "' characters\n")
        return None
    except Exception as message:
        print("Download error - Something went wrong when trying to decode " + \
              "the document from URL '" + url + "'")
        print("Error message was:", message, "\n")
        return None

    # Optionally write the contents to a local text file
    # (overwriting the file if it already exists!)
    if save_file:
        try:
            text_file = open(target_filename + '.' + filename_extension,
                             'w', encoding = char_set)
            text_file.write(web_page_contents)
            text_file.close()
        except Exception as message:
            print("Download error - Unable to write to file '" + \
                  target_filename + "'")
            print("Error message was:", message, "\n")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#--------------------------------------------------------------------#
#
# A function to open a local HTML document in your operating
# system's default web browser.  (Note that Python's "webbrowser"
# module does not guarantee to open local files, even if you use a
# 'file://..." URL). The file to be opened must be in the same folder
# as this module.
#
# Since this code is platform-dependent we do NOT guarantee that it
# will work on all systems.
#
def open_html_file(file_name):
    
    # Import operating system functions
    from os import system
    from os.path import isfile
    
    # Remove any platform-specific path prefixes from the
    # filename
    local_file = file_name[file_name.rfind('/') + 1:] # Unix
    local_file = local_file[local_file.rfind('\\') + 1:] # DOS
    
    # Confirm that the file name has an HTML extension
    if not local_file.endswith('.html'):
        raise Exception("Unable to open file " + local_file + \
                        " in web browser - Only '.html' files allowed")
    
    # Confirm that the file is in the same directory (folder) as
    # this program
    if not isfile(local_file):
        raise Exception("Cannot find file " + local_file + \
                        " in the same folder as this program")
    
    # Collect all the exit codes for each attempt
    exit_codes = []
    
    # Microsoft Windows: Attempt to "start" the web browser
    code = system('start ' + local_file)
    if code != 0:
        exit_codes.append(code)
    else:
        return 0
    
    # Apple macOS: Attempt to "open" the web browser
    code = system("open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Linux: Attempt to "xdg-open" the local file in the
    # web browser
    code = system("xdg-open './" + local_file + "'")
    if code != 0:
        exit_codes.append(code)       
    else:
        return 0
    
    # Give up!
    raise Exception('Unable to open file ' + local_file + \
                    ' in web browser - Exit codes: ' + \
                    str(exit_codes))

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#

# Name of the product images file.  To assist marking, your
# program should export your product images using this file name.



text_file_1 = open("Used Cars for Sale in Australia _ Buy Second-Hand Cars.html")
text_1 = text_file_1.read()
text_file_1.close()

text_file_2 = open("Buy a car _ Autotrader.html")
text_2 = text_file_2.read()
text_file_2.close()

website_1 = 'https://www.countrycars.com.au/widebay/search.php?neworused=ANY&pcode=C&makesel=ANY&modelsel=&location=A&neworused=ANY&keyword=Keyword&rego=Rego&minprice=0&maxprice=0&srch=Search+Cars'
open_1 = urlopen(website_1)
web_page_bytes_1 = open_1.read()
web_1 = web_page_bytes_1.decode('ASCII', 'backslashreplace')

website_2 = 'https://www.toyota.com.au/used-cars/for-sale?IsToyotaCertified=false&isHybrid=false&make=TOYO&model=&price.Maximum=&location='
open_2 = urlopen(website_2)
web_page_bytes_2 = open_2.read()
web_2 = web_page_bytes_2.decode('ASCII', 'backslashreplace')



the_window = Tk()
the_window.title('Shopping') #Sets window title
buttons = Frame(the_window)
choose_website = IntVar()
#img = PhotoImage(file="stay_home_shopping.jpg")

button_font = ('Times', 15) # font for the buttons
textbox_font = ('Times', 20)# font for the textboxes

website_get = Listbox(the_window, font = textbox_font, width = 43)
shopping_list = Listbox(the_window, font = textbox_font, width = 43)


website_get.grid(row = 6, column = 1, padx = 10, pady = 10)
shopping_list.grid(row = 6, column =3, padx = 10, pady = 10)

website_get.insert(END, 'Select a product')

counter_1 = 0# initialise variables
counter_2 = 0
counter_3 = 0
counter_4 = 0
def add_to_cart():#command for adding items to the shopping list
    if choose_website.get() == 0:# if nothing is selected
        website_get.delete(0, END)
        website_get.config(fg="red")
        website_get.insert(END, 'Please Choose an item.')
        
    if choose_website.get() == 1:
        global counter_1
        counter_1 = counter_1 + 1#add one to counter each time button pressed
        if counter_1 == 1:
            car_1 = findall('[2].[091][9438015] [A-Z]*.[A-Z]*.[A-Z]*[a-z]*.[A-Z]* ', text_1)
            cost_1 = findall('[$][0-9][0-9],[0-9][0-9][0-9]', text_1)
            
            num_2 = -1 #initialise counter to begin at 0
            for x in car_1:
                num_1 = num_2 + 1 #counter
                total_1 = str('• ') + x + cost_1[num_1] # goes through and adds each item together individually
                shopping_list.insert(END, total_1)
                
        elif counter_1 >= 1:#if counter reaches greater than you will no longer be able tot add items to cart
            website_get.delete(0, END)
            website_get.config(fg="red")
            website_get.insert(END, 'You may only have one of each item')
            
    if choose_website.get() == 2:#if button 2 is selected
        global counter_2
        counter_2 = counter_2 + 1
        if counter_2 == 1:
            car_2 = findall('<strong data-v-c8462878="" class="mm">(.*?)</strong>', text_2)###Continue here
            year_2 = findall('([2][0][012][0-9]) <strong data', text_2)
            cost_2 = findall('[$][0-9]...[0-9]{2}', text_2)

            num_2 = -1
            for y in car_2:
                num_2 = num_2 + 1
                total_2 = str('• ') + year_2[num_2] + str(' ') + y + cost_2[num_2]
                shopping_list.insert(END, total_2)
                
        elif counter_2 >= 1:
                website_get.delete(0, END)
                website_get.config(fg="red")
                website_get.insert(END, 'You may only have one of each item')
            
    if choose_website.get() == 3:#if button 3 is selected
        global counter_3
        counter_3 = counter_3 + 1
        if counter_3 == 1:
            car_3 = findall('Used ([12][0][012][0-9].[A-Z]*.[A-Z]*.[A-Z]*)', web_1)
            cost_3 = findall(' ([$][0-9].*,[0-9]*)', web_1)
            
            num_3 = -1
            for z in car_3:
                num_3 = num_3 + 1
                total_3 = str('• ') + z + str(' ') + cost_3[num_3]
                shopping_list.insert(END, total_3)
                
        elif counter_3 >= 1:
                website_get.delete(0, END)
                website_get.config(fg="red")
                website_get.insert(END, 'You may only have one of each item')
            
    if choose_website.get() == 4:#if button 4 is selected
        global counter_4
        counter_4 = counter_4 + 1
        if counter_4 == 1:
            car_4 = findall('  ([12][0-9][0-9][0-9].[A-Za-z]*.[a-z]*.[a-z]*.[a-z0-9]*.[a-z0-9]*.[a-z0-9]*.[a-z0-9]*.[a-z0-9]*)  ', web_2)
            cost_4 = findall('>([$][0-9]*.[0-9]*)</h3>', web_2)

            num_4 = -1
            list_4 = 0
            for a in car_4:
                list_4 = list_4 + 1
                num_4 = num_4 + 1
                total_4 = str('• ') + a + str(' ') + cost_4[num_4]
                shopping_list.insert(END, total_4)
                
        elif counter_4 >= 1:
                website_get.delete(0, END)
                website_get.config(fg="red")
                website_get.insert(END, 'You may only have one of each item')

cart_button = Button(the_window, text = 'Add to cart', command = add_to_cart)# add to cart button
cart_button.grid(row = 4, column = 2)#puts the add to cart button on the window in a grid formation


def website_chosen():
    if choose_website.get() == 1:#button 1
        website_get.config(fg="black")# makes sure the text is black
        website_get.delete(0, "end")# deletes whatever was previously displayed
        car_1 = findall('[2].[091][9438015] [A-Z]*.[A-Z]*.[A-Z]*[a-z]*.[A-Z]* ', text_1)# Finds all the cars on this website
        cost_1 = findall('[$][0-9]...[0-9]{2}', text_1)# finds the cost of each car
        
        num_1 = -1 #initialise counter to begin at 0
        list_1 = 0
        for x in car_1:
            list_1 = list_1 + 1
            num_1 = num_1 + 1 #counter
            total_1 = str(list_1) + str('. ') + x + cost_1[num_1] # goes through each list and adds each item together individually into another list
            website_get.insert(END, total_1)# inserts into the preview window
            
    if choose_website.get() == 2:#button 2
        website_get.config(fg="black")
        website_get.delete(0, "end")
        car_2 = findall('<strong data-v-c8462878="" class="mm">(.*?)</strong>', text_2)###Continue here
        year_2 = findall('([2][0][012][0-9]) <strong data', text_2)
        cost_2 = findall('[$][0-9]...[0-9]{2}', text_2)

        num_2 = -1
        list_2 = 0
        for y in car_2:
            list_2 = list_2 + 1
            num_2 = num_2 + 1
            total_2 = str(list_2) + str('. ') + year_2[num_2] + str(' ') + y + cost_2[num_2]
            website_get.insert(END, total_2)

    if choose_website.get() == 3:# button 3
        website_get.config(fg="black")
        website_get.delete(0, "end")
        car_3 = findall('Used ([12][0][012][0-9].[A-Z]*.[A-Z]*.[A-Z]*)', web_1)
        cost_3 = findall(' ([$][0-9].*,[0-9]*)', web_1)
        
        num_3 = -1
        list_3 = 0
        for z in car_3:
            list_3 = list_3 + 1
            num_3 = num_3 + 1
            total_3 = str(list_3) + str('. ') + z + str(' ') + cost_3[num_3]
            website_get.insert(END, total_3)
    if choose_website.get() == 4:#button 4
        website_get.config(fg="black")
        website_get.delete(0, "end")
        car_4 = findall('  ([12][0-9][0-9][0-9].[A-Za-z]*.[a-z]*.[a-z]*.[a-z0-9]*.[a-z0-9]*.[a-z0-9]*.[a-z0-9]*.[a-z0-9]*)  ', web_2)
        cost_4 = findall('>([$][0-9]*.[0-9]*)</h3>', web_2)
        
        num_4 = -1
        list_4 = 0
        for a in car_4:
            list_4 = list_4 + 1
            num_4 = num_4 + 1
            total_4 = str(list_4) + str('. ') + a + str(' ') + cost_4[num_4]
            website_get.insert(END, total_4)



old_website_1 = Radiobutton(the_window, text = 'Drive',
                            value = 1, font = button_font,
                            variable = choose_website, command = website_chosen)
old_website_2 = Radiobutton(the_window, text = 'Auto trader',
                            value = 2, font = button_font,
                            variable = choose_website, command = website_chosen)
live_website_1 = Radiobutton(the_window, text = 'Countrycars.com',
                            value = 3, font = button_font,
                             variable = choose_website, command = website_chosen)
live_website_2 = Radiobutton(the_window, text = 'Toyota.com',
                            value = 4, font = button_font,
                             variable = choose_website, command = website_chosen)

old_stock = Label(the_window, font = textbox_font, text = 'Old Stock')
old_stock.grid(row = 1, column = 2, sticky = W)

new_stock = Label(the_window, font = textbox_font, text = 'new Stock')
new_stock.grid(row = 1, column = 3, sticky = W)

old_website_1.grid(row = 2, column = 2, sticky = W)
old_website_2.grid(row = 3, column = 2, sticky = W)
live_website_1.grid(row = 2, column = 3, sticky = W)
live_website_2.grid(row = 3, column = 3, sticky = W)
