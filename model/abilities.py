from config.dbconfig import pg_config
import psycopg2

class abilitiesDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'],
                                                                  pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def getabilities(self):
        cursor = self.conn.cursor()
        query = "select * from abilities;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getabilityById(self, pabilities_id):
        cursor = self.conn.cursor()
        query = "select * from abilities where pabilities_id = %s;"

        cursor.execute(query, (pabilities_id,))
        result = cursor.fetchone()
        return result

    def insertability(self, pabilities_name):
        cursor = self.conn.cursor()
        query = "insert into abilities ( pabilities_name) values(%s)returning pabilities_id"
        cursor.execute(query, (pabilities_name,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid


    def deleteAbility(self, pabilities_id):
        cursor = self.conn.cursor()
        query = "delete from abilities where pabilities_id=%s;"
        cursor.execute(query,(pabilities_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0