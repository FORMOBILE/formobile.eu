"""
Module to create a .vcf file with contact info from a .csv file
"""
import base64
import os.path
import random
import pandas as pd


def generate_vcards(path_csv: str, target_path: str) -> str:
    """
    Generates a .vcf file that contains all contact data from the .csv file.

    Pictures are currently only tested for .png, .jpg and .jpeg

    :param path_csv: path to .csv file which contains the contact data
    :param target_path: path where the file should be stored
    :return: target_path
    """

    # Data that we'll use to populate the cards' fields.
    data_frame = pd.read_csv(path_csv, dtype={'plz': 'str', 'phone_h': 'str', 'phone_w': 'str'}).fillna("")

    pictures_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'datasets', 'pictures',
                                'contact_pictures')

    # What fields shall be populated?
    target_fields = {"Name": True,
                     "FullName": True,
                     "Organization": data_frame['orgs'],
                     "Address": True,
                     "Phone_h": (data_frame['phone_h'] != ""),
                     "Phone_w": (data_frame['phone_w'] != ""),
                     "Email": (data_frame['email'] != ""),
                     "Birthday": (data_frame['birthday'] != ""),
                     "Picture": (data_frame['picture'] != ""), }

    first_names = data_frame['first_names']
    last_names = data_frame['last_names']
    orgs = data_frame['orgs']
    phone_h = data_frame['phone_h']
    phone_w = data_frame['phone_w']
    email = data_frame['email']
    street = data_frame['street']
    plz = data_frame['plz']
    city = data_frame['city']
    birthday = data_frame['birthday']
    picture = data_frame['picture']

    class CardFiller:
        """
        class that represents an individual contact vCard
        """
        # pylint: disable=too-many-arguments
        def __init__(self, first_names: str, last_names: str, orgs: str, phone_h: str, phone_w: str,
                     street: str, plz: str, city: str, email: str, picture: str, birthday: str):
            self.first_names = first_names
            self.last_names = last_names
            self.orgs = orgs
            self.phone_h = phone_h
            self.phone_w = phone_w
            self.street = street
            self.plz = plz
            self.city = city
            self.email = email
            self.picture = picture
            self.birthday = birthday

        def fill_card(self, target_fields: dict, position: int) -> list:
            """
            Fills the data from the .csv file to the card
            :param target_fields: fields that should be populated
            :param position: position of the vCard in the concatenated .vcf file
            :return: list of strings - each representing a line in the vCard
            """
            new_card = ["BEGIN:VCARD", "VERSION:3.0", ]
            # Fill the Name field.
            if "Name" in target_fields:
                namefield = "N:"
                namefield += str(self.last_names[position % len(self.last_names)])
                namefield += ";"
                namefield += str(self.first_names[position % len(self.first_names)])
                new_card.append(namefield)
            if "FullName" in target_fields:
                fnamefield = "FN:"
                fnamefield += str(self.first_names[position % len(self.first_names)])
                fnamefield += " "
                fnamefield += str(self.last_names[position % len(self.last_names)])
                new_card.append(fnamefield)
            if "Birthday" in target_fields:
                bday = "BDAY:"
                bday += str(self.birthday[position % len(self.birthday)])
                new_card.append(bday)
            if "Organization" in target_fields:
                orgfield = "ORG:"
                orgfield += str(self.orgs[position % len(self.orgs)])
                new_card.append(orgfield)
            if target_fields['Picture'][position % len(self.picture)]:

                picture_path = os.path.join(pictures_dir, str(self.picture[position % len(self.picture)]))
                with open(picture_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                if picture_path.lower().endswith(('.jpg', '.jpeg')):
                    picture_field = "PHOTO;JPEG;ENCODING=BASE64:"
                    picture_field += str(encoded_string).strip('b\'')
                elif picture_path.lower().endswith('.png'):
                    picture_field = "PHOTO;PNG;ENCODING=BASE64:"
                    picture_field += str(encoded_string).strip('b\'')
                else:
                    pass
                new_card.append(picture_field)
            if target_fields['Phone_h'][position % len(self.phone_h)]:
                phonefield = "TEL;CELL;VOICE:"
                phonefield += str(self.phone_h[position % len(self.phone_h)])
                new_card.append(phonefield)
            if target_fields['Phone_w'][position % len(self.phone_h)]:
                phonefield_w = "TEL;WORK;VOICE:"
                phonefield_w += str(self.phone_w[position % len(self.phone_w)])
                new_card.append(phonefield_w)
            if "Address" in target_fields:
                addrfield = "ADR;WORK:;;"
                addrfield += str(self.street[position % len(self.street)])
                addrfield += ';'
                addrfield += str(self.plz[position % len(self.plz)])
                addrfield += ';'
                addrfield += str(self.city[position % len(self.city)])
                new_card.append(addrfield)
            if target_fields['Email'][position % len(self.email)]:
                emailfield = "EMAIL;PREF;HOME:"
                emailfield += str(self.email[position % len(self.email)])
                new_card.append(emailfield)

            new_card.append("REV:%d" % random.randrange(100, 500))
            new_card.append("END:VCARD")
            return new_card

    def rolodex_engine(card_limit: int, target_fields: dict) -> list:
        """
        Generates a list of strings each representing a line in the final .vcf file

        :param card_limit: amount of vCards the .vcf file will contain
        :param target_fields: fields that will be populated
        :return: List of strings
        """
        card_engine = CardFiller(first_names, last_names, orgs, phone_h, phone_w,
                                 street, plz, city, email, picture, birthday)
        rolodex = []
        for i in range(1, card_limit + 1):
            new_card = card_engine.fill_card(target_fields, i)
            for line in new_card:
                rolodex.append(line)
        return rolodex

    with open(target_path, "w") as rolodex_file:
        rolodex = rolodex_engine(len(data_frame), target_fields)
        for line in rolodex:
            rolodex_file.write(line)
            rolodex_file.write("\n")
    return target_path
