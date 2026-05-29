import numpy as np
import math as m

# constants
c = 1

# Lorentz transformation functions
def gamma_factor(v):
    gamma = 1/m.sqrt(1-((v*v)/(c*c)))
    return gamma

def calculate_relative_velocity(vA,vB):
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

    # call separate lorentz-functions to transform x and t
    T = lorentz_time_transform(t, x, v)
    X = lorentz_position_transform(t, x, v)
    return (T, X)

#def event_transformation()

# frame object definition
class Frame:
    all_frames = {}
    def __init__(self, name: str, velocity: float):
        self.name = name
        self.velocity = velocity
        self.all_frames[self.name] = self.velocity
    
    @staticmethod
    def relative_v(frame1, frame2):
        return calculate_relative_velocity(frame1.velocity, frame2.velocity)

# event object definition
class Event:
    def __init__(self, frame_name: str, t: float, x: float):
        self.frame_name = frame_name
        self.t = t
        self.x = x
        self.frame_velocity = self.get_frame_velocity(self.frame_name)

    @staticmethod
    def get_frame_velocity(frame_name):
        try: 
            return Frame.all_frames[frame_name]
        except KeyError:
            raise KeyError("This frame does not exist")
        
    def frame_switch(self, new_frame_name):
        new_frame_velocity = Event.get_frame_velocity(new_frame_name)
        relative_velocity = calculate_relative_velocity(self.frame_velocity, new_frame_velocity)
        new_x = lorentz_position_transform(self.t, self.x, relative_velocity)
        new_t = lorentz_time_transform(self.t, self.x, relative_velocity)
        self.frame_name = new_frame_name
        self.frame_velocity = new_frame_velocity
        self.x = new_x
        self.t = new_t


### testing ###
Frame_A = Frame("A", 0.5)
Frame_B = Frame("B", 0.7) 
#Frame_B = Frame("C", 1) #issue to fix: changing Frame  doens't change its entry in the dictionary, it justadds a new entry. 
#However, only if you change the name of the frame, (so B->C), if you only change the value then you arefine

Event_1 = Event("A", 14, 30)
Event_2 = Event("B", 7, 51)
print(Event_1.frame_name)

print(Frame.relative_v(Frame_A,Frame_B))
print(Frame_B.all_frames)
print(Frame_A.all_frames)
print(Event_1.frame_velocity)

Event_1.frame_switch("B")
print(Event_1.frame_name, Event_1.t, Event_1.x)
