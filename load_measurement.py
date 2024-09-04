import requests
import concurrent.futures
import random
import time

url = "https://apis-public.congtrinhviettel.com.vn/llm"
# url = "http://10.248.243.99:8099/llm"
def send_request(user, id_request):
    data = {
        "InputText": "điều hòa",
        "IdRequest": id_request,
        "NameBot": "ChatBot",
        "User": user,
        "GoodsCode": "",
        "ProvinceCode": "",
        "ObjectSearch": "",
        "PriceSearch": "",
        "DescribeSearch": "",
    }
    
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Check if request was successful
        print(f"User: {user}, IdRequest: {id_request}, Response: {response.json()}")
        print('=================================================================')

    except requests.RequestException as e:
        print(f"Error for User: {user}, IdRequest: {id_request}, Error: {e}")

def load_test(num_requests):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for i in range(num_requests):
            print(f"----------------------------------------{i}")
            user = random.randint(100, 999)  # Random user ID
            id_request = f"{int(time.time()) + i}"  # Unique ID for the request
            futures.append(executor.submit(send_request, user, id_request))
        # Wait for all futures to complete
        concurrent.futures.wait(futures)

# Example usage
t1 = time.time()
load_test(10)  # Send 100 requests
print('time full:',time.time() - t1)