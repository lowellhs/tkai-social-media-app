import matplotlib.pyplot as plt

iteration = ["1", "2", "3", "4"]

home_before_y   = [38.38, 37.70, 37.43, 38.58]
home_after_y    = [38.46, 35.06, 64.26, 65.47]

plt.plot(iteration, home_before_y, '-ob', label="Sebelum autoscaling")
plt.plot(iteration, home_after_y, '-og', label="Sesudah autoscaling")
plt.ylabel("requests per second")
plt.xlabel("pengujian ke-")
plt.legend(loc="upper left")
plt.show()

iteration = ["1", "2", "3", "4"]

profile_before_y   = [13.47, 13.21, 13.12, 13.31]
profile_after_y    = [13.02, 20.03, 20.37, 25.30]

plt.plot(iteration, profile_before_y, '-ob', label="Sebelum autoscaling")
plt.plot(iteration, profile_after_y, '-og', label="Sesudah autoscaling")
plt.plot(["3"], profile_after_y[2], 'or')
plt.ylabel("requests per second")
plt.xlabel("pengujian ke-")
plt.legend(loc="upper left")
plt.show()