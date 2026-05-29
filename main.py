import numpy as np
import math as m

# constants
c = 1

# Lorentz transformation functions
def gamma_factor(v):
    gamma = 1/m.sqrt(1-((v*v)/(c*c)))
    return gamma

def relative_velocity(vA,vB):
    # determine the relative velocity of frame B as seen by frame A, where vA and vB are measured by frame S
    V = (vB - vA)/(1-(vB*vA)/(c*c))
    return V
    # EXTREMELY IMPORTANT: if the input is vA,vB then what we get is vB|A (the velocity of B as seen by A). If the input is vB,vA we get vA|B.

def lorentz_time_transform(t, x, v):

    # call gamma factor function
    gamma = gamma_factor(v)

    # use gamma factor to determine T coordinate in the other frame
    T = gamma*(t-(v*x)/(c*c))
    return T

def lorentz_position_transform(t, x, v):

    # determine gamma-factor from velocity
    gamma = gamma_factor(v)

    # use gamma factor to determine X coordinate in the other frame
    X = gamma*(x-v*t)
    return X

def lorentz_transform(t, x, v):
    
    # create array to store new coordinates in
    new_coordinates = []

    # call separate lorentz-functions to transform x and t
    T = lorentz_time_transform(t, x, v)
    X = lorentz_position_transform(t, x, v)
    return (T, X)

# frame object definition
class Frame:
    all_frames = {}
    def __init__(self, name: str, velocity: float):
        self.name = name
        self.velocity = velocity
        self.all_frames[self.name] = self.velocity
    
    @staticmethod
    def relative_v(frame1, frame2):
        return relative_velocity(frame1.velocity, frame2.velocity)

# event object definition
class Event:
    def __init__(self, frame_name: str, t: float, x: float):
        self.frame_name = frame_name
        self.t = t
        self.x = x
        self.get_frame_velocity = self.get_frame_velocity(frame_name)

    @staticmethod
    def get_frame_velocity(frame_name):
        frame_name = "P"
        return frame_name



Frame_A = Frame("A", 0.5)
Frame_B = Frame("B", 0.7)

Event_1_A = Event("A", 14, 30)
Event_2_B = Event("B", 7, 51)
print(Event_1_A.frame_name)

print(Frame.relative_v(Frame_A,Frame_B))
print(Frame_B.all_frames)
print(Frame_A.all_frames)
