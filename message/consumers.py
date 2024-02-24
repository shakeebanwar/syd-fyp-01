import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatRoom, ChatMessage
from account.models import User, OnlineUser
import base64
from django.core.files.base import ContentFile
from notifications.util import send_message_notification

class ChatConsumer(AsyncWebsocketConsumer):
	def getUser(self, userId):
		return User.objects.get(id=userId)

	def getOnlineUsers(self):
		onlineUsers = OnlineUser.objects.all()
		return [onlineUser.user.id for onlineUser in onlineUsers]

	def addOnlineUser(self, user):
		try:
			OnlineUser.objects.create(user=user)
		except:
			pass

	def deleteOnlineUser(self, user):
		try:
			OnlineUser.objects.get(user=user).delete()
		except:
			pass

	def saveMessage(self, message, userId, roomId):
		userObj = User.objects.get(id=userId)
		chatObj = ChatRoom.objects.get(roomId=roomId)
		chatMessageObj = ChatMessage.objects.create(
			chat=chatObj, user=userObj, message=message
		)
		sender=chatObj.member.exclude(id=userObj.id).first()
		# sendObj=User.objects.get(id=sender.id)
		send_message_notification(sender,userObj.name,roomId)
		return {
			'action': 'message',
			'user': userId,
			'roomId': roomId,
			'message': message,
			# 'userImage': userObj.image.url,
			'userName': userObj.name,
			'timestamp': str(chatMessageObj.timestamp)
		}

	async def sendOnlineUserList(self):
		onlineUserList = await database_sync_to_async(self.getOnlineUsers)()
		chatMessage = {
			'type': 'chat_message',
			'message': {
				'action': 'onlineUser',
				'userList': onlineUserList
			}
		}
		await self.channel_layer.group_send('onlineUser', chatMessage)

	async def connect(self):
		self.userId = self.scope['url_route']['kwargs']['userId']
		self.userRooms = await database_sync_to_async(
			list
		)(ChatRoom.objects.filter(member=self.userId))
		for room in self.userRooms:
			await self.channel_layer.group_add(
				room.roomId,
				self.channel_name
			)
		await self.channel_layer.group_add('onlineUser', self.channel_name)
		self.user = await database_sync_to_async(self.getUser)(self.userId)
		await database_sync_to_async(self.addOnlineUser)(self.user)
		await self.sendOnlineUserList()
		await self.accept()

	async def disconnect(self, close_code):
		await database_sync_to_async(self.deleteOnlineUser)(self.user)
		await self.sendOnlineUserList()
		for room in self.userRooms:
			await self.channel_layer.group_discard(
				room.roomId,
				self.channel_name
			)


	def saveAttachment(self, attachment_data, userId, roomId):
		userObj = User.objects.get(id=userId)
		chatObj = ChatRoom.objects.get(roomId=roomId)
		# Assuming you have an Attachment model with a ForeignKey to ChatMessage
		content = base64.b64decode(attachment_data['content'])
		file = ContentFile(content, name=attachment_data['filename'])

		attachmentObj = ChatMessage.objects.create(
			chat=chatObj, user=userObj, file=file
		)
		return {
            'action': 'attachment',
            'user': userId,
			'file': attachmentObj.get_file_url(),
            'file_name': file.name,
            'userName': userObj.name,
            'timestamp': str(attachmentObj.timestamp)}

	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		action = text_data_json['action']
		roomId = text_data_json['roomId']
		chatMessage = {}

		if action == 'message':
			message = text_data_json['message']
			userId = text_data_json['user']
			chatMessage = await database_sync_to_async(
				self.saveMessage
			)(message, userId, roomId)

		elif action == 'attachment':
			attachment = text_data_json['attachment']
			userId = text_data_json['user']
			chatMessage = await database_sync_to_async(
				self.saveAttachment
			)(attachment, userId, roomId)

		elif action == 'typing':
			chatMessage = text_data_json
		# print(chatMessage)
		# Use send_group instead of send
		await self.channel_layer.group_send(
			roomId,
			{
				'type': 'chat_message',
				'message': chatMessage
			}
		)

	async def chat_message(self, event):
		message = event['message']
		await self.send(text_data=json.dumps(message))





	# async def chat_message(self, event):
	# 	message = event['message']
		
	# 	# Check if 'roomId' is present in the message dictionary
	# 	room_id = message.get('roomId')
		
	# 	if room_id:
	# 		# Send the message to the specified room group
	# 		await self.send_group(room_id, message)
	# 	else:
	# 		# Broadcast the message to all connected clients
	# 		await self.send_all(message)

	# async def send_all(self, message):
	# 	"""
	# 	Broadcasts the given message to all connected clients.
	# 	"""
	# 	await self.send(text_data=json.dumps(message))

	# async def send_group(self, group_name, message):
	# 	"""
	# 	Sends the given message to the given group.
	# 	"""
	# 	await self.channel_layer.group_send(
	# 		group_name,
	# 		{
	# 			'type': 'chat.message',
	# 			'message': message
	# 		}
	# 	)

