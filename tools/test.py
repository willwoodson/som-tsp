import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(0,20000,10000)

plt.figure()

plt.subplot(2,2,1) # 2行2列 第1个
t = 1000
y = 0.34*(1-np.exp(-x/t))
plt.plot(x,y,color='red',linewidth=3.0,linestyle='-')
plt.title('t = 1000')


plt.subplot(2,2,2) 
t = 2000
y = 0.34*(1-np.exp(-x/t))
plt.plot(x,y,color='red',linewidth=3.0,linestyle='-')
plt.title('t = 2000')

plt.subplot(2,2,3) 
t = 3000
y = 0.34*(1-np.exp(-x/t))
plt.plot(x,y,color='red',linewidth=3.0,linestyle='-')
# plt.title('t = 3000')

plt.subplot(2,2,4) 
t = 4000
y = 0.34*(1-np.exp(-x/t))
plt.plot(x,y,color='red',linewidth=3.0,linestyle='-')
# plt.title('t = 4000')

plt.show()
