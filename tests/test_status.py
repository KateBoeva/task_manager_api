import pytest

from app.models import Task


class TestStatus:
    def test_list(self, client, task_status):
        response = client.get("/statuses")

        assert response.status_code == 200
        assert response.json() == [{"id": task_status.id, "name": "To Do"}]

    def test_retrieve(self, client, task_status):
        response = client.get(f"/statuses/{task_status.id}")

        assert response.status_code == 200
        assert response.json() == {"id": task_status.id, "name": "To Do"}

    def test_retrieve_not_found(self, client):
        assert client.get("/statuses/999999").status_code == 404

    def test_create(self, client):
        response = client.post("/statuses", json={"name": "  Done  "})

        assert response.status_code == 201
        assert response.json()["name"] == "Done"
        assert client.get(f"/statuses/{response.json()['id']}").status_code == 200

    @pytest.mark.parametrize("name", ["", "   ", "x" * 31, "To\x00Do"])
    def test_create_invalid_name(self, client, name):
        assert client.post("/statuses", json={"name": name}).status_code == 422

    def test_create_duplicate_name(self, client, task_status):
        assert client.post("/statuses", json={"name": "To Do"}).status_code == 409

    def test_update(self, client, task_status):
        response = client.put(f"/statuses/{task_status.id}", json={"name": "Doing"})

        assert response.status_code == 200
        assert response.json() == {"id": task_status.id, "name": "Doing"}

    def test_update_same_name(self, client, task_status):
        assert client.put(f"/statuses/{task_status.id}", json={"name": "To Do"}).status_code == 200

    def test_update_not_found(self, client):
        assert client.put("/statuses/999999", json={"name": "Doing"}).status_code == 404

    def test_update_invalid_name(self, client, task_status):
        assert client.put(f"/statuses/{task_status.id}", json={"name": "   "}).status_code == 422

    def test_update_duplicate_name(self, client, task_status):
        other = client.post("/statuses", json={"name": "Done"}).json()

        assert client.put(f"/statuses/{other['id']}", json={"name": "To Do"}).status_code == 409
        assert client.get(f"/statuses/{other['id']}").json()["name"] == "Done"

    def test_delete(self, client, task_status):
        assert client.delete(f"/statuses/{task_status.id}").status_code == 204
        assert client.get(f"/statuses/{task_status.id}").status_code == 404

    def test_delete_not_found(self, client):
        assert client.delete("/statuses/999999").status_code == 404

    def test_delete_used_by_task(self, client, db_session, task_status, priority):
        db_session.add(Task(title="Task", status_id=task_status.id, priority_id=priority.id))
        db_session.commit()

        assert client.delete(f"/statuses/{task_status.id}").status_code == 409
        assert client.get(f"/statuses/{task_status.id}").status_code == 200
