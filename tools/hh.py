"""Single Hodgkin–Huxley neuron (classical squid-axon parameters), integrated with RK4."""
import numpy as np
C=1.0; GNa,GK,GL=120.,36.,0.3; ENa,EK,EL=50.,-77.,-54.4
def am(V): return 0.1*(V+40)/(1-np.exp(-(V+40)/10))
def bm(V): return 4*np.exp(-(V+65)/18)
def ah(V): return 0.07*np.exp(-(V+65)/20)
def bh(V): return 1/(1+np.exp(-(V+35)/10))
def an(V): return 0.01*(V+55)/(1-np.exp(-(V+55)/10))
def bn(V): return 0.125*np.exp(-(V+65)/80)
def rhs(y,I):
    V,m,h,n=y
    dV=(I-GNa*m**3*h*(V-ENa)-GK*n**4*(V-EK)-GL*(V-EL))/C
    return np.array([dV,am(V)*(1-m)-bm(V)*m,ah(V)*(1-h)-bh(V)*h,an(V)*(1-n)-bn(V)*n])
def sim(I,T=150,dt=0.01,V0=-65.):
    y=np.array([V0,am(V0)/(am(V0)+bm(V0)),ah(V0)/(ah(V0)+bh(V0)),an(V0)/(an(V0)+bn(V0))])
    N=int(T/dt); out=np.empty(N)
    for i in range(N):
        out[i]=y[0]
        k1=rhs(y,I);k2=rhs(y+dt/2*k1,I);k3=rhs(y+dt/2*k2,I);k4=rhs(y+dt*k3,I)
        y=y+dt/6*(k1+2*k2+2*k3+k4)
    return np.arange(N)*dt,out
if __name__=='__main__':
    for I in [5.5,6.0,6.2,6.3,7,8,10,12,15]:
        t,v=sim(I,T=300)
        sp=t[1:][(v[:-1]<0)&(v[1:]>=0)]
        print(I,len(sp),np.round(sp[:8],1))
