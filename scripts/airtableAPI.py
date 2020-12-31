from airtable import Airtable
from secret import atble_api, atble_base

api_key = atble_api
base_id = atble_base
tbl_name = 'Contacts'

"""
record: 
[
    {
    'id': 'string'
    'fields': {
        'Name': 'Smitty Werbenjagermangensen'
        'Contact Frequency': 'Bi-Annually'
        'Company': ['Nickelodeon Inc.']
        'Occupation': ['Public Figure', 'Influencer', 'Instagram Model']
        'Location': 'Pasadena'
        'Chat': -92
        'Contact Every?': 182
        'Last Contact': '2020-01-20'
        'To Chat': True
        'Notes': "Blerh de blerh'
        'Need': 'A hero who's gotta be strong, fast, and larger than life'
        }
    }
]

'Chat' is a formula based on "Last Contact" and "Contact Every?"

"""

def check_update_dictionary(update_dict: dict) -> None:

    columns = {'Name': str,
               'Contact Frequency': str,
               'Company': str,
               'Occupation': list,
               'Location': str,
               'Chat': int,
               'Contact Every?': int,
               'Last Contact': str,
               'To Chat?': bool,
               'Notes': str,
               "Need": str
        }

    frequency_drop = ['TBD', 'Weekly', 'Monthly', 'Quarterly', 'Bi-Annually', 'Annually' 'Never']

    dict_error_cols = [i for i in update_dict.keys() if i not in columns]  # Get all incorrect columns

    if len(dict_error_cols) > 0:  # Format Checking
        raise KeyError('The following column(s) are not available -> {}'.format(dict_error_cols))

    for j in update_dict:  # Check the variable type for each entry in dict

        if j == 'Contact Frequency' and update_dict[j] not in frequency_drop:  # Check update frequency
            raise ValueError("Value {} is not proper contact frequency -> {}".format(update_dict[j], frequency_drop))

        if type(update_dict[j]) != columns[j]:
            raise TypeError("Incorrect type {} for column '{}'".format(type(update_dict[j]), j))

        # TODO: Check format of date is parseable

    else:
        return None

class ATable():

    def __init__(self, api_key: str, base_id: str, table: str):
        self.tbl_obj = Airtable(base_id, table, api_key=api_key)
        self.table: list = self.tbl_obj.get_all()
        self.fields: list = list(self.table[0]['fields'].keys())

    def table_search(self, column_name, search_value) -> (list, None):
        if column_name not in self.fields:
            print('"{}" is not a valid field name')
            return None

        results = self.tbl_obj.search(column_name, search_value)

        return results

    def get_contact_suggestions(self, n: int=10, pers=True, prof=True, srch:str = "Chat > 0"):
        # TODO: Catch cases where format of srch string is incorrect
        records = self.tbl_obj.get_all(formula=srch)
        both_records = [i for i in records if i['fields']['Category'] == 'Both']
        pers_records = []
        prof_records = []

        if pers:
            pers_records = [i for i in records if i['fields']['Category'] == 'Personal']

        if prof:
            prof_records = [i for i in records if i['fields']['Category'] == 'Professional']

        all_recs = both_records + pers_records + prof_records
        all_recs = sorted(all_recs, key=lambda rec: rec['fields']['Chat'], reverse=True)

        if n and len(all_recs) > n:
            return(all_recs[:n])

        return all_recs


class Contact():

    def __init__(self, name: str):
        self.name = name
        self.contact_table = ATable(api_key=api_key, base_id=base_id, table='Contacts')
        self.search_results = self.contact_table.table_search('Name', self.name)

        if len(self.search_results) == 0:
            print('Contact "{}" not found in table'.format(self.name))
            self.contact_frequency = None
            self.company = None
            self.occupation = None
            self.location = None
            self.chat_countdown = 365

        if len(self.search_results) == 1:
            self.contact_frequency = self.search_results[0]['fields']['Contact Frequency']
            self.company = self.search_results[0]['fields']['Company']
            self.occupation = self.search_results[0]['fields']['Occupation']
            self.location = self.search_results[0]['fields']['Location']
            self.chat_countdown = self.search_results[0]['fields']['Chat']
            self.contact_every = self.search_results[0]['fields']['Contact Every']

        if len(self.search_results) > 1:
            print('Multiple results found for Name == "{}"'.format(self.name))


def update_contact_record(name: str, update_dict: dict):

    if check_update_dictionary(update_dict) == None:

        at = ATable(api_key=api_key, base_id=base_id, table='Contacts')  # Create Airtable Object
        record = at.tbl_obj.match('Name', name)  # Find the correct record from the name

        at.tbl_obj.update(record['id'], update_dict)

        print('Succesfully updated record for "{}"'.format(name))

        return None

    else:
        return KeyError("Error with update dictionary")



if __name__ == '__main__':
    t = ATable(api_key=api_key, base_id=base_id, table=tbl_name)

    recs = t.get_contact_suggestions(n=10)

    print(t.fields)

    name = 'Mike DiSanza'
    update_dict = {
        'Location': 'Atlanta',
        'Contact Frequency': 'Bi-Annually',
        'Last Contact': '2020-03-18',
        'To Chat?': True,
        'Notes': "The most BADASS of beards",
        'Need': "Needs a dope longsword and a fine steed to ride into battle"
    }

    update_contact_record('Mike DiSanza', update_dict=update_dict)