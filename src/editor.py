import tkinter as tk
import random
import math
import copy

# Main class: inherit from tk.Canvas class
class Editor(tk.Canvas):
    linesNb = 20

    # Bricks properties
    bricksWidth = 50
    bricksHeight = 20
    bricksNbByLine = 16
    bricksColors = {
        "r": "#e74c3c",
        "g": "#2ecc71",
        "b": "#3498db",
        "t": "#1abc9c",
        "p": "#9b59b6",
        "y": "#f1c40f",
        "o": "#e67e22",
    }

    # Screen properties
    screenHeight = 500
    screenWidth = bricksWidth*bricksNbByLine

    # This method creates the window and loads the level.
    # If the "X.txt" file (with X the level number) exists, the bricks
    # of the level are placed in the window and white bricks correspond to ".".
    # If the file doesn't exist, the window is filled with white bricks.
    def __init__(self, root, level):
        tk.Canvas.__init__(self, root, bg="#ffffff", bd=0, highlightthickness=0, relief="ridge", width=self.screenWidth, height=self.screenHeight)
        self.level = level
        try:
            file = open(str(self.level)+".txt")
            bricks = list(file.read().replace("\n", ""))[:(self.bricksNbByLine*self.linesNb)]
            file.close()
        except IOError:
            bricks = []
        for i in range(self.bricksNbByLine*self.linesNb-len(bricks)):
            bricks.append(".")
        for i, j in enumerate(bricks):
            col = i%self.bricksNbByLine
            line = i//self.bricksNbByLine
            if j == ".":
                color = "#ffffff"
            else:
                color = self.bricksColors[j]
            self.create_rectangle(col*self.bricksWidth, line*self.bricksHeight, (col+1)*self.bricksWidth, (line+1)*self.bricksHeight, fill=color, width=2, outline="#ffffff")
        for i, j in enumerate(self.bricksColors.items()):
            self.create_rectangle(i*self.bricksWidth, self.screenHeight-self.bricksHeight, (i+1)*self.bricksWidth, self.screenHeight, fill=j[1], width=2, outline="#ffffff")
        self.pack()

    # This method, called each time user wants to change a brick color,
    # changes the bricks color and saves the new grid in the "X.txt" file
    # (with X the level number) where white bricks are replaced with ".".
    def setColor(self, id, color):
        self.itemconfig(id, fill=color)
        
        content = ""
        for i in range(self.bricksNbByLine*self.linesNb):
            if i%self.bricksNbByLine == 0 and i != 0:
                content += "\n"
            brickColor = self.itemcget(i+1, "fill")
            brickId = [id for id, color in self.bricksColors.items() if color == brickColor]
            if brickId == []:
                content += "."
            else:
                content += brickId[0]
            
        file = open(str(self.level)+".txt", "w")
        file.write(content)
        file.close()


# This function is called when the user left clicks.
# If the user clicks on a brick at the bottom of the screen,
# he selects the color of the clicked brick.
# If the user clicks on a brick in the middle of the screen,
# the clicked brick takes the selected color.
def eventsLeftClick(event):
    global editor

    id = event.widget.find_closest(event.x, event.y)[0]
    if id <= editor.bricksNbByLine*editor.linesNb:
        if hasattr(editor, "selectedColor"):
            editor.setColor(id, editor.selectedColor)
    else:
        editor.selectedColor = editor.itemcget(id, "fill")
        
# This function is called when the user right clicks.
# The brick clicked becomes white.
def eventsRightClick(event):
    global editor

    id = event.widget.find_closest(event.x, event.y)[0]
    if id <= editor.bricksNbByLine*editor.linesNb:
        editor.setColor(id, "#ffffff")    


# Initialization of the window
root = tk.Tk()
root.title("Editor")
root.resizable(0,0)
root.bind("<Button-1>", eventsLeftClick)
root.bind("<Button-3>", eventsRightClick)

# Starting up of the editor
editor = Editor(root, int(input("What is the level number? ")))
root.mainloop()