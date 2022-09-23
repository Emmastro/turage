from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from .models import *


def home(request):
    # No home for now

    return redirect('passenger-ride-request')

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)


def handler403(request, exception):
    return render(request, '403.html', status=403)

def handler400(request, exception):
    return render(request, '400.html', status=400)


# TODO: separate passenger and driver views into different applications
# Passenger views


@method_decorator(login_required, name='dispatch')
class PassengerRideRequestView(CreateView):
    """
    """

    model = RideRequest
    fields = ['origin_waypoint', 'destination_waypoint', 'time_to_leave']
    template_name = "passenger_request.html"

    def form_valid(self, form):
        form.instance.passenger = Passenger.objects.get(
            pk=self.request.user.pk)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('my-requests-detail', kwargs={'pk': self.object.pk})


class RideRequestNearView(ListView):

    model = RideRequest
    fields = "__all__"
    template_name = "request_near.html"
    context_object_name = "ride_requests"


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



class MyRequestsView(ListView):
    """
    A passenger view of requests after making one
    """
    model = RideRequest
    fields = "__all__"
    template_name = "my_requests.html"
    context_object_name = "ride_requests"
    # TODO: how do we check if the request is matched?


class MyRequestsDetailView(DetailView):
    model=RideRequest

class RideRequestNearDetailView(DetailView):

    model = RideRequest
    fields = "__all__"
    template_name = "request_near_detail.html"
    context_object_name = "ride_request"

    def post(self, *args, **kwargs):
        
        self.object = self.get_object()


        try:
            if self.request.POST['cancel'] == '1':
                pass
                # TODO: should hide the request from this particular driver (or put it on the bottom of the list)
                #self.object.set_status_cancelled()
        except Exception as e:

            if self.request.POST['pickup'] == '1':
                self.object.set_status_accepted()
        else:
            pass
        return render(self.request, self.template_name, self.get_context_data())

def add_connection(request, *args, **kwargs):
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
