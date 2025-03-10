import math

COPPER_RESISTIVITY = 1.68e-8
COPPER_TEMP_COEF = 0.00393

def get_float_input(prompt, error_meassage="not right. Please type in a number."):
    while True:
        try:
            return float (input(prompt))
        except  ValueError:
            print("error_message")

def get_int_input(prompt, error_message="doesn't look whole number to me :( Please enter an integer."):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(error_message)

def get_positive_float_input(prompt, error_message="Needs to be a positive number, please."):
    while True:
        value = get_float_input(prompt)
        if value > 0:
            return value
        else:
            print(error_message)

def get_positive_int_input(prompt, error_message="Has to be a positive whole number this time."):
    while True:
        value = get_int_input(prompt)
        if value > 0:
            return value
        else:
            print(error_message)

#funtion for estimateing winding resistance, by taking wire gauge, motor size, coil info, and temperature into and returning cal motor resistance

def calculate_resistance(wire_gauge_awg, num_slots, turns_per_coil, stator_length, rotor_radius, ambient_temperature_c):
    awg_resistance_per_meter = {
        20: 0.03331,
        24: 0.08422
    }

    if wire_gauge_awg not in awg_resistance_per_meter:
        wire_gauge_awg = 20

    resistance_20c_per_meter = awg_resistance_per_meter.get(wire_gauge_awg, awg_resistance_per_meter[20])
    resistance_per_meter = resistance_20c_per_meter * (1 + COPPER_TEMP_COEF * (ambient_temperature_c - 20))
    wire_length_per_coil = 2 * (stator_length + 2 * rotor_radius)
    total_wire_length = num_slots * turns_per_coil * wire_length_per_coil
    motor_resistance = total_wire_length * resistance_per_meter
    return motor_resistance


 #funtion for rough guessing ke means motor speed to voltage, Higher Ke means more speed per volt 
#retuen approximate Ke value, SUPER simplified way to estimate ke, Real motors are more complex!
def estimate_motor_constant(magnet_strength, num_magnets, rotor_radius, stator_length, num_turns_per_coil, num_slots):
    k_factor = magnet_strength * num_magnets * rotor_radius * stator_length * num_turns_per_coil / num_slots
    k_e_approx = k_factor * 0.001
    return k_e_approx

#calculates total load torque , friction torque , and inertia torque based on mass, friction, radius, and desired acceleration.
def calculate_load_torque(mass_kg, friction_coefficient, rotor_radius_m, desired_acceleration_rad_s2=0):
    friction_torque = friction_coefficient * mass_kg * 9.81 * rotor_radius_m
    moment_of_inertia = 0.5 * mass_kg * (rotor_radius_m**2)
    inertia_torque = moment_of_inertia * desired_acceleration_rad_s2 if desired_acceleration_rad_s2 != 0 else 0
    total_load_torque = friction_torque + inertia_torque
    return total_load_torque, friction_torque, inertia_torque

#sorry tired of explaintion :(

def calculate_performance(num_stator_slots, wire_gauge_awg, turns_per_coil, magnet_strength, num_magnets, rotor_radius_cm, stator_length_cm, core_material, supply_voltage_v, ambient_temperature_c, load_mass_kg, friction_coefficient, desired_acceleration_rad_s2):
    rotor_radius_m = rotor_radius_cm / 100.0
    stator_length_m = stator_length_cm / 100.0

    motor_resistance = calculate_resistance(wire_gauge_awg, num_stator_slots, turns_per_coil, stator_length_m, rotor_radius_m, ambient_temperature_c)
    k_e = estimate_motor_constant(magnet_strength, num_magnets, rotor_radius_m, stator_length_m, turns_per_coil, num_stator_slots)
    k_t = k_e

    load_torque_nm, friction_torque_nm, inertia_torque_nm = calculate_load_torque(load_mass_kg, friction_coefficient, rotor_radius_m, desired_acceleration_rad_s2)

    rated_voltage = supply_voltage_v
    steady_state_load_torque = friction_torque_nm

    if k_e <= 0 or motor_resistance <= 0:
        operating_speed_rad_s = 0
        load_current_a = 0
    else:
        load_current_a = steady_state_load_torque / k_t
        back_emf_v = k_e * 0
        voltage_drop_resistance = load_current_a * motor_resistance
        operating_speed_rad_s = max(0, (supply_voltage_v - voltage_drop_resistance) / k_e)

    operating_speed_rpm = (operating_speed_rad_s * 60) / (2 * math.pi)
    input_power_w = supply_voltage_v * load_current_a
    output_power_w = steady_state_load_torque * operating_speed_rad_s
    efficiency_percent = (output_power_w / input_power_w) * 100 if input_power_w > 0 else 0
    heat_loss_rate_w = (load_current_a**2) * motor_resistance
    total_heat_generated_j = heat_loss_rate_w * 300

    approx_motor_mass_kg = 0.1
    specific_heat_capacity_j_kg_c = 400
    temperature_rise_c = total_heat_generated_j / (approx_motor_mass_kg * specific_heat_capacity_j_kg_c) if approx_motor_mass_kg > 0 and specific_heat_capacity_j_kg_c > 0 else 0

    return {
        "estimated_rated_voltage_v": rated_voltage,
        "operating_speed_rpm": operating_speed_rpm,
        "load_current_a": load_current_a,
        "input_power_w": input_power_w,
        "output_power_w": output_power_w,
        "torque_nm": steady_state_load_torque,
        "efficiency_percent": efficiency_percent,
        "heat_loss_rate_w": heat_loss_rate_w,
        "total_heat_generated_kj": total_heat_generated_j / 1000.0,
        "estimated_temperature_rise_c": temperature_rise_c,
        "motor_resistance_ohm": motor_resistance,
        "motor_constant_ke": k_e,
        "friction_torque_nm": friction_torque_nm,
        "inertia_torque_nm": inertia_torque_nm,
        "voltage_drop_resistance_v": voltage_drop_resistance,
        "back_emf_v_at_op_speed": k_e * operating_speed_rad_s
    }

def display_results(results):
    print("\n--- Motor Performance Results ---")
    print(f"Estimated Rated Voltage: {results['estimated_rated_voltage_v']:.2f} V")
    print(f"Operating Speed Under Load: {results['operating_speed_rpm']:.2f} RPM")
    print(f"Load Current: {results['load_current_a']:.2f} A")
    print(f"Input Power: {results['input_power_w']:.2f} W")
    print(f"Output Power: {results['output_power_w']:.2f} W")
    print(f"Torque: {results['torque_nm']:.2f} Nm")
    print(f"Efficiency: {results['efficiency_percent']:.2f} %")
    print(f"Heat Loss Rate: {results['heat_loss_rate_w']:.2f} W")
    print(f"Total Heat Generated in 5 minutes: {results['total_heat_generated_kj']:.2f} kJ")
    print(f"Estimated Temperature Rise: {results['estimated_temperature_rise_c']:.2f} °C")

    print("\n--- Extra Numbers ---")
    print(f"Motor Resistance: {results['motor_resistance_ohm']:.4f} Ohms")
    print(f"Motor Constant (Ke): {results['motor_constant_ke']:.4f} V/rad/s")
    print(f"Friction Torque: {results['friction_torque_nm']:.2f} Nm")
    print(f"Inertia Torque: {results['inertia_torque_nm']:.2f} Nm")
    print(f"Voltage Drop across Resistance: {results['voltage_drop_resistance_v']:.2f} V")
    print(f"Back EMF at Operating Speed: {results['back_emf_v_at_op_speed']:.2f} V")
    print("--- End of Results ---")


def explanation_menu():
    while True:
        print("\nMotor Input Parameters")
        print("1. Magnet Strength")
        print("2. Rotor Radius")
        print("3. Core Material ")
        print("4. Ambient Temperature (room temp)")
        print("5. Friction Coefficient (force of friction)")
        print("6. Desired Angular Acceleration")
        print("7. Wire Gauge (AWG)")
        print("8. Number of Stator Slots")
        print("9. Turns per Coil")
        print("10. Stator Length")
        print("11. Number of Magnets")
        print("12. Supply Voltage")
        print("13. Load Mass")
        print("14. Back to Main Menu")

        choice = input("Pick a number from 1 to 14: ")

        if choice == '1':
            print("\nMagnet Strength: How 'powerful' your magnets are.")
        elif choice == '2':
            print("\nRotor Radius: Width of spinning part, in cm.")
        elif choice == '3':
            print("\nCore Material: Material of motor core (Iron, Air).")
        elif choice == '4':
            print("\nAmbient Temperature: Air temperature around motor, in Celsius.")
        elif choice == '5':
            print("\nFriction Coefficient: 'Drag' or resistance in the system.")
        elif choice == '6':
            print("\nDesired Angular Acceleration: How quickly to speed up, rad/s^2 (0 for steady).")
        elif choice == '7':
            print("\nWire Gauge (AWG): Wire thickness. Smaller AWG = thicker wire.")
        elif choice == '8':
            print("\nNumber of Stator Slots: Slots in non-spinning part.")
        elif choice == '9':
            print("\nTurns per Coil: Wire loops per coil.")
        elif choice == '10':
            print("\nStator Length: Length of non-spinning part, in cm.")
        elif choice == '11':
            print("\nNumber of Magnets: Magnets on rotor.")
        elif choice == '12':
            print("\nSupply Voltage: Battery/power supply voltage, in Volts.")
        elif choice == '13':
            print("\nLoad Mass: Weight motor is moving, in kg.")
        elif choice == '14':
            return
        else:
            print("Oops, pick 1-14.")


def main():
    print("Welcome to the DC Hub Motor Performance Calculator!")
    print("\n**Important Note:** This calculator gives you *estimates* based on simplified math. Think of it as a starting point for your design ideas, not a perfectly accurate prediction of real-world performance. For really precise results, you'd need more advanced tools and probably some actual testing.")

    print("""
--- Required Information for Calculation ---
1. Primary Motor Design Inputs:
    - Number of stator slots
    - Wire gauge (AWG)
    - Number of turns per coil
2. Additional Required Inputs:
    - Magnet specifications (e.g., magnet strength and number of magnets)
    - Motor dimensions (e.g., rotor radius, stator length)
    - Core material properties (if applicable)
    - Supply voltage or battery specifications
    - Ambient temperature
3. Load Characteristics (Optional - enter values or type 'skip' individually):
    - Load mass
    - Friction coefficient
    - Desired acceleration
     (You can skip Load Characteristics for minimal load estimation)
""")

    while True:
        print("\n--- Main Menu ---")
        print("1. Input Parameter Info")
        print("2. Calculations!")
        print("3. Exit")

        main_choice = input("Choose an option (1, 2, or 3): ")

        if main_choice == '1':
            explanation_menu()
        elif main_choice == '2':
            print("\n--- Motor Details ---")
            print("\n--- Motor Winding Details ---")
            num_stator_slots = get_positive_int_input("Stator slots? ")
            wire_gauge_awg = get_positive_int_input("Wire gauge (AWG)? ")
            turns_per_coil = get_positive_int_input("Turns per coil? ")

            print("\n--- Motor Magnet and Size Specs ---")
            magnet_strength = get_positive_float_input("Magnet strength? ")
            num_magnets = get_positive_int_input("Number of magnets? ")
            rotor_radius_cm = get_positive_float_input("Rotor radius (cm)? ")
            stator_length_cm = get_positive_float_input("Stator length (cm)? ")
            core_material = input("Core material (or leave blank if air-core): ")

            print("\n--- Operating Conditions ---")
            supply_voltage_v = get_positive_float_input("Supply voltage (V)? ")
            ambient_temperature_c = get_float_input("Ambient temperature (°C)? ")

            print("\n--- Load Characteristics (Optional - type 'skip') ---")
            load_mass_str = input("Load mass (kg, or type 'skip')? ").lower()
            if load_mass_str == 'skip':
                load_mass_kg = 0.001
            else:
                load_mass_kg = get_positive_float_input(f"Load mass (kg)? ", error_message="Load mass needs to be positive.")

            friction_coefficient_str = input("Friction coefficient (or type 'skip')? ").lower()
            if friction_coefficient_str == 'skip':
                friction_coefficient = 0.001
            else:
                friction_coefficient = get_positive_float_input(f"Friction coefficient? ", error_message="Friction coefficient must be positive.")

            desired_acceleration_str = input("Desired angular acceleration (rad/s^2, 0 for steady state, or type 'skip')? ").lower()
            if desired_acceleration_str == 'skip':
                desired_acceleration_rad_s2 = 0
            else:
                desired_acceleration_rad_s2 = get_float_input(f"Desired angular acceleration (rad/s^2)? ", error_message="Desired acceleration must be a number.")

            results = calculate_performance(num_stator_slots, wire_gauge_awg, turns_per_coil, magnet_strength, num_magnets,
                                             rotor_radius_cm, stator_length_cm, core_material, supply_voltage_v,
                                             ambient_temperature_c, load_mass_kg, friction_coefficient, desired_acceleration_rad_s2)
            display_results(results)
        elif main_choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid option. Please type 1, 2, or 3.")

if __name__ == "__main__":
    main()


