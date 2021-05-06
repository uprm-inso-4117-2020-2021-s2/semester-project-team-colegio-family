from config.dbconfig import pg_config
import psycopg2

class movespoolDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'],
                                                                  pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def getmovesbypid(self,p_id):
        cursor = self.conn.cursor()
        query = "select * from moves_pool where p_id = %s;"
        cursor.execute(query,(p_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getmovesbymoveid(self,move_id):
        cursor = self.conn.cursor()
        query = "select * from moves_pool where move_id = %s;"
        cursor.execute(query,(move_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def insertmovepool(self, move_id, p_id):
        cursor = self.conn.cursor()
        query = "insert into moves_pool ( move_id, p_id) values(%s,%s)returning move_id"
        cursor.execute(query, (move_id,p_id,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid


    def deletemove(self, move_id):
        cursor = self.conn.cursor()
        query = "delete from moves_pool where move_id=%s;"
        cursor.execute(query,(move_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0