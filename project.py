# Colin Roche - G00349215

### Shunting Yard Algorithm ###
# Takes in a infix experssion and returns an equivalent postfix expression
# Example of string containing infix expression - "(a.b)|(c*.d)"
def shuntAlg(infix):
  """Shunting Vard Algorithm that converts infix expressions to postfix 
    expressions."""

  operationChar = { '*': 5, '.': 4, '|': 3 }
  postfix, stack =  "", ""
  
  # Read in infix expression a char at a time
  for c in infix:
    if c == '(':
      stack = stack + c
    elif c == ')':
      while stack[-1] != '(':
        # Add end of stack to postfix and remove from stack until '(' is found
        postfix, stack = postfix + stack[-1], stack[:-1]
      # Removing '(' from stack
      stack = stack[:-1]
    elif c in operationChar:
      # While operationChar from infix <= last operationChar on stack
      while stack and operationChar.get(c,0) <= operationChar.get(stack[-1],0):
        postfix, stack = postfix + stack[-1], stack[:-1]
      stack = stack + c
    # Is normal char, added to the postfix
    else:
      postfix = postfix + c
      
  # Pop all chars of stack to output    
  while stack:
    postfix, stack = postfix + stack[-1], stack[:-1]

  return postfix

class state:
  label, edge1, edge2 = None, None, None

class nfa:
  initial, accept = None, None

  # NFA constructor
  def __init__(self, initial, accept):
    self.initial, self.accept = initial, accept

### Thompson's Construction ###

def thompsonCompiler(postfix):
  """Compiler for compile a postfix expression to an NFA"""
  
  # Contains instances of the NFA class
  nfaStack = []

  for c in postfix:
    if c == '*':
      # Pop 1 NFA off of nfaStack
      nfa1 = nfaStack.pop()
      # Create new accept and initail states
      initial, accept = state(), state()
      # Join new initial state to the NFA's initial state and the new accpet state
      initial.edge1, initial.edge2 = nfa1.initial, accept
      # Join old accept state to new accept state and NFA's initial state
      nfa1.accept.edge1, nfa1.accept.edge2 = nfa1.initial, accept
      # Add new NFA containing these states to the nfaStack
      nfaStack.append(nfa(initial, accept))

    elif c == '.':
      # Pop 2 NFA's off of nfaStack
      nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
      # Join NFA's, first accept to second initial
      nfa1.accept.edge1 = nfa2.initial
      # Add new NFA containing these states to the nfaStack
      nfaStack.append(nfa(nfa1.initial, nfa2.accept))
    
    elif c == '|':
      # Pop 2 NFA's off of nfaStack
      nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
      # Create new accept and initial states
      initial, accept = state(), state()
      # Join initial state to initial states of NFA's on stack
      initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial
      # Joining the accept states of the NFA's popped from stack to new accept state
      nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept
      # Add new NFA containing these states to the nfaStack
      nfaStack.append(nfa(initial, accept))
      
    ## Normal char
    else:
      # Create new accept and initail states
      accept, initial = state(), state()
      # Join the initial and accept states using an arrow labelled c
      initial.label, initial.edge1 = c, accept
      # Add new NFA containing these states to the nfaStack
      nfaStack.append(nfa(initial, accept))
      
  return nfaStack.pop()

def follow(state):
  """Return the set of states that can be reached from state following e arrows"""
  
  # Create a set, add state as only member
  states = set()
  states.add(state)

  # Check if state has an arrow labelled empty(e) from it
  if state.label is None:
    # Check if edge1 has a state
    if state.edge1 is not None:
      # Follow edge1
      states |= follow(state.edge1)
    # Check if edge2 has a state
    if state.edge2 is not None:
      # Follow edge2
      states |= follow(state.edge2)
  
  # Return set
  return states

### Regular Expression Matcher ###

def matchStr(infix, string):
  """Matchs string to expression string (infix)"""

  # Call instance of Shunting's Algorithm  
  # Changes an infix expression to a postfix expression
  postfix = shuntAlg(infix)

  # Call instance of Thompson's Algorithm 
  # Compiles postfix expression to an nfa
  nfa = thompsonCompiler(postfix)

  # Create new Sets for current and next state
  currentSet, nextSet = set(), set()
  # Add NFA's initial state to the current set
  currentSet |= follow(nfa.initial)

  # Loop through char of string
  for s in string:
    # Loop through state of current set
    for c in currentSet:
      # Check is the state is labelled s
      if c.label == s:
        # Add the state of edge1 to next set
        nextSet |= follow(c.edge1)
    # Set current set to next set
    currentSet = nextSet
    # Set next set to new set, empty
    nextSet = set()
  
  # Check if accept state is in current set
  return (nfa.accept in currentSet)  

# Test
infixStrings = ["a.b.c*", "a.(b|d).c*", "(a.(b|d))*", "a.(b.b)*.c"]
strings = ["", "abc", "abbc", "abcc", "abad", "abbbc"]

# Loop through string of list
for i in infixStrings:
  # Loop through string of list
  for s in strings:
    print(matchStr(i, s), i, s)
