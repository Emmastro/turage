from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import *


def home(request):
    # No home for now

    return redirect('passenger-ride-request')


def automotive(request):

    return render(request, 'automotive.html')

# TODO: separate passenger and driver views into different applications
# Passenger views


@method_decorator(login_required, name='dispatch')
class PassengerRideRequestView(CreateView):
    """
    """

    model = RideRequest
    fields = ['origin_waypoint', 'destination_waypoint']
    template_name = "passenger_request.html"

    def form_valid(self, form):
        form.instance.passenger = Passenger.objects.get(
            pk=self.request.user.pk)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('my-requests-detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class RideRequestView(CreateView):
    """
    """

    model = RideRequest
    fields = "__all__"
    template_name = "request.html"


class RideRequestNearView(ListView):

    model = RideRequest
    fields = "__all__"
    template_name = "request_near.html"
    context_object_name = "ride_requests"
    # TODO: how do we check if the request is matched?


class MyRequestsView(ListView):
    """
    A passenger view of requests after making one
    """
    model = RideRequest
    fields = "__all__"
    template_name = "my_requests.html"
    context_object_name = "ride_requests"
    # TODO: how do we check if the request is matched?

    def get_queryset(self):
        # filter current user
        query = RideRequest.objects.filter(passenger__pk=self.request.user.pk)
        return query


class MyRequestsDetailView(DetailView):
    model = RideRequest
    fields = "__all__"
    template_name = "my_requests_detail.html"
    context_object_name = "ride_request"


class RideRequestNearDetailView(DetailView):

    model = RideRequest
    fields = "__all__"
    template_name = "request_near_detail.html"
    context_object_name = "ride_request"


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


def add_connection(Srequest, *args, **kwargs):
    """
    Adds waypoints and edges data to an existing waypoint
    """
    waypoint = models.Waypoint.objects.get(id=request.data['id'])

    waypoints = models.Waypoint.objects.filter(
        id__in=request.data['waypoints'])

    edges = models.Edge.objects.filter(id__in=request.data['edges'])

    waypoint.waypoints.add(*waypoints)
    waypoint.edges.add(*edges)
    waypoint.full_clean()
    waypoint.save()
