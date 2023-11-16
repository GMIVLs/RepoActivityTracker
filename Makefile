.PHONY: ngrokServer ngrokServerLogger flaskServerRun flaskServerLogger help

ngrokServer:
	./ngrokServer/ngrok http 127.0.0.1:5000

ngrokServerLogger:
	open http://127.0.0.1:4040/inspect/http

flaskServerRun:
	python3 -m src.S1localServer

flaskServerLogger:
	open http://127.0.0.1:5000/

help:
	@echo "Available commands:"
	@echo "ngrokServer        - Run ngrok server"
	@echo "ngrokServerLogger  - Open ngrok server logger in browser"
	@echo "flaskServerRun     - Run Flask server"
	@echo "flaskServerLogger  - Open Flask server logger in browser"


