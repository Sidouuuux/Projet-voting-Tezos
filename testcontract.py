# run this test (from tests directory):
# pytest pytest_template.py
# run all tests (from project directory):
# pytest tests


from os.path import dirname, join
from unittest import TestCase
from pytezos import ContractInterface, MichelsonRuntimeError

wallet1     = "tz1dFibFVfuWLBVJHSGrneVFKimuJauc5rEV"
wallet2     = "tz1ajkFrcXfHAXJm8yK8s7mamwth9u4ajzjw"
wallet3     = "tz1VtUMXUwuAfN4euuGg6YC23QT5WDk94M74"
wallet4     = "tz1fPexY96eBrdzXySYzyqq6vM2ZpN5e4q2g"
wallet5     = "tz1LuiwRnA63anqr6ot86xJR3VK86qJxURDj"
wallet6     = "tz1gzyiEoqCCoNjUpmJA1Z21cSf1VzS61E89"
wallet7     = "tz1fssLLW3K822LGaH219oF9ZF8FW8izZXRH"
wallet8     = "tz1fDYG7TcBXBMRfoB5QEtXqF1YunSo17aeo"
wallet9     = "tz1iWiN1hqFHEJEGW4gunUW6o2t1SC8sJoKT"
wallet10    = "tz1PJSVnbr8ztVSrT2NuBEmGubnYKcxk3zie"

admin       = "tz1LKe9GQfF4wfob11YjH9grP1YdEWZtPe9W"

class TestCounterContractTest(TestCase):

    @classmethod
    def setUpClass(cls):
        project_dir = dirname(dirname(__file__))
        cls.mycontract = ContractInterface.create_from(join(project_dir, '/home/ubuntu/sid-ahmed/voting_contract.tz'))

    def test_verify_voteno_admin(self):

            self.mycontract.no(False).result(
                storage = {
                "balanceofvotes":  { wallet10: True },
                "owner": admin,
                "contractPause":False,
                "yesVotes": 0,
                "noVotes": 1
                },
                source = admin
            )
        
    def test_verify_voteyes_admin(self):

            self.mycontract.yes(False).result(
                storage = {
                "balanceofvotes":  { wallet10: True },
                "owner": admin,
                "contractPause":False,
                "yesVotes": 0,
                "noVotes": 1
                },
                source = admin
            )
    
    def test_verify_voteno_noadmin(self):

            result = self.mycontract.no(False).result(
                storage = {
                "balanceofvotes":  {  },
                "owner": admin,
                "contractPause":False,
                "yesVotes": 0,
                "noVotes": 0
                },
                source = wallet4
            )
            self.assertEqual(1, result.storage["noVotes"])
    
    def test_verify_voteyes_noadmin(self):

        result = self.mycontract.yes(False).result(
            storage = {
            "balanceofvotes":  {  },
            "owner": admin,
            "contractPause":False,
            "yesVotes": 0,
            "noVotes": 0
            },
            source = wallet4
        )
        self.assertEqual(1, result.storage["yesVotes"])
    
    def test_verify_voteyes_paused(self):

        self.mycontract.yes(False).result(
            storage = {
            "balanceofvotes":  {  },
            "owner": admin,
            "contractPause":True,
            "yesVotes": 0,
            "noVotes": 0
            },
            source = wallet4
        )
    
    def test_verify_voteno_paused(self):

            self.mycontract.no(False).result(
                storage = {
                "balanceofvotes":  {  },
                "owner": admin,
                "contractPause":True,
                "yesVotes": 0,
                "noVotes": 0
                },
                source = wallet4
            )
    
    def test_verify_voteno_double(self):

            result = self.mycontract.no(False).result(
                storage = {
                "balanceofvotes":  { wallet4 : True },
                "owner": admin,
                "contractPause":False,
                "yesVotes": 0,
                "noVotes": 0
                },
                source = wallet4
            )

    def test_verify_voteyes_double(self):

            result = self.mycontract.yes(False).result(
                storage = {
                "balanceofvotes":  { wallet4 : True },
                "owner": admin,
                "contractPause":False,
                "yesVotes": 0,
                "noVotes": 0
                },
                source = wallet4
            )
    
    def test_verify_reset_admin(self):

            result = self.mycontract.reset(None).result(
                storage = {
                "balanceofvotes":  { wallet4 : True },
                "owner": admin,
                "contractPause":True,
                "yesVotes": 1,
                "noVotes": 0
                },
                source = admin
            )
            self.assertEqual({}, result.storage["balanceofvotes"])
            self.assertEqual(False, result.storage["contractPause"])
    
    def test_verify_reset_noadmin(self):

            self.mycontract.reset(None).result(
                storage = {
                "balanceofvotes":  { wallet4 : True },
                "owner": admin,
                "contractPause":True,
                "yesVotes": 1,
                "noVotes": 0
                },
                source = wallet2
            )
    
    def test_verify_pasued_10votes(self):

        result = self.mycontract.no(False).result(
            storage = {
            "balanceofvotes":  { wallet10: True },
            "owner": admin,
            "contractPause":False,
            "yesVotes": 0,
            "noVotes": 9
            },
            source = wallet4
        )
        self.assertEqual(True, result.storage["contractPause"])