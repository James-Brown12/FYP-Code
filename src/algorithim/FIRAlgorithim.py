import numpy as np

def spectralFactorization(roots, N):
    """
    Perform spectral factorization for  the polynomial B(z)BR(z) .

    Parameters:
    - roots: array of roots of the polynomial B(z)BR(z), which is of degree 2*N.
    - N: degree of B(z).

    Returns:
    - array of minimum phase (if any) roots of B(z).
    """
    
    # Ensure roots is a numpy array and N is an int
    roots = np.array(roots)
    N = int(N)

    #check size
    if len(roots) != 2*N:
        raise ValueError("The number of roots must be equal to 2 times the specified order.")

    # Select stable roots with absolute values less than 1.0
    b_roots = roots[np.abs(roots) < 1.0][:N]

    # If there are fewer stable roots than order, include additional roots
    if len(b_roots) < N:
        remaining_roots = roots[~np.isin(roots, b_roots)][:N- len(b_roots)]
        b_roots = np.concatenate((b_roots, remaining_roots))

    return b_roots


def FindB(A):
    """
    Function to find the polynomial the cross tarnsfer function (B_N(z)) from the bar transfer function (A_N(z))

    Parameters:  A: Coefficient array of polynomial in z^-1 of degree N in form [z^-N, z^-(N-1, ... z^-1, z^0]
                  
    Return:      B: coefficient array of polynomial in z^-1 of degree N B_N(z)
    """
    A = np.array(A)
    # Eq) 66 letting e^(-j*phi_tot) = 1
    BB_R = -1.0 * np.polymul(A, np.flip(A)) # -A_N(Z)A_RN(z)
    BB_R[A.size-1] += 1.0  # add 1 to z^-N term, where N is order of A

    #Find roots of B_N(z)B_NR(z)
    roots = np.array(np.poly1d(BB_R).roots )
    
    #Spectral factorization taking the minimum phase roots Eq) 67
    min_roots = spectralFactorization(roots, roots.size/2)
    
    #Build unscaled B from roots
    B_us = np.poly(min_roots)

    alpha = np.sqrt((-A[-1]*A[0])/(B_us[-1]*B_us[0])) #Scale factor 
    B = alpha*B_us # Scalin by alpha

    return np.flip(B) #flips coeffcients to give in correct order


def FindCoefficents(A,N):


    """
    Find coefficents kappa and phi from the z-transform coeffiecients of FIR filter designed using Digtal signal processing methods (Madsen and Zhao Ch 4.5)
    
    Parameters:  A: Coefficient array of polynomial in z^-1 of degree N in form [z^-N, z^-(N-1, ... z^-1, z^0]
                 N: Filter order
             
    Return:     kappa: List of power coupling coefficients kappa_n's (k_n, k_n-1, ... k_0)
                phi:   List of phase terms phi_n
                
    """
    B_N = np.array(FindB(A))
    A_N = np.array(A)
    phi = []  # List of phi_ns
    kappa = []  # List of kappas
    n = N

    while n >= 0:
        # Calculate kappa Eq) 60
        ratio = np.abs(B_N[0] / A_N[0])**2
        kappa_n = ratio / (1.0 + ratio)

        #def of cos and sin from coupling power ratio
        c_n = np.sqrt(1.0-kappa_n)
        s_n = np.sqrt(kappa_n)
        kappa.append(kappa_n)

        if n > 0:
            # Step-down recursion relation operations Eq) 61/62
            B_N1 =  (B_N * c_n - A_N * s_n )[1:]
            A_N1_tild = c_n * A_N + s_n * B_N

            # Calculate phi_n Eq) 65
            phi_n = -(np.angle(A_N1_tild[0]) + np.angle(B_N1[0]))
            phi.append(phi_n)

            # Update A_N1 and eliminate constant term same as multiply by z Eq)61
            A_N1 = np.exp(1j * phi_n) * A_N1_tild[:-1]

            # Ensure real coefficients
            A_N1 = np.real(A_N1)
            B_N1 = np.real(B_N1)

        n -= 1
        A_N = A_N1
        B_N = B_N1

    return kappa, phi


if __name__ == "__main__":
        # Example usage
        #Let A be the coeffents of the desired transfer function
    A = [-0.250,0.500,-0.250]
    #Let N be the disired order of you optical filter i.e) number of stages
    N = 2
    #calculate coefficents
    kappa,phi = FindCoefficents(A, N)

    print(kappa,phi)

"""
Result:

kappa= [0.1464466092745967, 0.4999999996262815, 0.8535533907254033] 
phi =[-3.141592653589793, -0.0]

This agrees with table 4.2 of Madsen and Zhao
"""

