from QB.database.db import DB

class IntField(DB):
    def __init__(self, table_name, field_name, lenght, null=False):
        # super().__init__()
        self.table_name = table_name
        self.field_name = field_name
        self.type = 'INTEGER'
        self.lenght = lenght
        self.null = null
        self._create_json_table(self.table_name, self.field_name, self.type, self.lenght, self.null)