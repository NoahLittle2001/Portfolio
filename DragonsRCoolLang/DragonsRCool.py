"""
The Calc language interpreter. The semantics of calc are as follows:
    - Math operators: +, -, *, /, **, ^
    - Parenthesis ()
    - All operations follow the usual order of operations.
    - Calc always does floating point arithmetic.
    - input can read a variable from the user.
      input x
      Prompt: "x="
    - Assignment is performed by "="
       x = 2
    - Any statement other than input or an assignment prints the
      result to the screen.
      x=2
      y=1
      x+y     ... print 3
Errors
    - identify context sensitive errors
    - Variables must be assigned before they are read.
"""
from Parser import Parser, ParseType
from Lexer import Token, Lexer
import sys
from enum import Enum, auto
from collections import ChainMap
import numpy as np


class RefType(Enum):
  VARIABLE = auto()
  FUNCTION = auto()


class Ref:
  """
    Reference which is bound to a name.
    """

  def __init__(self, ref_type, ref_value):
    self.ref_type = ref_type
    self.ref_value = ref_value


class RefEnv:

  def __init__(self, parent=None):
    self.tab = ChainMap()
    if parent:
      self.tab = ChainMap(self.tab, parent.tab)
    self.return_value = None

  def lookup(self, name):
    """
        Search for a symbol in the reference environment.
        """
    # try to find the symbol
    if name not in self.tab:
      return None

    return self.tab[name]

  def insert(self, name, ref):
    """
        Insert a symbol into the inner-most reference environment.
        """
    self.tab[name] = ref


def eval_parse_tree(t, env, glob):
  """
    Ealuate the given parse tree.
    """
  #print(t.node_type)
  if t.node_type == ParseType.PROGRAM:
    return eval_program(t, env, glob)
  if t.node_type == ParseType.FUNCTION:
    return eval_function(t, env, glob)
  elif t.node_type == ParseType.PARAMS:
    return eval_params(t, env, glob)
  elif t.node_type == ParseType.INDEX:
    return eval_index(t, env, glob)
  elif t.node_type == ParseType.BODY:
    return eval_body(t, env, glob)
  elif t.node_type == ParseType.ATOMIC:
    return eval_atomic(t, env, glob)
  elif t.node_type == ParseType.READ:
    return eval_read(t, env, glob)
  elif t.node_type == ParseType.WRITE:
    return eval_write(t, env,glob)
  elif t.node_type == ParseType.CREATEVAR:
    return eval_create_var(t, env,glob)
  elif t.node_type == ParseType.CREATEARRAY:
    return eval_create_array(t, env,glob)
  elif t.node_type == ParseType.REASSIGN:
    return eval_reassign(t, env,glob)
  elif t.node_type == ParseType.ADD:
    return eval_add(t, env,glob)
  elif t.node_type == ParseType.SUB:
    return eval_sub(t, env, glob)
  elif t.node_type == ParseType.MUL:
    return eval_mul(t, env, glob)
  elif t.node_type == ParseType.DIV:
    return eval_div(t, env, glob)
  elif t.node_type == ParseType.POW:
    return eval_pow(t, env, glob)
  elif t.node_type == ParseType.NEGATION:
    return eval_negation(t, env, glob)
  elif t.node_type == (ParseType.PATH):
    return eval_path(t, env, glob)
  elif t.node_type == (ParseType.LOOP):
    return eval_loop(t, env, glob)
  elif t.node_type == (ParseType.CONDITION):
    return eval_condition(t, env, glob)
  elif t.node_type == (ParseType.COMPARABLE):
    return eval_comparable(t, env, glob)
  elif t.node_type == ParseType.DEF:
    return eval_def(t, env, glob)
  elif t.node_type == ParseType.CALL:
    return eval_call(t, env, glob)
  elif t.node_type == ParseType.RETURN:
    return eval_return(t, env, glob)


def eval_program(t, env, glob):
  """
    Evaluate the program
  """
  for c in t.children:
    name = c.token.lexeme
    env.insert(name, Ref(RefType.FUNCTION, c))
  fun_result = None
  main = RefEnv(env)
  result = eval_parse_tree(t.children[0], main, env)

  # remember any non-none result
  if result is not None:
    fun_result = result

  # check to see if we have returned
  if env.return_value is not None:
    return env.return_value

  return fun_result


def eval_function(t, env, glob):
  """
    Evaluate the program
  """

  fun_result = None
  if t.children[0] != None:
    eval_parse_tree(t.children[0], env, glob)

  flip = False
  for c in t.children:
    if flip == True:
      result = eval_parse_tree(c, env, glob)
      # remember any non-none result
      if result is not None:
        fun_result = result
      # check to see if we have returned
      if env.return_value is not None:
        return env.return_value
    else:
      flip = True

  return fun_result


def eval_params(t, env, glob):
  pass

def eval_body(t, env, glob):
  """
    Evaluate the program
    """

  fun_result = None
  for c in t.children:
    result = eval_parse_tree(c, env, glob)

    # remember any non-none result
    if result is not None:
      fun_result = result

    # check to see if we have returned
    if env.return_value is not None:
      return env.return_value
  return fun_result


def eval_atomic(t, env, glob):
  """
    Evaluate the atomic value.
    """

  # get literals
  if t.token.token in (Token.NUMBER, Token.STRING):
    return t.token.value

  # get the variable
  v = env.lookup(t.token.lexeme)
  if not v:
    print(f"Undefined variable {t.token.lexeme} on line {t.token.line}")
    sys.exit(-1)
  elif v.ref_type != RefType.VARIABLE:
    print(f"{t.token.lexeme} on line {t.token.line} is not a variable.")
    sys.exit(-1)
  return v.ref_value


def bindSmall(env, name, ref):
  """
    Bind the name in env to ref according to the correct scope
    resolution rules.
    """
  v = env.lookup(env)
  if v:
    # rebind to an existing name
    v.ref_value = ref.ref_value
    v.ref_type = ref.ref_type
  else:
    env.insert(name, ref)


def bindBig(env, name, ref):
  """
    Bind the name in env to ref according to the correct scope
    resolution rules.
    """
  v = env.lookup(env)
  if v:
    # rebind to an existing name
    v.ref_value = ref.ref_value
    v.ref_type = ref.ref_type
  else:
    env.insert(name, ref)


def eval_read(t, env, glob):
  """
    Evaluate an input statement
    """
  global var
  #Catch to see if the item is an array
  if t.children[0].node_type == ParseType.INDEX:
    l = eval_parse_tree(t.children[0].children[0], env, glob)
    value = input("")
    idx = eval_parse_tree(t.children[0].children[1], env, glob)
    try:
      l[idx] = eval(value)
    except:
      l[idx] = value
  else:
    # get the variable we are going to write
    v = t.children[0].token.lexeme
    value = input("")
    try:
        bindSmall(env, v, Ref(RefType.VARIABLE, eval(value)))
        b = True
    except:
      bindSmall(env, v, Ref(RefType.VARIABLE, value))


def eval_write(t, env, glob):
  """
  Evaluate a print statement
  """
  for c in t.children[0].children:
    print(eval_parse_tree(c, env, glob), end=" ")
  print("")


def eval_create_var(t, env, glob):
  """
    Evaluate an assignment statement
  """
  global var
  # get the variable we are going to write
  v = t.children[0].token.lexeme
  # evaluate the expression and assign the result, env
  val = None
  if t.children[1] != None:
    val = eval_parse_tree(t.children[1], env, glob)
  if t.token.lexeme == "small":
    bindSmall(env, v, Ref(RefType.VARIABLE, val))
  elif t.token.lexeme == "big":
    bindBig(glob, v, Ref(RefType.VARIABLE, val))


def eval_create_array(t, env, glob):
  """
    Evaluate an assignment statement
    """
  global var
  # get the variable we are going to write
  v = t.children[0].token.lexeme
  # evaluate the expression and assign the result, env
  size = eval_parse_tree(t.children[1], env, glob)
  l = [None] * size
  a = np.array(l)
  if t.token.lexeme == "small":
    bindSmall(env, v, Ref(RefType.VARIABLE, a))
  elif t.token.lexeme == "big":
    bindBig(glob, v, Ref(RefType.VARIABLE, a))


def eval_reassign(t, env, glob):
  global var

  if t.children[0].node_type == ParseType.INDEX:
    l = eval_parse_tree(t.children[0].children[0], env, glob)
    val = eval_parse_tree(t.children[1], env, glob)
    idx = eval_parse_tree(t.children[0].children[1], env, glob)
    l[idx] = val
  else:
    #Makes sure that the variable is defined before reassigning
    test = eval_parse_tree(t.children[0], env, glob)
    v = t.children[0].token.lexeme
    # evaluate the expression and assign the result, env
    val = eval_parse_tree(t.children[1], env, glob)

    bindSmall(env, v, Ref(RefType.VARIABLE, val))


def eval_index(t, env, glob):
  l = eval_parse_tree(t.children[0], env, glob)
  idx = eval_parse_tree(t.children[1], env, glob)
  return l[idx]


def eval_add(t, env, glob):
  """
    Evaluate an addition operation.
    """
  return eval_parse_tree(t.children[0], env, glob) + eval_parse_tree(
    t.children[1], env, glob)


def eval_sub(t, env,glob):
  """
    Evaluate an subtraction operation.
    """
  return eval_parse_tree(t.children[0], env, glob) - eval_parse_tree(
    t.children[1], env, glob)


def eval_mul(t, env,glob):
  """
    Evaluate an multiplication operation.
    """
  return eval_parse_tree(t.children[0], env,glob) * eval_parse_tree(
    t.children[1], env,glob)


def eval_div(t, env, glob):
  """
    Evaluate an multiplication operation.
    """
  left = eval_parse_tree(t.children[0], env, glob)
  right = eval_parse_tree(t.children[1], env, glob)
  if right == 0:
    print(f"Division by 0 on line {t.token.line}")
    sys.exit(-1)
  return left / right


def eval_pow(t, env, glob):
  """
    Evaluate an exponent operation.
    """
  return eval_parse_tree(t.children[0], env, glob)**eval_parse_tree(t.children[1], env, glob)


def eval_negation(t, env, glob):
  """
    Evaluate a negation
    """
  return -eval_parse_tree(t.children[0], env, glob)


def eval_path(t, env, glob):
  """
    Evaluate a branch
    """
  if eval_parse_tree(t.children[0], env, glob):
    eval_parse_tree(t.children[1], env, glob)
  else:
    if t.children[2] != None:
      eval_parse_tree(t.children[2], env, glob)


def eval_loop(t, env, glob):
  while eval_parse_tree(t.children[0], env, glob):
    eval_parse_tree(t.children[1], env, glob)


def eval_condition(t, env, glob):
  """
    Evaluate a condition
    """
  if t.token.lexeme == "also":
    return eval_parse_tree(t.children[0], env, glob) and eval_parse_tree(
      t.children[1], env, glob)
  elif t.token.lexeme == "either":
    return eval_parse_tree(t.children[0], env, glob) or eval_parse_tree(
      t.children[1], env, glob)
  else:
    return eval_parse_tree(t, env, glob)


def eval_comparable(t, env, glob):
  if t.token.lexeme == "is":
    return eval_parse_tree(t.children[0],
                           env, glob) == eval_parse_tree(t.children[1], env, glob)
  elif t.token.lexeme == "not":
    return eval_parse_tree(t.children[0], env, glob) != eval_parse_tree(
      t.children[1], env, glob)
  elif t.token.lexeme == "eats":
    return eval_parse_tree(t.children[0], env, glob) < eval_parse_tree(
      t.children[1], env, glob)
  elif t.token.lexeme == "eats_more":
    return eval_parse_tree(t.children[0], env, glob) <= eval_parse_tree(
      t.children[1], env, glob)
  elif t.token.lexeme == "spits":
    return eval_parse_tree(t.children[0], env, glob) > eval_parse_tree(
      t.children[1], env, glob)
  elif t.token.lexeme == "spits_more":
    return eval_parse_tree(t.children[0], env, glob) >= eval_parse_tree(
      t.children[1], env, glob)


def eval_def(t, env, glob):
  """
  Define a function
  """

  # functions are always local (by design)
  name = t.token.lexeme
  env.insert(name, Ref(RefType.FUNCTION, t))


def eval_call(t, env, glob):
  """
    Call a function
    """
  name = t.token.lexeme
  arglist = t.children[0]

  # retrieve the function
  fun = env.lookup(name)
  if not fun:
    print(f"Call to undefined function {name} on line {t.token.line}")
    sys.exit(-1)
  elif fun.ref_type != RefType.FUNCTION:
    print(f"Call to non-function {name} on line {t.token.line}")
    sys.exit(-1)
  fun = fun.ref_value

  # Verify that they both have to have none or both have to have a number
  paramlist = fun.children[0]
  if (paramlist == None and arglist != None) or (paramlist != None and arglist == None):
    print(f"Wrong number of parameters to function {name} on line {t.token.line}")
    sys.exit(-1)
  if paramlist != None and arglist != None:
    # verify the parameter list
    if len(arglist.children) != len(paramlist.children):
      print(f"Wrong number of parameters to function {name} on line {t.token.line}")
      sys.exit(-1)
  
  # create the local environment
  local = RefEnv(glob)

  # all parameters are local (by design)
  if paramlist != None and arglist != None:
    for i in range(len(paramlist.children)):
      local.insert(paramlist.children[i].token.lexeme, Ref(RefType.VARIABLE, eval_parse_tree(arglist.children[i], env, glob)))
  
  # call the function
  return eval_parse_tree(fun, local, glob)


def eval_return(t, env, glob):
  """
    Evaluate Return
    """
  env.return_value = eval_parse_tree(t.children[0], env, glob)
  return env.return_value


if __name__ == "__main__":
  if len(sys.argv) == 2:
    f = open(sys.argv[1])
    l = Lexer(f)
  else:
    l = Lexer()
  parser = Parser(l)
  pt = parser.parse()
  eval_parse_tree(pt, RefEnv(), None)
