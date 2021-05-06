from flask import jsonify
from model.abilities import abilitiesDAO

class Abilities: 

    def build_map_dict(self, row):
        result = {}
        result['pabilities_id'] = row[0]
        result['pabilities_name'] = row[1]
        return result
    
    def build_attr_dict(self, pabilitiesid, pabilitiesname):
        result = {}
        result['pabilities_id'] = pabilitiesid
        result['pabilities_name'] = pabilitiesname
        return result

    def getAllAbilities(self):
        dao = abilitiesDAO()
        abilities_list = dao.getabilities()
        result_list = []
        for row in abilities_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(abilities_list)

    def getAbilitiesId(self, pid):
        dao = abilitiesDAO()
        ability = dao.getabilityById(pid)
        if not ability:
            return jsonify("Ability not found"), 404
        else:
            result = self.build_map_dict(ability)
            return jsonify(result)
    
    def newAbility(self, json):
        pabilities_name = json['pabilities_name']
        dao = abilitiesDAO()
        pid = dao.insertability(pabilities_name)
        result = self.build_attr_dict(pid, pabilities_name)
        return jsonify(result), 201

    def deleteAbility(self, pid):
        dao = abilitiesDAO()
        result = dao.deleteAbility(pid)
        if result:
            return jsonify("Ability Deleted"), 200
        else:
            return jsonify("Ability not found"), 404