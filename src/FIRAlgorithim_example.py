from algorithim import FIRAlgorithim as FIR

#Let A be the coeffents of the desired transfer function
A = [-0.250,0.500,-0.250]

#Let N be the disired order of you optical filter i.e) number of stages
N = 2

#calculate coefficents
kappa,phi = FIR.FindCoefficents(A, N)

print(kappa,phi)

"""
Result:

kappa= [0.1464466092745967, 0.4999999996262815, 0.8535533907254033] 
phi =[-3.141592653589793, -0.0]

This agrees with table 4.2 of Madsen and Zhao
"""
