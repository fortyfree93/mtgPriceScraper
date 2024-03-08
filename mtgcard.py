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
        self.formatted_card_name = self.__format_value(self.name)
        self.formatted_set_name = self.__format_value(self.set_name)    

        # special case to Map for manaBox
        self.formatted_set_name = self.formatted_set_name.split(':')[0].strip()

    def __format_value(self, value) -> str:
        # format the corresponding fields for the call at cardmarket
        formatted_value = value.replace(" ", "-")
        
        # Check if there is a letter or a space after the apostrophe
        apostrophe_index = formatted_value.find("'")
        if apostrophe_index != -1 and apostrophe_index < len(formatted_value) - 1:
            # If there is a letter after the apostrophe, replace it with "-"
            if formatted_value[apostrophe_index + 1].isalpha():
                formatted_value = formatted_value[:apostrophe_index] + "-" + formatted_value[apostrophe_index + 1:]
            # If there is a space after the apostrophe, remove it
            elif formatted_value[apostrophe_index + 1] == " ":
                formatted_value = formatted_value[:apostrophe_index] + formatted_value[apostrophe_index + 1:]
    

        return formatted_value

    def set_timestamp(self):
        self.last_update = datetime.now().strftime("%Y%m%d%H%M%S")