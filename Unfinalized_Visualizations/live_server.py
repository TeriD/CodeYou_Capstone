from livereload import Server
import webbrowser

# Path to the directory containing your HTML file
path = 'web/'

# Create a new Server instance
server = Server()

# Watch the directory for changes
server.watch(path)

# Serve the directory on port 8000
server.serve(root=path, port=8000, open_url_delay=False)

# Open the web browser to the specified address
webbrowser.open('http://localhost:8000')

print("Server is running at http://localhost:8000")

# Keep the server running
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("Server stopped.")
