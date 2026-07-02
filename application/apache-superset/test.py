import requests
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect, sync_playwright

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
    uri_sqllab = "http://127.0.0.1:8088/sqllab"

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
        page.wait_for_url("**/login/**")

        # Run the login procedure.
        page.type("input#username", "admin")
        page.type("input#password", "admin")
        page.click("[type=submit]")
        page.wait_for_load_state()

        # Navigate to SQL Lab. Older Superset versions open a query editor tab
        # automatically; newer ones (6.1+) start empty and require creating one.
        page.goto(uri_sqllab)
        page.wait_for_load_state()
        try:
            page.wait_for_selector(".ace_editor", timeout=5000)
        except PlaywrightTimeoutError:
            page.click('[data-test="add-tab-icon"]')

        # Invoke query on SQL Lab.
        # The ace editor's DOM id is randomly generated per tab instance, so
        # look it up by its `ace_editor` class instead of a fixed element id.
        sql = "SELECT region, mountain, height FROM sys.summits LIMIT 42;"
        page.wait_for_selector(".ace_editor")
        editor_id = page.eval_on_selector(".ace_editor", "el => el.id")
        page.evaluate(f"ace.edit('{editor_id}').setValue('{sql}')")
        page.get_by_role("button", name="Run").click()
        page.wait_for_load_state()

        # Verify SQL Lab response.
        locator = page.locator("body")
        # expect(locator).to_contain_text("42 rows")
        expect(locator).to_contain_text("Monte Rosa")

        # That's it.
        browser.close()
