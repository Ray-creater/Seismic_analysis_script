import matplotlib.pyplot as plt 


fig,axes=plt.subplots(1,1)
x_first=[1,2,3,4,5]
y_first=[1,2,3,4,5]
axes.plot(x_first,y_first)
axes.set_title("first")
fig.savefig("first.png")
axes.clear()
x_second=x_first
y_second=y_first.reverse()
axes.plot(x_first,y_first)

fig.savefig("second.png")
