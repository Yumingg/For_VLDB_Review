

def r1(x1,x2,m1,m2,m):
    return (m1*m2+m1*x1-x1*x1-x1*x2)/((m-x1-x2)*(m1*m2+m1*x1+m2*x2))

def Dr1_x1(x1,x2,m1,m2,m):
    a=m1*m1*(m2+x1)*(m2+x1)+m2*x2*((x1+x2)*(x1+x2)-m*(2*x1+x2))+m1*(m2*(x1*x1+m2*x2+2*x1*x2)-m*x1*(2*m2+x1))
    b=(m-x1-x2)*(m-x1-x2)*(m1*m2+m1*x1+m2*x2)*(m1*m2+m1*x1+m2*x2)
    return a/b

def r2(x1,x2,m1,m2,m):
    return (m1*m2+m2*x2-x2*x2-x1*x2)/((m-x1-x2)*(m1*m2+m1*x1+m2*x2))

def Dr2_x2(x1,x2,m1,m2,m):
    a=m2*m2*(m1+x2)*(m1+x2)+m1*x1*((x1+x2)*(x1+x2)-m*(x1+2*x2))+m2*(m1*(x2*x2+m1*x1+2*x1*x2)-m*x2*(2*m1+x2))
    b=(m-x1-x2)*(m-x1-x2)*(m1*m2+m1*x1+m2*x2)*(m1*m2+m1*x1+m2*x2)
    return a/b



def solve_equilibria(m1,m2):
    m=1
    x1=0
    x2=0
    alpha=0.01
    delta_x=0.00000001
    threshold_distance=0.00000001
    record_x1=[]
    record_x2=[]

    while True:
        #zprint(x1,x2)
        record_x1.append(x1)
        record_x2.append(x2)
        #numerical method
        Dr1=(r1(x1+delta_x,x2,m1,m2,m)-r1(x1,x2,m1,m2,m))/delta_x
        Dr2=(r2(x1,x2+delta_x,m1,m2,m)-r2(x1,x2,m1,m2,m))/delta_x
    #     analytic method 
    #     Dr1=Dr1_x1(x1,x2)
    #     Dr2=Dr2_x2(x1,x2)
    #     print('r1(true):',Dr1_x1(x1,x2),'r1(numerical):',Dr1)
    #     print('r2(true):',Dr2_x2(x1,x2),'r2(numerical):',Dr2)
        new_x1=x1+alpha*Dr1
        new_x2=x2+alpha*Dr2
        new_x1=min(max(0,new_x1),m1)
        new_x2=min(max(0,new_x2),m2)
        if (abs(new_x1-x1)<threshold_distance and abs(new_x2-x2)<threshold_distance):
            break
        x1=new_x1
        x2=new_x2
    print("x1 =", x1, "x2=",x2)
    return x1,x2