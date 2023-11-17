import os
from nio import AsyncClient, RoomMessageText
import asyncio
import json

homeserver = os.getenv("HOMESERVER")
access_token = os.getenv("ACCESS_TOKEN")
room_id = os.getenv("ROOM_ID")
json_data = os.getenv("JSON_DATA")

# Initialize the Matrix client
client = AsyncClient(homeserver, None)
client.access_token = access_token


async def send_message_to_room(room_id, message):
    # Send a message to the room
    response = await client.room_send(room_id=room_id,
                                      message_type="m.room.message",
                                      content={
                                          "msgtype": "m.text",
                                          "body": message
                                      })
    if isinstance(response, RoomMessageText):
        print(f"Message sent to {room_id} with event ID {response.event_id}")
    else:
        print(f"Failed to send message. Response: {response}")


# Define received_data at the top level if it's not part of another function or operation
received_data = None


async def main():
    # Load the JSON data from a file
    try:
        with open('data.json', 'r') as file:
            received_data = json.load(file)

            # Extract the 'commits' list
            commits_data = received_data.get('commits')
            ref = received_data.get('ref')
            repository_full_name = received_data.get('repository',
                                                     {}).get('full_name')

            if commits_data and isinstance(commits_data, list):
                # Process only the first commit in the list
                first_commit = commits_data[0] if len(
                    commits_data) > 0 else None
                if first_commit:
                    # Extract required fields
                    username = first_commit.get('committer', {}).get(
                        'username', 'Unknown User')
                    message = first_commit.get('message', 'No message')
                    timestamp = first_commit.get('timestamp', 'No timestamp')

                    # Format the message with ref and full_name
                    formatted_message = f"[\U0001F389] at [{timestamp}],\nAuthor: [{username}]\nin Repo: [{repository_full_name}]\non Branch: [{ref}]:\n\U00002728 Message: {message}"

                    # Send the message content
                    await send_message_to_room(room_id, formatted_message)
                else:
                    print("No commits found in the data.")
            else:
                print(
                    "'commits' field is missing or not a list in the JSON data."
                )
    except FileNotFoundError:
        print("The data file was not found.")
    except json.JSONDecodeError:
        print("The data file does not contain valid JSON.")
    finally:
        # Close the client connection
        await client.close()


asyncio.get_event_loop().run_until_complete(main())
