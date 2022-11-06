# tictactoe.py - Tic Tac Toe game


import pygame, sys, time, random


# a 3x3 tic-tac-toe board
CELL_X = 3
CELL_Y = 3

# (x1, y1), (x2, y2) and (x3, y3) for each "3 in a row"
TRIPLES = (
    ((1,1),(1,2),(1,3)), ((2,1),(2,2),(2,3)), ((3,1),(3,2),(3,3)),
    ((1,1),(2,1),(3,1)), ((1,2),(2,2),(3,2)), ((1,3),(2,3),(3,3)),
    ((1,1),(2,2),(3,3)), ((1,3),(2,2),(3,1)))

# dimensions in pixels of the margin (BASE) and cell size (SIZE)
MARG_X = 20
MARG_Y = 20
SIZE_X = 120
SIZE_Y = 120

# dimensions in pixels of the Pygame display
DISP_X = MARG_X + (SIZE_X * CELL_X) + MARG_X
DISP_Y = MARG_Y + (SIZE_Y * CELL_Y) + MARG_Y * 2.5
INIT_Y = DISP_Y - MARG_Y * 1.5

# colors taken from Google tic-tac-toe
DISP_COLOR = (20, 189, 172)
L_COLOR = (13, 161, 146)
W_COLOR = (8, 109, 99)
X_COLOR = (84, 84, 84)
O_COLOR = (242, 235, 211)

# line and shape thicknesses
L_WIDTH = 10
X_WIDTH = 15
O_WIDTH = 10


# where everything starts. create a game object and run it
def main():
  run_game(Game())


# most of the Pygame stuff - then hands off to the game object
def run_game(game):
  pygame.init()
  pygame.display.set_caption(game.caption)

  display = pygame.display.set_mode((DISP_X, DISP_Y))
  
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
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
    self.caption = 'Tic Tac Toe'
    self.reset()


  # start or restart the game
  def reset(self):
    self.cells = [['-'] * CELL_X for cell_y in range(CELL_Y)]
    self.player = 'X'
    self.computers_turn = False
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
    if self.game_init:
      self.draw_init(display)
    if self.game_over:
      self.draw_over(display)
    self.is_dirty = False


  # draw the game board lines
  def draw_lines(self, display):
    for cell_x in range(1, CELL_X):
      pygame.draw.line(display, L_COLOR, 
          to_disp(cell_x + 0.5, 1 - 0.5),
          to_disp(cell_x + 0.5, CELL_X + 0.5), L_WIDTH)
    for cell_y in range(1, CELL_Y):
      pygame.draw.line(display, L_COLOR, 
          to_disp(1 - 0.5, cell_y + 0.5),
          to_disp(CELL_Y + 0.5, cell_y + 0.5), L_WIDTH)


  # draw a game board cell
  def draw_cell(self, display, cell_x, cell_y):
    player = self.get_cell(cell_x, cell_y)
    (x_disp, y_disp) = to_disp(cell_x, cell_y)
    if player == 'X':
      r = to_size(0.35)
      pygame.draw.line(display, X_COLOR,
          (x_disp - r, y_disp - r), (x_disp + r, y_disp + r), X_WIDTH)
      pygame.draw.line(display, X_COLOR,
          (x_disp - r, y_disp + r), (x_disp + r, y_disp - r), X_WIDTH)
    if player == 'O':
      pygame.draw.circle(display, O_COLOR,
          (x_disp, y_disp), to_size(0.4), O_WIDTH)


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
    ((x1, y1), (x3, y3), player) = self.win_data
    if x1 != x3: x1 -= 0.5; x3 += 0.5
    if y1 != y3: y1 -= 0.5; y3 += 0.5
    if y1 == 2.5: y1 = 3.5; y3 = 0.5
    pygame.draw.line(display, O_COLOR,
        to_disp(x1, y1), to_disp(x3, y3), int(X_WIDTH / 2))


  # draw a message in the init pane
  def draw_message(self, display, message):
    font = pygame.font.SysFont(None, 24)
    image = font.render(message, True, W_COLOR)
    display.blit(image, (MARG_X, DISP_Y - MARG_Y))


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
      cell_x = random.randint(1, 3)
      cell_y = random.randint(1, 3)
      if self.play_cell(cell_x, cell_y, player):
        return True


  # try to play a cell which wins or (if not) blocks
  def play_win_block(self, player):
    for check in (player, opponent(player)):
      for triple in TRIPLES:
        cells = self.get_cells(triple)
        if cells.count(check) == 2 and cells.count('-') == 1:
          (cell_x, cell_y) = triple[cells.index('-')]
          self.play_cell(cell_x, cell_y, player)
          return True
    return False


  # play a cell and schedule redraw
  def play_cell(self, cell_x, cell_y, player):
    if (cell_x < 1 or CELL_X < cell_x or
        cell_y < 1 or CELL_Y < cell_y or
        self.get_cell(cell_x, cell_y) != '-'):
      return False
    self.set_cell(cell_x, cell_y, player)
    self.win_data = self.check_win()
    self.game_over = True if self.win_data else self.check_over()
    self.is_dirty = True
    return True


  # check if game over by testing for 3 in a row
  def check_win(self):
    for triple in TRIPLES:
      (cell1, cell2, cell3) = self.get_cells(triple)
      if cell1 == cell2 == cell3 != '-':
        return (triple[0], triple[2], cell1)
    return None


  # check if game over by counting unused cells
  def check_over(self):
    if sum(row.count('-') for row in self.cells) == 0:
      return True
    return False


  # get a triple of cells
  def get_cells(self, triple):
    return [self.get_cell(cell_x, cell_y) for (cell_x, cell_y) in triple]


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
  (grid_x, grid_y) = to_grid(disp_x, disp_y)
  (cell_x, cell_y) = (int(round(grid_x)), int(round(grid_y)))
  if abs(grid_x - cell_x) > 0.4 or abs(grid_y - cell_y) > 0.4:
    return (0, 0)
  return (cell_x, cell_y)


# transform display space coordinates to grid space
def to_grid(disp_x, disp_y):
  return ((disp_x - MARG_X) / SIZE_X + 0.5,
          (disp_y - MARG_Y) / SIZE_Y + 0.5)


# transform grid space coordinates to display space
def to_disp(grid_x, grid_y):
  return (MARG_X + SIZE_X * (grid_x - 0.5),
          MARG_Y + SIZE_Y * (grid_y - 0.5))


# transform grid space dimension to display space
def to_size(grid):
  return SIZE_X * grid


# and here we go!
if __name__ == '__main__':
  main()
