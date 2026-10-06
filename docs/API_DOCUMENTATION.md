# API Documentation
All protected routes use `Authorization: Bearer <JWT>`.
- POST `/api/auth/register` `{name,email,password}`
- POST `/api/auth/login` `{email,password}`
- GET `/api/auth/me`
- POST `/api/documents/upload` multipart `file`
- GET `/api/documents?q=`
- GET/DELETE `/api/documents/:id`
- POST `/api/ai/ask` `{document_ids:[1],question:"..."}`
- POST `/api/ai/summarize` `{document_id:1,type:"short"}`
- POST `/api/ai/extract` `{document_id:1}`
- POST `/api/ai/compare` `{document_ids:[1,2]}`
- GET `/api/chats`, GET `/api/chats/:id/messages`
