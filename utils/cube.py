import requests as rq
from bs4 import BeautifulSoup
def cube():
    # Fetch the webpage content
    url = "https://www.cathaybk.com.tw/cathaybk/personal/product/credit-card/cards/cube-list/"
    html = rq.get(url).text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    cube = {}
    # Function to check if an element has the specified attribute or class
    def match_element(element):
        if element.has_attr('data-ga-lv3-title'):
            return True
        elif 'cubre-a-blockTitle' in element.get('class', []):
            if "3%" in element.get_text(strip=True) and len(element.get_text(strip=True)) <= 5:
                return True
        return False

    # Traverse the entire HTML document and print matching elements
    tmp = ""
    for element in soup.find_all():
        if 'cubre-a-blockTitle' in element.get('class', []):
            if "3%" in element.get_text(strip=True) and len(element.get_text(strip=True)) <= 5:
                tmp = element.get_text(strip=True).replace("3%","")
                cube[tmp] = []
        if element.has_attr('data-ga-lv3-title'):
            cube[tmp].append(element.get_text(strip=True).upper())
    return cube
def find_key_for_value(target_value = "7-11" ):
    cube = cube()
    target_value = target_value.upper()
    for key, value in cube.items():
        if target_value in value:
            return target_value + " is " + key
        for item in value:
            if target_value in item:
                return item + " is " + key 
    return None
if __name__ == '__main__':
    find_key_for_value()
    
