import itertools
import heapq
import collections
import statistics

Purchase = collections.namedtuple('Purchase','timestamp amount')

class DataManager:
    def __init__(self):
        #TODO - make sure the additions and removals from sets are O(1)
        # maps user->friends
        self.friends = dict()
        # maps user->purchases
        self.purchases = dict()

    def processFriendshipOps(self,operations):
        '''
        Processes multiple additions and removals of friendhips at a time.
        '''
        pass

    def init_user(self,user_id):
        if user_id not in self.friends:
            self.friends[user_id] = set()
            #TODO - change this
            self.purchases[user_id] = collections.deque(maxlen=3)

    def get_neighbor_ids(self,user_id, depth):
        # TODO: turn on ASSERTS
        assert(depth >= 2)
        # Initialize to the depth 1 neighbors
        neighbors = set(self.friends[user_id])
        print('self friends',self.friends)
        print('self',str(self))

        seen = set()

        for cur_depth in range(depth - 1):
            for neighbor in neighbors:
                if neighbor not in seen:
                    cur_neighbors = self.friends[neighbor]
                    seen.add(neighbor)
                    neighbors.union(cur_neighbors)
                
        # user is not their own neighbor
        exclusion = set([user_id])
        print('ALL NEIGHBORS ',neighbors)
        print('ALL NEIGHBORS WITH EXCLUSION',neighbors - exclusion)
        return iter(neighbors - exclusion)

    def get_stats(self,user_id,D,T):
        #TODO -maybe modify this for...individual values being added also so this doesn't have to be calculated every single time.
        neighbors = self.get_neighbor_ids(user_id,D)
        purchase_lists = [ iter(self.purchases[user_id]) for user_id in neighbors]
        print('PURCHASE LISTS',purchase_lists)
        # Returns a dummy value that's the same as a no-op.
        #TODO - check whether you need to reverse based on the value of the floats here
        #TODO - replace the key function with a generator
        sorted_purchase_it = heapq.merge(*purchase_lists)
        # print('MERGED LISTS: ', [x for x in sorted_purchase_it])
        #TODO - check if this is unnecessary
        nums = itertools.islice(
            (purch.amount for purch in sorted_purchase_it),
            T)
        #TODO - check nums_dup
        nums,nums_dup = itertools.tee(nums)
        nums,nums_length = itertools.tee(nums)


        bee = [x for x in nums_length]
        print('T',T)
        print('THIS IS BEE',bee)

        # Dummy value for no length list
        if len(bee) < 2:
            return (0,0)

        stdev = statistics.stdev(itertools.islice(nums,T))
        mean = statistics.mean(nums_dup)
        print('stdev, mean',stdev, mean)
        #TODO - add rounding documentation to readme
        return (round(stdev/100.0,2),round(mean/100.0,2))

    def addPurchase(self,userID,timestamp,amount,D=None,T=None,make_stats=False):
        self.init_user(userID)
        self.purchases[userID].appendleft(Purchase(timestamp,amount))
        # {"event_type":"purchase", "timestamp":"2017-06-13 11:33:02", "id": "2", "amount": "1601.83", "mean": "29.10", "sd": "21.46"}

        if(make_stats):

            stats = self.get_stats(userID,D,T)
            if stats == (0,0):
                return None
            dev_bound = stats[1] + 3 * stats[0]
            print(self)
            print(stats)
            print(dev_bound)
            print(userID)
            if(dev_bound < amount):
                return stats

        return None

    def addFriendship(self, user1_id,user2_id):
        self.init_user(user1_id)
        self.init_user(user2_id)

        self.friends[user1_id].add(user2_id)
        self.friends[user2_id].add(user1_id)

    def removeFriendship(self,user1_id,user2_id):
        self.init_user(user1_id)
        self.init_user(user2_id)
        #TODO - what should I do if they remove friends that aren't in the table?
        self.friends[user1_id].remove(user2_id)
        self.friends[user2_id].remove(user1_id)

    def __str__(self):
        toString = []
        toString.append( "Friends:\n")
        toString.append( "\n".join(("{0} : {1}".format(uid,self.friends[uid]) for uid in self.friends)))
        toString.append( "\nPurchases:\n")
        toString.append( "\n".join(("{0} : {1}".format(uid,self.purchases[uid]) for uid in self.purchases)))
        return ''.join(toString)
