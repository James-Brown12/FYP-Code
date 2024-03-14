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


########MATERIAL PROPERTIES################
lamda = 1550e-9
n_g = 4.40063
n_e = 2.29916

x=1500 # x scale factor
y = 1000 # y scale factor

########COUPLERS################
width = 0.5 # width of the waveguide
sep = 100 #distance between two input ports of coupler 
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

########STRAIGHT################
straight_length = 400
srt = nd.strt(width= width, length=straight_length, xs='x')

########DLEAY################
#place all couplers
C1.put(3*x,0)
C2.put(3*x,0.25*y)
C3.put(3*x,0.5*y)
C4.put(3*x,0.75*y)
C5.put(3*x,y)
srt.put(3*x,-0.3*y)

C6.put(4*x,0)
C7.put(4*x,0.25*y)
C8.put(4*x,0.5*y)
C9.put(4*x,0.75*y)
C10.put(4*x,y)

bandwidths = [5e-9,2.5e-9]
c =0
for bandwidth in bandwidths:
    
    L_base = lamda**2/(2*n_g*bandwidth)      #defines length based on half FSR 
    L_fs = lamda/n_e                        #shifting factor 

    delay_length= L_base*1E6

    angle, radius = BumpWaveguide(straight_length, delay_length) #dL
    D1=delay1(width=width, length=straight_length, angle=angle, radius=radius)
    angle, radius = BumpWaveguide(straight_length, 2*delay_length) #2dL
    D2=delay1(width=width, length=straight_length, angle=angle, radius=radius)
    angle, radius = BumpWaveguide(straight_length, 2*delay_length + L_fs/2) #2dL +pi
    D3=delay1(width=width, length=straight_length, angle=angle, radius=radius)

    #second stage no shift dL => dL/2  
    angle, radius = BumpWaveguide(straight_length, delay_length/2) #dL/2
    D4=delay1(width=width, length=straight_length, angle=angle, radius=radius)
    D5=D1 #2*dL/2
    angle, radius = BumpWaveguide(straight_length, delay_length + L_fs/2) 
    D6=delay1(width=width, length=straight_length, angle=angle, radius=radius)

    #third stage with shift dL => dl/2  + L_fs/4 
    angle, radius = BumpWaveguide(straight_length, delay_length/2 + L_fs/4)
    D7=delay1(width=width, length=straight_length, angle=angle, radius=radius)
    D8=D6
    angle, radius = BumpWaveguide(straight_length, delay_length + L_fs)
    D9=delay1(width=width, length=straight_length, angle=angle, radius=radius)
    ######################################

    

    #place all delays
    D1.put(0,y+c)
    D2.put(0,0.5*y+c,flip=True)
    D3.put(0,0+c,flip=True)

    D4.put(x,y+c)
    D5.put(x,0.5*y+c,flip=True)
    D6.put(x,0+c,flip=True)

    D7.put(2*x,y+c)
    D9.put(2*x,0.5*y+c,flip=True)

    #################single 3 coupler stage 250nm gap###########################
    C1_250 = C1.put(0,-y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])
    ##############################################################

    ################single 4 coupler stage 250nm gap##############################
    C1_250 = C1.put(0,-2*y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C3.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C3.put(srt2_250.pin['b0'])
    D3_250 = D3.put(C3_250.pin['b1'],flip=True)
    srt3_250 = srt.put(C3_250.pin['b0'])
    C4_250 = C5.put(srt3_250.pin['b0'])
    ##############################################################

    ##########4 channel(5nm)- 4 coupler stages 250nm gap ##############################
    u1 = nd.sinebend(width=width, distance=150, offset=sep, xs='x')
    u2 = nd.sinebend(width=width, distance=150, offset=-sep, xs='x')

    C1_250 = C1.put(0,-3*y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C3.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C3.put(srt2_250.pin['b0'])
    D3_250 = D3.put(C3_250.pin['b1'],flip=True)
    srt3_250 = srt.put(C3_250.pin['b0'])
    C4_250 = C5.put(srt3_250.pin['b0'])

    #connections
    bend2 = u1.put(C4_250.pin["b0"])
    bend1 = u2.put(C4_250.pin["b1"])

    #lower stage
    C1_250 = C1.put("a0",bend1.pin["b0"])
    D1_250 = D4.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C3.put(D1_250.pin['b0'])
    D2_250 = D5.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C3.put(srt2_250.pin['b0'])
    D3_250 = D6.put(C3_250.pin['b1'],flip=True)
    srt3_250 = srt.put(C3_250.pin['b0'])
    C4_250 = C5.put(srt3_250.pin['b0'])

    #upper stage
    C1_250 = C1.put("a0",bend2.pin["b0"])
    D1_250 = D7.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C3.put(D1_250.pin['b0'])
    D2_250 = D8.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C3.put(srt2_250.pin['b0'])
    D3_250 = D9.put(C3_250.pin['b1'],flip=True)
    srt3_250 = srt.put(C3_250.pin['b0'])
    C4_250 = C5.put(srt3_250.pin['b0'])
    ################################################################

    ##########4 channel(5nm)- 3 coupler stages 250nm gap ##############################
    u1 = nd.sinebend(width=width, distance=150, offset=sep, xs='x')
    u2 = nd.sinebend(width=width, distance=150, offset=-sep, xs='x')
    C1_250 = C1.put(0,-4*y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])
    bend1 = u1.put(C3_250.pin["b0"])
    bend2 = u2.put(C3_250.pin["b1"])

    #lower stage
    C1_250 = C1.put("a0",bend1.pin["b0"])
    D1_250 = D4.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D5.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])

    #upper stage
    C1_250 = C1.put("a0",bend2.pin["b0"])
    D1_250 = D7.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D8.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])
    ################################################################


    ###################### single 3 coupler stage 300nm gap ###############################
    C1_300 = C6.put(4*x,-y+c)
    D1_300 = D1.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C7.put(D1_300.pin['b0'])
    D2_300 = D2.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C9.put(srt2_300.pin['b0'])
    #######################################################################

    ########################### single 4 coupler stage 300nm gap #######################
    C1_300 = C6.put(4*x,-2*y+c)
    D1_300 = D1.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C8.put(D1_300.pin['b0'])
    D2_300 = D2.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C8.put(srt2_300.pin['b0'])
    D3_300 = D3.put(C3_300.pin['b1'],flip=True)
    srt3_300 = srt.put(C3_300.pin['b0'])
    C4_300 = C10.put(srt3_300.pin['b0'])
    #######################################################################################

    ##########4 channel(5nm)- 4 coupler stages 300nm gap ##############################
    u1 = nd.sinebend(width=width, distance=150, offset=sep, xs='x')
    u2 = nd.sinebend(width=width, distance=150, offset=-sep, xs='x')

    C1_250 = C6.put(4*x,-3*y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C8.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C8.put(srt2_250.pin['b0'])
    D3_250 = D3.put(C3_250.pin['b1'],flip=True)
    srt3_250 = srt.put(C3_250.pin['b0'])
    C4_250 = C10.put(srt3_250.pin['b0'])

    #connections
    bend2 = u1.put(C4_250.pin["b0"])
    bend1 = u2.put(C4_250.pin["b1"])

    #lower stage
    C1_250 = C6.put("a0",bend1.pin["b0"])
    D1_250 = D4.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C8.put(D1_250.pin['b0'])
    D2_250 = D5.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C8.put(srt2_250.pin['b0'])
    D3_250 = D6.put(C3_250.pin['b1'],flip=True)
    srt3_250 = srt.put(C3_250.pin['b0'])
    C4_250 = C10.put(srt3_250.pin['b0'])

    #upper stage
    C1_250 = C6.put("a0",bend2.pin["b0"])
    D1_250 = D7.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C8.put(D1_250.pin['b0'])
    D2_250 = D8.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C8.put(srt2_250.pin['b0'])
    D3_250 = D9.put(C3_250.pin['b1'],flip=True)
    srt3_250 = srt.put(C3_250.pin['b0'])
    C4_250 = C10.put(srt3_250.pin['b0'])
    ################################################################

    ##########4 channel(5nm)- 3 coupler stages 300nm gap ##############################
    u1 = nd.sinebend(width=width, distance=150, offset=sep, xs='x')
    u2 = nd.sinebend(width=width, distance=150, offset=-sep, xs='x')
    C1_250 = C6.put(4*x,-4*y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C7.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C9.put(srt2_250.pin['b0'])
    bend1 = u1.put(C3_250.pin["b0"])
    bend2 = u2.put(C3_250.pin["b1"])

    #lower stage
    C1_250 = C6.put("a0",bend1.pin["b0"])
    D1_250 = D4.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C7.put(D1_250.pin['b0'])
    D2_250 = D5.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C9.put(srt2_250.pin['b0'])

    #upper stage
    C1_250 = C6.put("a0",bend2.pin["b0"])
    D1_250 = D7.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C7.put(D1_250.pin['b0'])
    D2_250 = D8.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C9.put(srt2_250.pin['b0'])
    ################################################################
    c=6000

nd.export_gds(filename="./src/GDS_Generator/Si-Run2.gds")