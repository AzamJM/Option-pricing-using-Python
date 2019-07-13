"""
Python code to implement a multi-step binomial tree to price the
option in both American and European cases
Author: Azam Jainullabudin Mohamed
"""
import numpy as np
import math

# Input from the question
r=0.04; # risk
volatility=0.2; # Volatility
time=2; # time
#n=5;  # input trees


# Function for evaluating the binomial option pricing
# for both European and American options
def binomial_tree(n, option):
    # Change in time based upon the value 
    dtime=time/n;
    # Up value
    u=np.exp(volatility*math.sqrt(dtime))
    # Down value
    d=1/u
    
    # probability value
    p=(np.exp(r*dtime)-d)/(u-d);
    
    # Initial stock value
    S0=[[42]]
    
    # To calculate the nodes values for n binomial tree
    for j in range(1,n+1):
        temp=[]
        for i in range(1,j+2):
            s=S0[0][0]*(u**(i-1))*(d**(j-(i-1)))
            temp.insert(j,s);
        S0.insert(i,temp)
    print("**********************************************")
    print("Current stock price in %d binomial option tree" % n)
    print("**********************************************")
    print(S0)
    print(" ")
    
    # Initializing new matrix to store the payoff values in american option
    new_mat=np.zeros([n+1,n+1])
    # Initialing matrix for comparing the values of payoff and f(ni)
    # to manipulate the early exercise optimal node
    early=np.zeros([n+1,n+1])
    # Matrix to store the f(ni) values at each node
    options=np.zeros([n+1,n+1])
    # Matrix containing the updated values of nodes in n binomial tree
    f_value=np.zeros([n+1, n+1])
    
    # Excercising the european and American option
    flag = 0
    for i in range(n,-1,-1):
        for j in range(0, i+1):
            # Exercising "European" option pricing
            if(option == "European" or option == "european" or option == "E" or option == "e"):
                if(i == n):
                    payoff = max(1500-(S0[i][j]**2)+(30*S0[i][j]), 0)
                    options[i,j] = payoff
                # Condition to calculate the payoff at the last column
                elif( i != n): 
                    options[i,j] = np.exp(-r * dtime)* ((1-p) * options[i+1, j] + p* options[i+1, j+1])
            
            # Exercising "American" option pricing
            if(option == "American" or option == "american" or option == "A" or option == "a"):
                if(flag == 1):
                    american_payoff = max(1500-(S0[i][j]**2)+(30*S0[i][j]), 0)
                    new_mat[i,j] = american_payoff
                if(i == n):
                    payoff = max(1500-(S0[i][j]**2)+(30*S0[i][j]), 0)
                    options[i,j] = payoff
                # Condition to calculate the payoff at the last column
                elif(i != n):
                    payoff = max(1500-(S0[i][j]**2)+(30*S0[i][j]), 0)
                    f_value[i,j] = np.exp(-r * dtime)* ((1-p) * options[i+1, j] + p* options[i+1, j+1])
                    options[i,j] = max(payoff, f_value[i,j])
                    
                # Validating the optimal node for early exercise option
                if(new_mat[i,j] >= options[i,j] and new_mat[i,j] != 0 and options[i,j] != 0):
                    early[i,j] = new_mat[i,j]
                elif(new_mat[i, j] != options[i,j]):
                    early[i,j] = 0
        flag=1
    
    print("")
    # Printing the F(ni) values by exercising European option pricing
    if(option == "European" or option == "european" or option == "E" or option == "e"):
        print("********************************************")
        print("European option pricing for %d step binomial" % n)
        print("********************************************")
        print(options)
    
    # Printing the F(ni) values by exercising American option pricing
    elif(option == "American" or option == "american" or option == "A" or option == "a"):
        print("***************************************************")
        print("American option pricing for %d step binomial" % n)
        print("**************************************************")
        print(options)
        #print("YES")
        #print(f_value)

        print("")
        print("**************************************************")
        print("American option payoff values for %d step binomial" % n)
        print("**************************************************")
        print(new_mat)
        print("")
        
        print("**** Comparing the payoff matrix with option matrix for ", end="")
        print("calculating the optimal option for early excercise ****")
        print("")
        print("***********************************************")
        print("Nodes at which early exercise can be beneficial")
        print("***********************************************")
        # To print the Optimal early exercise option
        for i in range(n,-1,-1):
            for j in range(0, i+1):
                if(early[i,j] != 0):
                    print("Early exercise value is optimal at node value", end=" ")
                    print(i, end= " ")
                    print(j, end=" ")
                    print("is", end= " ")
                    print(early[i,j])

# Start of the program
# Function call to binomial tree
# Exercising the binomial tree with European option
print("Enter the step of binomial tree")
n = int(input())
print("```````` EUROPEAN OPTION ````````")
binomial_tree(n, "European")
print("")
# Exercising the binomial tree with American option
print("```````` AMERICAN OPTION ````````")
binomial_tree(n, "American")