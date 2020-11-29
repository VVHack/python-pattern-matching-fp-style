import re

class NoMatch:
  def __init__(self):
    pass

class Match:
  patterns = []

  def __init__(self, obj):
    self.obj = obj
    self.val = None

  def get_args(self, pattern):
    for pat_tuple in Match.patterns:
      (obj_type, pat_regex, *handlers) = pat_tuple
      if type(self.obj) is obj_type:
        matches = pat_regex.match(pattern)
        if matches:
          handler_args = {}
          idx = 0
          for group in matches.groups():
            group = group.rstrip()
            value = handlers[idx](self.obj)
            if type(value) is NoMatch:
              matches = False
              break
            if re.match(r'^[0-9]+$', group):
              if value != int(group):
                matches = False
                break
            elif re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', group):
              handler_args[group] = value
            else:
              embedded_args = Match(value).get_args(group)
              if embedded_args == NoMatch():
                matches = False
                break
              handler_args.update(embedded_args)
            idx += 1
          if matches:
            return handler_args
          else:
            return None

  def case(self, pattern, handler):
    if self.val:
      return self
    handler_args = self.get_args(pattern)
    if handler_args:
      self.val = handler(**handler_args)
    return self

def head(l):
  if not len(l):
    return NoMatch()
  return l[0]

def tail(l):
  if len(l) < 2:
    return NoMatch()
  return l[1:]

Match.patterns.append((list, re.compile(r'([a-zA-Z0-9_]*)\s*::\s*(.*)'), head, tail))
Match.patterns.append((list, re.compile(r'([a-zA-Z0-9_]*)'), head))

#Match([1, 2, 3])\
#.case("h :: t", lambda h, t: print(f"The head is {h}, the tail is {t}"))\
#.val
#
#Match([1, 2, 3])\
#.case("h :: h2 :: t", lambda h, h2, t: print(f"The heads are {h} and {h2}, the tail is {t}"))\
#.val
#
#Match([1, 2, 3, 4])\
#.case("h :: h2 :: t", lambda h, h2, t: print(f"The heads are {h} and {h2}, the tail is {t}"))\
#.val
#
#Match([1, 2, 3, 4, 5])\
#.case("1 :: h :: t", lambda h, t: print(f"The heads are 1 and {h}, the tail is {t}"))\
#.val
#
#Match([6, 2, 3, 4, 5, 6, 7])\
#.case("1 :: h :: t", lambda h, t: print(f"The heads are 1 and {h}, the tail is {t}"))\
#.val
#
#Match([6, 2, 3, 4, 5, 6, 7])\
#.case("6 :: h :: t", lambda h, t: print(f"The heads are 6 and {h}, the tail is {t}"))\
#.val
#
#Match([1])\
#.case("h :: t", lambda h, t: print(f"The head is {h}, the tail is {t}"))\
#.val
#
#Match([1])\
#.case("h", lambda h: print(f"The head is {h}"))\
#.val