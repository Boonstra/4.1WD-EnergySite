'''
Created on 25 sep. 2013

@author: johan
'''

import sqlite3
import math
import random

class GenerateTestData():
    # Database name and connection.
    db = None
    conn = None
    # Base test data.
    streets = ['Robijnstraat', 'Travetijnstraat', 'Emeraldstraat', 'Admiraalstraat',
        'Generaalstraat', 'Keizerstraat']
    postcode_suffixes = ['AA', 'AB', 'AC', 'AD', 'AE', 'AF']
    categories = ['Zonnepaneel', 'Windmolen', 'Waterturbine' 'Hamsterwheel', 'Paardencarrousel',
        'Fiets', 'Vergistinginstallatie', 'Stoommachine', 'Fusiereactor', 'Gasturbine']
    devices = (
        ('Philips', 'Suncatcher 4140', 'Zonnepaneel'),
        ('Philips', 'Suncatcher 4150', 'Zonnepaneel'),
        ('NUON', 'Windmill 666', 'Windmolen'),
        ('Enexis', 'Windmill 777', 'Windmolen'),
        ('Pets & Co', 'Small brown hamster', 'Windmolen'),
    )
    times = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00']
    postcode_first = 9711
    postcode_last = 9750
    num_households = 500
    
    def __init__(self, db):
        self.conn = sqlite3.connect(db, isolation_level="DEFERRED")

    def __create_devices(self):
        cursor = self.conn.cursor()
        query = "INSERT INTO nrgweb_apparaat (merk, typenummer, categorie_id) VALUES(?, ?, ?)"
        device_ids = []
        for dev in self.devices:
            cursor.execute(query, dev)
            device_ids.append(cursor.lastrowid)
        return device_ids

    def __create_times(self):
        cursor = self.conn.cursor()
        query = "INSERT INTO nrgweb_metingtijden (tijd) VALUES(?)"
        for time in self.times:
            cursor.execute(query, (time, ))

    def __create_categories(self):
        cursor = self.conn.cursor()
        for category in self.categories:
            cursor.execute("INSERT INTO nrgweb_apparaatcategorie (categorie) VALUES(?)", (category, ))


    def generate_test_data(self):
        # Create the times.
        self.__create_times()
        # Create the devices.
        device_ids = self.__create_devices()
        # Create categories
        self.__create_categories()

        generated_households = 0
        entries_per_postcode = int(math.ceil(self.num_households * 1.0 / (self.postcode_last - self.postcode_first)))

        # Get the cursor and start the transaction.
        cursor = self.conn.cursor()

        current_postcode = self.postcode_first
        while generated_households < self.num_households:
            postcode_index = 0
            street_index = 0
            while postcode_index < entries_per_postcode and generated_households < self.num_households:
                street = self.streets[street_index]
                housenum = postcode_index + 1
                postcode = str(current_postcode) + self.postcode_suffixes[street_index]
                email = str(generated_households) + "@user.nl"
                print('{0} {1} ({2})'.format(street, housenum, postcode))

                # Create the huishouden
                query = "INSERT INTO nrgweb_huishouden (straat, huisnummer, huisnummer_toevoeging, "
                query += "woonplaats, postcode, aantal_personen, email, telefoonnummer, password) "
                query += "VALUES(?, ?, '', 'Grunn', ?, ?, ?, '0506661110', 'generated')"
                cursor.execute(query, (street, housenum, postcode, random.randint(1, 5), email))
                huishouden_id = cursor.lastrowid

                # Assign some random devices
                self.assign_random_devices(huishouden_id, device_ids)
                
                # Reset street index
                street_index += 1
                if street_index >= len(self.streets):
                    street_index = 0
                postcode_index += 1
                generated_households += 1
            # Increment the counter
            current_postcode += 1

        self.conn.commit()

    def assign_random_devices(self, huishouden_id, device_ids):
        max_num = len(device_ids)
        cursor = self.conn.cursor()
        meting_query = "INSERT INTO nrgweb_meting (apparaat_id, datum, tijd, waarde, huishouden_id) VALUES(?, DATE(), ?, ?, ?)"
        # Create a random number of devices.
        for i in range(random.randint(0, max_num)):
            assigned = []
            while True:
                device_id = device_ids[random.randint(0, max_num - 1)]
                if not device_id in assigned:
                    assigned.append(device_id)
                    break

            cursor.execute("INSERT INTO nrgweb_huishoudenapparaat (huishouden_id, apparaat_id) VALUES(?, ?)", (huishouden_id, device_id))
            link_id = cursor.lastrowid
            for time in self.times:
                # Random value between 1.0 and 2.0
                value = round(random.randint(1, 2) * 1.0 + random.random(), 2)
                cursor.execute(meting_query, (link_id, time, value, huishouden_id))
     
if __name__ == '__main__':
    gen = GenerateTestData('nrgdb.sqlite')
    gen.generate_test_data()