import unittest
import requests

class MainTests(unittest.TestCase):

  def test_web_availability(self):
    """
    Test that the web server is available and returns a 200 status code.

    :param self: instance of the class

    :return: nothing
    """
    url = f"https://www.cash.ch/news/alle?page=1"
    response = requests.get(url)
    # parse html
    result = response.content.decode('utf-8').splitlines()
    self.assertTrue(response.status_code == 200, f"Webpage <{url}> not available. Status code: {response.status_code}")
    self.assertTrue(len(result) > 0, f"Webpage <{url}> returned nothing.")


if __name__ == '__main__':
    unittest.main()

