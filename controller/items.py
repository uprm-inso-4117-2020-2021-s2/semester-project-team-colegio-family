from flask import jsonify
from model.items import items

class Items: 

    def build_map_dict(self, row):
        result = {}
        result['pitemid'] = row[0]
        result['items_name'] = row[1]
        return result
    
    def build_attr_dict(self, pitemid, items_name):
        result = {}
        result['pitemid'] = pitemid
        result['items_name'] = items_name
        return result

    def getAllItems(self):
        dao = items()
        items_list = dao.getitems()
        result_list = []
        for row in items_list:
            obj = self.build_map_dict(row)
            result_list.append(obj)
        return jsonify(items_list)

    def getItemId(self, pid):
        dao = items()
        item = dao.getitemById(pid)
        if not item:
            return jsonify("Item not found"), 404
        else:
            result = self.build_map_dict(item)
            return jsonify(result)
    
    def newItem(self, json):
        items_name = json['items_name']
        dao = items()
        pid = dao.insertitem(items_name)
        result = self.build_attr_dict(pid,items_name)
        return jsonify(result), 201

    def deleteItem(self, pid):
        dao = items()
        result = dao.deleteitem(pid)
        if result:
            return jsonify("Item Deleted"), 200
        else:
            return jsonify("Item not found"), 404