import pytest


@pytest.fixture
def payload(task_status, priority):
    return {"title": "Write tests", "status_id": task_status.id, "priority_id": priority.id}


class TestTask:
    def test_create(self, client, payload):
        response = client.post("/tasks", json={**payload, "description": "All endpoints"})

        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "Write tests"
        assert body["description"] == "All endpoints"
        assert body["status_id"] == payload["status_id"]
        assert body["priority_id"] == payload["priority_id"]
        assert body["created_at"] is not None

    def test_create_without_description(self, client, payload):
        response = client.post("/tasks", json=payload)

        assert response.status_code == 201
        assert response.json()["description"] is None

    def test_create_strips_title(self, client, payload):
        response = client.post("/tasks", json={**payload, "title": "  Write tests  "})

        assert response.json()["title"] == "Write tests"

    @pytest.mark.parametrize("field", ["status_id", "priority_id"])
    @pytest.mark.parametrize("value", [999999, 0, -1, 2_147_483_648, 10**30])
    def test_create_unknown_reference(self, client, payload, field, value):
        assert client.post("/tasks", json={**payload, field: value}).status_code == 400

    @pytest.mark.parametrize("title", ["", "   ", "x" * 256, "Wri\x00te"])
    def test_create_invalid_title(self, client, payload, title):
        assert client.post("/tasks", json={**payload, "title": title}).status_code == 422

    def test_create_invalid_description(self, client, payload):
        assert client.post("/tasks", json={**payload, "description": "a\x00b"}).status_code == 422

    def test_list(self, client, payload):
        created = client.post("/tasks", json=payload).json()

        response = client.get("/tasks")

        assert response.status_code == 200
        assert response.json() == [created]

    def test_retrieve(self, client, payload):
        created = client.post("/tasks", json=payload).json()

        response = client.get(f"/tasks/{created['id']}")

        assert response.status_code == 200
        assert response.json() == created

    @pytest.mark.parametrize("task_id", [999999, 2_147_483_648])
    def test_retrieve_not_found(self, client, task_id):
        assert client.get(f"/tasks/{task_id}").status_code == 404
