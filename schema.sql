CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT);
CREATE TABLE communities (id SERIAL PRIMARY KEY, name TEXT, description TEXT);
CREATE TABLE community_users (community_id INT NOT NULL, user_id INT NOT NULL, admin BOOLEAN DEFAULT FALSE);
CREATE TABLE threads (id SERIAL PRIMARY KEY, community_id INT NOT NULL, title TEXT, content TEXT);
CREATE TABLE thread_messages (id SERIAL PRIMARY KEY, thread_id INT NOT NULL, user_id INT NOT NULL, content TEXT);
CREATE TABLE threads_to_users(user_id INT NOT NULL, thread_id INT NOT NULL, vote INT NOT NULL);
CREATE TABLE messages_to_users (user_id INT NOT NULL, message_id INT NOT NULL, vote INT NOT NULL);

