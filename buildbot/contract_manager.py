'''
The buildbot_contract manager loads and validates a swagger file.
'''
import json
from swagger_spec_validator.validator20 import validate_spec

class buildbot_contract(object):

    def __init__(self, f_swagger):
        self.load_contract(f_swagger)
        self.schemes = self.data["schemes"]
        self.base_path = self.data["basePath"]
        self.paths = self.data["paths"]

    def load_contract(self, f_swagger):
        with open(f_swagger) as FIN:
            raw = FIN.read()
            js  = json.loads(raw)
        
        if validate_spec(js) is None:
            self.data = js
            return True

        msg = "Bad swaggerfile {}".format(f_swagger)
        raise SyntaxError(msg)

    def keys(self):
        return self.paths.keys()
    
class buildbot_action(object):

    def __init__(self,name,data,contracts):
        self.name = name
        self.data = data

        # Identify the [pre] contract
        self.pre_contract = None
        for contract in contracts.values():
            if contract.data["host"] in data["pre"]:
                self.pre_contract = contract

        assert(self.pre_contract is not None)
        
        # Assume for now that the [post] contract is internal
        # (this doesn't have to be true in the future)

        # + Identify the code_entry point

    def activate(self):
        # Run the action and validate against the contract
        print "ACTIVATE!"
        exit()


    

