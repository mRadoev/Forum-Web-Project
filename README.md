# Web-Project
### Database Schema

**SQL Schema**

### Project Environment

**Git Repo**

### Authentication

Token-based authentication for users using JWT (JSON Web Tokens) for generating and verifying tokens.

- Token endpoint for user login and registration
- Ensures unique users

### Forum Functionality

- Endpoints to create, read, update, and delete topics and replies
- Implementation of categories
- Administrators can manage users, topics, and categories

### Messaging System

- Endpoints for creating, viewing, and managing messages between users
- Messages are addressed to specific users
- Users can view conversations

### Voting System

- Endpoints to allow users to upvote replies
- Logic to prevent users from upvoting a reply multiple times

### Best Reply Feature

- Endpoint for the topic author to choose the best reply for their topic
- Only the topic author can select the best reply

### Testing

- Unit tests for each endpoint to ensure they behave as expected
- Postman tests
