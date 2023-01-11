import sqlite3

from os import listdir, getcwd, remove


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

    def insert(self, table, value, commit=True):
        q = f"INSERT INTO {self.tb_props[table]['name']} VALUES ('{value}')"
        self.execute(q, commit=commit)

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
        search_criteria = f'IN {value}' if len(value) > 1 else f"= ('{value[0]}')"
        q = f"DELETE FROM {self.tb_props[table]['name']} WHERE {table} {search_criteria};"
        print(q)
        exe = self.execute(q)
        return exe

    @staticmethod
    def delete_file(f_path, is_dir=False):
        if is_dir:
            l_dir = listdir(f_path)
            # print(l_dir)
            for f in l_dir:
                try:
                    remove(f'{f_path}/{f}')
                    print("% s removed successfully" % f_path)
                except OSError as error:
                    print(error)
                    print("File path can not be removed")
        else:
            try:
                remove(f'{f_path}/{f}')
                print("% s removed successfully" % f_path)
            except OSError as error:
                print(error)
                print("File path can not be removed")

    def insert_files(self, table, dir_name):  # provide the dir name which is the root folder contains files
        path = f'{getcwd()}/{dir_name}'
        l_dir = listdir(path)
        for f in l_dir:
            if f[0] != 'l':
                try:
                    self.insert(table, f, commit=False)
                except sqlite3.IntegrityError:
                    pass
        self.commit()


if __name__ == '__main__':
    mapper = Mapper()

    # mapper.create_table()
    # mapper.list('video')
    # mapper.insert_files('audio', 'aud')
    # mapper.insert_files('video', 'vid')

    mapper.delete('video', 'l-a-woman-meditating-8391363.mp4')
