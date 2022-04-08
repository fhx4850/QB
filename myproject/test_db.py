import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from QQ.db import DbInit, DbApply

class test_tab(DbInit):
    def __init__(self):
        super().__init__()
        self.IntegerField('test_f', 100)
        self.IntegerField('qqqq', 100, null=True)
        self.IntegerField('qw', 100)
    
test_tab()

class QB(DbInit):
    def __init__(self):
        super().__init__()
        self.IntegerField('qb', 200)
        # self.IntegerField('hello', 200)
        # self.IntegerField('Hello_w', 200)
        
QB()

f = DbApply()
f.apply()