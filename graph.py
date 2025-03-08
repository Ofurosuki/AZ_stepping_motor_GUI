import matplotlib.pyplot as plt

# Given data points
pos = [333000, 280000, 254000, 239000, 229000, 222000, 217000, 213000, 209500]
dist = [2.003, 2.987, 4.041, 5.055, 6.016, 6.996, 7.937, 9.04, 9.995]

# Plotting the data points
plt.figure(figsize=(8, 6))
plt.scatter(pos, dist, color='blue', label='Data Points')

# Adding labels and title
plt.xlabel('Position (m)')
plt.ylabel('Distance (m)')
plt.title('Distance vs. Position')
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
