from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ChatRoomSerializer, ChatMessageSerializer
from .models import ChatRoom, ChatMessage
from rest_framework import generics
from message.renderers import CustomStatusRenderer
from rest_framework.permissions import IsAuthenticated
from account.models import User

# class ChatRoomView(generics.ListCreateAPIView):
#     queryset = ChatRoom.objects.all()
#     serializer_class = ChatRoomSerializer
class ChatRoomView(APIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		chatRoom = ChatRoom.objects.filter(member=request.user.id)
		seller_profile=None
		client_profile=None

		serializer = ChatRoomSerializer(
			chatRoom, many=True, context={"request": request}
		)
		data=serializer.data
		
		user_id_to_remove = request.user.id
		for conversation in data:
    # Filter out members with the specified user_id
			conversation['member'] = [member for member in conversation['member'] if member['id'] != user_id_to_remove]

			# Iterate over remaining members in the conversation
			for member in conversation['member']:
				user_id = member['id']
				user = User.objects.get(id=user_id)
				member['profile'] = None
				print(user_id)
				try:
					if member['role'] == 'seller':
						seller_profile = user.seller.profile_picture
						member['profile'] = seller_profile.profile_picture.url
					elif member['role'] == 'client':
						client_profile = user.client.profile_picture
						member['profile'] = client_profile.profile_picture.url
						print(member)
				except Exception as e:
					print(e)
					continue

		data = [conversation for conversation in data if conversation['member']]
		# print(data)

# # Iterate over each conversation
# 		for conversation in data:
# 			# Filter out members with the specified user_id
# 			conversation['member'] = [member for member in conversation['member'] if member['id'] != user_id_to_remove]

# 		# Remove empty conversations (no members left after filtering)
# 		# data = [conversation for conversation in data if conversation['member']]

# 		# print(data)
# 		member_ids = [member['id'] for item in data for member in item['member']]
# 		for member in conversation['member']:
# 			user_id=member['id']
# 			user = User.objects.get(id=user_id)
# 			member['profile']=None
# 			print(user_id)
# 			try:
# 				if member['role'] == 'seller':
# 					seller_profile=user.seller.profile_picture
# 					member['profile'] = seller_profile
# 				if member['role'] == 'client':
# 					client_profile=user.client.profile_picture
# 					member['profile'] = client_profile
# 					print(member)
# 			except Exception as e:
# 				print(e)
# 				continue
# 		data = [conversation for conversation in data if conversation['member']]
# 		print(data)
		# for user_id in member_ids:
		# 	user = User.objects.get(id=user_id)
		# 	try:
		# 		if user.role == 'seller':
		# 			seller_profile=user.seller.profile_picture
		# 		if User.role == 'client':
		# 			client_profile=user.client.profile_picture
		# 	except:
		# 		pass

		# response_data={
		# 	"chatRooms":serializer.data,
		# 	"seller_profile_pic":seller_profile.profile_picture.url,
		# 	"client_profile_pic":client_profile.profile_picture.url if client_profile and client_profile.profile_picture else None

		# }
		response_data={
			"chatRooms":data,
		}
		return Response(response_data, status=status.HTTP_200_OK)

	def post(self, request):
		serializer = ChatRoomSerializer(
			data=request.data, context={"request": request}
		)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class MessagesView(ListAPIView):
	serializer_class = ChatMessageSerializer
	pagination_class = LimitOffsetPagination
	renderer_classes = [CustomStatusRenderer] 

	def get_queryset(self):
		roomId = self.kwargs['roomId']
		return ChatMessage.objects.\
			filter(chat__roomId=roomId).order_by('timestamp')
