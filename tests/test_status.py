from app.models import Status


class TestStatus:
    def test_status_list(self, client):
        status = Status(name='test')
        # todo: использует основную БД, нужно использовать тестовую БД
        response = client.get("/statuses")
        assert response.status_code == 200
        # todo: поменять на тестовые данные
        assert response.content == b'Status list: \n\n1: New\n2: In Progress\n3: Done\n7: BackLog'
        print(response.__dict__)
