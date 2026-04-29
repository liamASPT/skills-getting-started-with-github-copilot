from urllib.parse import quote

from src import app as app_module


def test_remove_success_removes_participant(client):
    activity_name = "Chess Club"
    email = app_module.activities[activity_name]["participants"][0]

    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/remove",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]


def test_remove_unknown_activity_returns_404(client):
    response = client.post(
        f"/activities/{quote('Unknown Club', safe='')}/remove",
        params={"email": "someone@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_non_member_returns_400(client):
    activity_name = "Chess Club"

    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/remove",
        params={"email": "not_member@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
