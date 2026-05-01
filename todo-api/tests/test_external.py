from unittest.mock import MagicMock, patch

from app import external_api


def test_get_users_returns_list():
    mock_response = MagicMock()
    mock_response.json.return_value = [{"id": 1, "name": "Leanne Graham"}]
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        result = external_api.get_users()

    assert isinstance(result, list)
    assert result[0]["id"] == 1


def test_get_posts_returns_list():
    mock_response = MagicMock()
    mock_response.json.return_value = [{"id": 1, "title": "Post 1"}]
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        result = external_api.get_posts()

    assert isinstance(result, list)


def test_get_post_by_id():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": 5, "title": "Specific Post"}
    mock_response.raise_for_status = MagicMock()

    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        result = external_api.get_post(5)

    assert result["id"] == 5