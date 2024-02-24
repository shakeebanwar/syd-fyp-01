import json
from channels.testing import ChannelsLiveServerTestCase
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from .models import ChatRoom, ChatMessage
from account.models import User, OnlineUser
from .consumers import ChatConsumer  # Import your consumer class
import channels

class ChatConsumerTestCase(ChannelsLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.channel_layer = get_channel_layer()

    async def connect_and_accept(self, user_id):
        communicator = self.get_communicator(user_id)
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        return communicator

    async def disconnect(self, communicator):
        await communicator.disconnect()

    def get_communicator(self, user_id):
        return channels.testing.WebsocketCommunicator(
            ChatConsumer.as_asgi(),
            f"/ws/chat/{user_id}/"
        )

    @database_sync_to_async
    def create_user(self, username, first_name, last_name):
        return User.objects.create(username=username, first_name=first_name, last_name=last_name)

    @database_sync_to_async
    def create_room(self, name):
        return ChatRoom.objects.create(name=name)

    async def test_chat_consumer(self):
        # Create a user and a room.
        user = await self.create_user(username="test_user", first_name="John", last_name="Doe")
        room = await self.create_room(name="Test Room")

        # Connect to the WebSocket.
        communicator = await self.connect_and_accept(user.id)

        # Send a message to the WebSocket consumer.
        message = {
            'action': 'message',
            'roomId': room.roomId,
            'message': 'Hello, world!',
            'user': user.id,
        }
        await communicator.send_json(message)

        # Receive and check the response.
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'chat_message')
        self.assertEqual(response['message']['action'], 'message')

        # Disconnect from the WebSocket.
        await self.disconnect(communicator)
