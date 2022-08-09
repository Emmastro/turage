from django.core.management.base import BaseCommand
from ride.models import Passenger, Driver, RideRequest


class Command(BaseCommand):

    def handle(self, *args, **options):

        for i in range(5):
            
            try:
                passenger = Passenger(username=f'Passenger{i}')
                passenger.set_password(f"Passenger{i}")
                passenger.save()
            except:
                print(f"Passenger{i} already exists")

            try:
                driver = Driver(username=f'Passenger{i}')
                driver.set_password(f"Passenger{i}")
                driver.save()
            except:
                print(f"Driver{i} already exists")

            ride_request = RideRequest(number_passengers=1)
            ride_request.save()
            #ride_request.passenger.add(passenger)
            #ride_request.save()