import socketio
import time

# Create a Socket.IO client
sio = socketio.Client()

item_received = False
typing_received = False

@sio.event
def connect():
    print("Connected to server")

@sio.event
def connect_error(data):
    print("The connection failed!")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('receive_message')
def on_message(data):
    global item_received
    print(f"Received message: {data}")
    if data.get('username') == 'SocketTester':
        print("PASS: Message received back correctly.")
        item_received = True

@sio.on('display_typing')
def on_typing(data):
    global typing_received
    print(f"Received typing event: {data}")
    if data.get('username') == 'SocketTester':
        print("PASS: Typing indicator received.")
        typing_received = True

def verify_socket():
    try:
        sio.connect('http://localhost:5000')
        
        # 1. Send Message
        print("\n[1] Sending message via Socket.IO...")
        sio.emit('send_message', {'message': 'Hello Socket', 'username': 'SocketTester'})
        time.sleep(2) # Wait for response
        
        # 2. Send Typing
        print("\n[2] Sending typing event...")
        sio.emit('typing', {'username': 'SocketTester'})
        time.sleep(2) # Wait for response
        
        sio.disconnect()
        
        if item_received and typing_received:
            print("\nSUCCESS: All Socket.IO tests passed.")
        else:
            print(f"\nFAIL: Message: {item_received}, Typing: {typing_received}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    verify_socket()
