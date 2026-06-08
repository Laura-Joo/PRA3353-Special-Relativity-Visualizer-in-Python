import math as m
from pyscript import document

# constants
c = 1

# Diagram controls
ORIGIN_X = 525
ORIGIN_Y = 600
SCALE = 20
axis_length = 30
amount_of_t_ticks = 30
amount_of_x_ticks = 26
tick_size = 10
static_axes_tick_size = 5
LIGHTCONE_SCALE = 70
worldline_length = 50
grid_count = 100

general_scale = 2

def spacetime_to_screen(x, t):

    screen_x = ORIGIN_X + general_scale*x * SCALE
    screen_y = ORIGIN_Y - general_scale*t * SCALE

    return (screen_x, screen_y)

# array management
all_frames = {}

def add_frame_to_total(frame):
    all_frames[frame.name] = frame

def get_frame_by_name(name):
    return all_frames.get(name)

# Lorentz transformation functions
def gamma_factor(v):
    gamma = 1/m.sqrt(1-((v*v)/(c*c)))
    return gamma

def relative_velocity(vA,vB):
    # determine the relative velocity of frame B as seen by frame A, where vA and vB are measured by frame S
    V = (vB - vA)/(1-(vB*vA)/(c*c))
    return V
    # EXTREMELY IMPORTANT: if the input is vA,vB then what we get is vB|A (the velocity of B as seen by A). If the input is vB,vA we get vA|B.

def lorentz_transform(t, x, v):

    gamma = gamma_factor(v)

    T = gamma*(t - (v * x)/(c * c))
    X = gamma*(x - v * t)
    return (T, X)

# Object definitions
class Frame:
    next_id = 0
    
    def __init__(self, name: str, color: str, velocity: float):
        self.id = Frame.next_id
        Frame.next_id += 1
        
        self.name = name
        self.color = color
        self.velocity = velocity
    
    def __repr__(self):
        return f"Frame({self.name}, v={self.velocity})"    

# Creating Frame objects & adding to array collection

lab_frame_velocity = 0.0
Lab_Frame = Frame("Observer", "black", 0.0)

Frame_A = Frame("A", "red", 0.0)
Frame_B = Frame("B", "green", 0.0)
Frame_C = Frame("C", "blue", 0.0)

add_frame_to_total(Lab_Frame)
add_frame_to_total(Frame_A)
add_frame_to_total(Frame_B)
add_frame_to_total(Frame_C)

### GENERAL FUNCTIONS ###

def clamp_velocity(event):

    inputbox = event.target

    try:
        value = float(inputbox.value)
    except:
        inputbox.value = "0"
        return
    
    value = max(-0.99, min(0.99, value))
    inputbox.value = str(value)

    update_velocities(event)

# Retrieve velocity inputs from entered values
def sync_frame_velocities():
    Frame_A.velocity = float(document.getElementById("velocity_A").value or 0)
    Frame_B.velocity = float(document.getElementById("velocity_B").value or 0)
    Frame_C.velocity = float(document.getElementById("velocity_C").value or 0)

### DRAWING FUNCTIONS ###

# line_creator: takes v of a frame and adjusts (or 'draws') the ct-line in the html with the corresponding line_id
def t_line_creator(v: float, line_id: str):
    
    line = document.getElementById(line_id)

    x1 = -v * axis_length
    t1 = -axis_length

    x2 = v * axis_length
    t2 = axis_length

    screen_x1, screen_y1 = spacetime_to_screen(x1, t1)
    screen_x2, screen_y2 = spacetime_to_screen(x2, t2)

    line.setAttribute("x1", str(screen_x1))
    line.setAttribute("y1", str(screen_y1))
    line.setAttribute("x2", str(screen_x2))
    line.setAttribute("y2", str(screen_y2))

# Create ticks on t-axes
def create_tick_marks(prefix, amount, color="black"):

    tick_layer = document.getElementById("axis_layer")

    for i in range(-amount, amount + 1):

        tick = document.createElementNS("http://www.w3.org/2000/svg","line")
        tick.id = f"{prefix}_{i}"
        tick.setAttribute("stroke", color)
        tick.setAttribute("stroke-width", "2")

        tick_layer.appendChild(tick)

# Create ticks on the black static axes
def draw_static_axes_ticks(event=None):

    for i in range(-amount_of_t_ticks, amount_of_t_ticks + 1):

        # coordinates on stationary ct-axis
        world_t = i
        world_x = 0

        screen_x, screen_y = spacetime_to_screen(world_x, world_t)

        x1 = screen_x - static_axes_tick_size
        y1 = screen_y

        x2 = screen_x + static_axes_tick_size
        y2 = screen_y

        tick = document.getElementById(f"static_x_axis_tick_{i}")

        tick.setAttribute("x1", str(x1))
        tick.setAttribute("y1", str(y1))
        tick.setAttribute("x2", str(x2))
        tick.setAttribute("y2", str(y2))

    for i in range(-amount_of_x_ticks, amount_of_x_ticks + 1):

        # coordinates on stationary x-axis
        world_t = 0
        world_x = i

        screen_x, screen_y = spacetime_to_screen(world_x, world_t)

        x1 = screen_x
        y1 = screen_y + static_axes_tick_size

        x2 = screen_x
        y2 = screen_y - static_axes_tick_size

        tick = document.getElementById(f"static_y_axis_tick_{i}")

        tick.setAttribute("x1", str(x1))
        tick.setAttribute("y1", str(y1))
        tick.setAttribute("x2", str(x2))
        tick.setAttribute("y2", str(y2))

# draw_t_ticks: draw tickmarks on the axes of the frames
def draw_t_ticks(v: float, prefix: str):

    gamma = gamma_factor(v)

    for i in range(-amount_of_t_ticks, amount_of_t_ticks + 1):

        # Proper time interval
        tau = i

        # Hyperbolic Minkowski coordinates
        world_t = gamma * tau
        world_x = v * gamma * tau

        screen_x, screen_y = spacetime_to_screen(world_x,world_t)

        # perpendicular direction
        perp_x = -1
        perp_y = v

        length = m.sqrt(perp_x**2 + perp_y**2)

        perp_x /= length
        perp_y /= length

        x1 = screen_x - perp_x * tick_size
        y1 = screen_y - perp_y * tick_size

        x2 = screen_x + perp_x * tick_size
        y2 = screen_y + perp_y * tick_size

        tick = document.getElementById(f"{prefix}_{i}")

        tick.setAttribute("x1", str(x1))
        tick.setAttribute("y1", str(y1))
        tick.setAttribute("x2", str(x2))
        tick.setAttribute("y2", str(y2))

# Create static gridlines
def create_static_grid():
    grid_layer = document.getElementById("grid_layer")

    # Vertical lines
    # (x_min, x_max)
    for i in range(-30, 27):

        line = document.createElementNS("http://www.w3.org/2000/svg","line")

        line.id = f"grid_x_{i}"

        x, y1 = spacetime_to_screen(i, -30)
        x, y2 = spacetime_to_screen(i, 30)

        line.setAttribute("x1", str(x))
        line.setAttribute("y1", str(y1))
        line.setAttribute("x2", str(x))
        line.setAttribute("y2", str(y2))

        line.setAttribute("stroke", "black")
        line.setAttribute("stroke-width", "1")
        line.setAttribute("opacity", "0.2")

        grid_layer.appendChild(line)

    # Horizontal lines
    # (y_min, y_max)
    for i in range(-30, 31):

        line = document.createElementNS("http://www.w3.org/2000/svg","line")

        x1, y = spacetime_to_screen(-30, i)
        x2, y = spacetime_to_screen(27, i)

        line.setAttribute("x1", str(x1))
        line.setAttribute("y1", str(y))
        line.setAttribute("x2", str(x2))
        line.setAttribute("y2", str(y))

        line.setAttribute("stroke", "black")
        line.setAttribute("stroke-width", "1")
        line.setAttribute("opacity", "0.2")

        grid_layer.appendChild(line)       

def draw_t_grid(frame):

    remove_t_grid(frame)

    v = relative_velocity(lab_frame_velocity, frame.velocity)
    gamma = gamma_factor(v)

    for i in range(-grid_count, grid_count + 1):
        
        translation = i / gamma
        
        x1 = -v * axis_length + translation
        t1 = -axis_length

        x2 = v * axis_length + translation
        t2 = axis_length

        screen_x1, screen_y1 = spacetime_to_screen(x1, t1)
        screen_x2, screen_y2 = spacetime_to_screen(x2, t2)

        t_line = document.createElementNS("http://www.w3.org/2000/svg","line")
        t_line.id = f"t_line_{frame.name}_{i}"

        t_line.setAttribute("x1", str(screen_x1))
        t_line.setAttribute("y1", str(screen_y1))
        t_line.setAttribute("x2", str(screen_x2))
        t_line.setAttribute("y2", str(screen_y2))
        t_line.setAttribute("stroke", f"{frame.color}")
        t_line.setAttribute("opacity", "0.5")

        grid_layer = document.getElementById("grid_layer")
        grid_layer.appendChild(t_line)

def remove_t_grid(frame):
    for i in range(-grid_count, grid_count + 1):
        t_line = document.getElementById(f"t_line_{frame.name}_{i}")
        if not t_line:
            continue
        t_line.remove() 

def draw_x_grid(frame):

    remove_x_grid(frame)

    v = relative_velocity(lab_frame_velocity, frame.velocity)
    gamma = gamma_factor(v)

    for i in range(-grid_count, grid_count + 1):
        
        translation = i / gamma

        x1 = -axis_length / v
        t1 = -axis_length + translation

        x2 = axis_length / v
        t2 = axis_length + translation

        screen_x1, screen_y1 = spacetime_to_screen(x1, t1)
        screen_x2, screen_y2 = spacetime_to_screen(x2, t2)

        x_line = document.createElementNS("http://www.w3.org/2000/svg","line")
        x_line.id = f"x_line_{frame.name}_{i}"

        x_line.setAttribute("x1", str(screen_x1))
        x_line.setAttribute("y1", str(screen_y1))
        x_line.setAttribute("x2", str(screen_x2))
        x_line.setAttribute("y2", str(screen_y2))
        x_line.setAttribute("stroke", f"{frame.color}")
        x_line.setAttribute("opacity", "0.5")

        if i == 0:
            x_line.setAttribute("opacity", "1")

        grid_layer = document.getElementById("grid_layer")
        grid_layer.appendChild(x_line)

def remove_x_grid(frame):
    for i in range(-grid_count, grid_count + 1):
        x_line = document.getElementById(f"x_line_{frame.name}_{i}")
        if not x_line:
            continue
        x_line.remove() 


def handle_grid_A_checkbox(event):

    checkbox = event.target

    if checkbox.checked:
        draw_t_grid(Frame_A)
        draw_x_grid(Frame_A)
    else:
        remove_t_grid(Frame_A)
        remove_x_grid(Frame_A)

def handle_grid_B_checkbox(event):

    checkbox = event.target

    if checkbox.checked:
        draw_t_grid(Frame_B)
        draw_x_grid(Frame_B)
    else:
        remove_t_grid(Frame_B)
        remove_x_grid(Frame_B)

def handle_grid_C_checkbox(event):

    checkbox = event.target

    if checkbox.checked:
        draw_t_grid(Frame_C)
        draw_x_grid(Frame_C)
    else:
        remove_t_grid(Frame_C)
        remove_x_grid(Frame_C)

### LIGHTCONE PER EVENT ###

def draw_light_cones(event_number):
   
    remove_lightcones(event_number)

    point = document.getElementById(f"event_point_{event_number}")
    if point is None:
        return
    
    x_coordinate = float(point.getAttribute("cx"))
    y_coordinate = float(point.getAttribute("cy"))

    positive_x_beginpoint = x_coordinate - (LIGHTCONE_SCALE * 10)
    positive_y_beginpoint = y_coordinate + (LIGHTCONE_SCALE * 10)

    negative_x_beginpoint = x_coordinate + (LIGHTCONE_SCALE * 10)
    negative_y_beginpoint = y_coordinate + (LIGHTCONE_SCALE * 10)

    positive_x_endpoint = x_coordinate + (LIGHTCONE_SCALE * 10)
    positive_y_endpoint = y_coordinate - (LIGHTCONE_SCALE * 10)

    negative_x_endpoint = x_coordinate - (LIGHTCONE_SCALE * 10)
    negative_y_endpoint = y_coordinate - (LIGHTCONE_SCALE * 10)

    positive_lightcone = document.createElementNS("http://www.w3.org/2000/svg","line")
    positive_lightcone.id = f"pos_lightcone_{event_number}"
    positive_lightcone.setAttribute("x1", str(positive_x_beginpoint))
    positive_lightcone.setAttribute("y1", str(positive_y_beginpoint))
    positive_lightcone.setAttribute("x2", str(positive_x_endpoint))
    positive_lightcone.setAttribute("y2", str(positive_y_endpoint))
    positive_lightcone.setAttribute("stroke", "black")

    negative_lightcone = document.createElementNS("http://www.w3.org/2000/svg","line")
    negative_lightcone.id = f"neg_lightcone_{event_number}"
    negative_lightcone.setAttribute("x1", str(negative_x_beginpoint))
    negative_lightcone.setAttribute("y1", str(negative_y_beginpoint))
    negative_lightcone.setAttribute("x2", str(negative_x_endpoint))
    negative_lightcone.setAttribute("y2", str(negative_y_endpoint))
    negative_lightcone.setAttribute("stroke", "black")

    event_layer = document.getElementById("event_layer")

    event_layer.appendChild(positive_lightcone)
    event_layer.appendChild(negative_lightcone)

def remove_lightcones(event_number):
    positive_lightcone = document.getElementById(f"pos_lightcone_{event_number}")
    negative_lightcone = document.getElementById(f"neg_lightcone_{event_number}")
    if not positive_lightcone:
        return
    
    positive_lightcone.remove()

    if not negative_lightcone:
        return
    
    negative_lightcone.remove()

def handle_lightcone_checkbox(event):

    checkbox = event.target

    event_number = checkbox.id.replace("lightcone_checkbox_", "")

    if checkbox.checked:
        draw_light_cones(event_number)

    else:
        remove_lightcones(event_number)


### WORLDLINE PER EVENT ###

# Draw worldline through an event
def draw_worldline(event_number):
    
    remove_worldline(event_number)

    point = document.getElementById(f"event_point_{event_number}")
    if point is None:
        return
    
    x_shift = float(point.getAttribute("cx")) - ORIGIN_X
    y_shift = float(point.getAttribute("cy")) - ORIGIN_Y

    selected_frame_name = document.getElementById(f"event_frames_selection_{event_number}").value
    selected_frame = get_frame_by_name(selected_frame_name)

    v = relative_velocity(lab_frame_velocity, selected_frame.velocity)

    x1 = -v * worldline_length
    t1 = -worldline_length

    x2 = v * worldline_length
    t2 = worldline_length

    screen_x1, screen_y1 = spacetime_to_screen(x1, t1)
    screen_x2, screen_y2 = spacetime_to_screen(x2, t2)

    screen_x1 += x_shift
    screen_y1 += y_shift
    screen_x2 += x_shift
    screen_y2 += y_shift

    worldline = document.createElementNS("http://www.w3.org/2000/svg","line")
    worldline.id = f"worldline_{event_number}"
    worldline.setAttribute("stroke", "orange")

    worldline.setAttribute("x1", str(screen_x1))
    worldline.setAttribute("y1", str(screen_y1))
    worldline.setAttribute("x2", str(screen_x2))
    worldline.setAttribute("y2", str(screen_y2))

    event_layer = document.getElementById("event_layer")

    event_layer.appendChild(worldline)

# Remove the worldline through an event    
def remove_worldline(event_number):
    worldline = document.getElementById(f"worldline_{event_number}")

    if not worldline:
        return
    
    worldline.remove()

def handle_worldline_checkbox(event):

    checkbox = event.target

    event_number = checkbox.id.replace("worldline_checkbox_", "")

    if checkbox.checked:
        draw_worldline(event_number)

    else:
        remove_worldline(event_number)

# Update the position of axes labels
def update_axis_label(v, label_id):

    label = document.getElementById(label_id)

    x = v * axis_length
    t = 0

    screen_x, screen_y = spacetime_to_screen(x, t)
    screen_x += 10
    screen_y = 40

    label.setAttribute("x", str(screen_x + 10))
    label.setAttribute("y", str(screen_y))

# Runs line creator and draw_ticks functions
def update_t_axes(event=None):

    velocity_A_in_view = relative_velocity(lab_frame_velocity,Frame_A.velocity)
    velocity_B_in_view = relative_velocity(lab_frame_velocity,Frame_B.velocity)
    velocity_C_in_view = relative_velocity(lab_frame_velocity,Frame_C.velocity)

    # Create frame wordlines
    t_line_creator(velocity_A_in_view, "t_axis_prime_A")
    t_line_creator(velocity_B_in_view, "t_axis_prime_B")
    t_line_creator(velocity_C_in_view, "t_axis_prime_C")

    # Draw ticks on the newly created axes
    draw_static_axes_ticks()
    draw_t_ticks(velocity_A_in_view, "tick_A")
    draw_t_ticks(velocity_B_in_view, "tick_B")
    draw_t_ticks(velocity_C_in_view, "tick_C")

    # Assign labels to each frame worldine
    update_axis_label(velocity_A_in_view, "label_A")
    update_axis_label(velocity_B_in_view, "label_B")
    update_axis_label(velocity_C_in_view, "label_C")

# Update axes and event points if vA/B/C changes
def update_velocities(event=None):

    sync_frame_velocities()

    document.getElementById("velocity_A_display").innerText = f"vA = {relative_velocity(lab_frame_velocity,Frame_A.velocity):.2f}c"
    document.getElementById("velocity_B_display").innerText = f"vB = {relative_velocity(lab_frame_velocity,Frame_B.velocity):.2f}c"
    document.getElementById("velocity_C_display").innerText = f"vC = {relative_velocity(lab_frame_velocity,Frame_C.velocity):.2f}c"

    update_t_axes() # Draw axes with ticks on them
    update_all_event_positions() # Red event dots updating

    checkbox_A = document.getElementById("gridlines_A") # Update gridlines when velocities change
    if checkbox_A.checked:
        remove_t_grid(Frame_A)
        remove_x_grid(Frame_A)
        draw_t_grid(Frame_A)
        draw_x_grid(Frame_A)

    checkbox_B = document.getElementById("gridlines_B") # Update gridlines when velocities change
    if checkbox_B.checked:
        remove_t_grid(Frame_B)
        remove_x_grid(Frame_B)
        draw_t_grid(Frame_B)
        draw_x_grid(Frame_B)

    checkbox_C = document.getElementById("gridlines_C") # Update gridlines when velocities change
    if checkbox_C.checked:
        remove_t_grid(Frame_C)
        remove_x_grid(Frame_C)
        draw_t_grid(Frame_C)
        draw_x_grid(Frame_C)

# Update axes when slider is adjusted
def update_lab_frame(event=None):

    global lab_frame_velocity

    lab_frame_velocity = float(
        document.getElementById("lab_velocity_slider").value)
    
    document.getElementById("lab_velocity_display").innerText = f"{lab_frame_velocity:.2f}c"

    update_velocities()
    update_t_axes()
    update_all_event_positions()

# Create axis label objects
def create_axis_label(label_id, text, color="black"):

    axis_layer = document.getElementById("axis_layer")

    label = document.createElementNS("http://www.w3.org/2000/svg","text")
    label.id = label_id
    label.textContent = text
    label.setAttribute("fill", color)
    label.setAttribute("font-size", "20")

    axis_layer.appendChild(label)

### VIEW ADJUSTING FUNCTIONS ###

def set_view_velocity(v):

    global lab_frame_velocity

    lab_frame_velocity = v

    slider = document.getElementById("lab_velocity_slider")
    slider.value = str(v)

    document.getElementById("lab_velocity_display").innerText = f"{v:.2f}c"

    update_t_axes()

def view_A(event=None):
    set_view_velocity(Frame_A.velocity)
    update_velocities()
    update_all_event_positions()

def view_B(event=None):
    set_view_velocity(Frame_B.velocity)
    update_velocities()
    update_all_event_positions()

def view_C(event=None):
    set_view_velocity(Frame_C.velocity)
    update_velocities()
    update_all_event_positions()

def view_lab(event=None):
    set_view_velocity(0.0)
    update_velocities()
    update_all_event_positions()


### EVENT FUNCTIONS ###

event_counter = 0

# Make points move as the axes are shifted    
def update_event_position(event_number):
    point = document.getElementById(f"event_point_{event_number}")
    if point is None:
        return
    
    t_input = document.getElementById(f"t_{event_number}")
    x_input = document.getElementById(f"x_{event_number}")
    frame_input = document.getElementById(f"event_frames_selection_{event_number}")

    if not t_input or not x_input or not frame_input:
        return
    if t_input.value == "" or x_input.value == "":
        return

    try:
        t = float(t_input.value)
        x = float(x_input.value)
    except:
        return

    event_frame = get_frame_by_name(frame_input.value)
    if event_frame is None:
        return

    v = relative_velocity(event_frame.velocity, lab_frame_velocity)
    T, X = lorentz_transform(t, x, v)

    screen_x, screen_y = spacetime_to_screen(X,T)

    point.setAttribute("cx", str(screen_x))
    point.setAttribute("cy", str(screen_y))


    # Redraw lightcones if checkbox is checked and coordinates/velocities change
    checkbox_lightcones = document.getElementById(f"lightcone_checkbox_{event_number}")

    if checkbox_lightcones is not None and checkbox_lightcones.checked:

        remove_lightcones(event_number)
        draw_light_cones(event_number)

        
    # Redraw worldline if checkbox is checked and coordinates/velocities change
    checkbox_worldline = document.getElementById(f"worldline_checkbox_{event_number}")

    if checkbox_worldline is not None and checkbox_worldline.checked:

        remove_worldline(event_number)
        draw_worldline(event_number)

    # Add and fill in the label of the new event
    label = document.getElementById(f"event_label_{event_number}")
    label.setAttribute("x", str(screen_x + 10))
    label.setAttribute("y", str(screen_y + 10))

def update_all_event_positions():
    points = document.querySelectorAll("[id^='event_point_']")
    for point in points:
        event_number = point.id.split("_")[-1]
        update_event_position(event_number)

def transform_event_button(event_number):

    sync_frame_velocities()

    # Selected frames
    event_frame_name = document.getElementById(f"event_frames_selection_{event_number}").value
    target_frame_name = document.getElementById(f"target_frames_selection_{event_number}").value

    event_frame = get_frame_by_name(event_frame_name)
    target_frame = get_frame_by_name(target_frame_name)

    # Event coordinates
    x = float(document.getElementById(f"x_{event_number}").value)
    t = float(document.getElementById(f"t_{event_number}").value)

    # Relative velocity
    v = relative_velocity(event_frame.velocity,target_frame.velocity)

    # Lorentz transform
    T, X = lorentz_transform(t, x, v)

    document.getElementById(f"result_{event_number}").innerText = f"T = {T:.3f}, X = {X:.3f}"
    update_event_position(event_number)

# Remove the created event
def remove_event(event_number):

    # Remove the entire event 'div'
    event_div = document.getElementById(f"event_{event_number}")
    if event_div is not None:
        event_div.remove()
    
    # Remove the point element
    point = document.getElementById(f"event_point_{event_number}")
    if point is not None:
        point.remove()

    # Remove the label
    label = document.getElementById(f"event_label_{event_number}")
    if label is not None:
        label.remove()

    # Remove the lightcones (if present)
    remove_lightcones(event_number)

    # Remove worldline through event (if present)
    remove_worldline(event_number)


# Generate an input-box in the HTML
def make_input(id, type="number", width="60px", placeholder=""):
    element = document.createElement("input")
    element.type = type
    element.id = id
    element.style.width = width
    element.placeholder = placeholder
    return element

# Create a new event 'div'
def add_event(event=None):
    global event_counter
    event_counter += 1

    # Create container space
    container = document.getElementById("event_container")

    # Create an event 'div' (so sort of object space)
    new_event = document.createElement("div")
    new_event.id = f"event_{event_counter}"
    new_event.style.border = "1px solid black"
    new_event.style.display = "inline-block"
    new_event.style.margin = "5px"
    new_event.style.padding = "10px"
    
    # Create title (= event number) in front of input boxes
    title = document.createElement("div")
    title.innerText = f"Event {event_counter}:"
    new_event.appendChild(title)

    # Create event frame text in front of dropbox
    event_label = document.createElement("span")
    event_label.innerText = " Event Frame :"
    new_event.appendChild(event_label)

    # Create a dropbox for event frame selection
    event_frame_select = document.createElement("select")
    event_frame_select.onchange = lambda e, n=event_counter: update_event_position(n)
    event_frame_select.id = f"event_frames_selection_{event_counter}"
    for f in all_frames.values():
        option = document.createElement("option")
        option.value = f.name
        option.innerText = f.name
        event_frame_select.appendChild(option)
    event_frame_select.style.margin = "10px"
    new_event.appendChild(event_frame_select)

    # Create t-input text
    t_label = document.createElement("span")
    t_label.innerText = " t: "
    new_event.appendChild(t_label)

    # Create t-input box
    t_input = make_input(f"t_{event_counter}",placeholder="t")
    t_input.oninput = lambda e, n=event_counter: update_event_position(n)
    new_event.appendChild(t_input)

    # Create x-input text
    x_label = document.createElement("span")
    x_label.innerText = " x: "
    new_event.appendChild(x_label)

    # Create x-input box
    x_input = make_input(f"x_{event_counter}",placeholder="x")
    x_input.oninput = lambda e, n=event_counter: update_event_position(n)
    new_event.appendChild(x_input)

    # Insert line break
    line_break = document.createElement("br")
    new_event.appendChild(line_break)

    # Create target frame text after dropbox
    target_label = document.createElement("span")
    target_label.innerText = " Target Frame :"
    new_event.appendChild(target_label)

    # Create a dropbox for target frame selection
    target_frame_select = document.createElement("select")
    target_frame_select.id = f"target_frames_selection_{event_counter}"
    for f in all_frames.values():
        option = document.createElement("option")
        option.value = f.name
        option.innerText = f.name
        target_frame_select.appendChild(option)
    target_frame_select.style.margin = "10px"
    new_event.appendChild(target_frame_select)

    # Create transform button
    trans_button = document.createElement("button")
    trans_button.type = "button"
    trans_button.innerText = "Transform"
    trans_button.onclick = lambda e, n=event_counter: transform_event_button(n)
    new_event.appendChild(trans_button)

    # Create result container
    result_container = document.createElement("div")
    result_container.style.marginTop = "10px"
    result_container.style.marginBottom = "10px"

    # Create transformed coordinate text before result
    result_label = document.createElement("span")
    result_label.innerText = "Transformed coordinates: "
    result_container.appendChild(result_label)

    # Create result display
    result = document.createElement("span")
    result.id = f"result_{event_counter}"
    result.innerText = ""
    result_container.appendChild(result)

    # Add entire result container
    new_event.appendChild(result_container)

    # Create SVG dot and insert into HTML
    event_point = document.createElementNS("http://www.w3.org/2000/svg","circle")
    event_point.id = f"event_point_{event_counter}"
    event_point.setAttribute("r", "6")
    event_point.setAttribute("fill", "orange")
    event_layer = document.getElementById("event_layer")
    event_layer.appendChild(event_point)

    # Create SVG dot label
    event_label = document.createElementNS("http://www.w3.org/2000/svg","text")
    event_label.id = f"event_label_{event_counter}"
    event_label.textContent = f"E{event_counter}"
    event_label.setAttribute("fill", "orange")
    event_label.setAttribute("font-size", "16")
    event_layer.appendChild(event_label)

    # Create 'show lightcone' checkbox & label container space
    lightcone_checkbox_container = document.createElement("div")

    lightcone_checkbox = document.createElement("input")
    lightcone_checkbox.type = "checkbox"
    lightcone_checkbox.id = f"lightcone_checkbox_{event_counter}"

    lightcone_checkbox.onchange = handle_lightcone_checkbox

    lightcone_checkbox_label = document.createElement("label")
    lightcone_checkbox_label.setAttribute("for", f"lightcone_checkbox_{event_counter}")
    lightcone_checkbox_label.innerText = "Show lightcone"

    lightcone_checkbox_container.appendChild(lightcone_checkbox)
    lightcone_checkbox_container.appendChild(lightcone_checkbox_label)

    new_event.appendChild(lightcone_checkbox_container)

    # Create 'worldline' checkbox & label container space
    worldline_checkbox_container = document.createElement("div")

    worldline_checkbox = document.createElement("input")
    worldline_checkbox.type = "checkbox"
    worldline_checkbox.id = f"worldline_checkbox_{event_counter}"

    worldline_checkbox.onchange = handle_worldline_checkbox

    worldline_checkbox_label = document.createElement("label")
    worldline_checkbox_label.setAttribute("for", f"worldline_checkbox_{event_counter}")
    worldline_checkbox_label.innerText = "Show worldline "

    container_tooltip = document.createElement("text")
    container_tooltip.className = "tooltip-container"

    symbol = document.createElement("text")
    symbol.innerText = "ⓘ"

    tooltip = document.createElement("div")
    tooltip.className = "tooltip-text"
    tooltip.innerText = "Please note: An event is a singular moment in spacetime (e.g. an exploding firecracker). By adding a worldline to the diagram, you are no longer looking at an event but at an object travelling through spacetime! The worldline is then the path the object travels with the set frame velocity."

    container_tooltip.appendChild(symbol)
    container_tooltip.appendChild(tooltip)

    worldline_checkbox_container.appendChild(worldline_checkbox)
    worldline_checkbox_container.appendChild(worldline_checkbox_label)
    worldline_checkbox_container.appendChild(container_tooltip)
    new_event.appendChild(worldline_checkbox_container)

    # Create 'Remove Event' button
    remove_button = document.createElement("button")
    remove_button.type = "button"
    remove_button.innerText = f"Remove Event {event_counter}"
    remove_button.onclick = lambda e, n=event_counter: remove_event(n)
    new_event.appendChild(remove_button)

    # Append the entire event to the container space
    container.appendChild(new_event)

# Run all relevant functions
def init():
    create_tick_marks("static_x_axis_tick", amount_of_t_ticks, "black")
    create_tick_marks("static_y_axis_tick", amount_of_x_ticks, "black")

    create_tick_marks("tick_A", amount_of_t_ticks, "red")
    create_tick_marks("tick_B", amount_of_t_ticks, "green")
    create_tick_marks("tick_C", amount_of_t_ticks, "blue")

    create_axis_label("label_A", "A", "red")
    create_axis_label("label_B", "B", "green")
    create_axis_label("label_C", "C", "blue")

    create_static_grid()
    update_lab_frame()
    update_velocities()

init()

