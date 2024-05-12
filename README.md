# Web-Project
### Database Schema

**SQL Schema**

### Project Environment

**Git Repo**

### Authentication

Token-based authentication for users using JWT (JSON Web Tokens) for generating and verifying tokens.

- Token endpoint for user login and registration
- Ensures unique user's username and email.

### Forum Functionality

- Endpoints to create topics and replies
- Endpoints to view categories and topics + search, sort_by, pagination options
- Endpoints to view replies and their votes
- Voting functionality (like/dislike)
- Only authenticated users can vote, create replies and topics.
- Creator of topic can choose the best reply to his topic.

### Messaging System

- Endpoints for creating, viewing, and managing messages between users
- Messages are addressed to specific users
- Users can view conversations

### Voting System

- Endpoints to allow users to like/dislike replies
- Logic to prevent users from upvoting a reply multiple times

### Best Reply Feature

- Endpoint for choosing topic's best reply
- Only the topic author can select the best reply

### Testing
- Postman tests
