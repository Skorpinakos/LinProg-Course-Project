from pulp import *


def add_generator(J_data,Z,X,problem):
    #print(J_data)
    k=J_data[0].copy() #k parameters
    k.append(-1) #for use in lpsum later, factor for X
    d=J_data[1].copy() #d parameters
    d.append(-1)  #for use in lpsum later, factor for Z
    j=J_data[2] #id for generator
    n=len(J_data[0]) #length of k,d lists

    
    
    y=[]
    x=[]
    for i in range(0,n):
        temp=(LpVariable("y_{}_{}".format(j,i+1), lowBound=0, upBound=1, cat='Binary'))#y_variables (binary)
        variables['y_j={}_i={}'.format(j,i+1)]=temp
        y.append(temp)
        temp=(LpVariable("x_{}_{}".format(j,i+1), lowBound=0, upBound=1, cat='Continuous'))#x variables (non negative)
        variables['x_j={}_i={}'.format(j,i+1)]=temp
        x.append(temp)
        
    x_and_X=x.copy()
    x_and_X.append(X)
    x_and_Z=x.copy()
    x_and_Z.append(Z)
    y_odds=[]
    y_evens=[]
    for i,variable in enumerate(y):
        if (i % 2)==1:
            y_odds.append(variable)
        if (i % 2)==0:
            y_evens.append(variable)

#Χji≤Yji
    for i in range(0,n):
        problem += x[i]-y[i]<=0

#Σ(Xji)=1
    problem += lpSum(x)==1

#Σ(Yji) ≤ 2
    problem += lpSum(y)<=2

#Χj=Σ(kji*Xji)
    problem += lpSum([x_and_X[i]*k[i] for i in range(0,n+1)])==0

#Ζj=Σ(dji*Xji)
    problem += lpSum([x_and_Z[i]*d[i] for i in range(0,n+1)])==0

#Yji+Yjr ≤ 1 
    print(y_evens, y_odds)
    del y_evens[0] 
    for i in range(0,n-1):
        if (i % 2)==1:
            del y_evens[0]
            
        if (i % 2)==0:
            del y_odds[0]
        print(y_evens,y_odds)
        if len(y_odds)>0:
            problem += lpSum(y_odds) + y[i] <=1
        if len(y_evens)>0:
            problem += lpSum(y_evens) + y[i] <=1
    
        

            
    return True



Q=5 #POWER DEMAND
variables={}
Z=[]
X=[]
f=open('data.txt','r',encoding='utf-8')
data_raw=f.read().split('\n&\n')
data=[]
for i in range(len(data_raw)):
    
    k,d,j=data_raw[i].split('\n')
    k=k.split(',')
    k=[float(x) for x in k]
    d=d.split(',')
    d=[float(x) for x in d]
    data.append([k,d,j])


for data_set in data:
    j=data_set[2]
    temp=LpVariable('Z_{}'.format(j), lowBound=0, upBound=None, cat='Continuous')#Z variable
    variables['Z_j={}'.format(j)]=temp
    Z.append(temp)
    temp=LpVariable('X_{}'.format(j), lowBound=0, upBound=None, cat='Continuous')#X variable
    variables['X_j={}'.format(j)]=temp
    X.append(temp)

problem = LpProblem("Project_gram_sund", LpMinimize)
#Σ(Ζj)
problem += lpSum(Z)
#Σ(Χj)=Q
problem += lpSum(X)==Q

for i,data_set in enumerate(data):
    add_generator(data_set,Z[i],X[i],problem)

problem.writeLP("proj_ver_2.lp")
problem.solve()

for v in problem.variables():
    print (v.name, "=", v.varValue)