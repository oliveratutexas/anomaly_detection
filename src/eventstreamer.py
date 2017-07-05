import collections
import json
import jsonschema
import time
from datamanager import DataManager

PurchaseEvent = collections.namedtuple('PurchaseEvent','type timestamp id amount')
FriendEvent = collections.namedtuple('FriendEvent','type timestamp id1 id2')

#TODO - Add pyvenv to this environment
class EventStreamer:
    '''
    Handles
      * Pulling information from streams
      * Writing information to streams
      * Formatting input from streams

    '''
    def __init__(self,Depth,Tlength,input_handler,event_schema,friend_schema,log_handler=None):
        # TODO - formatting
        self.D = Depth
        self.T = Tlength
        self.input_handler = input_handler
        self.log_handler = log_handler
        self.event_schema = event_schema
        self.friend_schema = friend_schema

    def timeToFloat(self,timeStr):
        return time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M:%S'))

    def parse_line(self,line):
        #TODO - replae json.loads with the proper object
        try:
            jsonschema.validate(json.loads(line),self.event_schema)
            # TODO - convert timestamp
            return json.loads(line,object_hook=lambda x: PurchaseEvent(x["event_type"],self.timeToFloat(x['timestamp']), int(x["id"]), int(float(x["amount"])*100)))

        except Exception as e:
            # TODO - this is ugly ^^ 
            try:
                jsonschema.validate(json.loads(line),self.friend_schema)
                return json.loads(line,object_hook=lambda x: FriendEvent(x["event_type"],self.timeToFloat(x["timestamp"]),int(x["id1"]),int(x["id2"])))
            except Exception as f:
                print('On this line',line)
                print('E Exception',e)
                print('F Exception',f)
                print("Both file reads failed")
                exit(1)



    def run(self, dm=None):
        #TODO - ugly parameter
        if(dm == None):
            dm = DataManager()
        
         
        #TODO - Is file termination the only valid ending?
        #TODO - add key to merge sort
        #TODO - replace heapsort with iterator merge
        #TODO - Will this speed things up?? : https://stackoverflow.com/questions/5832856/how-to-read-file-n-lines-at-a-time-in-python
        for line in self.input_handler:
            print(line)
            tup = self.parse_line(line)
            if(tup.type == 'purchase'):
                result = dm.addPurchase(tup.id,tup.timestamp,tup.amount,make_stats = (self.log_handler != None),D=self.D, T=self.T)
                if(self.log_handler != None):
                    print('GETS HERE')
                    print(result)
                    if(result):

                        dump_dict = json.loads(line)
                        dump_dict['mean'] = str(result[0])
                        dump_dict['sd'] = str(result[1])
                        json.dump(dump_dict,self.log_handler)

                        # write something with log handler

            elif(tup.type == 'befriend'):
                dm.addFriendship(tup.id1,tup.id2)

            elif(tup.type == 'unfriend'):
                dm.removeFriendship(tup.id1,tup.id2)

        return dm



