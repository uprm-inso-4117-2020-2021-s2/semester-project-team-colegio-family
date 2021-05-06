from config.dbconfig import pg_config
import psycopg2

class BasePokemonDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'],
                                                                  pg_config['password'], pg_config['dbport'], pg_config['host'])
        print("conection url:  ", connection_url)
        self.conn = psycopg2.connect(connection_url)

    def getAllPokemon(self):
        cursor = self.conn.cursor()
        query = "select * from base_pokemon;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPokemonById(self, pid):
        cursor = self.conn.cursor()
        query = "select * from base_pokemon where p_id = %s;"
        cursor.execute(query, (pid,))
        result = cursor.fetchone()
        return result

    def insertPokemon(self, p_id, p_name, p_type1, p_type2, base_hp, base_atk , base_def , base_spatk , base_spdef , base_spd):
        cursor = self.conn.cursor()
        query = "insert into base_pokemon (p_id, p_name, ptype1, ptype2, base_hp, base_atk,base_def, base_spatk,base_spdef,base_spd) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)returning p_id"

        cursor.execute(query, (p_id, p_name, p_type1, p_type2, base_hp, base_atk , base_def , base_spatk , base_spdef , base_spd,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid

    def updatePokemon(self, p_id, p_name, p_type1, p_type2, base_hp, base_atk , base_def , base_spatk , base_spdef , base_spd):
        cursor = self.conn.cursor()
        query = "update base_pokemon set p_name=%s, ptype1=%s, ptype2=%s, base_hp=%s, base_atk=%s, base_def=%s, base_spatk=%s, base_spdef=%s, base_spd=%s where p_id=%s"

        cursor.execute(query, (p_name, p_type1, p_type2, base_hp, base_atk , base_def , base_spatk , base_spdef , base_spd, p_id,))
        pid = cursor.fetchone()[0]
        self.conn.commit()
        return pid

    def deletePokemon(self, p_id):
        cursor = self.conn.cursor()
        query = "delete from base_pokemon where p_id=%s;"
        cursor.execute(query,(p_id,))
        # determine affected rows
        affected_rows = cursor.rowcount
        self.conn.commit()
        # if affected rows == 0, the part was not found and hence not deleted
        # otherwise, it was deleted, so check if affected_rows != 0
        return affected_rows !=0