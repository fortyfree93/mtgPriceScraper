from datetime import datetime

class Card():

    def __init__(self, name, set_code, set_name, collector_number, foil, rarity, quantity, mana_box_id, scryfall_id, purchase_price, misprint, altered, condition, language, purchase_price_currency, last_update):
        self.name = name
        self.set_code = set_code
        self.set_name = set_name
        self.collector_number = collector_number
        self.foil = foil
        self.rarity = rarity
        self.quantity = quantity
        self.mana_box_id = mana_box_id
        self.scryfall_id = scryfall_id
        self.purchase_price = purchase_price
        self.misprint = misprint
        self.altered = altered
        self.condition = condition
        self.language = language
        self.purchase_price_currency = purchase_price_currency                
        self.price_details = {
            'available': 0,
            'price_from': 0.0,
            'price_trend': 0.0,
            'price_avg_30': 0.0,
            'price_avg_7': 0.0,
            'price_avg_1': 0.0
        }        
        self.last_update = last_update

    def set_price_details(self, price_details):
        self.price_details = price_details

    def set_formattet_field_values(self):
        # format the corresponding fields for the call at cardmarket
        self.formatted_card_name = self.name.replace(" ", "-")
        self.formatted_set_name = self.set_name.replace(" ", "-")

        # special case to Map for manaBox
        self.formatted_set_name = self.formatted_set_name.split(':')[0].strip()

    def set_timestamp(self):
        self.last_update = datetime.now().strftime("%Y%m%d%H%M%S")