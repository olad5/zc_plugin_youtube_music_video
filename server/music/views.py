from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomSerializer
from django.http import JsonResponse

from music.utils.access_ops import *
from music.utils.request_client import RequestClient
from django.conf import settings
import json


# TODO: remove logging after testing
import logging
logging.basicConfig(
    level=logging.DEBUG, format="Line %(lineno)d - %(message)s",
)




class SidebarView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        data = {

            "message": "Plugin Sidebar Retrieved",
            "data": {
                "type": "Plugin Sidebar",
                "name": "Music Plugin",
                "description": "Shows Music items",
                "plugin_id": "61360ab5e2358b02686503ad",
                "organisation_id": "6134fd770366b6816a0b75ed",
                "user_id": "6139170699bd9e223a37d91b",
                "group_name": "Music",
                "show_group": False,
                "public_rooms": {
                    "room_name": "music room",
                    "room_id": "613e906115fb2424261b6652",
                    "collection_name": "room",
                    "type": "public_rooms",
                    "unread": 2,
                    "members": 23,
                    "icon": "headphones",
                    "action": "open",
                },
                "joined_rooms": {
                    "title": "general",
                    "room_id": "613e906115fb2424261b6652",
                    "collection_name": "room",
                    "type": "public_rooms",
                    "unread": 2,
                    "members": 23,
                    "icon": "headphones",
                    "action": "open",
                },
            },
            "success": "true"
        }
        return JsonResponse(data, safe=False)


class PluginInfoView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        data = {
            "message": "Plugin Information Retrieved",
            "data": {
                "type": "Plugin Information",
                "plugin_info": {"name": "Music room",
                                "description": ["This is a plugin that allows individuals in an organization to add music and video links from YouTube to a  shared playlist. Users also have the option to chat with other users in the music room and the option to like a song or video that is in the music room library."]
                                },
                "version": "v1",                            
                "scaffold_structure": "Monolith",
                "team": "HNG 8.0/Team Music Plugin",
                "developer_name": "Zurichat Music Plugin",
                "developer_email": "musicplugin@zurichat.com",
                "icon_url": "https://drive.google.com/file/d/1KB9uSWqg0rM21ohsPxGnG8_1xbcdReio/view?usp=drivesdk",
                "photos": "https://drive.google.com/file/d/1KB9uSWqg0rM21ohsPxGnG8_1xbcdReio/view?usp=drivesdk",
                "homepage_url": "https://music.zuri.chat/music/",
                "sidebar_url": "https://music.zuri.chat/music/api/v1/sidebar/",
                "install_url":  "https://music.zuri.chat/music/",
                'ping_url': 'http://music.zuri.chat/music/api/v1/ping'
            },
            "success": "true"
        }
        return JsonResponse(data, safe=False)


class PluginPingView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        server = [
            {'status': 'Success',
             'Report': ['The music.zuri.chat server is working']}
        ]
        return JsonResponse({'server': server})


class MediaView(GenericAPIView):
    def get(self, request):
        payload = {"email": "hng.user01@gmail.com", "password": "password"}

        request_client = RequestClient()

        response = request_client.request(
            method="GET",
            url=f"https://httpbin.org/anything",
            headers={"Content-Type": "application/json"},
            post_data=payload,
        )

        yourdata = response.response_data
        centrifugo_post("channel_name", {"event": "join_room"})
        # results = MediaSerializer(yourdata).data
        return Response(yourdata)



class CreateRoom(APIView):

    def post(self, requests):
        """
         This function is used to create a room
        """


        collection_name = "test_collection"
        data = data_read(collection_name)
        # return Response(data)
        for col in (data['data']):
            if col.get('room_name'):
                collection = (col)
        # Makes sure that only one music room is created
        if (collection['room_name']) == 'music room':
            logging.debug('Room already exists')
            return Response(collection)

        else:
            serializer = RoomSerializer(data=requests.data)

            if serializer.is_valid():
                res = data_write(collection, payload=serializer.data)

            return Response(res )


class RoomInfo(APIView):
    """
     This function is used to retrieve properties of a room
    """
    def get(self, request):


        data = data_read('test_collection')
        # TODO write exception code for invalid collection


        # TODO the for loop below is not needed, you need the filter for that
        # zc core github filter docs not clear
        for col in (data['data']):
            if col.get('room_name'):
                collection = (col)



        return Response(collection)



class UpdateRoom(APIView):

    """
     This function is used to update the properties of a room
    """

    def put(self, request):
        # TODO write exception code for invalid collection
        data = data_read('test_collection')
        for col in (data['data']):
            if col.get('room_name'):
                # gets the music room collection
                collection = col

        payload = json.load(request)
        collection_id  = (collection['_id'])
        response = data_edit('test_collection', payload,
                              object_id=collection_id)
        return Response(response)

