import pymysql
from DBUtils.PooledDB import PooledDB
from collections import namedtuple
from datetime import datetime


class Singleton(object):
    _instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if Singleton._instance is None:
            Singleton._instance = super(Singleton, cls).__new__(cls)
        return Singleton._instance


class MysqlManager(Singleton):
    pool = None

    def __init__(self, host="localhost", port=3306, user="root", password="123456", db="mysql", charset="utf8",
                 max_overflow=10):
        MysqlManager.pool = PooledDB(creator=pymysql, maxconnections=max_overflow, host=host, port=port, user=user,
                                     password=password,
                                     db=db, charset=charset, cursorclass=pymysql.cursors.DictCursor)

    @classmethod
    def execute(cls, sql):
        conn = cls.pool.connection()
        cur = conn.cursor()

        try:
            row_num = cur.execute(sql)
            conn.commit()
            records = cur.fetchall()
            if records:
                fields = [filed[0] for filed in cur.description]
                Record = namedtuple("Record", fields)
                for record in records:
                    yield Record(**record)

        except Exception as e:
            conn.rollback()
            raise RuntimeError("sql[{0}]执行出错:{1}".format(sql, str(e)))
        finally:
            conn.close()
            cur.close()

    @classmethod
    def insert(cls, table, **kwargs):
        keys = []
        values = []
        for key, value in kwargs.items():
            keys.append(key)
            values.append("'{0}'".format(value) if type(value) not in [int, float] else str(value))
        sql = "insert into {0}({1}) values({2})".format(table, ",".join(keys), ",".join(values))

        conn = cls.pool.connection()
        cur = conn.cursor()
        rows = 0

        try:
            rows = cur.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise RuntimeError("sql[{0}]执行出错:{1}".format(sql, str(e)))
        finally:
            conn.close()
            cur.close()
        return rows

    @classmethod
    def select(cls, table, conditions=None, order_by=None, limit=None):
        sql = "select * from {table}".format(table=table)

        if conditions:
            sql = "{query} where {conditions}".format(query=sql, conditions=conditions)

        if order_by:
            order_by = order_by if order_by[0] != "-" else "{0} desc".format(order_by[1:])
            sql = "{query} order by {order_by}".format(query=sql, order_by=order_by)

        if limit:
            sql = "{query} limit {num}".format(query=sql, num=limit)

        return cls.execute(sql)

    @classmethod
    def count(cls, table, conditions=None):
        sql = "select count(1) as nums from {table}".format(table=table)
        if conditions:
            sql = "{query} where {conditions}".format(query=sql, conditions=conditions)
        result = cls.execute(sql)
        for r in result:
            return r.nums
        return 0

    @classmethod
    def exist(cls, table, conditions):
        sql = "select 1 as is_exist from {table} where {conditions} limit 1".format(table=table, conditions=conditions)
        result = list(cls.execute(sql))
        if result:
            return True
        else:
            return False

if __name__ == "__main__":
    # mysqldb = MysqlManager(host="localhost")
    # print(mysqldb.exist("student", conditions="name='ouru'"))
    # mysqldb.insert("student", name="ouru", age=30, add_time=datetime.now())
    from guessDiceUtils import result_prediction
    mysqlConfig = {
        "host": "193.112.150.18",
        "port": 3306,
        "user": "ouru",
        "password": "5201314Ouru...",
        "db": "novel",
        "charset": "utf8",
        "max_overflow": 10,
    }
    mysqldb = MysqlManager(**mysqlConfig)
    history_records = list(mysqldb.select("tb_guess_dice", order_by="-period", limit=3))
    prediction = result_prediction(history_records)
    print(prediction)
