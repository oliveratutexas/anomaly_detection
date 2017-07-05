import itertools
import heapq
import collections
import statistics
import datetime

Purchase = collections.namedtuple('Purchase','timestamp streak amount')

class DataManager:
    def __init__(self):
        # maps user->friends
        self.friends = dict()
        # maps user->purchases
        self.purchases = dict()
        self.last_time_stamp = None
        self.streak = None

    def init_user(self,user_id,T):
        if user_id not in self.friends:
            self.friends[user_id] = set()
            self.purchases[user_id] = collections.deque(maxlen=T)

    def get_neighbor_ids(self,user_id, depth):
        assert(depth >= 1)

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
        neighbors = self.get_neighbor_ids(user_id,D)
        purchase_lists = [ iter(self.purchases[user_id]) for user_id in neighbors]
        print('PURCHASE LISTS',purchase_lists)
        # Returns a dummy value that's the same as a no-op.
        #TODO - check whether you need to reverse based on the value of the floats here
        sorted_purchase_it = heapq.merge(*purchase_lists)
        nums = itertools.islice(
            (purch.amount for purch in sorted_purchase_it),
            T)
        nums,nums_dup = itertools.tee(nums)
        nums,nums_length = itertools.tee(nums)


        exhausted_nums= [x for x in nums_length]

        # Dummy value for no length list
        if len(exhausted_nums) < 2:
            return (0,0)

        stdev = statistics.pstdev(itertools.islice(nums,T))
        mean = statistics.mean(nums_dup)

        return (round(mean/100.0,2),round(stdev/100.0,2))

    def addPurchase(self,userID,timestamp,amount,D,T,make_stats=False):
        self.init_user(userID,T)
        if(self.last_time_stamp != timestamp):
            #print(datetime.datetime.now())
            self.last_time_stamp = timestamp
            self.streak = 0
        else:
            #print(datetime.datetime.now())
            self.streak += 1
        self.purchases[userID].appendleft(Purchase(timestamp,self.streak,amount))

        if(make_stats):

            stats = self.get_stats(userID,D,T)
            if stats == (0,0):
                return None
            dev_bound = stats[0] + 3 * stats[1]
            print(self)
            print(stats)
            print(dev_bound)
            print(userID)
            if(dev_bound < amount):
                return stats

        return None

    def addFriendship(self, user1_id,user2_id,T):
        if(user1_id == user2_id):
            raise ValueError("User should not befriend self")
        self.init_user(user1_id,T)
        self.init_user(user2_id,T)

        self.friends[user1_id].add(user2_id)
        self.friends[user2_id].add(user1_id)

    def removeFriendship(self,user1_id,user2_id,T):
        if(user2_id not in self.friends[user1_id] or \
           user1_id not in self.friends[user2_id]):
            raise ValueError("Removing non-existant friendship")

        self.init_user(user1_id,T)
        self.init_user(user2_id,T)
        
        self.friends[user1_id].remove(user2_id)
        self.friends[user2_id].remove(user1_id)

    def __str__(self):
        toString = []
        toString.append( "Friends:\n")
        toString.append( "\n".join(("{0} : {1}".format(uid,self.friends[uid]) for uid in self.friends)))
        toString.append( "\nPurchases:\n")
        toString.append( "\n".join(("{0} : {1}".format(uid,self.purchases[uid]) for uid in self.purchases)))
        return ''.join(toString)
