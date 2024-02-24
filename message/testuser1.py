# import asyncio
# import json
# import websockets

# async def send_message():
#     async with websockets.connect('ws://localhost:8000/ws/users/2/chat/') as websocket:
#         while True:
#             response = await websocket.recv()
#             print("Received response:", response)
            
                
#             #  Handle received messages
#             try:
#                 message_data = json.loads(response)
#                 sender_user_id = message_data.get('user')
#                 print(sender_user_id)
                
#                 if sender_user_id is not None and sender_user_id != 2:
#                     print(f"Received message from user {sender_user_id}: {response}")
                    
#                     # Allow the user to write back
#                     user_response = input("Write your response (or type 'exit' to end): ")
#                     if user_response.lower() == 'exit':
#                         break
                    
#                     # Send the user's response back to the WebSocket
#                     reply_message = {
#                         'action': 'message',
#                         'roomId': 'CqBPC5ZzRnd8cPwjKLQMri',
#                         'message': user_response,
#                         'user': 2,
#                     }
#                     await websocket.send(json.dumps(reply_message))
                        
#             except json.JSONDecodeError:
#                 print("Received non-JSON message:", response)

# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(send_message())
#     loop.close()
import base64
import asyncio
import json
import websockets
async def send_message():
    async with websockets.connect('ws://localhost:8000/ws/users/1/chat/') as websocket:
        start = True
        while True:
            file_path = r'D:\bnr360freelanceplatform\djangoauth\message\views.py'

            with open(file_path, 'rb') as file:
                content = base64.b64encode(file.read()).decode()
        
            attachment_data = {
                'content': content,
                'filename': 'views.py',
                'filetype': 'text/plain',
            }

            attachment_message = {
                'action': 'attachment',
                'roomId': '7nG26k8qFPugkQwvQM6UJQ',  # Replace with the actual room ID
                'attachment': attachment_data,
                'user': 3,  # Replace with the actual user ID
            }
            if start:
                await websocket.send(json.dumps(attachment_message))
                start = False
            response = await websocket.recv()

            
                
             # Handle received messages
            try:
                message_data = json.loads(response)
                sender_user_id = message_data.get('user')
                
                if sender_user_id is not None and sender_user_id != 3:
                    print(f"Received message from user {sender_user_id}: {response}")
                    
                    # Allow the user to write back
                    user_response = input("Write your response (or type 'exit' to end): ")
                    if user_response.lower() == 'exit':
                        break
                    
                    # Send the user's response back to the WebSocket
                    reply_message = {
                        'action': 'message',
                        'roomId': '7nG26k8qFPugkQwvQM6UJQ',
                        'message': user_response,
                        'user': 1,
                    }
                    await websocket.send(json.dumps(reply_message))
                        
            except json.JSONDecodeError:
                print("Received non-JSON message:", response)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())
    loop.close()

