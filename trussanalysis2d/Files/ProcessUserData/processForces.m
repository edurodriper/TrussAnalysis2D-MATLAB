function [FORCES] = processForces(FILEDATA, FORCES)

fileData = FILEDATA.forces;


% Process forces file

fileLine = 1;

numberForces = fileData(fileLine, 1);
fileLine = fileLine + 1;
forceNodes = zeros(1, numberForces);
forceAngles = zeros(1, numberForces);
forceComponents = zeros(2, numberForces);
for numFor = 1 : numberForces
	forceNodes(numFor) = fileData(fileLine, 1);
	forceAngles(numFor) = fileData(fileLine, 2);
	forceComponents(1, numFor) = fileData(fileLine, 3);
	forceComponents(2, numFor) = fileData(fileLine, 4);
	fileLine = fileLine + 1;
end


FORCES.number_forces = numberForces;
FORCES.force_nodes = forceNodes;
FORCES.force_components = forceComponents;
FORCES.force_angles = forceAngles;