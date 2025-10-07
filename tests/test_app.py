def test_get_articles_returns_sorted_results(client):
    response = client.get('/api/articles')
    assert response.status_code == 200

    payload = response.get_json()
    articles = payload["articles"]

    assert [article["id"] for article in articles] == ["article-2", "article-1", "article-3"]
    assert articles[0]["source"]["name"] == "Source B"
    assert articles[0]["saved"] is True
    assert articles[-1]["summary"] == "Summary not available."


def test_get_articles_filters_by_category(client):
    response = client.get('/api/articles?category=technology')
    assert response.status_code == 200

    payload = response.get_json()
    ids = [article["id"] for article in payload["articles"]]

    assert ids == ["article-1", "article-3"]
    assert all(article["category"] == "technology" for article in payload["articles"])
