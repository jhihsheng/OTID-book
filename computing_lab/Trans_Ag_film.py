import meep as mp
mp.verbosity(1) #  output
import numpy as np
from meep.materials import Al, Ag
from meep_plot_style import *
import h5py
import os
import argparse

def sim_eot(l1, l2 ): ## side lengths of a rectangle (in unit of a) 

    ##################
    # Define simulation parameters
    a = 0.5           # Unit length, corresponds to 1 micron
    h = 0.2    # Film thickness, 20 nm in simulation units (a = 600 nm)
    r = 0.1   # Hole radius, 100 nm in simulation units
    dpml = 0.5        # PML thickness
    sz = 1.5          # Cell size in z-direction (non-PML region from z=-2 to z=2)
    cell_size = mp.Vector3(a, a, sz)
    resolution = 100  # Pixels per unit length (600 nm / 100 = 6 nm per pixel)
    fcen = 1 / 0.6      # Center frequency, f = c/lambda, lambda = 600 nm = a, so f = c/a = 1
    df = 1          # Frequency width for the Gaussian pulse
    nfreq = 100     # Number of frequency points for the spectrum

    # Define the geometry: silver film with a circular hole
    geometry = [
        # Silver film as a block, infinite in x and y due to periodic boundaries
        mp.Block(
            size=mp.Vector3(mp.inf, mp.inf, h),
            center=mp.Vector3(0, 0, 0),
            material=Ag  # Predefined silver material in Meep
        ),
        mp.Block(
            size=mp.Vector3(l1 * a, l2 * a, h),
            center=mp.Vector3(0, 0, 0),
            material=mp.Medium(epsilon=1)
        )
    ]
    ##################
    # Define the source: a Gaussian pulse plane wave
    sources = [
        mp.Source(
            mp.GaussianSource(frequency=fcen, fwidth=df),
            component=mp.Ex,  # x-polarized electric field
            center=mp.Vector3(0, 0, -0.2),  # Positioned before the film
            size=mp.Vector3(a, a, 0)  # Spans the xy-plane of the unit cell
            )
        ]

    boundary_layers=[mp.Absorber(thickness=dpml, direction=mp.Z)] ## !! Here, I do not use pml since pml can not deal with wave propagating parallel to the plane
    ##################
    # sim without structure
    sim = mp.Simulation(
        cell_size=cell_size,
        resolution=resolution,
        boundary_layers=boundary_layers,
        sources=sources,
        k_point=mp.Vector3(0, 0, 0),
        geometry=[]
    )


    # Add flux monitor for  incident
    flux_inci = sim.add_flux(
        fcen,
        df,
        nfreq,
        mp.FluxRegion(
            center=mp.Vector3(0, 0, 0.2),
            size=mp.Vector3(a, a, 0)
        )
    )
    # Run the simulation
    sim.run(until_after_sources=mp.stop_when_fields_decayed(5, mp.Ex, mp.Vector3(), 1e-6))
    # Get the incident flux data
    incident_flux = mp.get_fluxes(flux_inci)
    ##################  
    # Step 2: Simulation with the structure to compute transmitted flux
    sim.reset_meep()  # Reset the simulation

    sim = mp.Simulation(
        cell_size=cell_size,
        resolution=resolution,
        boundary_layers=boundary_layers,
        sources=sources,
        k_point=mp.Vector3(0, 0, 0),
        geometry=geometry  # Include the film and hole
    )

    # Add flux monitor at the same position as in the empty simulation
    flux_trans = sim.add_flux(
        fcen,
        df,
        nfreq,
        mp.FluxRegion(
            center=mp.Vector3(0, 0, 0.2),
            size=mp.Vector3(a, a, 0)
        )
    )

    # Run the simulation
    sim.run(until_after_sources=mp.stop_when_fields_decayed(5, mp.Ex, mp.Vector3(), 1e-6))
    # Get the transmitted flux data
    transmitted_flux = mp.get_fluxes(flux_trans)

    ##################
    
    # Compute the transmission spectrum
    transmission = [t / i for t, i in zip(transmitted_flux, incident_flux)]

    # Extract transmission at the center frequency
    flux_freqs = mp.get_flux_freqs(flux_trans)
    index = np.argmin(np.abs(np.array(flux_freqs) - fcen))
    transmission_at_fcen = transmission[index]
    ##

    # Output the result
    print(f"Transmission at f = {fcen} (lambda = 600 nm): {transmission_at_fcen}")
    print(f"l1 = {l1}, l2 = {l2}")

    # Optional: Plot the transmission spectrum
    import matplotlib
    matplotlib.use('Agg')  # Set Agg backend
    import matplotlib.pyplot as plt
    plt.plot(1000/ np.array(flux_freqs), transmission, 'y-', label='Transmission')
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Transmission')
    plt.ylim([0,1])
    plt.title('Transmission Spectrum of Silver Film with Hole')
    plt.legend()
    plt.grid(True)
    
    # Function to generate unique filenameimport os
    def get_unique_filename(base_name, extension, subfolder="img"):
        """
        Generates a unique filename by appending a counter if the filename already exists,
        and saves the file in the specified subfolder.

        Args:
            base_name (str): The base name of the file.
            extension (str): The file extension.
            subfolder (str, optional): The subfolder to save the file in. Defaults to "img".

        Returns:
            str: A unique filename including the subfolder path.
        """
        counter = 0
        while True:
            if counter == 0:
                filename = os.path.join(subfolder, f"{base_name}.{extension}")
            else:
                filename = os.path.join(subfolder, f"{base_name}_{counter}.{extension}")
            if not os.path.exists(filename):
                return filename
            counter += 1

    # Save plot with unique filename in the "img" subfolder
    base_name = "eot_trans"
    extension = "png"
    filename = get_unique_filename(base_name, extension)

    # Create the subfolder if it doesn't exist
    subfolder = os.path.dirname(filename) #get the subfolder name.
    if subfolder and not os.path.exists(subfolder):
        os.makedirs(subfolder)
        
    plt.savefig(filename)
    plt.close()
    return transmission_at_fcen

if __name__ == "__main__":
    print(f"Simulation of EOT: Start!")
    parser = argparse.ArgumentParser(description="Calculate EOT")
    parser.add_argument("l1", type=float, help="side length 1")
    parser.add_argument("l2", type=float, help="side length 1")    
    args = parser.parse_args()
    result = sim_eot(args.l1, args.l2)
    print(f" Trasmitance at 600 nm: {result}")
    print(f"Simulation of EOT: Finished!")