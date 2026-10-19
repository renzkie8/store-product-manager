# a project that manage the product of a sari-sari store
from tkinter import *
# here we are importing it to all (*) were not importing a variable but to all 

class MyStoreProdMng:

  def __init__(self):

    # CONFIGURATIONS AREA
    TK_WINDOW_WIDTH = 700
    TK_WINDOW_HEIGHT= 650

    #Window Code
    self.window = Tk()

    root = self.window

    root.title('Our Store Product Manager')
    
    #title of the tkinter or the window created
    root.geometry(f'{TK_WINDOW_WIDTH}x{TK_WINDOW_HEIGHT}+600+150')
    #the width x height of the window created this all no. is by px(pixel)
    # the second added number is the transition of window from left to rght(x coordinates)
    #the third added number is the transiton of window from bottom to top(y coordinaties) to center
    root.resizable(width= False, height= False)
    #to set the window to be not resizable (unresizeable)

    #TODO - Be frames per part of the window grid



    root.mainloop()
    
    ...
  #End def __init__
  ... #ELLIPSIS
    #Here is called ellipsis that is to End def__init__
    #End classMy Store Prod Mng

MyStoreProdMng()
#This will run the initializer the Tk object and it will run the main loop
    