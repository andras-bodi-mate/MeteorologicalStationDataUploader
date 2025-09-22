import uvicorn
import logging

from server import Server

def main():
    server = Server()
    uvicorn.run(server.app, host = "127.0.0.1", port = 8000, log_level = logging.WARNING)

if __name__ == "__main__":
    main()