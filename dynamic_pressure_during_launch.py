import matplotlib.pyplot as plt
import numpy as np


def density(height: float) -> float:
    """
    Returns the air density in slug/ft^3 based on altitude.
    Equations from
    https://www.grc.nasa.gov/www/k-12/rocket/atmos.html
    :param height: Altitude in feet
    :return: Density in slugs/ft^3
    """
    if height < 36152.0:
        temp = 59 - 0.00356 * height
        p = 2116 * ((temp + 459.7) / 518.6) ** 5.256
    elif 36152 <= height < 82345:
        temp = -70
        p = 473.1 * np.exp(1.73 - 0.000048 * height)
    else:
        temp = -205.05 + 0.00164 * height
        p = 51.97 * ((temp + 459.7) / 389.98) ** -11.388

    rho = p/(1718 * (temp+459.7))
    return rho


def velocity(time: float, acceleration: float) -> float:
    """
    Convert time to velocity using Vf = Vi + at
    (where Vf = final velocity,
    Vi = initial velocity, [0 in this case]
    a = acceleration, t = time
    :param time: int time in seconds
    :param acceleration: acceleration in ft/s^2
    :return: velocity in ft/s
    """
    return acceleration * time


def altitude(time: float, acceleration: float) -> float:
    """
    Convert time to altitude using the
    constant acceleration equation
    x = vi*t + 0.5*a*t^2, where vi = 0 in this case
    :param time: Time in seconds
    :param acceleration: acceleration in ft/s^2
    :return: Altitude in feet
    """
    return 0.5 * acceleration * time**2


plt.style.use("bmh")
y_values = []
x_values = np.arange(0.0, 550.0, 0.5)

for elapsed_time in x_values:
    accel = 51.76  # ft/s^2
    alt = altitude(elapsed_time, accel)
    # Dynamic pressure q = 0.5 * density * velocity^2
    q = 0.5 * density(alt) * velocity(elapsed_time, accel) ** 2
    y_values.append(q)

plt.plot(x_values, y_values, "b-", label=r"a = 51.76 $\frac{ft}{s^2}$")
max_val = max(y_values)
ind = y_values.index(max_val)
plt.annotate(
    "{:.2E} psf @ {} s".format(max_val, x_values[ind]),
    xy=(x_values[ind] + 2, max_val),
    xytext=(x_values[ind] + 15, max_val + 1e5),
    arrowprops=dict(facecolor="blue", shrink=0.05),
)
plt.xlim(0, 125)
plt.xlabel("Time (s)")
plt.ylabel("Pressure (psf)")
plt.title("Dynamic pressure as a function of time")
plt.legend()
plt.show()
