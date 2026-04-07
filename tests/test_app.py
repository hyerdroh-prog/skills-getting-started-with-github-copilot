from src.app import activities


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in data


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_returns_error_if_already_signed_up(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student is already signed up for this activity"


def test_delete_participant_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Removed {email} from {activity_name}"


def test_delete_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found"
