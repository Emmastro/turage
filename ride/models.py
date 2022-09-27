import logging

from django.db import models
from datetime import datetime
from django.utils import timezone
from django.core.exceptions import ValidationError


ALLOWED_TIME_DIFFERENCE = 30

from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: move user related models to accounts

class TurageUser(AbstractUser):
    """
    User profile.
    """

    gender = models.CharField(max_length=6, choices=[
                              ('Male', 'M'), ('Female', 'F')], blank=True)
    country = models.CharField(max_length=50, blank=True)
    national_id = models.IntegerField(null=True, blank=True)

    last_latitude = models.FloatField(null=True, blank=True)
    last_longitude = models.FloatField(null=True, blank=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    class Meta:

        verbose_name = 'Abstract User'



class Car(models.Model):
    """
    Docstring for Car.
    """
    model = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    nbr_seats = models.IntegerField()
    seat_used = models.IntegerField(default=0)
    plate_number = models.CharField(max_length=50)

    def __str__(self):
        return self.model +" " + self.plate_number

class Edge(models.Model):
    """
    Docstring for Edge.
    """
    distance = models.FloatField()
    # TODO: add relevant information about the edge/road linking the two nodes


class Waypoint(models.Model):
    """
    A waypoint is a Node or Vertice in the Network. It represents a picking or dropping point for a ride.
    A waypoint can be connected to 1 or more other waypoints, and their edges, saving data like distance between them or some other meta data
    are saved on the same index as the referenced node from the waypoints attribute.

    For example:
             (ab)           (ac) 
        A --------> B, A -------> C
        For Node A, the Node it's connected to are B and C, and they will be saved in that order on the waipoints attribute. 
        The edges of this connection, ab and ac will be saved in the attribute edges in the same order (ab, ac).

    So, when one cary for Nodes connected to A, they get B and C in this order, and when they cary for the edges, they get ab and ac in this order
    So, B would be matched to ab, the edge connecting it to A, and C to ac, the edge connecting it to A.
    """
    name = models.CharField(max_length=255, blank=False, null=False)
    waypoints = models.ManyToManyField('self', blank=True)
    edges = models.ManyToManyField('Edge', blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def clean(self):

        if self.name == '':
            raise ValidationError('Empty error message')
        
        return super().clean()

    def __str__(self) -> str:
        return self.name

class Driver(TurageUser):

    driver_license = models.CharField(max_length=50)
    direction = models.IntegerField(default=0)
    # TODO: add additional field for content from the driving licence
    #car = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Driver'

class Passenger(TurageUser):
    # TODO: would be community to be more general
    university = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Passenger'


class RideRequest(models.Model):
    """
    Represents a request for a ride.
    """

    # data collected when making a driving request
    origin_waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE, related_name='start_waypoint', null=True)
    destination_waypoint = models.ForeignKey(Waypoint, on_delete=models.CASCADE, related_name='destination_waypoint', null=True)
    number_passengers = models.IntegerField(default=1)

    time_requested = models.DateTimeField(auto_now_add=True, null=True)

    # the suggested time to leave. We consider by default users wants to leave as soon as possible
    # but they can choose to leave at a later time (in 1h, 2h, 3h, etc)
    time_to_leave = models.DateTimeField(auto_now_add=True, null=True)

    # Updates When a driver accepts driving request 
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)

    # TODO: status should be a choice field of waiting, accepted or cancelled
    status = models.CharField(max_length=30, default="waiting")

    time_accepted = models.DateTimeField(null=True, blank=True)
    time_cancelled = models.DateTimeField(null=True, blank=True)
    time_finished = models.DateTimeField(null=True, blank=True)

    # when the user makes a request, we set the price of the ride
    price = models.FloatField(null=True, blank=True)

    estimated_time = models.FloatField(null=True, blank=True)
    actual_time = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True) # TODO: handle unit. Default to Km
    # number of riding request this request has been matched with
    matched = models.BooleanField(default=False) # TODO: should not be changed outside the RideRequestMatched model
    

    def save(self, *args, **kwargs):
        """
        Save a Riding request, and try to match with existing requests. If there is no match,
        the matched field would stay False. This would allow on the next RidingRequest.save() 
        from a different request to try to match again.
        """

        if self.status == 'accepted':
            self.time_accepted = datetime.now(tz=timezone.utc)
            #alternative for datetime.now(tz=timezone.utc) ==> datetime.utcnow()
        elif self.status == 'finished':
            self.time_finished = datetime.now(tz=timezone.utc)

        elif self.status == 'cancelled':
            # TODO: should allow both drivers and passengers to cancel a request
            self.time_cancelled = datetime.now(tz=timezone.utc)

        else:
            # TODO: logging.info("check if the requests can be matched")

            super(RideRequest, self).save(*args, **kwargs)

            # TODO: remove comment to match the request
            logging.warning("not checking matching requests")
            # self.match_requests()
            return

        super(RideRequest, self).save(*args, **kwargs)

    def match_requests(self):
        """
            Check available driving requests to match
        """ 

        # filter request that haven't been accepted by a driver yet
        pending_reqests = RideRequest.objects.filter(status="waiting")

        # TODO: Time filter:
        #   filter requests that are  within 30min of the time suggested to leave
        #   of the current request

        def filter_time(request):

            time_diff = (request.time_to_leave-self.time_to_leave).total_seconds()/60
            if time_diff < ALLOWED_TIME_DIFFERENCE: 
                return True
            return False

        # list of all pending requests within the time the current request wants to leave 
        pending_reqests = filter(filter_time, pending_reqests)
        
        # Will contain the 
        pending_request_shortest_paths = []
        for pending_request in list(pending_reqests):

            pending_request_shortest_paths.append(
                self.get_shortest_path(pending_request.origin_waypoint, pending_request.destination_waypoint)
                )
        pending_request_shortest_paths = ["".join(x) for x in pending_request_shortest_paths]
        matches = []
        for i, path_i in enumerate(pending_request_shortest_paths):
            for j, path_j in enumerate(pending_request_shortest_paths):
                if i != j and path_i in path_j:
                    matches.append((path_i, path_j))

        print("Match found: ", matches)

    def get_shortest_path(self, waypoint1, waypoint2):
        """
        return: shortest path between the origin point of a request and the destination
        """    

        path = {}
        adj_node = {}
        queue = []
        waypoints = Waypoint.objects.all()
        waypoint1, waypoint2 = waypoint1.name, waypoint2.name
        logging.info(f"Searching shortest path for {waypoint1} and {waypoint2}")

        for node in waypoints:
            path[node.name] = float("inf")
            adj_node[node.name] = None
            queue.append(node.name)
            
        path[waypoint1] = 0
        
        while queue:        
            key_min = queue[0]
            min_val = path[key_min]
            for n in range(1, len(queue)):
                if path[queue[n]] < min_val:
                    key_min = queue[n]  
                    min_val = path[key_min]
            cur = key_min
            queue.remove(cur)

            for waypoint, edge in zip(
                Waypoint.objects.get(name=cur).waypoints.all(),
                Waypoint.objects.get(name=cur).edges.all()
                ):

                alternate = edge.distance + path[cur]
                
                if path[waypoint.name] > alternate:
                    path[waypoint.name] = alternate
                    adj_node[waypoint.name] = cur 

            #logging.info(f"PATH {path}")
            #logging.info(f"ADJ {adj_node}")
            #logging.info(f"QUEUE {queue}")

        shortest_path = []
        shortest_path.append(waypoint2)

        while True:
            waypoint2 = adj_node[waypoint2]
            if waypoint2 is None:
                break
            shortest_path.insert(0, waypoint2)

        logging.info(f"Shortest path found: {shortest_path}")
        return shortest_path

        
class RideRequestMatched(models.Model):
    """
    Represents driving request Matches
    Matched requests can be accepted by a driver as a unit request, thus, should inherit the accepting, cancelling ...
    behaviour of simple (not matched) riding requests

    TODO: create a logic for how the pricing changes based on the matched requests
    """
    matches = models.ManyToManyField(RideRequest)
    time_created = models.DateTimeField(auto_now_add=True)
    
    time_updated = models.DateTimeField(null=True)

    time_accepted = models.DateTimeField(null=True)
    time_cancelled = models.DateTimeField(null=True)
    time_finished = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):

        super(RideRequestMatched, self).save(*args, **kwargs)
        for match in self.matches.all():
            match.matched = True
            match.save()
        