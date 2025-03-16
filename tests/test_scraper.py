# tests/test_scraper.py
import pytest
from bs4 import BeautifulSoup
from myproject.scraper import parse_table_rows, create_countries_dictionary, fetch_page_html
import requests

# A sample HTML snippet for testing table parsing.
SAMPLE_HTML = """
<table class="wikitable">
    <tr>
        <th>Country</th>
        <th>City</th>
        <th>Population</th>
        <th>Area</th>
    </tr>
    <tr>
        <td>CountryA</td>
        <td>CityA</td>
        <td>1,000</td>
        <td>100 km²</td>
    </tr>
    <tr>
        <td>CountryB</td>
        <td>CityB</td>
        <td>2,500</td>
        <td>200 km²</td>
    </tr>
</table>
"""

@pytest.fixture
def table_rows():
    soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    return table.find_all("tr")[1:]  # Skip header

def test_parse_table_rows(table_rows):
    data_rows = parse_table_rows(table_rows)
    assert len(data_rows) == 2
    assert data_rows[0]["Country"] == "CountryA"
    assert data_rows[0]["Population"] == 1000
    assert data_rows[1]["Area"] == 200.0

def test_create_countries_dictionary(table_rows):
    data_rows = parse_table_rows(table_rows)
    countries_dict = create_countries_dictionary(data_rows)
    assert "CountryA" in countries_dict
    city_data = countries_dict["CountryA"][0]
    assert city_data["City"] == "CityA"
    # Verify population density.
    assert city_data["Population Density"] == 1000 / 100

# Integration test for fetch_page_html by faking network and compliance functions.
class FakeResponse:
    status_code = 200
    text = "<html><body>" + SAMPLE_HTML + "</body></html>"
    def raise_for_status(self):
        pass

def fake_requests_get(url):
    return FakeResponse()

def fake_is_allowed(url, user_agent="*"):
    return True

def test_fetch_page_html(monkeypatch):
    monkeypatch.setattr("myproject.compliance.is_allowed", fake_is_allowed)
    monkeypatch.setattr(requests, "get", fake_requests_get)
    html = fetch_page_html("https://example.com")
    assert "wikitable" in html
