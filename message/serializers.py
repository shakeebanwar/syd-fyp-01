from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from account.serializers import UserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    # Define a list of User IDs to be included when creating the ChatRoom
    members = serializers.ListField(write_only=True)
    member = UserSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        exclude = ['id']
    def create(self, validated_data):
        # Extract the list of member IDs from the validated data
        member_ids = validated_data.pop('members', [])
        
        # Create the ChatRoom
        chat_room = ChatRoom.objects.create(**validated_data)
        
        # Set the members for the ChatRoom using the member IDs
        chat_room.member.set(member_ids)
        
        return chat_room
    


class ChatMessageSerializer(serializers.ModelSerializer):
    userName = serializers.SerializerMethodField()
    file_name = serializers.SerializerMethodField()
	# userImage = serializers.ImageField(source='user.image')
    class Meta:
        model = ChatMessage
        fields = ['id', 'chat', 'userName', 'message', 'timestamp', 'file', 'file_name','user']
    def get_file_name(self, obj):
        if obj.file:
            return obj.file.name.replace('chat_attachments/', '')
        return None
    def get_userName(self, Obj):
        return Obj.user.name 
# class ChatMessageSerializer(serializers.ModelSerializer):
# 	userName = serializers.SerializerMethodField()
# 	# userImage = serializers.ImageField(source='user.image')

# 	class Meta:
# 		model = ChatMessage
# 		exclude = ['id', 'chat']

# 	def get_userName(self, Obj):
# 		return Obj.user.name 
