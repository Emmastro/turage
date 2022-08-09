from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import *


def home(request):
    # No home for now

    return redirect('ride-request')

# TODO: separate passenger and driver views into different applications
# Passenger views
@method_decorator(login_required, name='dispatch')
class RideRequestView(CreateView):
    """
    """

    model = RideRequest
    fields = "__all__"
    template_name = "request.html"


# Driver views

class RideRequestNearView(ListView):

    model = RideRequest
    fields = "__all__"
    template_name = "request_near.html"
    context_object_name = "ride_requests"


# class RidingRequestViewSet(ModelViewSet):
#     """
#     TODO: This view needs to support the following scenarios:
#         - Driver accepts request
#         - Passenger cancels request
#         - Driver cancels request
#         - Admin check all driving requests
#     """

#     queryset = models.RidingRequest.objects.all()
#     serializer_class = serializers.RidingRequestSerializer

#     # TODO: override the function for adding a driving request


#     @action(detail=False, methods=['POST'], name='accept')
#     def accept(self, request, *args, **kwargs):
#         riding = models.RidingRequest.objects.get(id=request.data['pk'])
#         riding.driver = models.Driver.objects.get(id=request.data['driver'])
#         riding.status = "accepted"
#         riding.full_clean()
#         riding.save()
#         return Response(status=status.HTTP_202_ACCEPTED)

    

# class WaypointViewSet(viewsets.ModelViewSet):

#     queryset = models.Waypoint.objects.all()
#     serializer_class = serializers.WaypointSerializer

#     @action(detail=False, methods=['POST'], name='add-connection')
#     def add_connection(self, request, *args, **kwargs):
#         """
#         Adds waypoints and edges data to an existing waypoint
#         """
#         waypoint = models.Waypoint.objects.get(id=request.data['id'])

#         waypoints = models.Waypoint.objects.filter(
#             id__in=request.data['waypoints'])

#         edges = models.Edge.objects.filter(id__in=request.data['edges'])

#         waypoint.waypoints.add(*waypoints)
#         waypoint.edges.add(*edges)
#         waypoint.full_clean()
#         waypoint.save()
#         response = {
#             "waypoints": list(map(dict, self.serializer_class(waypoint).data)),
#             "edges": list(map(dict, serializers.EdgeSerializer(edges).data))
#         }

#         return Response(status=status.HTTP_202_ACCEPTED, data=response)

#     @action(detail=False, methods=['POST'], name='add-waypoint')
#     def add_multiple(self, request, *args, **kwargs):

#         # TODO: add data validation

#         edges = request.data['edges']

#         all_edge_created = []
#         connection_list = []
#         for edge in edges:

#             edge_saved = models.Edge.objects.create(**edge)
#             all_edge_created.append(edge_saved)

#         waypoints = request.data['waypoints']
#         all_waypoint_created = []
#         for waypoint in waypoints:

#             # The edge set from the spreadsheet is the id of the edge on the list of edge created
#             # for a given API request. The id of the edges need to start from 0, and
#             # increment by 1

#             edge_list = get_list_from_string(waypoint.pop('edges'))
#             connection = get_list_from_string(waypoint.pop('waypoints'))
#             connection_list.append(connection)
#             waypoint_created = models.Waypoint.objects.create(**waypoint)
#             waypoint_created.full_clean()

#             for edge_id in edge_list:
#                 waypoint_created.edges.add(all_edge_created[edge_id])

#             all_waypoint_created.append(waypoint_created)

#         for i, waypoint in enumerate(all_waypoint_created):
#             for connection_id in connection_list[i]:
#                 waypoint.waypoints.add(all_waypoint_created[connection_id])

#         response = {
#             "waypoints": list(map(dict, self.serializer_class(all_waypoint_created, many=True).data)),
#             "edges": list(map(dict, serializers.EdgeSerializer(all_edge_created, many=True).data)),
#         }
        
#         return Response(status=status.HTTP_201_CREATED, data=response)

#     @action(detail=False, methods=['GET'], name='calcule')
#     def calcule(self, request, *args, **kwargs):
#         #result = {}#request.GET['a'] + request.GET['b']
#         result = {int(self.request.GET['a']) + int(self.request.GET['b'])}
#         return Response(status=status.HTTP_201_CREATED, data={'result': result})


# class EdgeViewSet(viewsets.ModelViewSet):

#     queryset = models.Edge.objects.all()
#     serializer_class = serializers.EdgeSerializer

#     # TODO: test return error if extra data are sent on the payload. Check for all views too. [Benson]


# class RidingRequestMatchesViewSet(viewsets.ModelViewSet):
#     """
#     Match multiple driving requests 
#     """
#     queryset = models.RidingRequest.objects.all()
#     serializer_class = serializers.RidingRequestMatchesSerializer

    

# class CarViewSet(viewsets.ModelViewSet):

#     queryset = models.Car.objects.all()
#     serializer_class = serializers.CarSerializer

