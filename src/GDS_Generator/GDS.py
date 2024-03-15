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


# use hashme
@nd.bb_util.hashme('cell2')
def SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length):
    grating_length=n_grating*grating_period
    grating_start=4
    wg_length=grating_start+grating_length+1
    #taper_length=730
    with nd.Cell(hashme=True) as gc:
        nd.strt(length=wg_length, width=11, xs='x').put(0)
        nd.taper(length=taper_length, width1=11, width2=0.5, xs='x').put()
        for i1 in range(n_grating-1):
            SWG_trench_start1=0.5*SWG_period*SWG_duty+0.5*SWG_period*(1-SWG_duty)
            SWG_trench_start2=-0.5*SWG_period*SWG_duty-0.5*SWG_period*(1-SWG_duty)
            for i2 in range(12):
                nd.strt(length=grating_period*(1-grating_duty),width=SWG_period*(1-SWG_duty),layer='SWG trench').put(grating_start,SWG_trench_start1)
                SWG_trench_start1=SWG_trench_start1+SWG_period
            for i2 in range(12):
                nd.strt(length=grating_period*(1-grating_duty),width=SWG_period*(1-SWG_duty),layer='SWG trench').put(grating_start,SWG_trench_start2)
                SWG_trench_start2=SWG_trench_start2-SWG_period
            grating_start=grating_start+grating_period
        nd.Pin('gc_in/out').put(wg_length+taper_length)
        nd.Pin('text').put(-20,0,90)
        nd.put_stub()
    return gc


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

def coupler1(width=0.5, length=20, sep=100, gap=20):
    with nd.Cell("Coupler") as C:
        # Upper arm
        u1 = nd.sinebend(width=width, distance=100, offset=-0.5*(sep-gap), xs='x').put(0, 0.5*sep)
        nd.strt(width= width, length=length, xs='x').put()
        u2 = nd.sinebend(width= width,distance=100, offset=0.5*(sep-gap), xs='x').put()
        

        # Lower arm
        nd.strt(width= width,length=length,xs='x').put(100, -0.5*sep)
        l2 = nd.sinebend(width= width,distance=100, offset=-0.5*(sep-gap), xs='x').put()

        # Add pins
        nd.Pin("a0", pin=u1.pin['a0']).put()
        nd.Pin("b0", pin=u2.pin['b0']).put()
        nd.Pin("b1", pin=l2.pin['b0']).put()
    return C


########MATERIAL PROPERTIES################
lamda = 1550e-9
n_g = 4.40063
n_e = 2.29916

x=2000 # x scale factor
y = 1500 # y scale factor

########Grating Darpan#########
SWG_period=0.45
SWG_duty=0.62
grating_period=0.718
grating_duty=0.55
n_grating=40
taper_length=450
##########Grating Darpan##########

########COUPLERS################
width = 0.5 # width of the waveguide
sep = 100 #distance between two input ports of coupler 
#Couplers 250nm gap
Ca=coupler1(width=width, length=60.3015, sep=sep, gap=0.25+width)
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
#######################
#place all couplers
#Ca.put(3*x,-0.2*y)
C=C1.put(3*x,0)
nd.text(text="0.5 coupler 250nm gap", height = 30,layer = 5).put(3*x-450,100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C2.put(3*x,0.25*y)
nd.text(text="0.29 coupler 250nm gap", height = 30,layer = 5).put(3*x-450,0.25*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C3.put(3*x,0.5*y)
nd.text(text="0.2 coupler 250nm gap", height = 30,layer = 5).put(3*x-450,0.5*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C4.put(3*x,0.75*y)
nd.text(text="0.08 coupler 250nm gap", height = 30,layer = 5).put(3*x-450,0.75*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C5.put(3*x,y)
nd.text(text="0.04 coupler 250nm gap", height = 30,layer = 5).put(3*x-450,1*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C6.put(4*x,0)
nd.text(text="0.5 coupler 300nm gap", height = 30,layer = 5).put(4*x-450,0*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C7.put(4*x,0.25*y)
nd.text(text="0.29 coupler 300nm gap", height = 30,layer = 5).put(4*x-450,0.25*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C8.put(4*x,0.5*y)
nd.text(text="0.2 coupler 300nm gap", height = 30,layer = 5).put(4*x-450,0.5*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C9.put(4*x,0.75*y)
nd.text(text="0.08 coupler 300nm gap", height = 30,layer = 5).put(4*x-450,0.75*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

C=C10.put(4*x,y)
nd.text(text="0.04 coupler 300nm gap", height = 30,layer = 5).put(4*x-450,1*y+100)
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['a1'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b0'])
SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C.pin['b1'])

##############################################################################################
bandwidths = [5e-9,2.5e-9]
c =0
nd.text(text="5nm Channel width Filter", height = 250,layer = 5).put(1.5*x,1.5*y)
nd.text(text="2.5nm Channel width Filter", height = 250,layer = 5).put(1.5*x,1.5*y+10000)
for bandwidth in bandwidths:
    ########DELAY############################
    L_base = lamda**2/(2*n_g*bandwidth)      #defines length based on half FSR 
    L_fs = lamda/n_e                        #shifting factor 

    delay_length= L_base*1E6

    angle, radius = BumpWaveguide(straight_length, delay_length) #dL
    D1=delay1(width=width, length=straight_length, angle=angle, radius=radius)
    angle, radius = BumpWaveguide(straight_length, 2*delay_length) #2dL
    D2=delay1(width=width, length=straight_length, angle=angle, radius=radius)
    angle, radius = BumpWaveguide(straight_length, 2*delay_length + L_fs/2) #2dL + pi
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
    Da = D1.put(0,y+c)
    nd.text(text="Delta L", height = 30,layer = 5).put(0,y+c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])

    Da = D2.put(0,0.5*y+c,flip=True)
    nd.text(text="2(Delta L)", height = 30,layer = 5).put(0,0.5*y+c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])

    Da = D3.put(0,c,flip=True)
    nd.text(text="2(Delta L)+pi", height = 30,layer = 5).put(0,c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])

    Da = D4.put(x,y+c)
    nd.text(text="(Delta L)/2", height = 30,layer = 5).put(x,y+c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])
    
    Da = D5.put(x,0.5*y+c,flip=True)
    nd.text(text="Delta L flipped", height = 30,layer = 5).put(x,0.5*y+c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])

    Da = D6.put(x,0+c,flip=True)
    nd.text(text="Delta L + pi", height = 30,layer = 5).put(x,c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])


    Da = D7.put(2*x,y+c)
    nd.text(text="Delta L/2 + L_fs/4", height = 30,layer = 5).put(2*x,y+c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])

    Da = D9.put(2*x,0.5*y+c,flip=True)
    nd.text(text="Delta L + L_fs", height = 30,layer = 5).put(2*x,0.5*y+c+150)
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',Da.pin['b0'])

    


    #################single 3 coupler stage 250nm gap###########################
    nd.text(text="single 4 coupler stages 250nm gap", height = 30,layer = 5).put(-450,-y+c+150)
    C1_250 = C1.put(0,-y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a1'])
    
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_250.pin['b1'])
    ##############################################################

    ################single 4 coupler stage 250nm gap##############################
    nd.text(text="single 4 coupler stages 250nm gap", height = 30,layer = 5).put(-450,-2*y+c+150)
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
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a1'])
    
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_250.pin['b1'])

    ##############################################################

    ##########4 channel(5nm)- 4 coupler stages 250nm gap ##############################
    u1 = nd.sinebend(width=width, distance=150, offset=sep, xs='x')
    u2 = nd.sinebend(width=width, distance=150, offset=-sep, xs='x')
    nd.text(text="4 channel- 4 coupler stages 250nm gap", height = 30,layer = 5).put(-450,-3*y+c+150)
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
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a1'])
    
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
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_250.pin['b1'])

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
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_250.pin['b1'])

    ################################################################

    ##########4 channel(5nm)- 3 coupler stages 250nm gap ##############################
    u1 = nd.sinebend(width=width, distance=150, offset=sep, xs='x')
    u2 = nd.sinebend(width=width, distance=150, offset=-sep, xs='x')
    nd.text(text="4 channel- 3 coupler stages 250nm gap", height = 30,layer=5).put(-450,-4*y+c+150)
    C1_250 = C1.put(0,-4*y+c)
    D1_250 = D1.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D2.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])
    bend1 = u1.put(C3_250.pin["b0"])
    bend2 = u2.put(C3_250.pin["b1"])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_250.pin['a1'])
    

    #lower stage
    C1_250 = C1.put("a0",bend1.pin["b0"])
    D1_250 = D4.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D5.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_250.pin['b1'])
    
    #upper stage
    C1_250 = C1.put("a0",bend2.pin["b0"])
    D1_250 = D7.put(C1_250.pin['b0'])
    srt1_250 = srt.put(C1_250.pin['b1'])
    C2_250 = C2.put(D1_250.pin['b0'])
    D2_250 = D8.put(C2_250.pin['b1'],flip=True)
    srt2_250 = srt.put(C2_250.pin['b0'])
    C3_250 = C4.put(srt2_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_250.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_250.pin['b1'])
    ################################################################


    ###################### single 3 coupler stage 300nm gap ###############################
    nd.text(text="3 coupler stages 300nm gap", height = 30,layer = 5).put(4*x-450,-y+c+150)
    C1_300 = C6.put(4*x,-y+c)
    D1_300 = D1.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C7.put(D1_300.pin['b0'])
    D2_300 = D2.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C9.put(srt2_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a1'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_300.pin['b1'])
    
    #######################################################################

    ########################### single 4 coupler stage 300nm gap #######################
    nd.text(text="4 coupler stages 300nm gap", height = 30,layer = 5).put(4*x-450,-2*y+c+150)
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
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a1'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_300.pin['b1'])
    
    #######################################################################################

    ##########4 channel(5nm)- 4 coupler stages 300nm gap ##############################
    u1 = nd.sinebend(width=width, distance=150, offset=sep, xs='x')
    u2 = nd.sinebend(width=width, distance=150, offset=-sep, xs='x')
    nd.text(text="4 channel- 4 coupler stages 300nm gap", height = 30,layer = 5).put(4*x-450,-3*y+c+150)
    C1_300 = C6.put(4*x,-3*y+c)
    D1_300 = D1.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C8.put(D1_300.pin['b0'])
    D2_300 = D2.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C8.put(srt2_300.pin['b0'])
    D3_300 = D3.put(C3_300.pin['b1'],flip=True)
    srt3_300 = srt.put(C3_300.pin['b0'])
    C4_300 = C10.put(srt3_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a1'])
    
    #connections
    bend2 = u1.put(C4_300.pin["b0"])
    bend1 = u2.put(C4_300.pin["b1"])

    #lower stage
    C1_300 = C6.put("a0",bend1.pin["b0"])
    D1_300 = D4.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C8.put(D1_300.pin['b0'])
    D2_300 = D5.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C8.put(srt2_300.pin['b0'])
    D3_300 = D6.put(C3_300.pin['b1'],flip=True)
    srt3_300 = srt.put(C3_300.pin['b0'])
    C4_300 = C10.put(srt3_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_300.pin['b1'])
    
    #upper stage
    C1_300 = C6.put("a0",bend2.pin["b0"])
    D1_300 = D7.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C8.put(D1_300.pin['b0'])
    D2_300 = D8.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C8.put(srt2_300.pin['b0'])
    D3_300 = D9.put(C3_300.pin['b1'],flip=True)
    srt3_300 = srt.put(C3_300.pin['b0'])
    C4_300 = C10.put(srt3_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C4_300.pin['b1'])
    
    ################################################################

    ##########4 channel(5nm)- 3 coupler stages 300nm gap ##############################
    nd.text(text="4 channel- 3 coupler stages 300nm gap", height = 30,layer = 5).put(4*x-450,-4*y+c+150)
    C1_300 = C6.put(4*x,-4*y+c)
    D1_300 = D1.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C7.put(D1_300.pin['b0'])
    D2_300 = D2.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C9.put(srt2_300.pin['b0'])
    bend1 = u1.put(C3_300.pin["b0"])
    bend2 = u2.put(C3_300.pin["b1"])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C1_300.pin['a1'])
    
    #lower stage
    C1_300 = C6.put("a0",bend1.pin["b0"])
    D1_300 = D4.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C7.put(D1_300.pin['b0'])
    D2_300 = D5.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C9.put(srt2_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_300.pin['b1'])
    
    #upper stage
    C1_300 = C6.put("a0",bend2.pin["b0"])
    D1_300 = D7.put(C1_300.pin['b0'])
    srt1_300 = srt.put(C1_300.pin['b1'])
    C2_300 = C7.put(D1_300.pin['b0'])
    D2_300 = D8.put(C2_300.pin['b1'],flip=True)
    srt2_300 = srt.put(C2_300.pin['b0'])
    C3_300 = C9.put(srt2_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_300.pin['b0'])
    SWG_grating_coupler(SWG_period,SWG_duty,grating_period,grating_duty,n_grating,taper_length).put('gc_in/out',C3_300.pin['b1'])
    
    ################################################################
    c=10000




nd.export_gds(filename="./src/GDS_Generator/Si-Run2.gds")