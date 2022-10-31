# fourinarow.py - Four in a Row game


import pygame, sys, time, random

# a 7x6 Four in a Row board
CELL_X = 7
CELL_Y = 6

# relative cells for Four in a Row
FOURS = (
  ((0,0), (1,0), (2,0), (3,0)),
  ((0,0), (1,1), (2,2), (3,3)),
  ((0,3), (1,2), (2,1), (3,0)),
  ((0,0), (0,1), (0,2), (0,3)),
)

# dimensions in pixels of the margin (BASE) and cell size (SIZE)
MARG_X = 20
MARG_Y = 20
SIZE_X = 60
SIZE_Y = 60

# dimensions in pixels of the Pygame display
DISP_X = MARG_X + (SIZE_X * CELL_X) + MARG_X
DISP_Y = MARG_Y + (SIZE_Y * CELL_Y) + MARG_Y * 2.5
INIT_Y = DISP_Y - MARG_Y * 1.5

# colors taken from Google tic-tac-toe
DISP_COLOR = (20, 189, 172)
HIGH_COLOR = (255, 255, 0)
L_COLOR = (13, 161, 146)
W_COLOR = (8, 109, 99)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)

# line and shape thicknesses
L_WIDTH = 5
X_WIDTH = 7
O_WIDTH = 5


# where everything starts. create a game object and run it
def main():
  run_game(Game())


# most of the Pygame stuff - then hands off to the game object
def run_game(game):
  pygame.init()
  pygame.display.set_caption(game.caption)

  display = pygame.display.set_mode((DISP_X, DISP_Y))
  
  game.font = pygame.font.SysFont("Arial", 16)
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.MOUSEMOTION:
        game.motion(event.pos[0], event.pos[1])
      if event.type == pygame.MOUSEBUTTONDOWN:
        game.click(event.pos[0], event.pos[1])
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
          game.reset()

    if game.is_dirty:
      display.fill(DISP_COLOR)
      game.draw(display)
      pygame.display.update()
    
    game.update()
    time.sleep(1/20)


# the game class - the uniqueness of tic-tac-toe
class Game:
  def __init__(self):
    self.caption = '  Connect 4'
    self.reset()


  # start or restart the game
  def reset(self):
    self.cells = [['-'] * CELL_X for cell_y in range(CELL_Y)]
    self.player = 'X'
    self.computers_turn = False
    self.highlight = (0, 0)
    self.win_data = None
    self.game_init = True
    self.game_over = False
    self.is_dirty = True

  
  # update game model after frame display
  def update(self):
    if self.game_over:
      return
    if self.computers_turn:
      if not self.play_win_block(self.player):
        self.play_random(self.player)
      self.player = opponent(self.player)
      self.computers_turn = False


  # refresh the display frame
  def draw(self, display):
    self.draw_lines(display)
    for cell_x in range(1, CELL_X + 1):
      for cell_y in range(1, CELL_Y + 1):
        self.draw_cell(display, cell_x, cell_y)
    self.draw_highlight(display)
    if self.game_init:
      self.draw_init(display)
    if self.game_over:
      self.draw_over(display)
    self.is_dirty = False


  # draw the game board lines
  def draw_lines(self, display):
    for cell_x in range(0, CELL_X + 1):
      pygame.draw.line(display, L_COLOR, 
          to_disp(cell_x + 0.5, 1 - 0.5),
          to_disp(cell_x + 0.5, CELL_Y + 0.5), L_WIDTH)
    for cell_y in range(0, CELL_Y + 1):
      pygame.draw.line(display, L_COLOR, 
          to_disp(1 - 0.5, cell_y + 0.5),
          to_disp(CELL_X + 0.5, cell_y + 0.5), L_WIDTH)


  # draw a game board cell
  def draw_cell(self, display, cell_x, cell_y):
    player = self.get_cell(cell_x, cell_y)
    (disp_x, disp_y) = to_disp(cell_x, cell_y)
    if player == '-':
      self.draw_text(display, disp_x, disp_y, f'{cell_x},{cell_y}')
    if player == 'X':
      r = to_disp_dx(0.35)
      pygame.draw.line(display, X_COLOR,
          (disp_x - r, disp_y - r), (disp_x + r, disp_y + r), X_WIDTH)
      pygame.draw.line(display, X_COLOR,
          (disp_x - r, disp_y + r), (disp_x + r, disp_y - r), X_WIDTH)
    if player == 'O':
      pygame.draw.circle(display, O_COLOR,
          (disp_x, disp_y), to_disp_dx(0.4), O_WIDTH)


  # draw the cell highlight
  def draw_highlight(self, display):
    (cell_x, cell_y) = self.highlight
    if cell_x == 0 or cell_y == 0:
      return
    (disp_x, disp_y) = to_disp(cell_x - 0.45, 6.45)
    (disp_dx, disp_dy) = to_disp_d(0.9, 5.9)
    pygame.draw.rect(display, HIGH_COLOR,
        (disp_x, disp_y, disp_dx, disp_dy), 2)

    
  # draw the init pane
  def draw_init(self, display):
    pygame.draw.line(display, L_COLOR,
        (0, INIT_Y), (DISP_X, INIT_Y), 2)
    self.draw_message(display, 'Click Here for Computer to Play First')

    
  # draw the game over embellishments
  def draw_over(self, display):
    if self.win_data == None:
      self.draw_message(display, 'It\'s a tie!')
      return
    ((x1, y1), (x4, y4), player) = self.win_data
    if x1 != x4: x1 -= 0.5; x4 += 0.5
    if y1 <  y4: y1 -= 0.5; y4 += 0.5
    if y1 >  y4: y1 += 0.5; y4 -= 0.5
    width = X_WIDTH / 2.0 if (x1 == x4 or y1 == y4) else X_WIDTH / 1.5
    pygame.draw.line(display, O_COLOR,
        to_disp(x1, y1), to_disp(x4, y4), int(width))


  # draw a message in the init pane
  def draw_message(self, display, text):
    self.draw_text(display, DISP_X / 2, (INIT_Y + DISP_Y) / 2, text)


  # draw text centered at a display point
  def draw_text(self, display, disp_x, disp_y, text):
    image = self.font.render(text, True, W_COLOR)
    rect = image.get_rect(center=(disp_x, disp_y))
    display.blit(image, rect)

    
  # action mouse motion
  def motion(self, mouse_x, mouse_y):
    if self.game_over:
      (cell_x, cell_y) = (0, 0)
    else:
      (cell_x, cell_y) = to_cell(mouse_x, mouse_y)
    if self.highlight != (cell_x, cell_y):
      self.highlight = (cell_x, cell_y) 
      self.is_dirty = True

      
  # action mouse click
  def click(self, mouse_x, mouse_y):
    if self.game_over:
      return
    self.click_cell(mouse_x, mouse_y)
    self.click_init(mouse_x, mouse_y)


  # action mouse click in cell
  def click_cell(self, mouse_x, mouse_y):
    (cell_x, cell_y) = to_cell(mouse_x, mouse_y)
    if self.play_cell(cell_x, cell_y, self.player):
      self.player = opponent(self.player)
      self.computers_turn = True
      self.game_init = False
      return True
    return False


  # action mouse click in init pane
  def click_init(self, mouse_x, mouse_y):
    if self.game_init and mouse_y > INIT_Y:
      self.computers_turn = True
      self.game_init = False
      self.is_dirty = True
      return True
    return False


  # play a random cell
  def play_random(self, player):
    while True:
      if self.game_over:
        return False
      cell_x = random.randint(1, CELL_X)
      if self.play_cell(cell_x, CELL_Y, player):
        return True


  # check if a space is playable
  def is_availible(self, cell_x, cell_y):
    return cell_y == 1 or self.get_cell(cell_x, cell_y - 1) != "-"
      

    
  # try to play a cell which wins or (if not) blocks
  def play_win_block(self, player):
    for four in FOURS:
      cell_dx = four[3][0]
      cell_dy = max(four[0][1], four[3][1])
      for cell_x in range(0, CELL_X + 1 - cell_dx):
        for cell_y in range(0, CELL_Y + 1 - cell_dy):
          cells = self.get_four_cells(cell_x, cell_y, four)
          if (cells.count("X") == 3 or cells.count("O") == 3) and cells.count('-') == 1:
            cell_d = four[cells.index("-")]
            if self.is_availible(cell_x + cell_d[0], cell_y + cell_d[1]):
              self.play_cell(cell_x, cell_y, player)
              return True
    return False


  # play a cell and schedule redraw
  def play_cell(self, cell_x, cell_y, player):
    if (cell_x < 1 or CELL_X < cell_x or
      cell_y < 1 or CELL_Y < cell_y or
      self.get_cell(cell_x, CELL_Y) != '-'):
      return False
    for test_y in range(1, CELL_Y + 1):
      if self.get_cell(cell_x, test_y) == '-':
        self.set_cell(cell_x, test_y, player)
        self.win_data = self.check_win()
        self.game_over = self.win_data != None or self.check_over()
        self.is_dirty = True
        return True
    return False


  # check if game over by testing for 4 in a row
  def check_win(self):
    for four in FOURS:
      cell_dx = four[3][0]
      cell_dy = max(four[0][1], four[3][1])
      for cell_x in range(1, CELL_X + 1 - cell_dx):
        for cell_y in range(1, CELL_Y + 1 - cell_dy):
          (cell1, cell2, cell3, cell4) = self.get_four_cells(
            cell_x, cell_y, four)
          if cell1 == cell2 == cell3 == cell4 != '-':
            cell1_xy = (cell_x + four[0][0], cell_y + four[0][1])
            cell4_xy = (cell_x + four[3][0], cell_y + four[3][1])
            return (cell1_xy, cell4_xy, cell1)
    return None


  # check if game over by counting unused cells
  def check_over(self):
    if sum(row.count('-') for row in self.cells) == 0:
      return True
    return False


  # get a four in a row of cells
  def get_four_cells(self, cell_x, cell_y, four):
    return [self.get_cell(cell_x + x, cell_y + y) for (x, y) in four]


  # get and set individual cells
  def get_cell(self, cell_x, cell_y):
    return self.cells[cell_y - 1][cell_x - 1]

  def set_cell(self, cell_x, cell_y, player):
    self.cells[cell_y - 1][cell_x - 1] = player

# end of Game class


# calculate opponent of player
def opponent(player):
  return 'O' if player == 'X' else 'X'


# transform display (or mouse) space coordinates to cell indexes
def to_cell(disp_x, disp_y):
  cell_x = to_cell_x(disp_x)
  cell_y = to_cell_y(disp_y)
  return (cell_x, cell_y)

def to_cell_x(disp_x):
  grid_x = to_grid_x(disp_x)
  cell_x = int(round(grid_x))
  return cell_x if abs(grid_x - cell_x) < 0.4 else 0

def to_cell_y(disp_y):
  grid_y = to_grid_y(disp_y)
  cell_y = int(round(grid_y))
  return cell_y if abs(grid_y - cell_y) < 0.4 else 0


# transform display space dimensions to grid space
def to_grid_d(disp_dx, disp_dy):
  return (to_grid_dx(disp_dx), to_grid_dy(disp_dy))

def to_grid_dx(disp_dx):
  return disp_dx / SIZE_X

def to_grid_dy(disp_dy):
  return disp_dy / SIZE_Y


# transform display space coordinates to grid space
def to_grid(disp_x, disp_y):
  return (to_grid_x(disp_x), to_grid_y(disp_y))

def to_grid_x(disp_x):
  return (disp_x - MARG_X) / SIZE_X + 0.5

def to_grid_y(disp_y):
  return CELL_Y - (disp_y - MARG_Y) / SIZE_Y + 0.5


# transform grid space dimensions to display space
def to_disp_d(grid_dx, grid_dy):
  return (to_disp_dx(grid_dx), to_disp_dy(grid_dy))

def to_disp_dx(grid_dx):
  return grid_dx * SIZE_X

def to_disp_dy(grid_dy):
  return grid_dy * SIZE_Y


# transform grid space coordinates to display space
def to_disp(grid_x, grid_y):
  return (to_disp_x(grid_x), to_disp_y(grid_y))

def to_disp_x(grid_x):
  return MARG_X + SIZE_X * (grid_x - 0.5)

def to_disp_y(grid_y):
  return MARG_Y + SIZE_Y * (CELL_Y - grid_y + 0.5)

  
# and here we go!
if __name__ == '__main__':
  main()
