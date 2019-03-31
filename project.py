# Colin Roche - G00349215

### Shunting Yard Algorithm ###
# Takes in a infix experssion and returns an equivalent postfix expression
# Example of string containing infix expression - "(a.b)|(c*.d)"
def shuntAlg(infix):

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
      
  # Add whats left of the stack to the postfix    
  while stack:
    postfix, stack = postfix + stack[-1], stack[:-1]

  return postfix

print(shuntAlg("(a.b)|(c*.d)"))

### Thompson's Construction ###

class state:
  label = None
  edge1 = None
  edge2 = None

class nfa:
  initial = None
  accept = None

  # NFA constructor
  def __init__(self, initial, accept):
    self.initial = initial
    self.accept = accept

def thompsonCompiler(postfix):
  # Contains instances of the NFA class
  nfaStack = []

  for c in postfix:
    if c == '*':
      nfa1 = nfaStack.pop()
      initial = state()
      accept = state()
      initial.edge1 = nfa1.initial
      initial.edge2 = accept
      nfa1.accept.edge1 = nfa.initial
      nfa1.accept.edge2 = accept
      nfaStack.append(nfa(initial, accept))

    elif c == '.':
      nfa2 = nfaStack.pop()
      nfa1 = nfaStack.pop()
      nfa1.accept.edge1 = nfa2.initial
      nfaStack.append(nfa(nfa1.initial, nfa2.accept))
    
    elif c == '|':
      nfa2 = nfaStack.pop()
      nfa1 = nfaStack.pop()
      initial = state()
      accept = state()
      initial.edge1 = nfa1.initial
      initial.edge2 = nfa2.initial
      nfa1.accept.edge1 = accept
      nfa2.accept.edge1 = accept
      nfaStack.append(nfa(initial, accept))
      
    else:
      accept = state()
      initial = state()
      initial.label = c
      initial.edge1 = accept
      nfaStack.append(nfa(initial, accept))
      
  return nfaStack.pop()


print(thompsonCompiler("ab.cd.|"))
print(thompsonCompiler("aa*"))