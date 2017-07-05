
import sys
import os.path
import jsonschema
from jsonschema import ValidationError,SchemaError
import collections
import fileinput
import json
import itertools
import heapq

from eventstreamer import EventStreamer
from datamanager import DataManager

Params = collections.namedtuple('Params','D T')

def check_paths(paths):
    '''
    '''
    for name,path in paths:
        if( not os.path.isfile(path)):
            #TODO - properly throw an error
            print('Invalid File Path for: {0}'.format(name))
            exit(1)

def get_params(param_string,params_schema_path):
    params_schema = load_schema(params_schema_path)
    try:
        jsonschema.validate(json.loads(param_string),params_schema)
        params_obj = json.loads(param_string,object_hook=lambda x:Params(int(x['D']),int(x['T'])))
        return params_obj
    except ValidationError as ve:
        print('Invalid parameters, check depth and transaction length')
        raise(ve)

def load_schema(file_path):
    with open(file_path) as fp:
        try:
            return json.load(fp)
        except ValidationError as e:
            #TODO - correct this
            print("\n\nError parsing purchase and friend schemas\n\n")
            raise(e)




if __name__=='__main__':
    print(sys.argv)


    batch_path = sys.argv[1]
    stream_path = sys.argv[2]
    flagged_path = sys.argv[3]

    # paths to json schemas for validation
    purchase_schema_path = './src/log_schemas/purchase.schema.json'
    friendaction_schema_path = './src/log_schemas/friendaction.schema.json'
    params_schema_path = './src/log_schemas/params.schema.json'

    paths = [
             ('batch',batch_path),
             ('stream',stream_path),
             # ('output',flagged_path),
             ('params_schema',params_schema_path),
             ('friend schema',friendaction_schema_path),
             ('purchase_schema',purchase_schema_path) ]

    check_paths(paths)
    friendact_schema = load_schema(friendaction_schema_path)
    purchase_schema = load_schema(purchase_schema_path)
    params = None

    es = EventStreamer()
    # Read in batch files
    with open(batch_path) as batch_in:
        #read params from first line of batch file
        params = get_params(batch_in.readline(),params_schema_path)
        # capture the state from batch processing
        dm = es.run(params.T,params.D,batch_in,purchase_schema,friendact_schema)

    with open(stream_path) as stream_in, open(flagged_path,'w+') as stream_out:
        # enable file output
        # ...with old state

        es.run(params.T,params.D,stream_in,purchase_schema,friendact_schema,log_fh=stream_out,dm=dm)





