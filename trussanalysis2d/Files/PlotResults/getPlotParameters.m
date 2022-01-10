function [PLOT] = getPlotParameters(MESH, SOLUTION, PLOT)

nodeCoordinates = MESH.node_coordinates;
nodeDisplacements = SOLUTION.global_displacements;


% Node coordinates
ncX = nodeCoordinates(1, :);
ncY = nodeCoordinates(2, :);

% Truss limits
tXMin = min(ncX);
tXMax = max(ncX); 
tYMin = min(ncY); 
tYMax = max(ncY);

% Truss size
tXSize = tXMax - tXMin;
tYSize = tYMax - tYMin;

% Margins
margins = 0.09 * max([tXSize, tYSize]);

% Plot limits
pXMin = tXMin - margins;
pXMax = tXMax + margins;
pYMin = tYMin - margins;
pYMax = tYMax + margins;
plotXLimits = [pXMin, pXMax];
plotYLimits = [pYMin, pYMax];

% Axis size
aXSize = pXMax - pXMin;
aYSize = pYMax - pYMin;

% Figure size
fXSize = aXSize / 0.84;
fYSize = aYSize / 0.88;

% Paper orientation
if (fXSize > fYSize)
	paperSize = [29.7, 21.0];
	paperPosition = [0, 0, 29.7, 21.0];
	if (fXSize/fYSize > 297/210)
		fXSizePaper = 29.7;
		plotScale = fXSizePaper / fXSize;
	else
		fYSizePaper = 21.0;
		plotScale = fYSizePaper / fYSize;
	end
else
	paperSize = [21.0, 29.7];
	paperPosition = [0, 0, 21.0, 29.7];
	if (fXSize/fYSize > 210/297)
		fXSizePaper = 21.0;
		plotScale = fXSizePaper / fXSize;
	else
		fYSizePaper = 29.0;
		plotScale = fYSizePaper / fYSize;
	end
end

% Deformed scale factor
maxDispl = max(abs(nodeDisplacements));
scaleFactor = margins * 0.5 / maxDispl;


PLOT.plot_x_limits = plotXLimits;
PLOT.plot_y_limits = plotYLimits;
PLOT.paper_size = paperSize;
PLOT.paper_position = paperPosition;
PLOT.plot_scale = plotScale;
PLOT.scale_factor = scaleFactor;
