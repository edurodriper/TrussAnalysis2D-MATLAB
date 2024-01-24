clear;
clc;

addpath(genpath('Files'));


% Process user data

initializeVariables(); % done

[INFO] = getProjectInfo(INFO);% done

[FILEDATA] = readPropertiesFiles(FILEDATA, INFO);% done

[MESH] = processMesh(FILEDATA, MESH);
[DISPLACEMENTS] = processDisplacements(FILEDATA, DISPLACEMENTS);
[FORCES] = processForces(FILEDATA, FORCES);

writeInputData(INFO, MESH, DISPLACEMENTS, FORCES);


% Analysis

[DOFS] = processDOFS(MESH, DISPLACEMENTS, DOFS);

[ANALYSIS] = getGlobalStiffnessMatrix(MESH, ANALYSIS);
[ANALYSIS] = getGlobalForceVector(FORCES, DOFS, ANALYSIS);
[ANALYSIS] = getNewDisplacementVector(DISPLACEMENTS, DOFS, ANALYSIS);
[ANALYSIS] = getNewTransformationMatrix(DISPLACEMENTS, DOFS, ANALYSIS);

[SOLUTION] = solveDisplacement(ANALYSIS, DOFS, SOLUTION);
[SOLUTION] = solveReaction(SOLUTION, DISPLACEMENTS);
[SOLUTION] = solveStress(MESH, SOLUTION);

writeResults(INFO, MESH, DISPLACEMENTS, SOLUTION);


% Plot results

[PLOT] = getPlotParameters(MESH, SOLUTION, PLOT);

plotTruss(INFO, PLOT, MESH, FORCES, DISPLACEMENTS);
plotStress(INFO, PLOT, MESH, FORCES, DISPLACEMENTS, SOLUTION);
plotDeformation(INFO, PLOT, MESH, DISPLACEMENTS, SOLUTION);
