import math as m
from pyscript import document

# constants
c = 1

# arrays
all_events = []
all_frames = []

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

    # call separate lorentz-functions to transform x and t
    T = lorentz_time_transform(t, x, v)
    X = lorentz_position_transform(t, x, v)
    return (T, X)

def transform_event(event, target_frame):
    T, X = lorentz_transform(event.t, event.x, relative_velocity(event.frame.velocity, target_frame.velocity))
    return Event(target_frame, T, X)

# Array management functions
def add_event_to_total(event):
    all_events.append(event)

def remove_event_from_total(event):
    all_events.remove(event)

def add_frame_to_total(frame):
    all_frames.append(frame)

def remove_frame_from_total(frame):
    all_frames.remove(frame)

def get_frame_by_name(name):
    for frame in all_frames:
        if frame.name == name:
            return frame
    return None

# frame object definition
class Frame:
    next_id = 0
    
    def __init__(self, name: str, velocity: float):
        self.id = Frame.next_id
        Frame.next_id += 1
        
        self.name = name
        self.velocity = velocity
    
    def __repr__(self):
        return f"Frame({self.name}, v={self.velocity})"    

# event object definition
class Event:
    next_id = 0

    def __init__(self, frame: Frame, t: float, x: float):
        self.id = Event.next_id
        Event.next_id += 1

        self.frame = frame
        self.t = t
        self.x = x

    def __repr__(self):
        return f"Event({self.frame.name}, t={self.t}, x={self.x}, event_number={self.next_id})"

# Creating Frame objects & adding to array collection
Frame_A = Frame("A", 0.0)
Frame_B = Frame("B", 0.0)
Frame_C = Frame("C", 0.0)

add_frame_to_total(Frame_A)
add_frame_to_total(Frame_B)
add_frame_to_total(Frame_C)


### CALCULATOR PART ###

# transform_btn: function that handles the coordinate 'Transform' button of the program (separate from the line drawing stuff)
def transform_btn(event):
    Frame_A.velocity = float(document.getElementById("velocity_A").value)
    Frame_B.velocity = float(document.getElementById("velocity_B").value)
    Frame_C.velocity = float(document.getElementById("velocity_C").value)


    event_frame_name = document.getElementById("event_frames_selection").value
    target_frame_name = document.getElementById("target_frames_selection").value

    event_frame = get_frame_by_name(event_frame_name)
    target_frame = get_frame_by_name(target_frame_name)

    x = float(document.getElementById("x_input").value)
    t = float(document.getElementById("t_input").value)

    v_event = event_frame.velocity
    v_target = target_frame.velocity

    v = relative_velocity(v_event, v_target)
    T, X = lorentz_transform(t,x,v)

    document.getElementById("result").innerText = f"T = {T:.3f}, X = {X:.3f}"


### LINE DRAWING PART ###

# line_creator: takes v of a frame and adjusts (or 'draws') the ct-line in the html with the corresponding line_id
def t_line_creator(v: float, line_id: str):
    
    line = document.getElementById(line_id)

    origin_x = 300
    origin_y = 600

    scale = 300    
    screen_x1 = origin_x
    screen_y1 = origin_y

    axis_length = 1

    x2 = v * axis_length
    t2 = axis_length

    screen_x2 = origin_x + x2 * scale
    screen_y2 = origin_y - t2 * scale

    line.setAttribute("x1", str(screen_x1))
    line.setAttribute("y1", str(screen_y1))
    line.setAttribute("x2", str(screen_x2))
    line.setAttribute("y2", str(screen_y2))

# update_t_axes: vA/B/C is set equal to what the user entered, and then line_creator is run for those v's.
def update_t_axes(event=None):

    vA = Frame_A.velocity
    vB = Frame_B.velocity
    vC = Frame_C.velocity

    vA_rel = relative_velocity(active_frame.velocity, vA)
    vB_rel = relative_velocity(active_frame.velocity, vB)
    vC_rel = relative_velocity(active_frame.velocity, vC)

    t_line_creator(vA_rel, "t_axis_prime_A")
    t_line_creator(vB_rel, "t_axis_prime_B")
    t_line_creator(vC_rel, "t_axis_prime_C")

# enter_velocities: 
def enter_velocities(event=None):

    Frame_A.velocity = float(document.getElementById("velocity_A").value)
    Frame_B.velocity = float(document.getElementById("velocity_B").value)
    Frame_C.velocity = float(document.getElementById("velocity_C").value)

    document.getElementById("velocity_A_display").innerText = f"vA = {Frame_A.velocity:.2f}c"
    document.getElementById("velocity_B_display").innerText = f"vB = {Frame_B.velocity:.2f}c"
    document.getElementById("velocity_C_display").innerText = f"vC = {Frame_C.velocity:.2f}c"

    update_t_axes(event)

active_frame = Frame_A

def set_view(frame_name, event=None):
    global active_frame
    active_frame = get_frame_by_name(frame_name)
    update_t_axes()

def view_A(event=None):
    set_view("A")

def view_B(event=None):
    set_view("B")

def view_C(event=None):
    set_view("C")