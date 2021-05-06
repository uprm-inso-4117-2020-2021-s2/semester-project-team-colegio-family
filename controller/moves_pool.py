from flask import jsonify
from model.moves_pool import movespoolDAO

class MovesPool: 

    def build_map_dict(self, row):
        result = {}
        result['move_id'] = row[0]
        result['p_id'] = row[1]
        return result

    def build_map_dict2(self, row):
        result = {}
        result['move_id'] = row[0]
        return result

    def build_map_dict3(self, row):
        result = {}
        result['p_id'] = row[1]
        return result
    
    def build_attr_dict(self, move_id, p_id):
        result = {}
        result['move_id'] = move_id
        result['p_id'] = p_id
        return result

    def getPidByMovesId(self, moveId):
        dao = movespoolDAO()
        move = dao.getmovesbymoveid(moveId)
        if not move:
            return jsonify("Pokemon not found by moves Id"), 404
        else:
            result = self.build_map_dict2(move)
            return jsonify(result)

    def getMovesByPid(self, pid):
        dao = movespoolDAO()
        move = dao.getmovesbypid(pid)
        if not move:
            return jsonify("Move not found by pokemon"), 404
        else:
            result = self.build_map_dict3(move)
            return jsonify(result)
    
    def insertMovePool(self, json):
        move_id = json['move_id']
        p_id = json['p_id']
        dao = movespoolDAO()
        pid = dao.insertmovepool(move_id, p_id)
        result = self.build_attr_dict(move_id, p_id)
        return jsonify(result), 201

    def deleteMove(self, pid):
        dao = movespoolDAO()
        result = dao.deletemove(pid)
        if result:
            return jsonify("Move Deleted"), 200
        else:
            return jsonify("Move not found"), 404