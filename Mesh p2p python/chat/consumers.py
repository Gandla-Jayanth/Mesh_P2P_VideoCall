import json
from channels.generic.websocket import AsyncWebsocketConsumer

class VideoCallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'video_pool'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        
        # Broadcast to others that a new user connected
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'sender_channel_name': self.channel_name
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
        # Notify others
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'sender_channel_name': self.channel_name
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        # --- CRITICAL FIX: Add the Sender's ID to the payload ---
        # This tells the recipient who is speaking to them
        data['callerId'] = self.channel_name

        if action == 'offer':
            await self.channel_layer.send(
                data['target'],
                {
                    'type': 'send_offer',
                    'payload': data
                }
            )
        
        elif action == 'answer':
            await self.channel_layer.send(
                data['target'],
                {
                    'type': 'send_answer',
                    'payload': data
                }
            )
            
        elif action == 'ice-candidate':
            await self.channel_layer.send(
                data['target'],
                {
                    'type': 'send_ice_candidate',
                    'payload': data
                }
            )

    # --- Handlers for Group Messages ---

    async def user_joined(self, event):
        # Don't send "user joined" to the person who just joined
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'action': 'user-connected',
                'userId': event['sender_channel_name']
            }))

    async def user_left(self, event):
        await self.send(text_data=json.dumps({
            'action': 'user-disconnected',
            'userId': event['sender_channel_name']
        }))

    async def send_offer(self, event):
        await self.send(text_data=json.dumps(event['payload']))

    async def send_answer(self, event):
        await self.send(text_data=json.dumps(event['payload']))

    async def send_ice_candidate(self, event):
        await self.send(text_data=json.dumps(event['payload']))