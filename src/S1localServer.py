import os
from flask import Flask, request, render_template_string
import json
import subprocess

PORT = int(os.getenv('PORT'))


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        received_data = request.json
        # Write the JSON data to data.json file
        with open('data.json', 'w') as json_file:
            json.dump(received_data, json_file, indent=4, sort_keys=True)

        # Run E2sendingMessageClientElement.py script
        try:
            subprocess.run(["python", "./src/E2sendingMessageClientElement.py"],
                           check=True)
            print("E2sendingMessageClientElement.py executed successfully.")
        except subprocess.CalledProcessError as e:
            print(
                f"An error occurred while executing E2sendingMessageClientElement.py: {e}"
            )

        return 'Data received and E2sendingMessageClientElement.py script executed', 200
    else:
        try:
            # Try to load the data from the file for GET requests
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
                pretty_data = json.dumps(data, indent=4, sort_keys=True)
        except (IOError, json.JSONDecodeError):
            pretty_data = 'No data received yet or data is invalid'
        # Render the data in a simple HTML template when accessed via GET
        return render_template_string("""
            <html>
                <body>
                    <h1>Received JSON Data:</h1>
                    <pre>{{ data }}</pre>
                </body>
            </html>
        """,
                                      data=pretty_data)


if __name__ == '__main__':
    app.run(debug=True, port=PORT)
