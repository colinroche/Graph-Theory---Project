# Colin Roche - G00349215

# Shunting Yard Algorithm 
# takes in a infix experssion and returns an equivalent postfix expression
# example of string containing infix expression - "(a.b)|(c*.d)"
def shuntAlg(infix):

  operationChar = { '*': 5, '.': 4, '|': 3 }
  postfix, stack =  "", ""
  
  # read in infix expression a char at a time
  for c in infix:
    if c == '(':
      stack = stack + c
    elif c == ')':
      while stack[-1] != '(':
        postfix, stack = postfix + stack[-1], stack[:-1]
      stack = stack[:-1]
    elif c in operationChar:
      while stack and operationChar.get(c,0) <= operationChar.get(stack[-1],0):
        postfix, stack = postfix + stack[-1], stack[:-1]
      stack = stack + c
    else:
      postfix = postfix + c
      
  while stack:
    postfix, stack = postfix + stack[-1], stack[:-1]

  # returns postfix expression
  return postfix

print(shuntAlg("(a.b)|(c*.d)"))