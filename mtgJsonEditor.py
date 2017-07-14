

import json

class Card(object):
    def __init__(self, name, types, subtypes, cmc, un_card):
        self.name = name
        self.types = types
        self.subtypes = subtypes
        self.cmc = cmc
        self.un_card = un_card


        
class MtgJsonStripper:
        
    def __init__:
        
        # load original json data
        with open('AllSets.json', encoding='utf8') as data_file:
            parsed_json = json.load(data_file)
            
            
        cards = []
        names_set = set()
        # for each expansion set in the json data
        for set in parsed_json:
            # check if set is a prerelease set. If so, ignore it
            if set[0] == 'p':
                continue
            
            # for each card in the set
            for card in parsed_json[set]['cards']:
                # if the card is a token, ignore it
                if card['layout'] == 'token': continue
                
                # If current card is not in the set of already examined cards
                if card['name'] not in names_set:
                    name = card['name']
                    try:
                        # save name, types, subtypes, cmc, and set of each card as a card object
                        types = card['types']
                        subtypes = []
                        if 'subtypes' in card:
                            subtypes = card['subtypes']
                        cmc = 0
                        if 'cmc' in card:
                            cmc = card['cmc']
                        un_card = (set == 'UGL') or (set == 'UNH')
                        new_card = Card(name, types, subtypes, cmc, un_card)
                        
                        # add card object to list of cards, add card name to set
                        cards.append(new_card)
                        names_set.add(name)
                    except:
                        print('Failure with card {}'.format(name))
                
        # save contents of cards list as new json document
        truncated_mtg = open('truncated_mtg.json', 'w')
        
        truncated_mtg.write('[\n')
        for card in cards:
            truncated_mtg.write(json.dumps(card.__dict__))
            if i < len(cards) - 1:
                truncated_mtg.write(',')
            truncated_mtg.write('\n')
        truncated_mtg.write(']')
            
        truncated_mtg.close()


