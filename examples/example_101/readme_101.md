This is the simplest possible truss (3 nodes 3 elements, simply supported)


# Mesh details

The nodes are:

| Node | X | Y |   
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 0 |
| 3 | 0 | 2 |

The element connectivity is defined in the following table:

| Element | Node 1 | Node 2 | CrossSection ID|
| --- | --- | --- | --- |
| 1 | 1 | 2 | 1 |
| 2 | 2 | 3 | 1 |
| 3 | 3 | 1 | 1 |

The mateiral Id is defined in the following table:

| Crossection ID | E (Pa) | A $m^2$ |
| --- | --- | --- |
| 1 | 2000 | 1 |

# Displacement boundary conditions

## Pinned Nodes
The table below presents the pinned nodes:

| NodeID |Angle | Dx | Dy | 
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |


## Roller Nodes
For the **roller nodes**. The table below presents the roller nodes:


| NodeID | Rolling direction | Angle | Distance |
| --- | --- | --- | --- |
| 2 | 1 | 0 | 0 |


where:
- Rolling direction: can be either 1(:normal) or 2 (: parallel), and determines if the normal or parallel direction to  the plane is **fixed**. 
- Angle: is the angle between the global x-axis and the roller support plane.
- Distance: is the normal displacement of the roller support plane.


# Forces

The table below presents the forces:

| NodeID | Angle | Fx | Fy |
| --- | --- | --- | --- |
| 3 | 0 | 1000 |  |

where:
- NodeId  : is the node id where the force is applied.
- Angle: is the angle between the global x-axis and the force direction.
- Fx: is the force in the x direction.
- Fy: is the force in the y direction.
