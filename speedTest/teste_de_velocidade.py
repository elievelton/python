import speedtest

st = speedtest.Speedtest()
down_speedt = st.download()
up_speed = st.upload()
ping = st.results.ping
best_server = st.get_best_server()

#convert to Mbps
down_speed = down_speedt / 1_000_000
up_speed_mbps = up_speed / 1_000_000

print(f"Download Speed: {down_speed:.2f} Mbps")
print(f"Upload Speed: {up_speed_mbps:.2f} Mbps")
print(f"Ping: {ping} ms")
print(f"Best Server: {best_server['sponsor']} located in {best_server['name']}, {best_server['country']}")