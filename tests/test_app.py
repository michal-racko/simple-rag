import uuid
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from api.v1.app import app, get_db


@pytest.fixture
def client(db_session):
    def _override_get_db():
        return db_session

    app.dependency_overrides[get_db] = _override_get_db
    return TestClient(app)


def test_get_conversation(client,
                          db_conversation,
                          db_question,
                          db_answer):
    response = client.get(
        f'/conversations/{db_conversation.id}'
    )
    assert response.status_code == 200
    data = response.json()

    assert data == {
        'id': db_conversation.id,
        'questions': [{
            'text': db_question.text,
            'answer': db_answer.text
        }]
    }


def test_get_conversations_wrong_id(client,
                                    db_conversation,
                                    db_question,
                                    db_answer):
    response = client.get(
        f'/conversations/{uuid.uuid4()}'
    )
    assert response.status_code == 404


def test_post_conversation(client,
                           user_question,
                           chatbot_response):
    with patch('api.v1.app._request_rag') as mock_request_rag:
        mock_request_rag.return_value = chatbot_response
        response = client.post(
            '/conversations/',
            json={'text': user_question}
        )

    assert response.status_code == 201
    data = response.json()

    assert data['questions'][0]['text'] == user_question
    assert data['questions'][0]['answer'] == chatbot_response


def test_post_conversation_wrong_data(client):
    response = client.post(f'/conversations/', json={'abc': 123})
    assert response.status_code == 422


def test_put_conversation(client,
                          db_conversation,
                          db_question,
                          db_answer,
                          user_question,
                          chatbot_response):
    with patch('api.v1.app._request_rag') as mock_request_rag:
        mock_request_rag.return_value = chatbot_response
        response = client.put(
            f'/conversations/{db_conversation.id}',
            json={'text': user_question}
        )

    assert response.status_code == 200
    data = response.json()

    assert data == {
        'id': db_conversation.id,
        'questions': [
            {
                'text': db_question.text,
                'answer': db_answer.text
            },
            {
                'text': user_question,
                'answer': chatbot_response
            }
        ]
    }


def test_put_conversation_wrong_id(client,
                                   user_question):
    response = client.put(
        f'/conversations/{uuid.uuid4()}',
        json={'text': user_question}
    )
    assert response.status_code == 404


def test_put_conversation_wrong_data(client,
                                     db_conversation):
    response = client.put(
        f'/conversations/{db_conversation.id}',
        json={'abc': 123}
    )
    assert response.status_code == 422
