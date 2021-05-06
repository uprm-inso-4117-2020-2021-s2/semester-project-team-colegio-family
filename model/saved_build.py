from config.dbconfig import pg_config
import psycopg2

class SavedBuildDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'],
                                                                  pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def getAllPokemon(self):
        cursor = self.conn.cursor()
        query = "select * from saved_builds;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPokemonById(self, pokemon_id):
        cursor = self.conn.cursor()
        query = "select * from saved_builds where pokemon_id = %s;"

        cursor.execute(query, (pokemon_id,))
        result = cursor.fetchone()
        return result

    def insertPokemon(self, p_id , pokemon_name, pokemon_lvl, pabilities_id):
        cursor = self.conn.cursor()
        query = "insert into saved_builds ( p_id , pokemon_name, pokemon_lvl, pabilities_id) values(%s,%s,%s,%s)returning pokemon_id"
        cursor.execute(query, (p_id , pokemon_name, pokemon_lvl, pabilities_id,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid

    def updatePokemon(self, pokemon_id, p_id , pokemon_name, pokemon_lvl, pabilities_id):
        cursor = self.conn.cursor()
        query = "update saved_builds set p_id=%s, pokemon_name=%s, pokemon_lvl=%s, pabilities_id=%s where pokemon_id=%s;"
        cursor.execute(query, (p_id , pokemon_name, pokemon_lvl, pabilities_id,pokemon_id,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid

    def deletePokemon(self, pokemon_id):
        cursor = self.conn.cursor()
        query = "delete from saved_builds where pokemon_id=%s;"
        cursor.execute(query,(pokemon_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0