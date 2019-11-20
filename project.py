
import numpy as np
import random as ran
# import fractions
from sage.misc.randstate import random
import sys

# #n=3, k = 4. gamma=9, T=6
# def modulus(x1,x2,p):
# 	a = x1
# 	b = x2
# 	return mod(a*(b**(p-2)),p)

def mod1(x,p):
	temp = x%p
	if temp>(p*1.0/2):
		temp=temp-p
	return temp
# def mod1(x,p):
# 	temp=x%p
# 	if temp<0:
# 		temp=temp+p
# 	return p

def  CRT(q0_added_t0_p,e_Q_delta,x0):
	sum1 = 0
	for i in range(0,len(q0_added_t0_p)):
		p_cap=x0/q0_added_t0_p[i]
		# print "p_cap:\n",p_cap
		# print "q0_added_t0_p[i]:\n",q0_added_t0_p[i]
		R=IntegerModRing(q0_added_t0_p[i])
		inv_p_cap=1/R(p_cap)
		# print type(ZZ(inv_p_cap))
		# print "inv_p_cap:\n",inv_p_cap
		sum1 = sum1+e_Q_delta[i]*p_cap*ZZ(inv_p_cap)
	sum1=mod1(sum1,x0)
	return sum1

# def GCD(x, y):
# 	gcd=0
# 	small = min(x, y)
# 	for i in range(1, small+1):
# 		if((x % i == 0) and (y % i == 0)):
# 			gcd = i
# 	return gcd 

#ENCRYPTION
def Encryption(Message,Y,X,x0):
	c=0
	for i in range(0,len(Message)):
		c=c+Message[i]*Y[i]
	# j=np.random.randint(0,len(X))
	# sum1=0
	# for k in range(0,j):
	# 	sum1=sum1+X[k]
	# c=c+sum1
	# c=mod(c,x0)
	return c

# def Encryption1(k,M,Q,p,x0,q0,row):
# 	row=max(row+11,2*row+5)
# 	Q1=[-1]*(k+1)
# 	Q1[0] = np.random.randint(0,q0,size=1,dtype='i4')
# 	for i in xrange(1,k+1):
# 		temp = np.random.randint(1,2**(row+1),size=1,dtype='i4')-2**row
# 		print(temp)
# 		Q1[i]=(temp)*Q[i-1]+M[i-1]
# 	print(Q1)
# 	return CRT(Q1,p,x0)

#DECRYTION
def Decryption(p,c,Q):
	M = [0]*len(Q)
	for i in range(0,len(Q)):
		temp = mod1(c,p[i])
		# print temp
		M[i] = mod1(temp,Q[i])
		if M[i] < 0:
			print M[i]+Q[i]
		else:
			print M[i]
	# return M
#--------------------------------#


lamda=6
eta=lamda**2
l_Q=int(eta/8)
se = 16
k=input("Enter length of input Message:")
p=[0]*k
p[0]=next_prime(ZZ.random_element(2**(eta-2),(2**(eta-1))))
for i in range(1,k):
	p[i]=next_prime(p[i-1])
# print "p value:\n",p

row=2*lamda
gamma=lamda**3
T=gamma+lamda
delta=np.identity(k,dtype=int)#[[1,0],[0,1]]
# print delta
p_mul = 1
for i in range(0,len(p)):
	p_mul = p_mul*p[i]
# print "p_i multiplication:",val
# random_no=np.random.randint(2**(gamma-1),(2**gamma))
q0 = next_prime(2**(gamma-1))
# print "q0 value:\n",q0

x0 = q0*p_mul
# print "x0 value:\n",x0


Q=[0]*k

# Q[0]= next_prime(ZZ.random_element(2**(l_Q-2),2**(l_Q-1)))
# for t in range(1,k):
count=0
temp0=next_prime(ZZ.random_element(2**(l_Q-4),2**(l_Q-1)))
while True:
	temp0 = next_prime(temp0)
	if(GCD(temp0,x0)) == 1:
		Q[count]=temp0
		count=count+1
	if count==k:
		break

# print "Q value:\n",Q


X =[0] * 2**lamda
q0_added_t0_p=[q0]+p

# print "Added q0:",q0_added_t0_p

for i in range(0,len(X)):
	e_Q_delta=[0]*(k+1)
	e_Q_delta[0]=ZZ.random_element(0,q0)
	for j in range(1,k+1):
		temp1=ZZ.random_element(-2**row, 2**row)
		e_Q_delta[j]=temp1*Q[j-1]
	
	# print q0_added_t0_p
	# print e_Q_delta
	# print x0
	X[i] = CRT(q0_added_t0_p,e_Q_delta,x0)
# print X

mu =[0] * 2**lamda
for i in range(0,len(X)):
	ran.seed(se)
	chi = ran.randint(0,2**gamma)
	mu[i] = chi%p_mul+ZZ.random_element(0,int(2**(k*eta)/p_mul))*p_mul-ZZ.random_element(-2**row, 2**row)
# print "Y starts from here:"
Y = [0]*k
for i in range(0,len(Y)):
	e_Q_delta=[0]*(k+1)
	# e=[0]*(k+1)
	e_Q_delta[0]=ZZ.random_element(0,q0)
	# print(e[0])
	for j in range(1,k+1):
		temp2=ZZ.random_element(-2**row, 2**row)
		e_Q_delta[j]=temp2*Q[j-1]+delta[i][j-1]
	# print "q0_added_t0_p:",q0_added_t0_p
	# print "e_Q_delta:",e_Q_delta
	# print "x0",x0
	Y[i] = CRT(q0_added_t0_p,e_Q_delta,x0)
# print Y

X =[0] * 2**lamda
	
for i in range(0,len(X)):
	ran.seed(se)
	chi = ran.randint(0,2**gamma)
	X[i] = chi - mu[i]

Message =[0]*k
for i in range(0,k):
	Message[i]=ZZ.random_element(0,Q[i]) #[2,3]#,1,1]
print "Radom message:",Message
# print Q
print("Encryption:")
c = Encryption(Message,Y,X,x0)
print(c)

# c = Encryption1(k,M,Q,[q0]+p,x0,q0,row)
# print(c)
# print()
print("Decryption")
Messg=Decryption(p,c,Q)
