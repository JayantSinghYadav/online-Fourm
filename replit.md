# Spidy's World Chat — FOURM

## Overview
A real-time chat application that syncs messages across devices using WebSockets. Messages are stored in server memory and broadcast to all connected clients in real-time. Includes admin panel for moderation.

## Project Structure
- `index.html` - Main HTML file with Socket.IO client for real-time chat
- `styles.css` - Styling for the chat interface
- `server.py` - Flask server with Socket.IO for WebSocket communication
- `frontend-chat-no-backend.html` - Original HTML file from the GitHub import (using Firebase)

## Features
- Real-time message synchronization via WebSockets
- Guest user system with persistent names in localStorage
- Online user count display
- Message export functionality
- Responsive design
- Password-protected clear chat (password: 872652)
- Admin panel with password protection (password: 8726520)
- Message read receipts tracking
- Each message shows unique ID

## Admin Features (Password: 8726520)
- View all online users with connection times
- Kick/remove any user from the chat
- Check which users have seen specific messages
- Real-time user management

## Technology Stack
- Frontend: HTML, CSS, JavaScript with Socket.IO client
- Backend: Flask with Flask-SocketIO
- Server: Running on port 5000 (0.0.0.0)
- Real-time: WebSocket connections via Socket.IO

## Passwords
- Clear Chat: 872652
- Admin Panel: 8726520

## Recent Changes
- 2025-11-02: Initial setup for Replit environment
  - Created index.html as the main entry point
  - Replaced Firebase backend with Flask-SocketIO WebSocket server
  - Configured workflow to serve on port 5000
  - Added Python dependencies (flask, flask-socketio, simple-websocket)
  - Fixed permission errors by implementing local backend
  - Added online user count feature
  - Added password-protected clear chat
  - Implemented admin panel with user management
  - Added message read receipts tracking
  - Deployment configured for autoscale
