import unittest
# import User, FriendGraph, EventStreamer
from datamanager import DataManager

class GraphTests(unittest.TestCase):

   def test_add(self):
      graph = DataManager()
      graph.addFriendship(1,2,10)
      graph.addFriendship(1,3,10)

      test_dict = dict()
      test_dict[1] = set([2,3])
      test_dict[2] = set([1])
      test_dict[3] = set([1])
      print(graph)
      self.assertEqual(test_dict,graph.friends)

   def test_remove(self):

      graph = DataManager()
      graph.addFriendship(1,2,10)
      graph.addFriendship(1,3,10)
      graph.removeFriendship(1,2,10)

      test_dict = dict()
      test_dict[1] = set([3])
      test_dict[2] = set([])
      test_dict[3] = set([1])

      self.assertEqual(test_dict,graph.friends)

   @unittest.expectedFailure
   def test_invalid_remove(self):
      graph = DataManager()
      graph.removeFriendship(1,2,10)


   @unittest.expectedFailure
   def test_self_add(self):
      graph = DataManager()
      graph.addFriendship(1,1,10)




if __name__=='__main__':
   unittest.main()
