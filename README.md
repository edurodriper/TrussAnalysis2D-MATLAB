# TrussAnalysis2D

MATLAB program to solve statically determinate and indeterminate two-dimensional truss structures using the finite element method. Allows user to calculate nodes displacements, support reactions and elements forces and stresses for a given truss design imported into the program via three separate text files. Low size program (~50KB) fully compatible with [Octave](https://www.gnu.org/software/octave/).

![](/readme_images/rm_introexample_light.svg#gh-light-mode-only)![](/readme_images/rm_introexample_dark.svg#gh-dark-mode-only)



## Features

- **Unlimited nodes and elements**
- **Supports**
    - **Pin:** Constrain the two translational degrees-of-freedom in a given node.
    - **Roller:** Node is free to translate in any given direction. The direction normal to the rolling direction is constrained.
- **Prescribed displacements:** Ability to apply zero or non-zero prescribed displacements to each nodal supports. In a pin support these displacements constrain the node final position. In roller supports the prescribed displacement indicates the node displacement normal to the rolling plane.
- **External forces:** Apply external forces to the structure where multiple loads can be applied to the same node. A force can be applied to any node and if applied in a pin or roller node, the reaction forces take that force into consideration.
- **Materials:** Each material is defined with two parameters: Young's modulus and cross-section area.
- **Project folder:** Result file with `.dat` extension and three `.pdf` files containing a visual representation of the truss structure, deformation and member stresses.



#### Why _TrussAnalysis2D_?

The major difference between this program and other open-source or commercial software is the ability to define a roller direction beyond the typical vertical or horizontal rolling supports and at the same time applying non-zero displacements to pin or roller support. Another difference involves the application of forces to the truss structure.  Its possible to apply forces to prescribed degrees of freedom which means that is possible to apply a force to a pin support and as a consequence the support reaction forces will change.



## Instructions

Start the program by running ` TrussAnalysis2D.m` inside `trussanalysis2d` folder.

1. **Select project folder:** Select a folder from the dialog box.  This folder directory, `$projectDir$`, is used to store output files and can be used to save the model input files.
2. **Input filename for output files:** Write the name of the output files in the command window. This name, `$fileName$`, is used as a prefix for the output files name.
3. **Select truss design input files:** Select mesh, displacements and forces text files (in that order) from the dialog box. Default search folder is given by the project directory, `$projectDir$`.



## Input Files

#### Mesh File

This file contains all the relevant information about the truss geometry and material properties. Number of nodes and their coordinates, element connectivity, and material properties are given in this file following the structure below. 

```text
Number of nodes
x coordinate (m), y coordinate (m) [for node #1]
x coordinate (m), y coordinate (m) [for node #2]
...
Number of elements
Node 1, Node 2, Material number [for element #1]
Node 1, Node 2, Material number [for element #2]
...
Number of materials
E (Pa), A (m^2) [for material #1]
E (Pa), A (m^2) [for material #2]
...
```

The nodal coordinates are given in the global x-y coordinate system and their orientation is shown in the figure below.

![](/readme_images/rm_node_coordinate_system_light.svg#gh-light-mode-only)![](/readme_images/rm_node_coordinate_system_dark.svg#gh-dark-mode-only)

#### Displacements File

Now, the number of pin and roller supports are defined. For both types of support, non-zero prescribed displacements can be given and for roller supports any rolling plane can be considered.

```text
Number of pin supports
Node, Axis angle (deg), x' displacement (m), y' displacement (m), [for pin #1]
Node, Axis angle (deg), x' displacement (m), y' displacement (m), [for pin #2]
...
Number of roller supports
Node, Rolling direction (1 or 2), Axis angle (deg), n' displacement (m) [for roller #1]
Node, Rolling direction (1 or 2), Axis angle (deg), n' displacement (m) [for roller #2]
...
```

In a pin support node, the final node position is given by local x'-y' components and the angle between local and global coordinate system is also needs to be given.

![](/readme_images/rm_pin_displacement_light.svg#gh-light-mode-only)![](/readme_images/rm_pin_displacement_dark.svg#gh-dark-mode-only)

For a roller support two rolling directions can be considerer. Number 1 to define rolling along the local x' axis and number 2 to define rolling along the local y' axis (figure below). The local x'-y' system can also be rotated by a given angle around the global x-y coordinate system to make possible the rolling in any two-dimensional direction.

![](/readme_images/rm_roller_direction_light.svg#gh-light-mode-only)![](/readme_images/rm_roller_direction_dark.svg#gh-dark-mode-only)

For a roller support node only the distance between rolling planes is necessary to define that rolling support prescribed displacement. This distance is perpendicular to the rolling plane.

![](/readme_images/rm_roller_displacement_light.svg#gh-light-mode-only)![](/readme_images/rm_roller_displacement_dark.svg#gh-dark-mode-only)

#### Forces File

Force application file follows the same idea as the displacements file. Forces are given in their local x'-y' system and this coordinate system can be rotated around the global coordinate system. 

```text
Number of forces
Node, Axis angle (deg), x' force (N), y' force (N) [for force #1]
Node, Axis angle (deg), x' force (N), y' force (N) [for force #2]
...
```

Multiple forces can be applied to the same node and to any node (pinned or roller node).

![](/readme_images/rm_force_components_light.svg#gh-light-mode-only)![](/readme_images/rm_force_components_dark.svg#gh-dark-mode-only)



## Output Files

- **Truss data:** File `$fileName$_DATA.dat` contains a summary of the input data provided. Lists all node coordinates, element connectivity and individual material properties, pin and roller supports properties and forces components and location. 

- **Results:** Individual node displacements, element forces and stresses and support reactions are given in ` $fileName$_RESULTS.dat` file.

- **Truss plot:** File `$fileName$_TRUSS.pdf` contains a representation of the truss with the correspondent pin and roller nodes and arrows representing all the applied forces.

- **Deformation plot:** File `$fileName$_DEFORMATION.pdf` contains a representation of the undeformed and deformed truss. The deformation  is scaled by a given amount to be visually illustrative. The scale factor is given in the title, in between parenthesis. 

- **Stress plot:** Element stresses are illustrated in file `$fileName$_STRESS.pdf`. Members in compression are represented in red and members in tension are represented in blue. Zero stress members are displayed in a light gray color.  Reaction forces are also represented in their true direction.



## Examples

> Input files and output results files for both examples are in the folder `examples`.

#### Example 1

In example 1, roller support **B** settles down **10 mm** and roller support **C** settles down **5 mm**. For all members **E = 200 GPa** and **A = 0.0015 m^2^** except the area of member **BD**. For that member **A~BD~= 0.0005 m^2^**. 

![](/readme_images/rm_example1_light.svg#gh-light-mode-only)![](/readme_images/rm_example1_dark.svg#gh-dark-mode-only)

#### Example 2

In example 2, all members properties are **E = 200 GPa** and **A = 0.0015 m^2^**.

![](/readme_images/rm_example2_light.svg#gh-light-mode-only)![](/readme_images/rm_example2_dark.svg#gh-dark-mode-only)



## Author

- Eduardo Pereira (original MATLAB/GNU Octave version)
- Nikolaos Papadakis (Python implementation)