from pyswip import Prolog, prolog

class SubwayProlog():
  def __init__(self):
    self.prolog = Prolog()
    # import prolog file
    self.prolog.consult("prolog.pl") 
    self.prologRetract()

  # update counter and convert result into a list
  def convertResult(self, result):
    c = 0
    listed = []
    while (c < len(result)):
      listed.append(result[c].value)
      c += 1
    return listed

  # clear all previous selections
  def prologRetract(self):
    self.prolog.retractall("chosen_meals(X)")
    self.prolog.retractall("chosen_breads(X)")
    self.prolog.retractall("chosen_mains(X)")
    self.prolog.retractall("chosen_veggies(X)")
    self.prolog.retractall("chosen_sauces(X)")
    self.prolog.retractall("chosen_topups(X)")
    self.prolog.retractall("chosen_sides(X)")
    self.prolog.retractall("chosen_drinks(X)")

  # assert chosen options into prolog list
  def addChoice(self, X, op):
    if op == 'meal':
      self.prolog.assertz("chosen_meals({})".format(X))
    elif op == 'bread':
      self.prolog.assertz("chosen_breads({})".format(X))
    elif op == 'main':
      self.prolog.assertz("chosen_mains({})".format(X))
    elif op == 'veg':
      self.prolog.assertz("chosen_veggies({})".format(X))
    elif op == 'sauce':
      self.prolog.assertz("chosen_sauces({})".format(X))
    elif op == 'topup':
      self.prolog.assertz("chosen_topups({})".format(X))
    elif op == 'side':
      self.prolog.assertz("chosen_sides({})".format(X))
    else:
      self.prolog.assertz("chosen_drinks({})".format(X))

  # options given to users based on prolog logic
  def defaultOptions(self, category):
    result = list(self.prolog.query("default_options({}, X)".format(category)))[0]["X"]
    return self.convertResult(result)

  def availableOptions(self, category):
    result = list(self.prolog.query("available_options({}, X)".format(category)))
    return result if result == [] else self.convertResult(result[0]["X"])

  def chosenOptions(self, category):
    result = list(self.prolog.query("chosen_options({}, X)".format(category)))
    return result if result == [] else self.convertResult(result[0]["X"])

  def userOptions(self, category):
    return list(set(self.availableOptions(category)) - set(self.chosenOptions(category)))
    