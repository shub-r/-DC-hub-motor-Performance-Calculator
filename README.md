![Logo image1](https://github.com/user-attachments/assets/8eba302e-c8f1-4546-9e0b-66469b2d8a95)

# DC Hub Motor Performance Estimator/Calculator (Python)

The DC Hub Motor Performance Calculator is a Python tool designed to estimate the performance of a DC hub motor based on user-supplied design inputs. It provides key parameters such as operating speed, torque, efficiency, heat loss, and temperature rise, giving you a practical insight into motor behavior.


## Requirements & Input Data
**Primary Motor Design Inputs:**
1. **Number of stator slots:** Determines the spaces for coil placement, influencing the motor’s magnetic flux distribution.  
2. **Wire gauge (AWG):** Specifies the wire thickness, affecting resistance and current-carrying capacity.  

3. **Number of turns per coil:** Impacts the coil’s electromagnetic strength and overall motor constant.  

**Additional Inputs:**

4. **Magnet strength:** Indicates the intensity of the magnetic field (in Tesla or relative scale) driving the motor.  
5. **Number of magnets:** Sets the total magnetic field strength within the rotor.  
6. **Rotor radius (cm):** Influences torque and rotational dynamics based on the motor’s size.  
7. **Stator length (cm):** Defines the length of the stationary part, affecting overall motor dimensions and performance.  
8. **Core material:** Affects magnetic properties and efficiency; iron enhances flux, while air-core simplifies design.  
9. **Supply voltage (V):** Provides the driving force for the motor, determining speed and current draw.  

10. **Ambient temperature (°C):** Influences resistance and thermal performance by altering material properties. 

**Load Characteristics(Optional):**


11. **Load mass (kg):** The weight the motor must drive, directly impacting the required torque.  
12. **Friction coefficient:** Represents system friction, which adds to the torque needed to overcome resistance.  
13. **Desired angular acceleration (rad/s²):** Sets the target acceleration, affecting inertial torque (use 0 for steady-state).
## Installation

1. **Prerequisites:**  
   check you have [Python 3.x](https://www.python.org/downloads/) installed on your system.

2. **Clone the Repository:**  
   Open your terminal and run:  
   ```bash
   https://github.com/shub-r/-DC-hub-motor-Performance-Calculator.git
   ```

3. **Navigate to the Project Directory:**  
   ```bash
   cd dc-hub-motor-performance-calculator
   ```

4. **Run the Tool:**  
   Execute the script with:  
   ```bash
   python motor_calculator.py
   ```

you’re ready to use the DC Hub Motor Performance Calculator!
and performance your estimations  

by shhubham.R
act.for.collage@gmail.com
