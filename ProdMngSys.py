from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import tkinter
import random
import pymysql
import csv
from datetime import datetime
import numpy as np

#Window Code
window = tkinter.Tk()

#title of the tkinter or the window created
window.title('Our Store Product Manager')
# CONFIGURATIONS AREA
TK_WINDOW_WIDTH = 1080
TK_WINDOW_HEIGHT= 720

window.geometry(f'{TK_WINDOW_WIDTH}x{TK_WINDOW_HEIGHT}+400+150')
 #the width x height of the window created this all no. is by px(pixel)
 # the second added number is the transition of window from left to rght(x coordinates)
 #the third added number is the transiton of window from bottom to top(y coordinaties) to center
my_root = ttk.Treeview(window, show='headings', height=20)
style = ttk.Style()

#TODO 
placeholderArray= ['','','','','']
numeric = '1234567890'
alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def connection():
   con = pymysql.connect(
      host ='localhost',
      user = 'root',
      passwd ='',
      db = 'storeproductmanager'
   )
   return con
con = connection()
cursor = con.cursor()
#This will run the initializer the Tk object and it will run the main loop

for i in range (0,5):
  placeholderArray[i]=tkinter.StringVar()

def read():
   cursor.connection.ping()
   sql = f"SELECT `sell id`, `name`, `price`, `quantity`, `item type`, `date` FROM procks ORDER BY `id` DESC"
   cursor.execute(sql)
   results = cursor.fetchall()
   con.commit()
   con.close()
   return results

#after the subroor view/ the bank data of products
def refreshTable():
    for data in my_root.get_children():
       my_root.delete(data)
    for array in read():
       my_root.insert(parent='', index='end', iid=array, text="", values=(array),tag= "orow")
    my_root.tag_configure('orow', background="#EEEEEE")
    my_root.pack()
#Button that generates a unique Item ID

def setph(word, num):
    for ph in range(0,3):
       if ph == num:
          placeholderArray[ph].set(word)


def generateRand():
    sellId = ''
    for i in range(0,3):    
       randnum = random.randrange(0,(len(numeric)-1))
       sellId = sellId + str(numeric[randnum])
    randnum = random.randrange(0,(len(alpha)-1))
    sellId = sellId + '-' + str(alpha[randnum])

    print("generated: "+ sellId)
    setph(sellId, 0)

#save data into the database by MySQL (inc label 2-4) the save btn that is connected to what is input and save in the sell id grid(window)

def save():
   sellId = str(sellIdProduct.get())
   nameId = str(nameIdProduct.get())
   priceId = str(priceIdProduct.get())
   quantId = str(quantIdProduct.get())
   ItemId = str(ItemIdCombo.get())
   valid = True
   if not(sellId and sellId.strip()) or not(nameId and nameId.strip()) or not(priceId and priceId.strip()) or not(quantId and quantId.strip()) or not(ItemId and ItemId.strip()):
      # to show the warning error on each Id so, the strip is used at the each start to end of the Id strip to remove white spaces and symbols(if repeatedly show to the orig. string)
      #show a warning window
      messagebox.showwarning("", "Please fill up the necessary entries")
      return
   # this and if and if only will show if a entries are not fullfill (any range of entries composing of alphanumerickeys)
   if len(sellId) < 5:
      messagebox.showwarning("", "Invalid Sell Id")
      return
   if(not(sellId[3]== '-')):
      valid = False
   for i in range(0,3):
      if(not(sellId[i] in numeric)):
         valid = False
         break
   if(not(sellId[4]in alpha)):
      valid = False
   if not(valid):
      messagebox.showwarning("", "Invalid Sell Id")
      return
   
   try:
      cursor.connection.ping()
       # if in the def read( the description are being read by ID, here the def is to save each input of the ID to check if its already in used in realtime)
      sql = f"SELECT* FROM procks WHERE `sell id` = '{sellId}' "
      cursor.execute(sql)
      #check each row(s) input item_num  in the database of that localdata of SQL, this fetchall func is always used when executing the data from the SqL datab.
      checkItemNum = cursor.fetchall()
      if len(checkItemNum) > 0:
         messagebox.showwarning("", "Sell Id already exist")
         return
      else: 
         cursor.connection.ping()
         sql =f"INSERT INTO procks( `sell id`, `name`, `price`, `quantity`, `item type`) VALUES ('{sellId}','{nameId}','{priceId}','{quantId}','{ItemId}')"
         cursor.execute(sql)
      con.commit()
      con.close()
      for num in range(0,5):
            setph('',(num))
   except Exception as e:
       messagebox.showwarning("", "Saving Error:" + str(e))
       return
   refreshTable()

   
#update data into the database by MySQL (inc label 2-4) the update btn that is connected to what is input and save in the sell id grid(window)

def update():
    selectedSellId = ''
    try:
        selectedSell = my_root.selection()[0]
        selectedSellId = str(my_root.item(selectedSell)['values'][0])  
    except:
        messagebox.showwarning("", "Please select a data row")
    print(selectedSellId)
    sellId = str(sellIdProduct.get())
    nameId = str(nameIdProduct.get())
    priceId = str(priceIdProduct.get())
    quantId = str(quantIdProduct.get())
    ItemId = str(ItemIdCombo.get())

    if not(sellId and sellId.strip()) or not(nameId and nameId.strip()) or not(priceId and priceId.strip()) or not(quantId and quantId.strip()) or not(ItemId and ItemId.strip()):
      # to show the warning error on each Id so, the strip is used at the each start to end of the Id strip to remove white spaces and symbols(if repeatedly show to the orig. string)
      #show a warning window
      messagebox.showwarning("", "Please fill up the necessary entries")
      return
    if (selectedSellId!= sellId):
      messagebox.showwarning("", "Cannot change the input Sell Id")
      return
    try:
      cursor.connection.ping()
       # if in the def read( the description are being read by ID, here the def is to save each input of the ID to check if its already in used in realtime)
      sql = f"UPDATE procks SET `name`= '{nameId}', `price`= '{priceId}', `quantity` = '{quantId}', `item type` = '{ItemId}' WHERE `sell id` = '{sellId}' "
      cursor.execute(sql)
      #check each row(s) input item_num  in the database of that localdata of SQL, this fetchall func is always used when executing the data from the SqL datab.
      con.commit()
      con.close()
      for num in range(0,5):
            setph('',(num))
    except Exception as err:
        messagebox.showwarning("","Error occured ref: "+str(err))
        return
    refreshTable()

#Delete data into the database
def delete():
   try:
      if(my_root.selection()[0]):
         decision = messagebox.askquestion("", "Are you Sure to Delete the selected Data" )
         if(decision !='yes'):
            return
         else:
            selectedSell = my_root.selection()[0]
            sellId = str(my_root.item(selectedSell)['values'][0])
            try:
                cursor.connection.ping()
       # if in the def read( the description are being read by ID, here the def is to save each input of the ID to check if its already in used in realtime)
                sql = f"DELETE FROM procks WHERE `sell id` = '{sellId}' "
                cursor.execute(sql)
                #check each row(s) input item_num  in the database of that localdata of SQL, this fetchall func is always used when executing the data from the SqL datab.
                con.commit()
                con.close()
                messagebox.showinfo("", "Data has been Deleted")
            except:
               messagebox.showinfo("", "Error occured, try again")
            refreshTable()
   except:
       messagebox.showwarning("", "Please select a data row") 


def select():
   try:
      selectedSell = my_root.selection()[0]
      sellId = str(my_root.item(selectedSell)['values'][0])
      nameId = str(my_root.item(selectedSell)['values'][1]) 
      priceId = str(my_root.item(selectedSell)['values'][2]) 
      quantId = str(my_root.item(selectedSell)['values'][3]) 
      ItemId = str(my_root.item(selectedSell)['values'][4]) 
      setph(sellId,0)
      setph(nameId,1)
      setph(priceId,2)
      setph(quantId,3)
      setph(ItemId,4)
   except:
      messagebox.showwarning("", "Please select a data row")

def find():
    sellId = str(sellIdProduct.get())
    nameId = str(nameIdProduct.get())
    priceId = str(priceIdProduct.get())
    quantId = str(quantIdProduct.get())
    ItemId = str(ItemIdCombo.get())
    cursor.connection.ping()
    if (sellId and sellId.strip()):
       sql = f"SELECT `sell id`, `name`, `price`, `quantity`, `item type`, `date` FROM procks WHERE `sell id` LIKE '%{sellId}%' "
    elif (nameId and nameId.strip()):
       sql = f"SELECT `sell id`, `name`, `price`, `quantity`, `item type`, `date` FROM procks WHERE `name` LIKE '%{nameId}%'  "
    elif (priceId and priceId.strip()):
       sql = f"SELECT `sell id`, `name`, `price`, `quantity`, `item type`, `date` FROM procks WHERE `price` LIKE '%{priceId}%'  "
    elif (quantId and quantId.strip()):
       sql = f"SELECT `sell id`, `name`, `price`, `quantity`, `item type`, `date` FROM procks WHERE `quantity` LIKE '%{quantId}%'  "
    elif (ItemId and ItemId.strip()):
       sql = f"SELECT `sell id`, `name`, `price`, `quantity`, `item type`, `date` FROM procks WHERE `item type` LIKE '%{ItemId}%'  "
    else:
       messagebox.showwarning("", "Please fill unnecesary entries")
       return
    cursor.execute(sql)
    try: 
       result = cursor.fetchall();
       for num in range(0,5):
          setph(result[0][num],(num))
       con.commit()
       con.close()
    except:
       messagebox.showwarning("", "Sorry, did not find any related data")

def clear():
   for num in range(0,5):
       setph('',(num))


def exportExcel():
    cursor.connection.ping()
    sql = f"SELECT `sell id`, `name`, `price`, `quantity`, `item type`, `date` FROM procks ORDER BY `id` DESC"
    cursor.execute(sql)
    dataraw=cursor.fetchall()
    date = str(datetime.now())
    #the module datetime is used here simply, the date time is a manipulatingparameters for year, month, day.
    date = date.replace(' ', '_')
    date = date.replace(':', '-')
    dateFinal = date[0:20]
    with open("stocks_"+dateFinal+".csv",'a',newline='') as f:
        # finally after many code csv import had been light up becoz of this code  as CSV subtly
        # a simply list of para.m to specify to that of created file to a format of that CSV characteristics
        w = csv.writer(f, dialect='excel')
        for record in dataraw:
            w.writerow(record)
    print("saved: stocks_"+dateFinal+".xlsx")
    con.commit()
    con.close()
    messagebox.showinfo("","Excel file successfully been downloaded")


#frame overll window code
frame = tkinter.Frame(window, bg ="#12337A"  )
frame.pack()

ButtonColor = "#102620"

# To have and to have bar frames at the center top
#to the overall sub-window in the horizontal lane
manageFrame = tkinter.LabelFrame(frame, text = "TOOLS", borderwidth=8)
manageFrame.grid (row = 0, column=0, sticky="n", padx=[615,0], pady=0, ipadx=[10])

#Button_Changes_configuration 
saveButton = Button(manageFrame, text= "SAVE", width=10, borderwidth=3, background=ButtonColor, fg='green', command= save)
updateButton = Button(manageFrame, text= "UPDATE", width=10, borderwidth=3, background=ButtonColor, fg='green', command= update)
deleteButton = Button(manageFrame, text= "DELETE", width=10, borderwidth=3, background=ButtonColor, fg='green', command= delete)
selectButton = Button(manageFrame, text= "SELECT", width=10, borderwidth=3, background=ButtonColor, fg='green', command=select)
findButton = Button(manageFrame, text= "FIND", width=10, borderwidth=3, background=ButtonColor, fg='green', command= find)
clearButton = Button(manageFrame, text= "CLEAR", width=10, borderwidth=3, background=ButtonColor, fg='green', command= clear)
exportButton = Button(manageFrame, text= "EXPORT EXCEL", width=10, borderwidth=3, background=ButtonColor, fg='green',command=exportExcel)

#TODO - to have and be frames per part of the window of the selected area grid
saveButton.grid(row=0, column=0, padx=5, pady=5)
updateButton.grid(row=1, column=0, padx=5, pady=5)
deleteButton.grid(row=2, column=0, padx=5, pady=5)
selectButton.grid(row=3, column=0, padx=5, pady=5)
findButton.grid(row=4, column=0, padx=5, pady=5)
clearButton.grid(row=5, column=0, padx=5, pady=5)
exportButton.grid(row=6, column=0, padx=5, pady=5)

# for the overall CREATE SUB-WINDOW in the ylane
productFrame = tkinter.LabelFrame(frame, text = "CREATE", borderwidth=7)
productFrame.grid (row = 0, column=0, sticky="n", padx=[0,180], pady=[0,100], ipadx=[40])

#Button_Changes_configuration 
sellIdLabel = Label(productFrame,text="SELL ID",anchor="n", width=12 )
nameIdLabel = Label(productFrame,text="NAME ID",anchor="n", width=12)
priceIdLabel = Label(productFrame,text="PRICE ID",anchor="n", width= 12)
quantIdLabel = Label(productFrame,text="QUANT ID",anchor="n", width= 12)
ItemIdLabel = Label(productFrame,text="ITEM ID",anchor="n", width= 12)

#TODO - to have and be frames per part of the window of the selected area grid

sellIdLabel.grid(row=0, column=0, padx=12)
nameIdLabel.grid(row=1, column=0, padx=12)
priceIdLabel.grid(row=2, column=0, padx=12)
quantIdLabel.grid(row=3, column=0, padx=12)
ItemIdLabel.grid(row=4, column=0, padx=12)

#set the class for the classification of each of items class be called and be valid when classify

classArray = ['Food','Computer Parts', 'Personal Care', 'Drink', 'Gadgets']

#Button_Changes_configuration _ for productentry
sellIdProduct = Entry(productFrame, width= 50, textvariable=placeholderArray[0])
nameIdProduct = Entry(productFrame, width= 50, textvariable=placeholderArray[1])
priceIdProduct = Entry(productFrame,width= 50, textvariable=placeholderArray[2])
quantIdProduct= Entry(productFrame, width= 50,textvariable=placeholderArray[3])
# a combobox is one of the created module of tk that makes a another box combo added to the grid selection
# of the selected category its like a added selection for that only specific grid/gui
ItemIdCombo = ttk.Combobox(productFrame, width= 47, textvariable=placeholderArray[4], values=classArray)

#to have and be frames per part of the window of the selected area grid(3)-Product entries
sellIdProduct.grid(row=0, column=2, padx=5, pady=5)
nameIdProduct.grid(row=1, column=2, padx=5, pady=5)
priceIdProduct.grid(row=2, column=2, padx=5, pady=5)
quantIdProduct.grid(row=3, column=2, padx=5, pady=5)
ItemIdCombo.grid(row=4, column=2, padx=5, pady=5)

generateIdbutton = Button(productFrame,text='GENERATE ID', borderwidth=3,background=ButtonColor, fg='white',command=generateRand)
generateIdbutton.grid(row=0, column=3, padx=5, pady=5)

#the_subview root of the window / the things below that is functioning a like spreadsheet where the 
#data is being stored 
style.configure(window)
my_root['columns'] = ('Sell Id','Name Id', 'Price Id', 'Quant Id', 'Item Id', 'Date Id')
my_root.column ('#0', width=0, stretch=NO)
my_root.column('Sell Id', anchor=W, width=70)
my_root.column('Name Id', anchor=W, width=130)
my_root.column('Price Id', anchor=W, width=130)
my_root.column('Quant Id', anchor=W, width=100)
my_root.column('Item Id', anchor=W, width=150)
my_root.column('Date Id', anchor=W, width=150)

my_root.heading('Sell Id',text='Sell Id',anchor=W)
my_root.heading('Name Id',text='Name ',anchor=W)
my_root.heading('Price Id',text='Price ',anchor=W)
my_root.heading('Quant Id',text='Quantity',anchor=W)
my_root.heading('Item Id',text='Item type ',anchor=W)
my_root.heading('Date Id',text='Date ',anchor=W)

my_root.tag_configure('orow',background='#EEEEEE')
my_root.pack()

refreshTable()

window.resizable(width= False, height= False)
#to set the window to be not resizable (unresizeable)

window.mainloop()

