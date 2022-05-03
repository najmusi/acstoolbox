# ACS Toolbox - Python Guidance, Navigation and Control
Test

![ACS Toolbox](images/overview/ACSToolbox.jpg)

**ACS Toolbox** is an open-source pure Python library developed by professional Guidance, Navigation and Control engineers for satellite Attitude Control System (ACS) design. The creators have engineered the ACS for notable and successful space missions such as GHGSat-D/C ([GHGSat](https://www.ghgsat.com/)), Kepler GEN1 Cluster ([Kepler Communications](https://www.keplercommunications.com/)) and AISSat-1/2 ([FFI](https://www.ffi.no/en)). Their designs have being utilized in over 30 satellites sent into orbit and showcased numerous times at the [European Space Agency GNC Conference](https://atpi.eventsair.com/QuickEventWebsitePortal/20a05-gnc-2020/website). 


The algorithms in this library are fundamental for ACS design and have been repurposed by the creators for use by the general public.

## Open-Source Features

- [ ] Astrodynamics
- [ ] Time Keeping
- [ ] Orbit Propagator
   - [ ] Earth
   - [ ] Moon
- [ ] Ephemerides
   - [ ] Sun
   - [ ] Moon
   - [ ] Earth's Magnetic Field
- [ ] Sensor Selection
   - [ ] Sun Sensors
   - [ ] Magnetometers
   - [ ] Rate Gyros
- [ ] Actuator Selection
   - [ ] Magnetic Torque Actuators
   - [ ] Reaction Wheels
- [ ] Hardware Placement

## Enterprise Features

ACS Toolbox is sponsored by Astris Aerospace for public use. The enterprise version of the toolbox contains higher fidelity algorithms across all modules and numerous professional tools for commercial satellite missions. These additional features include:

- [ ] Sensor Calibration
- [ ] High Precision Orbit Propagators (Earth/Moon)
   - [ ] Gravitational Potential Effects
   - [ ] Third-Body Effects
   - [ ] Tidal Effects
- [ ] High Precision Earth Rotation
- [ ] Estimation (EKF, Particle, Batch)
- [ ] Control
- [ ] ACS Simulator
   - [ ] Attitude Dynamics
   - [ ] Calibrated Sensor Integration
   - [ ] Flight Code Integration

For more information contact inquiries@astrisaerospace.com.

## Documentation

A comprehensive documentation of the **ACS Toolbox**, including a user guide and an API reference, is currently under progress at Read the Docs.

## Examples

Inside the `Examples` directory, several Jupyter notebooks demonstrate how the **ACS Toolbox** can be used for ACS design. 

## Requirements

To limit unnecessary dependencies, **ACS Toolbox** has requires a very small number of Python package:

- `Matplotlib` - Orbit and Celestial Sphere Plotting
- `NumPy` - Matrix Math
- `SciPy` - Numerical propagation and root finding

This library has been developed independently by the authors in order to maintain integrity for real-world ACS applications.

# Citing

Please cite the **Astris Aerospace ACS Toolbox** if you use the library for your projects. Additionaly, please contact us to let us know what was useful and what could be improved.

