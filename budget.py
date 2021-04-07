class Category:

  def __init__(self, name): #constructor
    self.name = name
    self.ledger = list()

  def __str__(self):
    title = f"{self.name:*^30}\n"
    items = ""
    total = 0
    for i in self.ledger:
      items += f"{i['description'][0:23]:23}" + f"{i['amount']:>7.2f}" + "\n"
      total += i["amount"]
    output = title + items + "Total: " + str(total)
    return output


  def deposit(self, amount, description = ""):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description = ""):
    if self.check_funds(amount): 
      self.ledger.append({"amount": -amount, "description": description})
      return True
    else:
      return False

  def get_balance(self):
    balance = 0
    for i in self.ledger:
      balance += i["amount"]
    return balance

  def transfer(self, amount, destinationCategory):
    if self.check_funds(amount):
      self.withdraw(amount, "Transfer to " + destinationCategory.name)
      destinationCategory.deposit(amount, "Transfer from " + self.name)
      return True
    else:
      return False

  def check_funds(self, amount):
    if amount > self.get_balance():
      return False
    else:
      return True

  def get_withdrawals(self):
    spending = 0
    for i in self.ledger:
      if i['amount'] < 0:
        spending += i['amount']
    return spending


def truncate(n):
  multiplier = 10
  return int(n * multiplier) / multiplier

def get_totals(categories):
  total = 0
  breakdown = []
  for category in categories:
    total += category.get_withdrawals()
    breakdown.append(category.get_withdrawals())
  rounded = list(map(lambda x: truncate(x/total), breakdown))
  return rounded

def create_spend_chart(categories):
  res = "Percentage spent by category\n"
  i = 100
  totals = get_totals(categories)
  while i >= 0:
    cat_spaces = ' '
    for total in totals:
      if total * 100 >= i:
        cat_spaces += "o  "
      else:
        cat_spaces += "   "
    res += str(i).rjust(3) + "|" + cat_spaces + ("\n")
    i -= 10
  
  dashes = "-" + "---" * len(categories)
  names = []
  x_axis = ""
  for category in categories:
    names.append(category.name)

  maxi = max(names, key=len)

  for x in range(len(maxi)):
    nameStr = '     '
    for name in names:
      if x >= len(name):
        nameStr += "   "
      else:
        nameStr += name[x] + "  "

    if (x != len(maxi) -1):
      nameStr += "\n"

    x_axis += nameStr

  res += dashes.rjust(len(dashes)+4) + "\n" + x_axis
  return res
