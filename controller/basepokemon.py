from flask import jsonify
from model.basepokemon import BasePokemonDAO

class BasePokemon: 

    def build_map_dict(self, row):
        result = {}
        result['p_id'] = row[0]
        result['p_name'] = row[1]
        result['ptype1'] = row[2]
        result['ptype2'] = row[3]
        result['base_hp'] = row[4]
        result['base_atk'] = row[5]
        result['base_def'] = row[6]
        result['base_spatk'] = row[7]
        result['base_spdef'] = row[8]
        result['base_spd'] = row[9]
        return result
    
    def build_attr_dict(self, pid, pname, ptype1, ptype2, bhp, batk, bdef, bspatk, bspdef, bspd):
        result = {}
        result['p_id'] = pid
        result['p_name'] = pname
        result['ptype1'] = ptype1
        result['ptype2'] = ptype2
        result['base_hp'] = bhp
        result['base_atk'] = batk
        result['base_def'] = bdef
        result['base_spatk'] = bspatk
        result['base_spdef'] = bspdef
        result['base_spd'] = bspd
        return result

    def getAllPokemon(self):
        dao = BasePokemonDAO()
        pokemon_list = dao.getAllPokemon()
        result_list = []
        for row in pokemon_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(pokemon_list)

    def getPokemonId(self, pid):
        dao = BasePokemonDAO()
        pokemon = dao.getPokemonById(pid)
        if not pokemon:
            return jsonify("Pokemon not found"), 404
        else:
            result = self.build_map_dict(pokemon)
            return jsonify(result)
    
    def newPokemon(self, json):
        p_id = json['p_id']
        p_name = json['p_name']
        ptype1 = json['ptype1']
        ptype2 = json['ptype2']
        base_hp = json['base_hp']
        base_atk = json['base_atk']
        base_def = json['base_def']
        base_spatk = json['base_spatk']
        base_spdef = json['base_spdef']
        base_spd = json['base_spd']
        dao = BasePokemonDAO()
        pid = dao.insertPokemon(p_id,p_name, ptype1,ptype2, base_hp, base_atk, base_def, base_spatk, base_spdef, base_spd)
        result = self.build_attr_dict(pid, p_name, ptype1, ptype2, base_hp, base_atk, base_def, base_spatk, base_spdef, base_spd)
        return jsonify(result), 201

    def deletePokemon(self, pid):
        dao = BasePokemonDAO()
        result = dao.deletePokemon(pid)
        if result:
            return jsonify("Pokemon Deleted"), 200
        else:
            return jsonify("Pokemon not found"), 404

    def updatePokemon(self, json, pid):
        p_name = json['p_name']
        p_type1 = json['p_type1']
        p_type2 = json['p_type2']
        base_hp = json['base_hp']
        base_atk = json['base_atk']
        base_def = json['base_def']
        base_spatk = json['base_spatk']
        base_spdef = json['base_spdef']
        base_spd = json['base_spd']
        dao = BasePokemonDAO()
        updated = dao.updatePokemon(pid, p_name, p_type1,p_type2, base_hp, base_atk, base_def, base_spatk, base_spdef, base_spd)
        result = self.build_attr_dict(pid, p_name, p_type1, p_type2, base_hp, base_atk, base_def, base_spatk, base_spdef, base_spd)
        return jsonify(result), 200
    