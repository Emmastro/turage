
from .models import *


def get_string_to_list(string):
    try:
        return [int(a) for a in string.split(";")]
    except:
        return [int(string)]

def add_multiple(waypoints, edges):

    # TODO: add data validation

    all_edge_created = []
    connection_list = []
    for edge in edges.to_dict('records'):

        print(edge)
        edge_saved = Edge.objects.create(**edge)
        all_edge_created.append(edge_saved)

    all_waypoint_created = []
    for waypoint in waypoints.to_dict('records'):

        # The edge set from the spreadsheet is the id of the edge on the list of edge created
        # for a given API request. The id of the edges need to start from 0, and
        # increment by 1

        edge_list = get_string_to_list(waypoint.pop('edges'))
        connection = get_string_to_list(waypoint.pop('waypoints'))
        connection_list.append(connection)
        waypoint_created = Waypoint.objects.create(**waypoint)
        waypoint_created.full_clean()

        for edge_id in edge_list:
            waypoint_created.edges.add(all_edge_created[edge_id])

        all_waypoint_created.append(waypoint_created)

    for i, waypoint in enumerate(all_waypoint_created):
        for connection_id in connection_list[i]:
            waypoint.waypoints.add(all_waypoint_created[connection_id])

