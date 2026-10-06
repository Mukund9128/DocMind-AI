from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..extensions import db
from ..models import (
    Document,
    DocumentChunk,
    Summary,
    Chat,
    Message
)
from ..services.rag_service import retrieve
from ..services.llm_service import complete

import json


# ==========================================================
# BLUEPRINT
# ==========================================================

bp = Blueprint(
    'ai',
    __name__,
    url_prefix='/api/ai'
)


# ==========================================================
# HELPER: GET DOCUMENTS OWNED BY CURRENT USER
# ==========================================================

def owned(ids, uid):
    return Document.query.filter(
        Document.id.in_(ids),
        Document.user_id == uid
    ).all()


# ==========================================================
# ASK AI / RAG
# ==========================================================

@bp.post('/ask')
@jwt_required()
def ask():

    d = request.get_json() or {}

    try:
        ids = [
            int(x)
            for x in d.get('document_ids', [])
        ]
    except (TypeError, ValueError):
        return jsonify(
            error='Invalid document IDs'
        ), 400

    q = (
        d.get('question')
        or ''
    ).strip()

    uid = int(get_jwt_identity())

    if not ids or not q:
        return jsonify(
            error='document_ids and question are required'
        ), 400

    # ------------------------------------------------------
    # Verify document ownership
    # ------------------------------------------------------

    docs = owned(ids, uid)

    if len(docs) != len(set(ids)):
        return jsonify(
            error='Unauthorized or missing document'
        ), 403

    # ------------------------------------------------------
    # Get document chunks
    # ------------------------------------------------------

    chunks = DocumentChunk.query.filter(
        DocumentChunk.document_id.in_(ids)
    ).all()

    # Semantic retrieval
    hits = retrieve(
        q,
        chunks
    )

    if not hits:
        return jsonify(
            answer=(
                'I could not find sufficient information '
                'in the selected document(s).'
            ),
            sources=[]
        )

    # ------------------------------------------------------
    # Document names
    # ------------------------------------------------------

    names = {
        doc.id: doc.original_filename
        for doc in docs
    }

    # ------------------------------------------------------
    # Build RAG context
    # ------------------------------------------------------

    context = '\n\n'.join(
        f'[Source: {names[h.document_id]}, '
        f'page {h.page_number}] '
        f'{h.content}'
        for h in hits
    )

    # ------------------------------------------------------
    # Ask Gemini
    # ------------------------------------------------------

    try:

        ans = complete(
            (
                'Answer only from supplied context. '
                'If unsupported, say you could not find '
                'sufficient information. '
                'Cite source names/pages in the answer.'
            ),
            f'''Context:
{context}

Question:
{q}
'''
        )

    except Exception as e:
        return jsonify(
            error=str(e)
        ), 503

    # ------------------------------------------------------
    # Prepare citations
    # ------------------------------------------------------

    sources = [
        {
            'document': names[h.document_id],
            'document_id': h.document_id,
            'page': h.page_number,
            'excerpt': h.content[:240]
        }
        for h in hits
    ]

    # ------------------------------------------------------
    # Save chat
    # ------------------------------------------------------

    chat = Chat(
        user_id=uid,
        title=q[:100]
    )

    db.session.add(chat)
    db.session.flush()

    db.session.add_all([
        Message(
            chat_id=chat.id,
            role='user',
            content=q
        ),
        Message(
            chat_id=chat.id,
            role='assistant',
            content=ans,
            sources_json=json.dumps(sources)
        )
    ])

    db.session.commit()

    return jsonify(
        answer=ans,
        sources=sources,
        chat_id=chat.id
    )


# ==========================================================
# SUMMARIZE DOCUMENT
# ==========================================================

@bp.post('/summarize')
@jwt_required()
def summarize():

    d = request.get_json() or {}

    # ------------------------------------------------------
    # Safely read document ID
    # ------------------------------------------------------

    try:
        document_id = int(
            d.get('document_id', 0)
        )
    except (TypeError, ValueError):
        return jsonify(
            error='Invalid document ID'
        ), 400

    # ------------------------------------------------------
    # Summary type
    # ------------------------------------------------------

    summary_type = (
        d.get('type', 'short')
        or 'short'
    ).strip().lower()

    if summary_type not in [
        'short',
        'detailed'
    ]:
        summary_type = 'short'

    uid = int(get_jwt_identity())

    # ------------------------------------------------------
    # Check document ownership
    # ------------------------------------------------------

    doc = Document.query.filter_by(
        id=document_id,
        user_id=uid
    ).first()

    if not doc:
        return jsonify(
            error='Document not found'
        ), 404

    # ------------------------------------------------------
    # STEP 1:
    # CHECK CACHED SUMMARY BEFORE CALLING GEMINI
    # ------------------------------------------------------

    cached = Summary.query.filter_by(
        document_id=document_id,
        summary_type=summary_type
    ).first()

    if cached:

        return jsonify(
            summary=cached.content,
            cached=True,
            message='Saved summary loaded successfully.'
        )

    # ------------------------------------------------------
    # STEP 2:
    # GET DOCUMENT CONTENT
    # ------------------------------------------------------

    chunks = (
        DocumentChunk.query
        .filter_by(
            document_id=document_id
        )
        .order_by(
            DocumentChunk.chunk_index
        )
        .limit(30)
        .all()
    )

    if not chunks:
        return jsonify(
            error=(
                'No document content available '
                'for summarization.'
            )
        ), 400

    text = '\n\n'.join(
        chunk.content
        for chunk in chunks
        if chunk.content
    )

    if not text.strip():
        return jsonify(
            error=(
                'No readable text found '
                'in this document.'
            )
        ), 400

    # ------------------------------------------------------
    # STEP 3:
    # GENERATE SUMMARY
    # ------------------------------------------------------

    try:

        if summary_type == 'detailed':

            instruction = '''
Create a detailed but clear summary of the supplied
document.

Include:
- Main topic
- Important concepts
- Key facts
- Important requirements
- Important dates or deadlines if present
- Final conclusion

Use only information from the supplied document.
Do not invent information.
'''

        else:

            instruction = '''
Create a concise and clear summary of the supplied
document.

Focus on the most important points.

Use only information from the supplied document.
Do not invent information.
'''

        summary = complete(
            instruction,
            f'''
DOCUMENT NAME:
{doc.original_filename}

DOCUMENT CONTENT:

{text}
'''
        )

    except Exception as e:

        return jsonify(
            error=str(e),
            cached=False
        ), 503

    # ------------------------------------------------------
    # STEP 4:
    # SAVE SUMMARY TO MYSQL
    # ------------------------------------------------------

    saved_summary = Summary(
        document_id=document_id,
        summary_type=summary_type,
        content=summary
    )

    db.session.add(
        saved_summary
    )

    db.session.commit()

    # ------------------------------------------------------
    # STEP 5:
    # RETURN GENERATED SUMMARY
    # ------------------------------------------------------

    return jsonify(
        summary=summary,
        cached=False,
        message=(
            'Summary generated and saved successfully.'
        )
    )


# ==========================================================
# EXTRACT INFORMATION
# ==========================================================

@bp.post('/extract')
@jwt_required()
def extract_info():

    d = request.get_json() or {}

    try:
        document_id = int(
            d.get('document_id', 0)
        )
    except (TypeError, ValueError):
        return jsonify(
            error='Invalid document ID'
        ), 400

    uid = int(
        get_jwt_identity()
    )

    # ------------------------------------------------------
    # Check ownership
    # ------------------------------------------------------

    doc = Document.query.filter_by(
        id=document_id,
        user_id=uid
    ).first()

    if not doc:
        return jsonify(
            error='Document not found'
        ), 404

    # ------------------------------------------------------
    # Get document content
    # ------------------------------------------------------

    chunks = (
        DocumentChunk.query
        .filter_by(
            document_id=document_id
        )
        .order_by(
            DocumentChunk.chunk_index
        )
        .limit(30)
        .all()
    )

    if not chunks:
        return jsonify(
            error='No document content available.'
        ), 400

    text = '\n'.join(
        chunk.content
        for chunk in chunks
        if chunk.content
    )

    if not text.strip():
        return jsonify(
            error='No readable text found in this document.'
        ), 400

    # ------------------------------------------------------
    # Extract structured information
    # ------------------------------------------------------

    try:

        result = complete(
            '''
Return valid JSON with these keys:

organizations
people
dates
deadlines
requirements
important_numbers
key_topics
action_items

Use only supplied document text.
Do not invent information.
''',
            text
        )

        return jsonify(
            result=result
        )

    except Exception as e:

        return jsonify(
            error=str(e)
        ), 503


# ==========================================================
# COMPARE TWO DOCUMENTS
# ==========================================================

@bp.post('/compare')
@jwt_required()
def compare():

    d = request.get_json() or {}

    try:

        ids = [
            int(x)
            for x in d.get(
                'document_ids',
                []
            )
        ]

    except (TypeError, ValueError):

        return jsonify(
            error='Invalid document IDs'
        ), 400

    uid = int(
        get_jwt_identity()
    )

    # ------------------------------------------------------
    # Must select exactly two documents
    # ------------------------------------------------------

    if len(ids) != 2:
        return jsonify(
            error='Select exactly two documents'
        ), 400

    # ------------------------------------------------------
    # Verify ownership
    # ------------------------------------------------------

    docs = owned(
        ids,
        uid
    )

    if len(docs) != 2:
        return jsonify(
            error='Unauthorized or missing document'
        ), 403

    document_texts = []

    # ------------------------------------------------------
    # Prepare both documents
    # ------------------------------------------------------

    for doc in docs:

        chunks = (
            DocumentChunk.query
            .filter_by(
                document_id=doc.id
            )
            .order_by(
                DocumentChunk.chunk_index
            )
            .limit(15)
            .all()
        )

        text = '\n'.join(
            f'[Page {chunk.page_number}] '
            f'{chunk.content}'
            for chunk in chunks
        )

        document_texts.append(
            f'''
DOCUMENT NAME:
{doc.original_filename}

DOCUMENT CONTENT:
{text}
'''
        )

    # ------------------------------------------------------
    # Comparison prompt
    # ------------------------------------------------------

    prompt = f'''
You must compare TWO documents.

========================
DOCUMENT 1
========================

{document_texts[0]}


========================
DOCUMENT 2
========================

{document_texts[1]}


Create a complete comparison.

Your response MUST contain all the following sections:

1. Document 1 Summary

2. Document 2 Summary

3. Similarities

4. Differences

5. Important Facts

6. Requirements

7. Dates and Deadlines

8. Contradictions

9. Final Conclusion


IMPORTANT RULES:

- Discuss BOTH documents.
- Use only information from the supplied documents.
- Do not invent information.
- Do not stop after Document 1.
- Clearly explain similarities and differences.
- Mention document names when useful.
- If information for a section does not exist, write:
  "Not found in the supplied documents."
- Keep the response concise but complete.
'''

    # ------------------------------------------------------
    # Generate comparison
    # ------------------------------------------------------

    try:

        comparison = complete(
            '''
You are an enterprise document comparison assistant.

Your job is to compare BOTH supplied documents accurately.

Never invent information.

Always complete every requested comparison section.
''',
            prompt
        )

        return jsonify(
            comparison=comparison
        )

    except Exception as e:

        return jsonify(
            error=str(e)
        ), 503