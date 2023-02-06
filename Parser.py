"""
This is a recursive descent parser for the calc
language. 

To write a parser:

    1.) Construct the basic interface (lexer, next, has, must_be).
    2.) Convert each BNF rule into a mutually recursive function.
    3.) Add data structures to build the parse tree.
"""
import sys
from Lexer import Token, Lexer
from enum import Enum, auto


class ParseType(Enum):
  PROGRAM = auto()
  FUNCTION = auto()
  PARAMS = auto()
  BODY = auto()
  ATOMIC = auto()
  RETURN = auto()
  CREATEVAR = auto()
  REASSIGN = auto()
  WRITE = auto()
  INPUT = auto()
  LIST = auto()
  ASSIGN = auto()
  PATH = auto()
  LOOP = auto()
  CREATEARRAY = auto()
  COMPARABLE = auto()
  CONDITION = auto()
  EQ = auto()
  NOT = auto()
  GT = auto()
  GTEQ = auto()
  LT = auto()
  LTEQ = auto()
  ADD = auto()
  SUB = auto()
  MUL = auto()
  DIV = auto()
  POW = auto()
  NEGATION = auto()
  DEF = auto()
  IF = auto()
  IFELSE = auto()
  PRINT = auto()
  READ = auto()
  CALL = auto()
  INDEX = auto()


ariness = {
  ParseType.ATOMIC: 0,
  ParseType.INPUT: 1,
  ParseType.CREATEARRAY: 2,
  ParseType.ASSIGN: 2,
  ParseType.ADD: 2,
  ParseType.SUB: 2,
  ParseType.MUL: 2,
  ParseType.DIV: 2,
  ParseType.POW: 2,
  ParseType.NEGATION: 1,
  ParseType.INDEX: 2
}


class ParseTree():

  def __init__(self, node_type=ParseType.FUNCTION, token=None):
    self.node_type = node_type
    self.children = []
    self.token = token

  def print(self, level=0):
    """
      A debug method to print the tree
      """
    # print the left half
    for c in self.children[-1:(len(self.children) // 2) - 1:-1]:
      if not c:
        print((level + 1) * '|  ' + 'NIL')
      elif type(c) == list:
        print((level + 1) * '|  ' + f'{c}')
      else:
        c.print(level + 1)

    # print current node
    indent = level * '|  '
    if self.node_type == ParseType.ATOMIC or\
       self.node_type == ParseType.COMPARABLE or\
       self.node_type == ParseType.CONDITION:
      print(indent + str(self.token.lexeme))
    else:
      print(indent + self.node_type.name + f'({len(self.children)})')

    # print the right half
    for c in self.children[(len(self.children) // 2) - 1::-1]:
      if not c:
        print(indent + '|  NIL')
      elif type(c) == list:
        print(indent + f'|  {c}')
      else:
        c.print(level + 1)

  def insert_left_leaf(self, leaf):
    """
        Insert at the extreme left position
        """
    if ariness[self.node_type] != len(self.children):
      self.children.insert(0, leaf)
      return

    self.children[0].insert_left_leaf(leaf)


class Parser:
  """
    Parser state will follow the lexer state.
    We consume the stream token by token.
    Match our tokens, if no match is possible, 
    print an error and stop parsing.
    """

  def __init__(self, lexer):
    self.__lexer = lexer

  def __next(self):
    """
        Advance the lexer.
        """
    self.__lexer.next()

  def __has(self, t):
    """
        Return true if t matches the current token.
        """
    ct = self.__lexer.get_tok()
    return ct.token == t

  def __must_be(self, t):
    """
        Return true if t matches the current token.
        Otherwise, we print an error message and
        exit.
        """
    if self.__has(t):
      return True

    # print an error
    ct = self.__lexer.get_tok()
    print(
      f"Parser error at line {ct.line}, column {ct.col}.\nReceived token {ct.token.name} expected {t.name}"
    )
    sys.exit(-1)

  def __get_tok(self):
    return self.__lexer.get_tok()

    # print an error
    ct = self.__lexer.get_tok()
    print(
      f"Parser error at line {ct.line}, column {ct.col}.\nReceived token {ct.token.name} expected {ct.name}"
    )
    sys.exit(-1)

  def parse(self):
    self.__next()
    node = ParseTree(ParseType.PROGRAM, None)
    while self.__has(Token.DRAGON):
      node.children.append(self.__function())
    self.__must_be(Token.END)
    return node

  ###########
  # From here on down, everything is calc specific
  ###########

  ##print(self.__lexer.get_tok().token.name)
  # Done
  def __function(self):
    self.__must_be(Token.DRAGON)
    self.__next()
    self.__must_be(Token.ID)
    node = ParseTree(ParseType.FUNCTION, self.__get_tok())
    self.__next()
    param = self.__param_list()
    self.__must_be(Token.FIRE)
    self.__next()
    body = self.__body()
    self.__must_be(Token.EXTINGUISH)
    self.__next()
    node.children.append(param)
    node.children.append(body)
    return node

  #DOne
  def __param_list(self):
    if not self.__has(Token.ID):
      return None
    node = ParseTree(ParseType.PARAMS, self.__get_tok())
    while self.__has(Token.ID):
      node.children.append(ParseTree(ParseType.ATOMIC, self.__get_tok()))
      self.__next()
      if self.__has(Token.COMMA):
        self.__next()
    return node

  #Done
  def __body(self):
    if self.__must_be(Token.LTHANS):
      node = ParseTree(ParseType.BODY, self.__get_tok())
      while self.__has(Token.LTHANS):
        line = self.__line()
        node.children.append(line)
      return node

  #Done
  def __line(self):
    self.__must_be(Token.LTHANS)
    self.__next()
    node = self.__command()
    self.__must_be(Token.GTHANS)
    self.__next()
    return node

  #Done
  def __command(self):
    if self.__has(Token.BIG) or self.__has(Token.SMALL):
      return self.__create_var()
    elif self.__has(Token.BURN):
      return self.__loop()
    elif self.__has(Token.CONSUME):
      return self.__read()
    elif self.__has(Token.SHOOT):
      return self.__write()
    elif self.__has(Token.PATH):
      return self.__path()
    elif self.__has(Token.HATCH):
      return self.__call()
    elif self.__has(Token.RETURN):
      return self.__return()
    else:
      return self.__reassign()

  #Done
  def __return(self):
    self.__must_be(Token.RETURN)
    node = ParseTree(ParseType.RETURN, self.__get_tok())
    self.__next()
    node.children.append(self.__expr())
    return node

  #done
  def __create_var(self):
    if self.__has(Token.SMALL) or self.__must_be(Token.BIG):
      scope = self.__get_tok()
      self.__next()
      self.__must_be(Token.ID)
      idNode = ParseTree(ParseType.ATOMIC, self.__get_tok())
      self.__next()
      if self.__has(Token.LPAREN):
        node = ParseTree(ParseType.CREATEARRAY, scope)
        node.children.append(idNode)
        self.__next()
        node.children.append(self.__expr())
        self.__must_be(Token.RPAREN)
        self.__next()
        self.__must_be(Token.DOLLAR)
        self.__next()
        return node
      else:
        node = ParseTree(ParseType.CREATEVAR, scope)
        node.children.append(idNode)
        if self.__has(Token.ASSIGN):
          self.__next()
          node.children.append(self.__expr())
        else:
          node.children.append(None)
        self.__must_be(Token.DOLLAR)
        self.__next()
        return node

  #Done
  def __reassign(self):
    if self.__must_be(Token.ID):
      node = ParseTree(ParseType.REASSIGN, self.__get_tok())
      node.children.append(self.__ref())
      if self.__has(Token.ASSIGN):
        self.__next()
        node.children.append(self.__expr())
      else:
        node.children.append(None)
      self.__must_be(Token.DOLLAR)
      self.__next()
      return node

  def __write(self):
    self.__must_be(Token.SHOOT)
    node = ParseTree(ParseType.WRITE, self.__get_tok())
    self.__next()
    node.children.append(self.__list())
    self.__must_be(Token.DOLLAR)
    self.__next()
    return node

  #Return list not a tree
  #Done
  def __list(self):
    if not self.__has(Token.ID) and self.__has(Token.STRING) and self.__has(
        Token.NUMBER):
      return None
    node = ParseTree(ParseType.LIST, "People")
    while self.__has(Token.ID) or self.__has(Token.STRING) or self.__has(Token.NUMBER):
      if self.__has(Token.ID):
        node.children.append(self.__ref())
      else:
        node.children.append(ParseTree(ParseType.ATOMIC, self.__get_tok()))
        self.__next()
      if self.__has(Token.COMMA):
        self.__next()
    return node

  #Done
  def __read(self):
    self.__must_be(Token.CONSUME)
    node = ParseTree(ParseType.READ, self.__get_tok())
    self.__next()
    node.children.append(self.__ref())
    self.__must_be(Token.DOLLAR)
    self.__next()
    return node

  #Done
  def __loop(self):
    self.__must_be(Token.BURN)
    node = ParseTree(ParseType.LOOP, self.__get_tok())
    self.__next()
    node.children.append(self.__condition())
    self.__must_be(Token.FIRE)
    self.__next()
    node.children.append(self.__body())
    self.__must_be(Token.EXTINGUISH)
    self.__next()
    return node

  #Done
  def __path(self):
    self.__must_be(Token.PATH)
    node = ParseTree(ParseType.PATH, self.__get_tok())

    self.__next()
    node.children.append(self.__condition())
    self.__must_be(Token.HERE)
    self.__next()
    node.children.append(self.__body())
    self.__must_be(Token.HERE)
    self.__next()
    if self.__has(Token.THERE):
      self.__next()
      node.children.append(self.__body())
      self.__must_be(Token.THERE)
      self.__next()
    else:
      node.children.append(None)
    return node

  #Done
  def __condition(self):
    node = self.__comparable()
    if self.__has(Token.ALSO) or self.__has(Token.EITHER):
      node2 = ParseTree(ParseType.CONDITION, self.__get_tok())
      self.__next()
      node2.children.append(node)
      node2.children.append(self.__condition())
      node = node2
    return node

  #Done
  def __comparable(self):
    left = self.__expr()
    if self.__has(Token.EQ) \
    or self.__has(Token.NOT) \
    or self.__has(Token.LT) \
    or self.__has(Token.LTEQ) \
    or self.__has(Token.GT)\
    or self.__must_be(Token.__GTEQ):
      node = ParseTree(ParseType.COMPARABLE, self.__get_tok())
      self.__next()
    node.children.append(left)
    node.children.append(self.__expr())
    return node

  #Done
  def __expr(self):
    node = self.__term()
    expr2 = self.__expr2()
    if expr2:
      expr2.insert_left_leaf(node)
      node = expr2
    return node

  #Done
  def __expr2(self):
    if self.__has(Token.PLUS):
      node = ParseTree(ParseType.ADD, self.__get_tok())
      self.__next()
      node.children.append(self.__term())
      expr2 = self.__expr2()
      if expr2:
        expr2.insert_left_leaf(node)
        node = expr2
      return node

    elif self.__has(Token.MINUS):
      node = ParseTree(ParseType.SUB, self.__get_tok())
      self.__next()
      node.children.append(self.__term())
      expr2 = self.__expr2()
      if expr2:
        expr2.insert_left_leaf(node)
        node = expr2
      return node

  #Done
  def __term(self):
    node = self.__factor()
    term2 = self.__term2()
    if term2:
      term2.insert_left_leaf(node)
      node = term2
    return node

  #Done
  def __term2(self):
    if self.__has(Token.TIMES):
      node = ParseTree(ParseType.MUL, self.__get_tok())
      self.__next()
      node.children.append(self.__factor())
      expr2 = self.__term2()
      if expr2:
        expr2.insert_left_leaf(node)
        node = expr2
      return node

    #Done
    elif self.__has(Token.DIVIDE):
      node = ParseTree(ParseType.DIV, self.__get_tok())
      self.__next()
      node.children.append(self.__factor())
      expr2 = self.__term2()
      if expr2:
        expr2.insert_left_leaf(node)
        node = expr2
      return node

  #Done
  def __factor(self):
    if self.__has(Token.MINUS):
      node = ParseTree(ParseType.NEGATION, self.__get_tok())
      self.__next()
      node.children.append(self.__exponent())
      f2 = self.__factor2()
      if f2:
        f2.insert_left_leaf(node)
        node = f2
      return node
    else:
      node = self.__exponent()
      f2 = self.__factor2()
      if f2:
        f2.insert_left_leaf(node)
        node = f2
      return node

  #Done
  def __factor2(self):
    if self.__has(Token.POW):
      node = ParseTree(ParseType.POW, self.__get_tok())
      self.__next()
      node.children.append(self.__factor())
      return node
    else:
      return None

  #Done
  def __exponent(self):
    if self.__has(Token.LCURLY):
      self.__next()
      node = self.__expr()
      self.__must_be(Token.RCURLY)
      self.__next()
      return node
    elif self.__has(Token.ID):
      return self.__ref()
    elif self.__has(Token.HATCH):
      return self.__call()
    else:
      return self.__literal()

  #Done
  def __ref(self):
    self.__must_be(Token.ID)
    node = ParseTree(ParseType.ATOMIC, self.__get_tok())
    self.__next()
    if self.__has(Token.LPAREN):
      node2 = ParseTree(ParseType.INDEX, self.__get_tok())
      self.__next()
      node2.children.append(self.__expr())
      if self.__must_be(Token.RPAREN):
        self.__next()
        node2.insert_left_leaf(node)
        node = node2
    return node

  #Done
  def __literal(self):
    if self.__has(Token.NUMBER) or self.__must_be(Token.STRING):
      node = ParseTree(ParseType.ATOMIC, self.__get_tok())
      self.__next()
      return node

  def __call(self):
    self.__must_be(Token.HATCH)
    self.__next()
    self.__must_be(Token.ID)
    node = ParseTree(ParseType.CALL, self.__get_tok())
    self.__next()
    self.__must_be(Token.LBRACKET)
    self.__next()
    if not self.__has(Token.RBRACKET):
      node.children.append(self.__list())
    else:
      node.children.append(None)
    self.__must_be(Token.RBRACKET)
    self.__next()
    return node


if __name__ == "__main__":
  if len(sys.argv) == 2:
    f = open(sys.argv[1])
    l = Lexer(f)
  else:
    l = Lexer()

  p = Parser(l)
  p.parse().print()
