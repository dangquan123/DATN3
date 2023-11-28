import matplotlib.pyplot as plt

x = 10
y = []
rate = 0.01

for i in range(100):
    x = x - rate*(2*x + 3)
    y.append(x**2+3)

plt.plot(y)
plt.xlabel("so_lan")
plt.ylabel("gia_tri")
plt.title("gredient")

plt.show()

print(y[-1])