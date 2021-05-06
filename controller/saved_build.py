from flask import jsonify
from model.saved_build import SavedBuildDAO

class SavedBuild: 

    def build_map_dict(self, row):
        result = {}
        result['pokemon_id'] = row[0]
        result['p_id'] = row[1]
        result['pokemon_name'] = row[2]
        result['pokemon_lvl'] = row[3]
        result['pabilities_id'] = row[4]
        return result
    
    def build_attr_dict(self, pokemon_id, p_id, pokemon_name, pokemon_lvl, pabilities_id):
        result = {}
        result['pokemon_id'] = pokemon_id
        result['p_id'] = p_id
        result['pokemon_name'] = pokemon_name
        result['pokemon_lvl'] = pokemon_lvl
        result['pabilities_id'] = pabilities_id
        return result

    def getAllPokemon(self):
        dao = SavedBuildDAO()
        pokemon_list = dao.getAllPokemon()
        result_list = []
        for row in pokemon_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(pokemon_list)

    def getPokemonId(self, pid):
        dao = SavedBuildDAO()
        pokemon = dao.getPokemonById(pid)
        if not pokemon:
            return jsonify("Pokemon not found in saved builds"), 404
        else:
            result = self.build_map_dict(pokemon)
            return jsonify(result)
    
    def insertPokemon(self, json):
        p_id = json['p_id']
        pokemon_name = json['pokemon_name']
        pokemon_lvl = json['pokemon_lvl']
        pabilities_id = json['pabilities_id']
        dao = SavedBuildDAO()
        pid = dao.insertPokemon(p_id, pokemon_name,pokemon_lvl, pabilities_id)
        result = self.build_attr_dict(pid, p_id, pokemon_name,pokemon_lvl, pabilities_id)
        return jsonify(result), 201

    def deletePokemon(self, pid):
        dao = SavedBuildDAO()
        result = dao.deletePokemon(pid)
        if result:
            return jsonify("Pokemon Deleted from saved builds"), 200
        else:
            return jsonify("Pokemon not found in saved builds"), 404

    def updatePokemon(self, json, pid):
        p_id = json['p_id']
        pokemon_name = json['pokemon_name']
        pokemon_lvl = json['pokemon_lvl']
        pabilities_id = json['pabilities_id']
        dao = SavedBuildDAO()
        updated = dao.updatePokemon(pid, p_id, pokemon_name,pokemon_lvl, pabilities_id)
        result = self.build_attr_dict(pid, p_id, pokemon_name,pokemon_lvl, pabilities_id)
        return jsonify(result), 200
    