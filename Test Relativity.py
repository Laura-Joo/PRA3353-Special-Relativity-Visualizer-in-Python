import numpy as np

c = 299792458 #m/s

def lorentz_time(t,x,vA,vB):
    v = (vB - vA)/(1-(vB*vA)/(c*c))
    gamma = 1/np.sqrt(1-((v*v)/(c*c)))
    print("The gamma factor is ",gamma)
    T = gamma*(t-(v*x)/(c*c))
    return T

print("The time that B sees the Event is ",lorentz_time(0,10,0.5*29979245.8,29979245.8),"s")

# I wrote this with the idea that there are 3 frames in mind: frame S which is 'stationary', and frame A which is moving with respect 
# to S, and another frame B which is moving with respect to A and S.
#
# This is an example where we call the function lorentz_time and fill in the values:
# t = 0 in A's frame
# x = 10 from some Event as seen from A's frame
# vA = 0.5*29979245.8 m/s, so this is the velocity of frame A as seen by 'rest frame' S.
# vB = 29979245.8 m/s, so this is the velocity of frame B as seen by S.
#
# Velocity addition tells us that u' = (vB - vA) / ( (1 - vB*vA) / c^2), meaning that A sees B moving with a velocity of u'.
# I called u' = v in the function above, so the coordinates x and t that we fill in are the coordinates of an Event that is seen by A. 