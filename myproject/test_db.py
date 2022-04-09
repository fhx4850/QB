import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from QB.database.db import DbApply
from QB.database.db_init import DbInitField, DbApply

class test_tab(DbInitField):
    def __init__(self):
        super().__init__()
        self.IntegerField('test_f', 100)
        self.IntegerField('qqqq', 100, null=True)
        # self.IntegerField('qw', 100)
    

class QB(DbInitField):
    def __init__(self):
        super().__init__()
        self.IntegerField('qb', 200)
        # self.IntegerField('hello', 200)
        # self.IntegerField('Hello_w', 200)
        
test_tab()
QB()

f = DbApply()
f.apply()