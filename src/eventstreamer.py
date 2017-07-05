import collections
from collections import OrderedDict
import json
import jsonschema
from jsonschema import ValidationError, SchemaError
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

    def timeToFloat(self,timeStr):
        return time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M:%S'))

    def parse_line(self,line,event_schema,friend_schema):
        """
        Returns the appropriate tuple for a particular line in the log file
        """
        try:
            jsonschema.validate(json.loads(line),event_schema)
            return json.loads(line,object_hook=lambda x: PurchaseEvent(x["event_type"],self.timeToFloat(x['timestamp']), int(x["id"]), int(float(x["amount"])*100)))

        except Exception as e:
            # TODO - this is ugly ^^ 
            try:
                jsonschema.validate(json.loads(line),friend_schema)
                return json.loads(line,object_hook=lambda x: FriendEvent(x["event_type"],self.timeToFloat(x["timestamp"]),int(x["id1"]),int(x["id2"])))
            except Exception as f:
                print('On this line',line)
                print('E Exception',e)
                print('F Exception',f)
                print("Both file reads failed")
                raise(f)


    def write_line(self,line,result,log_fh):
        #read from original dict.
        dump_dict = json.loads(line)
        #add mean and standard deviation. Format to float
        dump_dict['mean'] = "{:0.2f}".format(result[0])
        dump_dict['sd'] = "{:0.2f}".format(result[1])
        json.dump(OrderedDict([("event_type","purchase"), ("timestamp",dump_dict["timestamp"]),("id",dump_dict["id"]),("amount",dump_dict["amount"]),("mean",dump_dict["mean"]),("sd",dump_dict["sd"])]),log_fh)
        log_fh.write("\n")


    def run(self, T,D,input_fh,event_schema,friend_schema,log_fh=None,dm=None):
        _dm = None
        if(dm == None):
            _dm = DataManager()
        else:
            _dm = dm

        #TODO - Will this speed things up?? : https://stackoverflow.com/questions/5832856/how-to-read-file-n-lines-at-a-time-in-python
        for line in input_fh:
            tup = self.parse_line(line,event_schema,friend_schema)

            if(tup.type == 'purchase'):
                result = _dm.addPurchase(tup.id,tup.timestamp,tup.amount,D,T,make_stats = (log_fh != None))
                if(log_fh != None and result != (0,0)):
                    self.write_line(line,result,log_fh)

                        # write something with log handler

            elif(tup.type == 'befriend'):
                _dm.addFriendship(tup.id1,tup.id2,T)

            elif(tup.type == 'unfriend'):
                _dm.removeFriendship(tup.id1,tup.id2,T)

        return _dm



