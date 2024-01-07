import requests
from playwright.sync_api import sync_playwright

from util import get_auth_headers


uri_dataset = "http://127.0.0.1:8088/api/v1/dataset/"
uri_chart = "http://127.0.0.1:8088/api/v1/chart/data"


def test_api():
    """
    Create datasets and probe creating a graph using the Superset HTTP API.
    """
    requests.post(
        uri_dataset,
        headers=get_auth_headers(),
        json={"database": 1, "schema": "sys", "table_name": "summits"},
    ).raise_for_status()

    graph_request = {
      "datasource": {
        "id": 1,
        "type": "table"
      },
      "queries": [
        {
          "metrics": [
            "count"
          ]
        }
      ],
      "result_format": "json",
      "result_type": "full",
    }
    response = requests.post(uri_chart, headers=get_auth_headers(), json=graph_request)
    response.raise_for_status()
    assert response.status_code == 200
    result = response.json()["result"][0]
    assert result["data"] == [{'count': 1605}]


def test_ui():
    """
    Log in to Superset UI, navigate to SQL Lab, and exercise a query.
    """
    uri_home = "http://127.0.0.1:8088/"
    uri_sqllab = "http://127.0.0.1:8088/superset/sqllab"

    with sync_playwright() as p:
        browser = p.firefox.launch(
            headless=True,
            firefox_user_prefs={
                "network.cookie.cookieBehavior": 4,
                "security.insecure_field_warning.contextual.enabled": False,
                "security.certerrors.permanentOverride": False,
                "network.stricttransportsecurity.preloadlist": False,
                "security.enterprise_roots.enabled": True,
                "security.mixed_content.block_active_content": False,
            })

        # Navigate to Apache Superset.
        page = browser.new_page()
        page.goto(uri_home)

        # Run the login procedure.
        assert page.text_content(".panel-title") == "Sign In"
        assert page.url.endswith("/login/")
        page.type("input#username", "admin")
        page.type("input#password", "admin")
        page.click("input[type=submit]")

        # Verify login was successful, and being navigated to `Home`.
        html_title = page.text_content("title").strip()
        assert html_title == "Superset"
        assert page.url.endswith("/superset/welcome/")

        # Invoke SQL Lab with an example query, and verify response.
        sql = "SELECT * FROM sys.summits LIMIT 42;"
        page.goto(uri_sqllab)
        page.wait_for_selector("#ace-editor")
        page.evaluate(f"ace.edit('ace-editor').setValue('{sql}')")
        page.get_by_role("button", name="Run").click()
        page.wait_for_timeout(500)
        page_body = page.text_content("div.ant-tabs-content-holder")
        assert "42 rows returned" in page_body
        assert "Monte Rosa" in page_body

        # That's it.
        browser.close()
