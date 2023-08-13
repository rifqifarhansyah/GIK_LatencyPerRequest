import matplotlib.pyplot as plt

throughput = [7.29, 14.56, 21.73, 28.51, 35.15, 42.09, 48.45, 54.22, 61.86, 68.73]

latency = [0.0368387, 0.0365545, 0.037462567, 0.038892575, 0.04100068, 0.0405296, 0.042450729, 0.045604613, 0.043117444, 0.04251794]

# Plotting
plt.figure(figsize=(8, 6))

plt.plot( throughput, latency, label='num_request : 10')


plt.xlabel('Throughput (query/second)')
plt.ylabel('Latency (second)')
plt.title('Throughput vs Latency (Duration 1 s)')
plt.legend()

plt.grid(True)
plt.show()
