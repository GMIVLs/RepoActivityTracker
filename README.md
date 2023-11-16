# REPO ACTIVITIES TRACKER

![Static Badge](https://img.shields.io/badge/ngrok%20version-3.4.0-blue)
![Static Badge](https://img.shields.io/badge/Python-3.11.5-red)
![Static Badge](https://img.shields.io/badge/Flask-2.2.2-Yellow)
![Static Badge](https://img.shields.io/badge/Werkzeug-2.2.3-red)

## ChangeLog

- `2023-11-16: 23:00`: ngrok server delpoyed, and works flawlessly.

## TODO

- [ ] Automate this to any github repo.
  - [ ] Parsing more fields form data.json
  - [x] Listen to more events
- [x] Adding Makefile to run the commands.

## HOW IT WORKS

The `ngrko` server is used to send messages to our `Element` client using
`Matrix` servre. The processes will track all the changes at our
`AnimationEngineCPP` when any user will push to the repository according to the diagram below.

```sh
+------------------+       +----------------+
| GitHub Repository| ----> | GitHub Webhook |
+------------------+       +----------------+
                                     │
         ┌───────────────────────────┘
         │
         │ (Webhook Trigger on git push event)
         │  [forward ngrok-> 127.0.0.1:<port_number>]
         v
        +---------------+       +---------------------+       +----------------------+
        | ngrok Server  | ----> | Local Flask Server  | <---- |sending_message Script|
        +---------------+       +---------------------+       +----------------------+
                                        |                         [parse data.json]
                           [Listen to 127.0.0.1:<port_number>]
                                        |
                                        |
                                        | (Process & Display JSON)
                                        v
                                   +-----------------+
                                   | Element Client  |
                                   +-----------------+
                                   [Show the message]
```

# NGROK SERVER DETAILS

- GitHub Repository: The starting point where a git push triggers the webhook.
- GitHub Webhook: Activated by the repository's action to send a POST request
  with the JSON payload.
- ngrok Server: Forwards the POST request from the GitHub Webhook to the Local
  Flask Server.
- Local Flask Server: Receives the JSON payload, processes it, displays it in a
  browser, and writes it to data.json.
- sending_message Script: Reads the data.json file and sends a formatted
  message to the Element Client of Matrix.
- Element Client: The final destination where the message is received and
  displayed.
