from django.core.management.base import BaseCommand
from ride.models import Car, Edge, Passenger, Driver, RideRequest, RideRequestMatched, Waypoint
from django.db.utils import IntegrityError

import pandas as pd

from django.conf import settings

class Command(BaseCommand):
    path = settings.BASE_DIR 
    spreadsheet = path + '/ride/test_data/data_valid.xlsx'
    print(spreadsheet)
    mapping = [
        ('cars', Car),
        ('drivers', Driver),
        ('edges', Edge),
        ('passengers', Passenger),
    ]

    def handle(self, *args, **options):

        # Create test waypoints

        # Create test passengers and drivers

        self.load_spreadsheet_test_data()
        # for i in range(5):
        #     print(f"loop {i}")

        #     passenger = self.demo_passengers(i)
        #     driver = self.demo_driver(i)
        #     waypoint = Waypoint.objects.create(
        #         name=f"Waypoint {i}",
        #         #address=f"Address {i}",
        #         latitude=0,
        #         longitude=0,
        #     )
        #     waypoint.save()
        #     #ride_request = self.demo_ride_request(i, passenger, waypoint)
        #     #self.demo_ride_request_matched(i, driver, ride_request)
        #     # create test ride request
        #     ride_request, ride_request_created = RideRequest.objects.get_or_create(
        #         number_passengers=1, passenger=passenger, driver=driver,
        #         distance=4)
        #     #ride_request.save()

        #     # Match request 1 and 2
        #     if i == 1:

        #         match = RideRequestMatched()
        #         match.save() # save to generate an id
        #         match.matches.add(ride_request)
        #         match.matches.add(RideRequest.objects.get(id=1))
        #         match.save()

    def demo_driver(self, i):
        try:
            driver = Driver(username=f'Driver{i}')
            driver.set_password(f"Driver{i}")
            driver.save()
        except IntegrityError as e:
            print(f"Driver{i} already exists")
        return driver

    def demo_passengers(self, i):
        try:
            passenger = Passenger(username=f'Passenger{i}')
            passenger.set_password(f"Passenger{i}")
            passenger.save()
        except IntegrityError as e:
            print(f"Passenger{i} already exists")
        return passenger

    def load_spreadsheet_test_data(self):
        """
        Tests data for each model can be loaded as expected, 
        and wrong data input returns that appropriate error based on the test cases 
        from the test spreadsheet.
        """

        for (sheet_name, model) in self.mapping:

            data = pd.read_excel(self.spreadsheet, sheet_name=sheet_name)
            data.fillna('', inplace=True)

            if sheet_name == 'drivers':
                cars = data['car']
                data.drop(columns=['car'], inplace=True)
            for row in data.to_dict('records'):
                response_code = row.pop('response_code')
                
                instance = model.objects.create(**row)
                instance.save()