from datetime import datetime

class Card():

    def __init__(self, name, set_code, set_name, collector_number, foil, rarity, quantity, mana_box_id, scryfall_id, purchase_price, misprint, altered, condition, language, purchase_price_currency, last_update, error):
        self.name = name
        self.set_code = set_code
        self.set_name = set_name
        self.collector_number = collector_number

        if foil == 'foil' or foil == 'True':
            self.foil = True
        else:
            self.foil = False

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
            'available': None,
            'price_from': None,
            'price_trend': None,
            'price_avg_30': None,
            'price_avg_7': None,
            'price_avg_1': None
        }        
        self.last_update = last_update
        
        if error == '':
            self.error = None
        else:
            self.error = error

    def set_price_details(self, price_details):
        self.price_details = price_details

    def set_formattet_field_values(self):
        self.formatted_card_name = self.__format_value(self.name)
        self.formatted_set_name = self.__format_value(self.set_name)    

        # Special case for "Duel Decks" sets
        if self.formatted_set_name.startswith('Duel-Decks'):
            self.formatted_set_name = self.formatted_set_name.split(':')[0].strip()
        else:
            self.formatted_set_name = self.formatted_set_name.replace(':', '').strip()

        # Special case for card names that contain ','
        self.formatted_card_name = self.formatted_card_name.replace(',', '').strip()


    def __format_value(self, value) -> str:
        # format the corresponding fields for the call at cardmarket
        formatted_value = value.replace(" ", "-")
        
        # Check if there is a letter or a space after the apostrophe
        apostrophe_index = formatted_value.find("'")
        if apostrophe_index != -1 and apostrophe_index < len(formatted_value) - 1:
            
            # If there is an 's' after the apostrophe, simply remove the apostrophe
            if formatted_value[apostrophe_index + 1] == "s":
                formatted_value = formatted_value[:apostrophe_index] + formatted_value[apostrophe_index + 1:]
            # If there is a letter after the apostrophe, replace it with "-"
            elif formatted_value[apostrophe_index + 1].isalpha():
                formatted_value = formatted_value[:apostrophe_index] + "-" + formatted_value[apostrophe_index + 1:]            
            # If there is a space after the apostrophe, remove it
            elif formatted_value[apostrophe_index + 1] == " ":
                formatted_value = formatted_value[:apostrophe_index] + formatted_value[apostrophe_index + 1:]
    
        return formatted_value

    def set_timestamp(self):
        self.last_update = datetime.now().strftime("%Y%m%d%H%M%S")

    def has_price_details(self) -> bool:
       """Check if price details are initialized"""
       return all(self.price_details[field] != '' for field in [
            'available', 'price_from', 'price_trend', 'price_avg_30', 'price_avg_7', 'price_avg_1' ])