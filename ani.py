import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import updater

# Fixing random state for reproducibility
np.random.seed(19680801)

zer = np.zeros(41)
x_axis = np.arange(-20,21)



# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0.1, 0.1, 0.85, 0.85], frameon=False)
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)

n_points = 10

position = updater.getAllReqs()
positionboys = updater.getAllBoys()


plt.plot(x_axis,zer,c='black', linewidth=0.5)
plt.plot(zer,x_axis,c='black', linewidth=0.5)
plt.xlabel('X - AXIS')
plt.ylabel('Y - AXIS')
scat = ax.scatter(position[:, 0], position[:, 1], c='r',s=10)
scat3 = ax.scatter(positionboys[:, 0], positionboys[:, 1], c='purple',s=10)
scat4 = ax.scatter(0, 0, c='b',s=10)

def update(frame_number):
	position = updater.getAllReqs()
	scat.set_offsets(position)
	positionboys = updater.getAllBoys()
	scat3.set_offsets(positionboys)
	


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=100)


plt.show()