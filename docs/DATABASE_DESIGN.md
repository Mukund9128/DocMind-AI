# Database Design
Users own Documents and Chats. Documents contain DocumentChunks and cached Summaries. Chats contain Messages. Foreign keys use ownership/cascade semantics in ORM models. Important lookup columns such as email, user_id and document_id are indexed.
