"""
Grader file for Columbus problem
"""

def grade(autogen, key):
  if 'cross site request forgery' == key.lower():
    return (True, 'Good work!')
  else:
    return (False, 'Nope')
