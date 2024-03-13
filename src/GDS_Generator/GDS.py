import nazca as nd
import numpy as np
nd.clear_layout()
import numpy as np
from scipy.optimize import minimize


nd.add_layer(name='waveguide', layer=1, accuracy=0.001)
nd.add_layer(name='trench', layer=2, accuracy=0.001)
nd.add_layer(name='grating trench', layer=3, accuracy=0.001)
nd.add_layer(name='SWG trench', layer=4, accuracy=0.001)

nd.add_layer2xsection(xsection='x', layer='waveguide')
nd.add_layer2xsection(xsection='x', layer='trench', growx=3,growy=3)



def MZI(width=0.5, Lc=0.25, length=20, sep=100, gap=0.25):
    with nd.Cell("MZI") as MZI:
        C1 = coupler(width = width, length=Lc, gap=gap+width, sep=sep).put()
        St_u = nd.strt(width= width, length=length, xs='x').put(C1.pin['b0'])
        St_l = nd.strt(width= width, length=length, xs='x').put(C1.pin['b1'])
        C2 = coupler(width = width, length=Lc, gap=gap+width, sep=sep).put(St_u.pin['b0'])



        # Add pins
        nd.Pin("a0", pin=C1.pin['a0']).put()
        nd.Pin("a1", pin=C1.pin['a1']).put()
        nd.Pin("b0", pin=C2.pin['b0']).put()
        nd.Pin("b1", pin=C2.pin['b1']).put()
    return MZI

def delay1(width=0.5, length=100, angle=130.5699, radius=32.9115):
    with nd.Cell("delay") as delay:
        nd.trace.trace_start()
        S1 = nd.bend(width= width,angle=angle, radius=radius,xs='x').put()
        S2 = nd.bend(width= width,angle=angle, radius=radius,xs='x').put(S1.pin['b0'], flip = 'True')
        S3 = nd.bend(width= width,angle=angle, radius=radius,xs='x').put(S2.pin['b0'], flip = 'True')
        S4 = nd.bend(width= width,angle=angle, radius=radius,xs='x').put(S3.pin['b0'])
        nd.trace.trace_stop()
        


        # Add pins
        nd.Pin("a0", pin=S1.pin['a0']).put()
        nd.Pin("b0", pin=S4.pin['b0']).put()
        print (nd.trace.trace_length())
    return delay


def BumpWaveguide(straight_length, delay_length):
    """
    Calculate the angle and radius of a bump in a waveguide.

    Parameters:
    - straight_length: Length of the straight part of the waveguide.
    - delay_length: Length of the delayed part of the waveguide.

    Returns:
    - angle: Angle in degrees.
    - radius: Radius of the waveguide.
    """
    total_length = straight_length + delay_length
    initial_angle_rad = np.deg2rad(0)

    def fun(angle_rad):
        return abs(angle_rad / np.sin(angle_rad) - total_length / straight_length)

    x0 = initial_angle_rad
    res = minimize(fun, x0, method='Nelder-Mead')

    angle_rad = np.abs(res.x[0])
    angle = np.rad2deg(angle_rad)
    radius = straight_length / (4 * np.sin(angle_rad))

    return angle, radius

# You can define other functions in this file as well if needed

def coupler(width=0.5, length=20, sep=100, gap=20):
    with nd.Cell("Coupler") as C:
        # Upper arm
        u1 = nd.sinebend(width=width, distance=100, offset=-0.5*(sep-gap), xs='x').put(0, 0.5*sep)
        nd.strt(width= width, length=length, xs='x').put()
        u2 = nd.sinebend(width= width,distance=100, offset=0.5*(sep-gap), xs='x').put()
        

        # Lower arm
        l1 = nd.sinebend(width= width,distance=100, offset=0.5*(sep-gap),xs='x').put(0, -0.5*sep)
        nd.strt(width= width,length=length,xs='x').put()
        l2 = nd.sinebend(width= width,distance=100, offset=-0.5*(sep-gap), xs='x').put()

        # Add pins
        nd.Pin("a0", pin=u1.pin['a0']).put()
        nd.Pin("a1", pin=l1.pin['a0']).put()
        nd.Pin("b0", pin=u2.pin['b0']).put()
        nd.Pin("b1", pin=l2.pin['b0']).put()
    return C

def read_xy_file(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.split())
            data.append((x, y))
    return data

def find_x_for_y(data, y_values, tol=0.1):
    x_values = []
    for y in y_values:
        for x, y_val in data:
            if abs(y_val - y) <= tol:
                x_values.append(x)
                break
        else:
            x_values.append(None)  # If Y value not found, append None
    return x_values

lamda = 1550e-9
#silicon @1550nm
n_g = 4.40063
n_e = 2.29916

#define delay_length from parameters
bandwidth = 5e-9
L_base = lamda**2/(2*n_g*bandwidth)      #defines length based on half FSR 
L_fs = lamda/n_e                        #shifting factor 

[0.5,0.29,0.2,0.08,0.04]
width = 0.5 # width of the waveguide
sep = 100 #distance between two input ports of coupler 

########DLEAY################
straight_length = 100
delay_length= L_base
angle, radius = BumpWaveguide(straight_length, delay_length)
########################
y = 100 #scale factor

#Couplers 250nm gap
C1=coupler(width=width, length=60.3015, sep=sep, gap=0.25+width) #0.5
C2=coupler(width=width, length=44.2211, sep=sep, gap=0.25+width) #0.29
C3=coupler(width=width, length=36.1809, sep=sep, gap=0.25+width) #0.2
C4=coupler(width=width, length=22.5126, sep=sep, gap=0.25+width) #0.08
C5=coupler(width=width, length=15.2764, sep=sep, gap=0.25+width) #0.04

#Couplers 300nm gap
C6=coupler(width=width, length=95.6784, sep=sep, gap=0.3+width) #0.5
C7=coupler(width=width, length=69.1457, sep=sep, gap=0.3+width) #0.29
C8=coupler(width=width, length=57.0854, sep=sep, gap=0.3+width) #0.2
C9=coupler(width=width, length=35.3769, sep=sep, gap=0.3+width) #0.08
C10=coupler(width=width, length=24.9246, sep=sep, gap=0.3+width)#0.04


C1=coupler(width=width, length=92, sep=sep, gap=gap+width).put(0,0)
D1= delay1(width=width, length=straight_length, angle=angle, radius=radius).put(C1.pin['b0'])
S_lower=nd.strt(width= width, length=straight_length, xs='x').put(C1.pin['b1'])
C2=coupler(width=width, length=66, sep=sep, gap=gap+width).put(D1.pin['b0'])
straight_length = 400
delay_length= 200*2
angle, radius = BumpWaveguide(straight_length, delay_length)
D1= delay1(width=width, length=straight_length, angle=angle, radius=radius).put(C2.pin['b1'], flip=True)
S_lower=nd.strt(width= width, length=straight_length, xs='x').put(C2.pin['b0'])
C3=coupler(width=width, length=12, sep=sep, gap=gap+width).put(S_lower.pin['b0'])



C1=coupler(width=width, length=92, sep=sep, gap=gap+width).put(C3.pin['b0'])
D1= delay1(width=width, length=straight_length, angle=angle, radius=radius).put(C1.pin['b0'])
S_lower=nd.strt(width= width, length=straight_length, xs='x').put(C1.pin['b1'])
C2=coupler(width=width, length=66, sep=sep, gap=gap+width).put(D1.pin['b0'])
straight_length = 400
delay_length= 200*2
angle, radius = BumpWaveguide(straight_length, delay_length)
D1= delay1(width=width, length=straight_length, angle=angle, radius=radius).put(C2.pin['b1'], flip=True)
S_lower=nd.strt(width= width, length=straight_length, xs='x').put(C2.pin['b0'])
C3=coupler(width=width, length=12, sep=sep, gap=gap+width).put(S_lower.pin['b0'])





nd.export_gds(filename="./src/GDS_Generator/Si-Run2.gds")