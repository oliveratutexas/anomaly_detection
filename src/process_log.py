
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
    for name,path in paths:
        if( not os.path.isfile(path)):
            #TODO - properly throw an error
            print('Invalid File Path for: {0}'.format(name))
            exit(1)

def get_params(param_string,params_schema_path):
    with open(params_schema_path) as params_schema:
        try:
            # print(type(json.load(params_schema)))
            params_dict = json.loads(params_schema.read().strip())
            # print(params_dict)
            jsonschema.validate(json.loads(param_string),params_dict)
            params_obj = json.loads(param_string,object_hook=lambda x:Params(int(x['D']),int(x['T'])))
            return params_obj
        except ValidationError as ve:
            print(ve)
            print('Invalid parameters, check depth and transaction length')
            exit(1)
        except SchemaError as se:
            print(se)
            print('Invalid schema, check params schema file')
            exit(1)



if __name__=='__main__':
    print(sys.argv)

    # TODO - replace these with proper arguments

    batch_path = sys.argv[1]
    stream_path = sys.argv[2]
    flagged_path = sys.argv[3]

    purchase_schema_path = './src/log_schemas/purchase.schema.json'
    friendaction_schema_path = './src/log_schemas/friendaction.schema.json'
    params_schema_path = './src/log_schemas/params.schema.json'
    #TODO - add multiple with open statements
    paths = [
             ('batch',batch_path),
             ('stream',stream_path),
             ('output',flagged_path),
             ('params_schema',params_schema_path),
             ('friend schema',friendaction_schema_path),
             ('purchase_schema',purchase_schema_path) ]

    check_paths(paths)
    friendact_schema = None
    purchase_schema = None
    params = None

    with open(friendaction_schema_path) as fasf, open(purchase_schema_path) as psf:
        try:
            friendact_schema = json.load(fasf)
            purchase_schema = json.load(psf)
        except:
            #TODO - correct this
            #TODO - test with more args than necessary
            print("\n\nSomethings wrong with schemas\n\n")
            exit(1)

    with open(batch_path) as batch_in:
        params = get_params(batch_in.readline(),params_schema_path)
        es = EventStreamer(params.D, params.T, batch_in,purchase_schema,friendact_schema)
        dm = es.run()

    with open(stream_path) as stream_in, open(flagged_path,'w') as stream_out:
        es = EventStreamer(params.D, params.T, stream_in,purchase_schema,friendact_schema,log_handler=stream_out)
        es.run(dm=dm)

    # with open(flagged_path) as out_log:
    #     EventStreamer(params.D, params.T, out_log)

    # TODO - call fi# les separately
    # with fileinput.input(files=(batch_path,stream_path)) as fused_stream:
    #     event_stream = EventStreamer()
    #     pass




