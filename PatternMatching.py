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
            # Case 1: If the group is a literal
            # TODO: Right now we have support for int literals only, need other types too
            if re.match(r'^[0-9]+$', group):
              # Check if the value is consistent with the literal found
              if value != int(group):
                matches = False
                break
            # Case 2: If the group is a variable
            elif re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', group):
              # The variable would be an argument to the handler
              handler_args[group] = value
            # Case 3: If the group is another pattern that needs to be matched
            else:
              embedded_args = Match(value).get_args(group)
              if embedded_args == NoMatch() or not embedded_args:
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
  if not l or not len(l):
    return NoMatch()
  if len(l) == 1:
    return []
  return l[1:]

def get_head_only(l):
  if len(l) > 1:
    return NoMatch()
  return head(l)

Match.patterns.append((list, re.compile(r'(.*)\s*::\s*(.*)'), head, tail))
Match.patterns.append((list, re.compile(r'(.*)'), get_head_only))
