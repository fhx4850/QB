import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from QB import settings
from QB.database.db_fields import IntField
import json
from QB.database.db import DB

class DbInitField(IntField):
    def __init__(self):
        self.table_name = self.__class__.__name__
        self.reset_fields()
        
    def __del__(self):
        self.delete_not_committed_fields()

    def IntegerField(self, name, lenght, null=False):
        IntField.__init__(self, self.table_name, name, lenght, null)
        
    def reset_fields(self):
        if os.stat(settings.DBLOGPATH).st_size != 0:
            with open(settings.DBLOGPATH) as db_l:
                json_data = json.load(db_l)
            if self.table_name in json_data.keys():
                for i in json_data[self.table_name][0]['table_field']:
                    i['commit'] = 0
                with open(settings.DBLOGPATH, 'w') as db_l:
                    json.dump(json_data, db_l, indent=4)
                
    def delete_not_committed_fields(self):
            if os.stat(settings.DBLOGPATH).st_size != 0:
                with open(settings.DBLOGPATH) as db_l:
                    json_data = json.load(db_l)
            if self.table_name in json_data.keys():
                for i in json_data[self.table_name]:
                    for x, j in enumerate(i['table_field']):
                        if j['commit'] == 0:             
                            i['table_field'].pop(x)
                with open(settings.DBLOGPATH, 'w') as db_l:
                    json.dump(json_data, db_l, indent=4)
                    
                    
class DbApply(DB):
    def __init__(self):
        super().__init__()
    
    def __del__(self):
        return super().__del__()
    
    # @classmethod
    def apply(self):
        with open(settings.DBLOGPATH) as db_i:
            db_init = json.load(db_i)
            __class__._crate_new_db_table(db_init)
            query = __class__._parse_query()
            self.test_query(db_init)
            for i in query:
                pass
                # self._database_query(i)
      
    @classmethod
    def _crate_new_db_table(self, db_init):            
        create = []
        for i in db_init:
            db_dict = {}
            db_dict['table_name'] = i
            for j in db_init[i]:
                db_dict['table_field'] = j['table_field']
                create.append(db_dict)
            
        with open(settings.DBQUERYPATH, 'w') as q:
            db_query = 'CREATE TABLE '
            for x, i in enumerate(create):
                if x == 0:
                    e = db_query + str(i['table_name'] + '(\nid INTEGER PRIMARY KEY,')
                else:
                    e = '\n\n' + db_query + str(i['table_name'] + '(\nid INTEGER PRIMARY KEY,')                    
                q.write(e)
                for x, j in enumerate(i['table_field']):
                    if j['null']:
                        null = ' NULL'
                    else:
                        null = ' NOT NULL'                        
                    if x == len(i['table_field'])-1:
                        q.write('\n' + str(j['field_name']) + ' ' + str(j['field_type'] + null + ')'))
                    else:
                        q.write('\n' + str(j['field_name']) + ' ' + str(j['field_type']) + null + ',')
    
    
    def test_query(self, db_init):
        create = []
        for i in db_init:
            db_dict = {}
            db_dict['table_name'] = i
            for j in db_init[i]:
                db_dict['table_field'] = j['table_field']
                create.append(db_dict)
                
        for i in create:
            tableInDb = self._search_table_by_name(i['table_name'])
            if tableInDb:
                for j in i['table_field']:
                    if(self._search_table_column(i['table_name'], j['field_name'])):
                        print(f"ALTER TABLE `{i['table_name']}` CHANGE `{j['field_name']}` `{j['field_name']}` {j['field_type']} NULL")
                        # 'ALTER TABLE `test_tab` CHANGE `eee` `eee` VARCHAR(11) NOT NULL;'
                    else:
                        if j['null']:
                            # pass
                            print(f"ALTER TABLE `{i['table_name']}` ADD `{j['field_name']}` {j['field_type']} NULL")
                        else:
                            # pass
                            print(f"ALTER TABLE `{i['table_name']}` ADD `{j['field_name']}` {j['field_type']} NOT NULL")
            
     
    @classmethod
    def _parse_query(self):
        with open(settings.DBQUERYPATH, 'r') as q:
            qr = q.read()
            query = qr.split('\n\n')
        return query