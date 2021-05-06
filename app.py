from flask import Flask, jsonify, request
from flask_cors import CORS
from controller.basepokemon import BasePokemon
from controller.abilities import Abilities
from controller.items import Items
from controller.moves import Moves
from controller.moves_pool import MovesPool
from controller.saved_build import SavedBuild

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

@app.route('/pokemons', methods=['GET', 'POST'])
def pokemons():
    if request.method == 'POST':
        return BasePokemon().newPokemon(request.json)
    else:
        return BasePokemon().getAllPokemon()

@app.route('/pokemon/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def spec_pokemon(pid):
    if request.method == 'PUT':
        return BasePokemon().updatePokemon(request.json, pid)
    elif request.method == 'DELETE':
        return BasePokemon().deletePokemon(pid)
    else:
        return BasePokemon().getPokemonId(pid)

@app.route('/abilities', methods=['GET', 'POST'])
def abilities():
    if request.method == 'POST':
        return Abilities().newAbility(request.json)
    else:
        return Abilities().getAllAbilities()

@app.route('/ability/<int:aid>', methods=['GET', 'DELETE'])
def spec_ability(aid):
    if request.method == 'DELETE':
        return Abilities().deleteAbility(aid)
    else:
        return Abilities().getAbilitiesId(aid)

@app.route('/items', methods=['GET', 'POST'])
def items():
    if request.method == 'POST':
        return Items().newItem(request.json)
    else:
        return Items().getAllItems()

@app.route('/item/<int:iid>', methods=['GET', 'DELETE'])
def spec_item(iid):
    if request.method == 'DELETE':
        return Items().deleteItem(iid)
    else:
        return Items().getItemId(iid)

@app.route('/moves', methods=['GET', 'POST'])
def moves():
    if request.method == 'POST':
        return Moves().newMove(request.json)
    else:
        return Moves().getAllMoves()

@app.route('/move/<int:mid>', methods=['GET', 'DELETE'])
def spec_move(mid):
    if request.method == 'DELETE':
        return Moves().deleteMove(mid)
    else:
        return Moves().getMoveId(mid)

@app.route('/moves-pool', methods=['POST'])
def moves_pool():
    if request.method == 'POST':
        return MovesPool().insertMovePool(request.json)

@app.route('/move-pool/<int:mid>', methods=['GET', 'DELETE'])
def spec_move_pool(mid):
    if request.method == 'DELETE':
        return MovesPool().deleteMove(mid)
    else:
        return MovesPool().getPidByMovesId(mid)

@app.route('/move-pool-by-pid/<int:pid>', methods=['GET'])
def spec_movePoolId_ByPid(pid):
    if request.method == 'GET':
        return MovesPool().getMovesByPid(pid)

@app.route('/saved-build', methods=['GET', 'POST'])
def saved_build():
    if request.method == 'POST':
        return SavedBuild().insertPokemon(request.json)
    else:
        return SavedBuild().getAllPokemon()

@app.route('/saved-build/<int:pid>', methods=['GET', 'PUT', 'DELETE'])
def spec_saved_build(pid):
    if request.method == 'PUT':
        return SavedBuild().updatePokemon(request.json, pid)
    elif request.method == 'DELETE':
        return SavedBuild().deletePokemon(pid)
    else:
        return SavedBuild().getPokemonId(pid)

if __name__ == '__main__':
    app.run()