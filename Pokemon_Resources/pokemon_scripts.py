
from json import dump
from re import compile
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
from requests import get
from sys import exit



trash_words = ('<td class="cell-num cell-fixed" data-sort-value="',
                '"><span',
                'class="infocard-cell-img"><img class="img-fixed icon-pkmn"',
                'src=',
                'alt=',
                'icon"></span><span class="infocard-cell-data">',
                '</span></td> <td class="cell-name"><a class="ent-name" href="/pokedex/',
                'title="View Pokedex for',                
                '</a></td><td class="cell-icon"><a class="',
                '<br> <small class="text-muted">',
                '</small></td><td',
                '" href="/type/',
                '</a><br> <a class="',
                '" href="/type/',
                '" href="/type/',                
                'type-icon',
                'type-',
                '</a></td>',                
                '<td class="cell-total">',
                '</td>',
                '<td class="cell-num">',
                '/span',
                '/td',
                '/a',                
                '">',
                '">',
                '>',
                '<',
                '"',                
                )


NORMAL = 'normal'
FIRE = 'fire'
WATER = 'water'
GRASS = 'grass'
ELECTRIC = 'electric'
ICE = 'ice'
FIGHTING = 'fighting'
POISON = 'poison'
GROUND = 'ground'
FLYING = 'flying'
PSYCHIC = 'psychic'
BUG = 'bug'
ROCK = 'rock'
GHOST = 'ghost'
DARK = 'dark'
DRAGON = 'dragon'
STEEL = 'steel'
FAIRY = 'fairy'

POKEMON_TYPES = (
    NORMAL,
    FIRE,
    WATER,
    GRASS,
    ELECTRIC,
    ICE,
    FIGHTING,
    POISON,
    GROUND,
    FLYING,
    PSYCHIC,
    BUG,
    ROCK,
    GHOST,
    DARK,
    DRAGON,
    STEEL,
    FAIRY,
)

STAT_NAMES = (
    'HealthPoints',
    'AttackPoints',
    'DefensePoints',
    'SpAttackPoints',
    'SpDefensePoints',
    'Speed',    
    )


'''
Formato extracted from first line
0 -> id
1 -> image_link
2 -> pokemon _name
3 -> text_id
4 -> pokemon_name_lowercase
5 -> text_id_with#
6 -> pokemon _name
7 -> pokemon _name
next places cant be determined because there could be more than one type
'''


def beautiful_soup_attempt():
    url = 'https://pokemondb.net/pokedex/all'
    page = get(url)
    soup = BeautifulSoup(page.content, 'html.parser')    
    count = 0
    type_re = compile(r'/type/[a-z]+')
    poke_name_re = compile(r'View Pokedex for #[0-9]{3} ')
    three_num_re = compile(r'[0-9]{3}')
    pokemon_list = []
    for table_row in soup.find_all('tr'):
        poke_dict = {'Type' : []}
        stat_ls = []
        for table_content in table_row.descendants:
            if table_content:
                if isinstance(table_content, Tag):
                    tag = table_content                    
                    if tag.get('data-src'):
                        poke_dict['PictureLink'] = tag.get('data-src')
                    if tag.get('href'):
                        info = tag.get('href')
                        if type_re.match(info):
                            poke_dict['Type'].append(info.replace('/type/', '').strip())
                    if tag.get('title'):                        
                        title = tag.get('title')                                                
                        if poke_name_re.search(title):
                            trash_len = len(poke_name_re.search(title).group(0))
                            poke_dict['Name'] = title[trash_len:]
                    if tag.get('data-sort-value'):
                        poke_dict['Id'] = str(tag.get('data-sort-value'))
                    if tag.get('class') == ['cell-total']:
                        poke_dict['TotalPoints'] = int(tag.text)
                    if tag.get('class') == ['cell-num']:
                        stat_ls.append(int(tag.text))

        for stat_name, stat_num in zip(STAT_NAMES, stat_ls):
            poke_dict[stat_name] = stat_num
        try:
            poke_dict['TotalPointsGenOne'] = poke_dict['TotalPoints'] - poke_dict['SpAttackPoints']
        
        except:
            pass
            
        pokemon_list.append(poke_dict)

                
    return pokemon_list
    

def replace_many_words(current_str, word_ls):    
    for word in word_ls:
        current_str = current_str.replace(word, ' ')
    return current_str

def get_next_line(file_handle):
    return file_handle.readline().strip()

def get_pokemon_type(text_line):
    current_types = []
    for type in POKEMON_TYPES:
        if text_line.find(type) != 1:
            current_types.append(type)
    return current_types

pokemon_list = []

poke_info = beautiful_soup_attempt()
poke_info.pop(0)
#     print('\n\n')
with open('poke_fots/pokemon_json_data', 'w') as dest_file:
    dump(poke_info, dest_file)

exit(0)

with open('poke_fots/pokemon_info', 'r') as src_file:
    with open('poke_fots/pokemon_json_data', 'w') as dest_file:

        try:
            count = 0
            while True:
                print(count)
                if count == 151:
                    break                                
                poke_dict = {}
                current_line = get_next_line(src_file)
                current_line = get_next_line(src_file)
                current_line = replace_many_words(current_line, trash_words)                
                current_info = current_line.split()                
                print(current_info)
                print(current_line)
                
                
                poke_dict['TotalPoints'] = int(replace_many_words(get_next_line(src_file), trash_words).strip()) # Total stat points
                poke_dict['HealthPoints'] = int(replace_many_words(get_next_line(src_file), trash_words).strip()) # Health points
                poke_dict['AttackPoints'] = int(replace_many_words(get_next_line(src_file), trash_words).strip()) # Attack points
                poke_dict['DefensePoints'] = int(replace_many_words(get_next_line(src_file), trash_words).strip()) # Defense points
                poke_dict['SpecialAttackPoints'] = int(replace_many_words(get_next_line(src_file), trash_words).strip()) # Special Attack points
                poke_dict['SpecialDefensePoints'] = int(replace_many_words(get_next_line(src_file), trash_words).strip()) # Special Defefnse points
                poke_dict['Speed'] = int(replace_many_words(get_next_line(src_file), trash_words).strip()) # Speed points                
                poke_dict['GenerationOneTotalPoints'] = poke_dict['TotalPoints'] - poke_dict['SpecialAttackPoints']
                if current_line.find('Mega ') != -1:
                    continue
                pokemon_list.append(poke_dict)
                count += 1

                

                
                

                
        except Exception as e:
            print(e)
            raise e