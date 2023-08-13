import requests
import time
from concurrent.futures import ThreadPoolExecutor

# Fungsi untuk mengukur latency
def measure_latency(num_requests):
    jsonquery = {
        "Ls": 256,
        "query_id": 1234,
        "query": [0.00407, 0.01534, 0.02498],
        "k": 10
    }


    start_time = time.time()  # Catat waktu mulai
    for _ in range(num_requests):
        response = requests.post('http://localhost:3001', json=jsonquery)
        # print(f"Response Latency {_} : {response.text}")
    end_time = time.time()    # Catat waktu selesai

    latency = end_time - start_time
    return latency


# Fungsi untuk mengukur throughput dengan threading
def measure_throughput(num_requests, duration, num_clients):
    jsonquery = {
        "Ls": 256,
        "query_id": 1234,
        "query": [0.00407, 0.01534, 0.02498],
        "k": 10
    }

    # Fungsi yang akan dieksekusi oleh setiap thread
    def make_request(_):
        for i in range(num_requests):
            start_time = time.time()
            response = requests.post('http://localhost:3001', json=jsonquery)
            # print(f"Response throughput {_} , {i}: {response.text}")
            end_time = time.time()
            latencyPerResponse = end_time - start_time
            print(f"Latency {i+1} : {latencyPerResponse:.6f}")
            time.sleep(duration / num_requests)

    start_time = time.time()  # Catat waktu mulai

    # Membuat ThreadPoolExecutor dengan jumlah thread sesuai num_clients
    with ThreadPoolExecutor(max_workers=num_clients) as executor:
        # Mengeksekusi fungsi make_request sebanyak num_clients kali menggunakan thread pool
        executor.map(make_request, range(num_clients))
        print(f"Num Clients: {num_clients}")
        print(f"Num Request: {num_requests}")

    end_time = time.time()    # Catat waktu selesai

    elapsed_time = end_time - start_time
    throughput = (num_requests * num_clients) / elapsed_time

    return throughput

num_requests = 10
# Mengukur dan mencetak latency
latency = measure_latency(num_requests)
print(f"Latency: {latency:.6f} seconds")

# Mengukur dan mencetak throughput (misalnya, 50 permintaan dalam 10 detik dengan 3 client)
duration = 1
num_clients = 1
throughput = measure_throughput(num_requests, duration, num_clients)
print(f"Throughput: {throughput:.2f} queries per second")
