import re
from PatternMatching import Match

def remove_all_ones(arr):
  if arr == []:
    return []
  return Match(arr)\
    .case("1 :: rest",
          lambda rest: remove_all_ones(rest))\
    .case("h :: rest",
          lambda h, rest: [h] + remove_all_ones(rest))\
    .case("last",
          lambda last: [last])\
    .val

print(remove_all_ones([1,2,1,2,3,11,13,1,6])) # Prints: [2, 2, 3, 11, 13, 6]

class Pair:
  def __init__(self, first, second):
    self.first = first
    self.second = second
  def __str__(self):
    return f"Pair({self.first}, {self.second})"

Match.patterns.append((Pair, re.compile(r'Pair\((.*),(.*)\)'), lambda pr: pr.first, lambda pr: pr.second))

p = Pair(3, 5)
Match(p)\
  .case("Pair(first,second)",
        lambda first, second: print(f"The first is {first} and the second is {second}"))
# Prints: The first is 3 and the second is 5

arr = [Pair(3, 5), Pair(8, 9), Pair(4, 2), Pair(9, 0), Pair(1, 3), Pair(6, 9)]

def pr_array(arr):
  return str([str(pr) for pr in arr])

def all_pairs_with_nines(arr, result=[]):
  if arr == []:
    return result
  return Match(arr)\
    .case("Pair(9,s) :: rest",
          lambda s, rest: all_pairs_with_nines(rest, result + [Pair(9, s)]))\
    .case("Pair(f,9) :: rest",
          lambda f, rest: all_pairs_with_nines(rest, result + [Pair(f, 9)]))\
    .case("h :: rest",
          lambda h, rest: all_pairs_with_nines(rest, result))\
    .val
print(pr_array(all_pairs_with_nines(arr)))
# Prints: ['Pair(8, 9)', 'Pair(9, 0)', 'Pair(6, 9)']

