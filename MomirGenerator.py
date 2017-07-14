# Current issues:
#   discrepencies between list populations and gatherer counts:
#       Artifact creatures: Gatherer - 549, this - 550
#       pure creatures: Gatherer - 8319, this - 8324
#       pure enchantment: Gatherer - 2088, this - 2084
#       pure lands: Gatherer - 580, this - 581


# TODO:
#   optimize CMC indices so that they can be determined without having to walk through the list every time

# long-term:
#   automatically check for card updates
#   validate card count discrepencies (maybe using gatherer?)

import json
import random


class Card(object):
    def __init__(self, name, types, subtypes, cmc, un_card):
        self.name = name
        self.types = types
        self.subtypes = subtypes
        self.cmc = cmc
        self.un_card = un_card
        
        

class Generator:
    
    def __init__(self, *args, **kwargs):
        self.artifacts = []
        self.artifact_lands = []
        self.artifact_creatures = []
        self.enchantment_artifacts = []

        self.creatures = []
        self.enchantment_creatures = []
        self.land_creatures = []

        self.enchantments = []
        self.lands = []
        self.planeswalkers = []
        
        self.un_artifacts = []
        self.un_artifact_creatures = []
        self.un_creatures = []
        self.un_enchantments = []
        self.un_lands = []
        
        
    
        with open('truncated_mtg.json', encoding='utf8') as data_file:
            cards = json.load(data_file)

 
        
        self.addCardsToList(cards)

        # self.printCardCounts()
        
 
    def getPermanent(self, options):
        creature_bool = options[0]
        artifact_bool = options[1]
        enchantment_bool = options[2]
        planeswalker_bool = options[3]
        land_bool = options[4]
        
        uncard_bool = options[5]
        no_aura_equipment_bool = options[6]
        
        cmc = options[8]
        
        
        # concatenate lists of requested permanent types
        permanents = []
        if artifact_bool:
            permanents += self.artifacts
        if creature_bool:
            permanents += self.creatures
        if enchantment_bool:
            permanents += self.enchantments
        if land_bool:
            permanents += self.lands
        if planeswalker_bool:
            permanents += self.planeswalkers
        
        if artifact_bool or creature_bool:
            permanents += self.artifact_creatures
        if artifact_bool or land_bool:
            permanents += self.artifact_lands
        if artifact_bool or enchantment_bool:
            permanents += self.enchantment_artifacts
        if creature_bool or enchantment_bool:
            permanents += self.enchantment_creatures
        if creature_bool or land_bool:
            permanents += self.land_creatures
 
        
        # sort permanents list by cmc
        permanents = sorted(permanents, key=lambda card: card.cmc)

        #print("{} possible permanents".format(len(permanents)))
        
        # find start index of requested cmc
        start_index = 0
        found = False
        for i in range(len(permanents)):
            #print("\tcmc = {}".format(permanents[i].cmc))
            if permanents[i].cmc == cmc:
                start_index = i
                found = True
                break
        if not found:
            print("No permanent of requested CMC exists for requested permanent types.")
            return None
        
        #print("Start index: {}".format(start_index))
        
        # find end index of requested cmc
        end_index = 0
        found = False
        for i in range(start_index +1, len(permanents)):
            if permanents[i].cmc != cmc:
                end_index = i
                found = True
                break
        if not found:
            end_index = len(permanents)
        
        #print("End index: {}".format(end_index))
        
        
        # NOTE: This is a simple but poor solution here. Better to separate
        # out un-cards and equipment/auras, but I'm tired of making and
        # concatenating lists. Consider fixing this TODO, I guess
        while True:
            card_index = random.randrange(start_index, end_index)
            card = permanents[card_index]
            # check if selected card violates either un-card or equip/aura constraints
            if (not uncard_bool) and card.un_card: continue
            if no_aura_equipment_bool and ('Aura' in card.subtypes or 'Equipment' in card.subtypes): continue
            print('Card has types {}, subtypes {}'.format(card.types, card.subtypes))
            break
        
        
        return permanents[card_index]
                

    def addCardsToList(self, cards):
        for card in cards:
            name = card['name']
            types = card['types']
            subtypes = card['subtypes']
            cmc = card["cmc"]
            un_card = card['un_card']
            
            card = Card(name, types, subtypes, cmc, un_card)
        
            if 'Artifact' in card.types:
                if 'Land' in card.types:
                    self.artifact_lands.append(card)
                elif 'Creature' in card.types:
                    self.artifact_creatures.append(card)
                elif 'Enchantment' in card.types:
                    self.enchantment_artifacts.append(card)
                else:
                    self.artifacts.append(card)
            elif 'Creature' in card.types:
                if 'Enchantment' in card.types:
                    self.enchantment_creatures.append(card)
                elif 'Land' in card.types:
                    self.land_creatures.append(card)
                else:
                    self.creatures.append(card)
            elif 'Enchantment' in card.types:
                self.enchantments.append(card)
            elif 'Land' in card.types:
                self.lands.append(card)
            elif 'Planeswalker' in card.types:
                self.planeswalkers.append(card)


    def printCardCounts(self):
        # print list counts
        print("num artifacts: {}".format(len(self.artifacts)))
        print("num artifact lands: {}".format(len(self.artifact_lands)))
        print("num artifact creatures: {}".format(len(self.artifact_creatures)))
        print("num enchantment artifacts: {}".format(len(self.enchantment_artifacts)))

        print("num creatures: {}".format(len(self.creatures)))
        print("num enchantment creatures: {}".format(len(self.enchantment_creatures)))
        print("num land creatures: {}".format(len(self.land_creatures)))

        print("num enchantments: {}".format(len(self.enchantments)))
        print("num lands: {}".format(len(self.lands)))
        print("num planeswalkers: {}".format(len(self.planeswalkers)))
    
                
# the following code is for if this is executed from the command line
if __name__ == "__main__":
    generator = Generator()

    valid_types = ['land', 'creature', 'artifact', 'enchantment']
    need_input = True
    while need_input:    
        types_string = input("Types? ").lower()
     
        if types_string == 'all':
            types = valid_types
            break
            
        types = types_string.split()
        need_input = False
        
        # validate input
        for type in types:
            if type not in valid_types:
                print("{} is not a valid permanent type. Valid types are: {}".format(type, valid_types))
                need_input = True
        
        

    while True:
        cmc = input("CMC? ")
        if cmc == "quit":
            break
            
        try:
            cmc = int(cmc)
            card = generator.getPermanent(cmc, types)
            if card is not None:
                print(card.name)
        except:
            print("CMC must be an integer")