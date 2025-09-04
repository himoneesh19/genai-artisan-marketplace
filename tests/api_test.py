import requests

BASE_URL = "http://127.0.0.1:5000"

def test_generate_marketing_copy():
    url = f"{BASE_URL}/api/generate_marketing_copy"
    data = {
        "craft_type": "Pottery",
        "description": "Handmade pottery with traditional designs"
    }
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_generate_social_media_post():
    url = f"{BASE_URL}/api/generate_social_media_post"
    data = {
        "craft_type": "Pottery",
        "description": "Handmade pottery with traditional designs"
    }
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_generate_craft_story():
    url = f"{BASE_URL}/api/generate_craft_story"
    data = {
        "craft_type": "Pottery",
        "description": "Handmade pottery with traditional designs"
    }
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

def test_generate_product_visual():
    url = f"{BASE_URL}/api/generate_product_visual"
    data = {
        "craft_type": "Pottery",
        "description": "Handmade pottery with traditional designs"
    }
    response = requests.post(url, data=data)
    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    test_generate_marketing_copy()
    test_generate_social_media_post()
    test_generate_craft_story()
    test_generate_product_visual()
