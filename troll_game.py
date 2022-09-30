import discord
import os
import requests
from discord.ui import Button, View
import math
import random
import inflect

async def troll_game(message):
  def create_grid(cube):
    grid_size = 9  # Max is 12
    grid = [[cube for y in range(grid_size)] for x in range(grid_size)]
    for y in range(len(grid)):
      for x in range(len(grid)):
        if y == 0:
          grid = rItem(y,x,":green_square:",grid)
    return grid
  
  def grid_to_string(grid):
    string = ""
    for row in grid:
      for x in range (len(row)):
        string += row[x]
        if x  == (len(row) - 1):
          string += "\n"
    return string

  def string_to_grid(string):
    grid = []
    rows = string.splitlines()
    for row in rows:
      cells = row.split("::")
      for x in range (len(cells)):
        cell = cells[x].replace(":","")
        cell = ":" + cell + ":"
        cells[x] = cell
      grid.append(cells)

    return grid

  def find_item(grid,item):
    for x in range (len(grid)):
      for y in range(len(grid)):
        if grid[x][y] == item:
          return x,y

  def setMenuScreen():
    grid = create_grid(":red_square:")
    grid = rItem(2,2,":regional_indicator_c:",grid)
    grid = rItem(2,3,":regional_indicator_a:",grid)
    grid = rItem(2,4,":regional_indicator_u:",grid)
    grid = rItem(2,5,":regional_indicator_g:",grid)
    grid = rItem(2,6,":regional_indicator_h:",grid)
    grid = rItem(2,7,":regional_indicator_t:",grid)
    grid = rItem(2,1,":troll:",grid)
    grid = rItem(4,2,":regional_indicator_p:",grid)
    grid = rItem(4,3,":regional_indicator_r:",grid)
    grid = rItem(4,4,":regional_indicator_e:",grid)
    grid = rItem(4,5,":regional_indicator_s:",grid)
    grid = rItem(4,6,":regional_indicator_s:",grid)
    grid = rItem(5,2,":regional_indicator_a:",grid)
    grid = rItem(5,3,":regional_indicator_r:",grid)
    grid = rItem(5,4,":regional_indicator_r:",grid)
    grid = rItem(5,5,":regional_indicator_o:",grid)
    grid = rItem(5,6,":regional_indicator_w:",grid)
    grid = rItem(6,3,":regional_indicator_f:",grid)
    grid = rItem(6,4,":regional_indicator_o:",grid)
    grid = rItem(6,5,":regional_indicator_r:",grid)
    grid = rItem(7,1,":regional_indicator_r:",grid)
    grid = rItem(7,2,":regional_indicator_e:",grid)
    grid = rItem(7,3,":regional_indicator_f:",grid)
    grid = rItem(7,4,":regional_indicator_r:",grid)
    grid = rItem(7,5,":regional_indicator_e:",grid)
    grid = rItem(7,6,":regional_indicator_s:",grid)
    grid = rItem(7,7,":regional_indicator_h:",grid)
    return grid

  def move_spy(grid):
    sx,sy = find_item(grid,":spy:")
    tx,ty = find_item(grid,":troll:")

    newX, newY = sx, sy
    if tx < sx:
      newX = sx - 1
    if tx > sx:
      newX = sx + 1

    if (ty < sy):
      newY = sy - 1
    if (ty > sy):
      newY = sy + 1

    if (grid[newX][newY] == ":troll:"):
      grid = setMenuScreen()
    else:
      grid[newX][newY] = ":spy:"

      grid[sx][sy] = ":blue_square:"

    return grid

  def move_spy_start(grid):
    
    x,y = find_item(grid,":spy:")

    grid[x][y] = ':blue_square:'

    grid[0][4] = ':spy:'

    return grid
    
    
  def move_troll(direction,grid):
    global score
    
    x,y = find_item(grid,":troll:")

    replace = True

    newX = x
    newY = y

    if direction == "up":
      if x != 1:
        newX = x - 1
        newY = y
    elif direction == "down":
      if x != 8:
        newX = x + 1
        newY = y
    elif direction == "left":
      if y != 0:
        newX = x
        newY = y - 1
    elif direction == "right":
      if y != 8:
        newX = x
        newY = y + 1

    if grid[newX][newY] == ":spy:":
      return grid

    if grid[newX][newY] == ":hammer:":
      grid = move_spy_start(grid)
      posX,posY = create_star_position(grid)
      grid[posX][posY] = ':hammer:'

    grid[x][y] = ':blue_square:'
    grid[newX][newY] = ':troll:'

    score += 1
    print(score)
    
    return grid

  def create_star_position(grid):
    created = False
    while created == False:
      created = True
      posX = random.randint(0,8)
      posY = random.randint(1,8)
      if (grid[posY][posX] != ':blue_square:'):
        created = False
    return posY, posX
        
  def rItem(positionX,positionY,newString,grid): # Replace Grid Item
    grid[positionX][positionY] = newString
    return grid

  
  grid = create_grid(":blue_square:")

  grid = rItem(4,4,":troll:",grid)

  grid = rItem(0,4,":spy:",grid)

  starX, starY = create_star_position(grid)
  grid = rItem(starX,starY,":hammer:",grid)
  
  grid = grid_to_string(grid)

  global score
  score = 0
  
  async def button_callback(interaction):
    global score
    direction = interaction.data['custom_id']
    grid = interaction.message.content
    grid = string_to_grid(grid)
    if (grid[2][2] == ":regional_indicator_c:"):
      grid = create_grid(":blue_square:")
      grid = rItem(4,4,":troll:",grid)
      grid = rItem(0,4,":spy:",grid)
      starX, starY = create_star_position(grid)
      grid = rItem(starX,starY,":hammer:",grid)
      score = 0
    else :
      grid = move_troll(direction,grid)
      grid = move_spy(grid)
      p = inflect.engine()
      if (score < 10):
        strScore = p.number_to_words(score)
        grid = rItem(0,4,":" + strScore + ":",grid)
      elif score == 10:
        grid = rItem(0,4,":keycap_ten:",grid)
      else :
        scoreStr = str(score)
        strNumber1 = p.number_to_words(scoreStr[0])
        strNumber2 = p.number_to_words(scoreStr[1])
        grid = rItem(0,3,":" + strNumber1 + ":",grid)
        grid = rItem(0,4,":" + strNumber2 + ":",grid)
      
    grid = grid_to_string(grid)
    await interaction.response.edit_message(content = grid)
    
    
  
  button = Button(label = " X ",  row = 1, )
  button2 = Button(label = "  ", row = 1, style = discord.ButtonStyle.green, emoji = "🔼", custom_id = "up")
  button3 = Button(label = " X ", row = 1, )
  button4 = Button(label = "  ", row = 2, style = discord.ButtonStyle.green , emoji = "◀", custom_id = "left")
  button5 = Button(label = " X ", row = 2, )
  button6 = Button(label = "  ", row = 2, style = discord.ButtonStyle.green , emoji = "▶" ,custom_id = "right")
  button7 = Button(label = " X ", row = 3, )
  button8 = Button(label = "  ", row = 3, style = discord.ButtonStyle.green, emoji = "🔽" ,custom_id = "down")
  button9 = Button(label = " X " , row = 3, )

  button2.callback = button_callback
  button4.callback = button_callback
  button6.callback = button_callback
  button8.callback = button_callback
  
  view = View()
  view.add_item(button)
  view.add_item(button2)
  view.add_item(button3)
  view.add_item(button4)
  view.add_item(button5)
  view.add_item(button6)
  view.add_item(button7)
  view.add_item(button8)
  view.add_item(button9)

  await message.channel.send(grid,view=view)