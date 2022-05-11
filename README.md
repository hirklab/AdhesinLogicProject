# AdhesinLogicProject

## Simulation scripts 
All simulation scripts are for Dedalus and must be run in a Dedalus python environment. The following scripts are in scripts/
* 1D_interact.ipynb and 1D_no_interact.ipybn simulate two colonies in 1D that either have complementary adhesin pairs and form a visible interface, or don't have complementary adhesin pairs, and so don't form a visible interface. Shown in Fig. 2c and video S4.
* 2D_interact.ipynb and 2D_interact.ipynb simulate the same problem, but now in 2D. Shown in Fig. 2c and video S4.
* Model_calibration.ipynb runs a parameter sweep to find the parameters that best fit the data, as shown in Fig. S1. These parameters are saved and used elsewhere. It also runs the adhesin strength sweep, shown in Fig. 2d.
* DifferentGrowthRates.ipynb simulates colonies that expand at different rates for Fig. 2g. 
* DifferentSeedingRatios.py is a script that simulates many different initial seeding ratios of colonies with complementary adhesin pairs, and saves an image of the final time point. Shown in Fig. 2f and 2i.
* Escher.ipynb simulates the Escher like transmutation pattern of Fig. 1e.
* UofA.ipynb simulates the U of A pattern of Fig S28
* Voronoi.ipynb simulates the Voronoi seeding pattern of Fig. S28
* Multiple_waves.ipynb simulates two colonies with complementary adhesin pairs, with multiple chemotactic waves. This simulation is shown in Fig. S4.
* Star.ipynb simulates the pattern from Fig. 4f.
* LineGrow.ipynb simulates when a colony is seeded in a line, shown in Fig. S15a
* Circle.ipynb simulates a colony seeded in a circular pattern, shown in Fig. S15c.
* Hexagonal_lattice.ipynb simulates a hexagonal lattice, shown in Fig. 4a.
* Triangular_lattice.ipynb simulates a triangular lattice, shown in Fig. 4a.
* Square_lattice.ipynb simulates the square lattice shown in Fig. 4a.
* Selective_lattice.ipynb simulates a pattern shown in Fig. 4e.
* 1D_3Species.ipynb simulates a mixed seeding of strains, shown in Fig. S3
* 3Pair_square_lattice.ipynb simulates a selective pattern requiring 3 adhesin pairs on a square grid. As shown in Fig. S27.

