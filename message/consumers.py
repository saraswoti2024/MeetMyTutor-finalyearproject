import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import CustomUser
from .models import *
from django.db.models import Q
from asgiref.sync import sync_to_async
from urllib.parse import urlparse, parse_qs, urljoin
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        #authenticated user id
        user = self.scope["user"]  
        self.user = user.username
        self.me = user.id
        #from endpoint path bata aako id
        self.other_userid = self.scope.get('url_route').get('kwargs').get('user_id') #reciever 
        # self.user2 = self.other_userid.username
        self.room_name = None
        self.room_group_name = None
        print(self.me,'-----------------------------id1----------')
        print(self.user,'-----------------------------id1u----------')
        print(self.other_userid,'--------------------------id2---------')

        await self.accept()

        if self.other_userid is None:
            await self.close()
            return

        if not self.me : 
            await self.send(text_data=json.dumps({"error": "Authentication required"}))
            await self.close()
            return 
        print('-----------------------------1')
        self.room_name = self.get_room_name(self.me, self.other_userid)
        print("-----------------------------------------------")
        print(self.room_name)
        self.room_group_name = f'chat_{str(self.room_name)}'   
        print(self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name,self.channel_name)

            
    #     history = await self.get_chat_history(self.me,self.other_userid)
    #     await self.send(text_data = json.dumps({'chat_history' : history},cls=DjangoJSONEncoder))

    # @sync_to_async
    # def get_chat_history(self,id1,id2):
    #     message  = Message.objects.filter(
    #             Q(sender_id = id1, receiver_id = id2)| 
    #             Q(sender_id = id2, receiver_id = id1)
    #         ).order_by('-timestamp').values(
    #             'sender__username', 'content', 'timestamp')
    #     return list(message)       
    
      
    async def disconnect(self,code):
      await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self,text_data):
        print(text_data,'data in text')
        data = json.loads(text_data)
        message = data['message']
        receiver = await sync_to_async(CustomUser.objects.get)(id = self.other_userid )
       
        
        message_obj = await sync_to_async(Message.objects.create)(
            sender_id = self.me,
            reciever = receiver,
            content = message,
            title =  self.room_group_name,
        )

        await self.channel_layer.group_send(
            self.room_group_name,{
                'type' : 'chat_message',
                'message' : message,
                'username' : self.user,
                'timestamp': message_obj.timestamp.isoformat()  
            }
        )    
  
    async def chat_message(self,event):
            await self.send(text_data = json.dumps({
                'message' : event['message'],
                'username'  : event['username'],
                'timestamp': event.get('timestamp') 
            }))
    
    def get_room_name(self, id1, id2):
        print(id1,'--------------')
        print(id2,'----------------id2------')
        return f"{min(int(id1), int(id2))}_{max(int(id1), int(id2))}"