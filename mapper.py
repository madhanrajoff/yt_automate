import sqlite3


class Mapper:
    def __init__(self):
        self.conn = sqlite3.connect('mapper.db')
        self.cur = self.conn.cursor()

        self.tb_props = {'video': {'name': 'video', 'attr': ['video'], 'len': '255'},
                         'audio': {'name': 'audio', 'attr': ['audio'], 'len': '255'}}

    def commit(self):
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            self.conn.close()

    def execute(self, q, commit=True):
        self.cur.execute(q)
        if not commit:
            return self.cur.fetchall()

        self.commit()

    def create_table(self):
        def gen(table):
            q = f"CREATE TABLE IF NOT EXISTS {self.tb_props[table]['name']} ("
            for inx, attr in enumerate(self.tb_props[table]['attr']):
                q += f"{attr} VARCHAR({self.tb_props[table]['len']}) NOT NULL UNIQUE"
                if inx < len(self.tb_props[table]['attr']) - 1:
                    q += ", "
            q += ");"
            print(q)
            return q

        for tb in self.tb_props.keys():
            q = gen(tb)
            self.execute(q, commit=False)
        self.commit()

    def insert(self, table, value):
        q = f"INSERT INTO {self.tb_props[table]['name']} VALUES ('{value}')"
        self.execute(q)

    def get(self, table, value):
        q = f"SELECT * FROM {self.tb_props[table]['name']} WHERE {table} = '{value}'"
        print('query - ', q)
        exe = self.execute(q, commit=False)
        return exe

    def list(self, table):
        q = f"SELECT * FROM {self.tb_props[table]['name']}"
        exe = self.execute(q, commit=False)
        print(exe)
        return exe

    def delete(self, table, *value):
        q = f"DELETE FROM {self.tb_props[table]['name']} WHERE {table} IN {value};"
        print(q)
        exe = self.execute(q)
        return exe


if __name__ == '__main__':
    mapper = Mapper()

    # mapper.create_table()

    # mapper.delete('video', 'drone-footage-of-ocean-waves-7666608.mp4', 'sea-water-blue-ocean-7513671.mp4')
    # mapper.list('video')

    # mapper.delete('audio', '3 HOURS of GENTLE NIGHT RAIN, Rain Sounds to Sleep, Study, Relax, Reduce Stress, help insomnia.mp3', 'sea-water-blue-ocean-7513671.mp4')
    mapper.list('audio')

