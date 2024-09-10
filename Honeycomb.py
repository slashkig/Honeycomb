import turtle, random
# Functions ------------------------------------------------------------------------
# Draws one comb
def hexagon(b, fc):
  t.fillcolor(fc)
  t.showturtle()
  bees[b].hideturtle()
  t.forward(40)
  t.right(60)
  for i in range(2):
    if i == 0:
      t.begin_fill()
    else:
      t.end_fill()
      t.pendown()    
    for j in range(6):
      t.right(60)
      t.forward(40)
  t.penup()
  t.goto(bees[b].pos())
  if pos[b] not in combs:
    combs.append(pos[b][:])
    comb_stat.append(0)
    comb_type.append("empty")
  bees[b].showturtle()
  t.hideturtle()
# Initializes one bee
def create_bee(init_coord, init_pos):
  b = turtle.Turtle()
  b.hideturtle()
  b.speed(7)
  b.color("black", "yellow")
  b.penup()
  b.goto(init_coord)
  b.showturtle()
  pos.append(init_pos)
  pollen.append(1)
  food.append(1)
  turns.append(list(range(6)))
  bees.append(b)
# Bee communism
def distribute(p1, p2, mult=1, div=2):
  total = p1 + p2
  rem = total % div
  p1 = mult * (total - rem) / div + rem
  p2 = (div - mult) * (total - rem) / div
  return (p1, p2)
# Converts a filled comb back into its empty state
def clean():
  hexagon(n, "goldenrod")
  comb_type[c_id] = "empty"
  comb_stat[c_id] = 0

# Setup ----------------------------------------------------------------------------
# Create comb and bee tracking variables
combs, comb_stat, comb_type, pos, pollen, food, turns, bees = [[] for i in range(8)]
# Create an invisible turtle that manages drawing and movement guidance
t = turtle.Turtle()
t.hideturtle()
t.penup()
t.pensize(5)
t.speed(0)
t.left(30)
t.pencolor("sienna")
for i in range(3): # Creates the starting bees
  create_bee((0, 0), [0, 0])
hexagon(0, "goldenrod") # Starting comb
# Main ----------------------------------------------------------------------------
for i in range(1000):
  for n, b in enumerate(bees[:]):
    # Checks if the bee is fed
    if food[n] < 0:
      b.fillcolor("red")
    if b.fillcolor() == "red":
      if food[n] >= 0:
        b.fillcolor("yellow")
      continue
    elif i % 50 == 49:
      food[n] -= 1
    
    # Semi-random bee movement
    num = random.choice(turns[n]) # Decides the direction
    b.setheading(60 * num)
    # Changes position tracker and modifies rotation weights
    if turns[n].count(num) > 1:
      turns[n].remove(num)
    if num <= 2:
      pos[n][0] += num % 2 + 1
      pos[n][1] += 1 - num
      turns[n].append(num + 3)
    else:
      pos[n][0] -= (num - 3) % 2 + 1
      pos[n][1] -= 1 - (num - 3)
      turns[n].append(num - 3)
    # Moves the bee
    t.goto(b.pos())
    t.setheading(b.heading() + 90)
    for j in range(2):
      t.right(60)
      t.forward(40)
    b.goto(t.pos())
    
    # Interaction with other bees in the comb
    for ind in range(len(bees)):
      if pos[n] == pos[ind] and n != ind:
        pollen[n], pollen[ind] = distribute(pollen[n], pollen[ind])
        if food[n] + food[ind] > 0:
          food[n], food[ind] = distribute(food[n], food[ind])

    # Bee does one action
    num = random.randint(1, 5)
    if pos[n] not in combs and num <= pollen[n] - 1: # Build new comb
      hexagon(n, "goldenrod")
    elif pos[n] not in combs: # Gather material
      pollen[n] += random.randint(1, 2)
    else: # Comb work
      c_id = combs.index(pos[n])
      stat = comb_stat[c_id]
      tp = comb_type[c_id]
      if tp == "empty": # Create a specialized comb
        if num <= food[n] - 3:
          if comb_type.count("FDstorage") <= comb_type.count("brood") + 1 or food[n] > random.randint(6, 10): # Create food storage comb
            hexagon(n, "gold")
            comb_type[c_id] = "FDstorage"
          else: # Create bee raising comb
            hexagon(n, "burlywood")
            comb_type[c_id] = "brood"
            food[n] -= 1

        elif num < pollen[n] - 3: # Create material storage comb
          hexagon(n, "khaki")
          comb_type[c_id] = "SFstorage"

        elif num < pollen[n]: # Create food production comb
          hexagon(n, "sandy brown")
          comb_type[c_id] = "processing"          
          pollen[n] -= 0.5
      # Maintain a specialized comb -------------------------
      tp = comb_type[c_id]
      if tp == "brood" and food[n] >= 3: # Grow a young bee
        if stat == 3:
          clean()
          create_bee(t.pos()[:], pos[n][:])
          continue
        t.dot((stat + 2)**2, "khaki")
        food[n] -= 2
        comb_stat[c_id] += 1

      elif tp == "processing": # 
        if stat == 2:
          food[n] += 2
          clean()
          continue
        elif pollen[n] < 1 and stat < 1:
          pollen[n] += stat * 1.25 + 0.5
          clean()
          continue
        t.dot(5 + stat * 2.5, ("yellow", "gold", "orange", "dark orange", "chocolate")[int(stat * 2.5)])
        comb_stat[c_id] += 0.4
        pollen[n] -= 0.5
      
      elif tp == "FDstorage": # Add or take food from storage
        if food[n] * 2 < stat:
          t.dot(2 * stat + 2, "gold")
        comb_stat[c_id], food[n] = distribute(comb_stat[c_id], food[n], 2, 3)
        stat = comb_stat[c_id]
        if food[n] < 3 and stat >= 3 - food[n]:
          comb_stat[c_id] -= 3 - food[n]
          food[n] = 3
          if stat == 0:
            clean()
            continue
        elif food[n] < 3 and stat < 3:
          food[n] += stat
          clean()
          continue
        t.dot(2 * comb_stat[c_id], "goldenrod")

      elif tp == "SFstorage": # Add or take material from storage
        if pollen[n] < 2 and stat <= 3:
          pollen[n] += stat
          clean()
          continue
        elif pollen[n] < stat:
          t.dot(2 * stat + 2, "khaki")
        comb_stat[c_id], pollen[n] = distribute(comb_stat[c_id], pollen[n])
        t.dot(2 * comb_stat[c_id], "dark orange")
