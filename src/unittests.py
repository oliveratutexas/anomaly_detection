import unittest
# import User, FriendGraph, EventStreamer
from AnomalyChecker import FriendGraph, User, EventStreamer

class StressTests(unittest.TestCase):
   def test_large_users(self):
      pass
   def test_large_friend_actions(self):
      pass
   def test_large_transactions(self):
      pass

class GraphTests(unittest.TestCase):

   def test_add(self):
      graph = FriendGraph()
      graph.addFriendship(1,2)
      graph.addFriendship(1,3)

      test_dict = dict()
      test_dict[1] = set([2,3])
      test_dict[2] = set([1])
      test_dict[3] = set([1])
      print(graph)
      self.assertEqual(test_dict,graph.users)

   def test_remove(self):

      graph = FriendGraph()
      graph.addFriendship(1,2)
      graph.addFriendship(1,3)
      graph.removeFriendship(1,2)

      test_dict = dict()
      test_dict[1] = set([3])
      test_dict[2] = set([])
      test_dict[3] = set([1])

      self.assertEqual(test_dict,graph.users)

   def test_invalid_remove(self):
      pass

   def test_invalid_add(self):
      pass

if __name__=='__main__':
   unittest.main()
