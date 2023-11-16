from nio import AsyncClient, RoomMessageText
import asyncio
import json

# Configuration
homeserver = 'https://matrix.org'  # Replace with your homeserver URL if different
access_token = ''
room_id = ''  # Replace with your room ID
json_data = 'data.json'  # The file where you saved the received JSON

# Initialize the Matrix client
client = AsyncClient(homeserver, None)
client.access_token = access_token

async def send_message_to_room(room_id, message):
    # Send a message to the room
    response = await client.room_send(
        room_id=room_id,
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": message
        }
    )
    if isinstance(response, RoomMessageText):
        print(f"Message sent to {room_id} with event ID {response.event_id}")
    else:
        print(f"Failed to send message. Response: {response}")

# Define received_data at the top level if it's not part of another function or operation
received_data = None

async def main():
    global received_data  # Ensure that you're referring to the global variable

    # Load the JSON data from a file if it's not already loaded
    if received_data is None:
        try:
            with open('data.json', 'r') as file:
                received_data = json.load(file)
        except FileNotFoundError:
            print("The data file was not found.")
            return
        except json.JSONDecodeError:
            print("The data file does not contain valid JSON.")
            return

    # Now check if received_data has content
    if received_data:
        # Convert the Python dictionary to a JSON string
        #message = json.dumps(received_data, indent=4)
        message = received_data.get('message')
        message = json.dumps(received_data, indent=4)

        # Send the message
        await send_message_to_room(room_id, message)
    else:
        print("No data to send.")

    # Close the client connection
    await client.close()# Run the async main function
asyncio.get_event_loop().run_until_complete(main())

