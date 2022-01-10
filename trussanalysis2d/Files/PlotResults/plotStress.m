function [] = plotStress(INFO, PLOT, MESH, FORCES, DISPLACEMENTS, SOLUTION)

projectDir = INFO.project_directory;
fileName = INFO.file_name;
plotXLimits = PLOT.plot_x_limits;
plotYLimits = PLOT.plot_y_limits;
paperSize = PLOT.paper_size;
paperPosition = PLOT.paper_position;
numberNodes = MESH.number_nodes;
plotScale = PLOT.plot_scale;
numberElements = MESH.number_elements;
nodeCoordinates = MESH.node_coordinates;
elementConnectivity = MESH.element_connectivity;
numberForces = FORCES.number_forces;
forceNodes = FORCES.force_nodes;
forceComponents = FORCES.force_components;
forceAngles = FORCES.force_angles;
numberPin = DISPLACEMENTS.number_pin;
pinNodes = DISPLACEMENTS.pin_nodes;
numberRoller = DISPLACEMENTS.number_roller;
rollerNodes = DISPLACEMENTS.roller_nodes;
rollerDirections = DISPLACEMENTS.roller_directions;
rollerAngles = DISPLACEMENTS.roller_angles;
elementStress = SOLUTION.element_stress;
globalReactions = SOLUTION.global_reactions;


newFileName = [fileName, '_STRESS.pdf'];
filePath = [projectDir, '\', newFileName];


% Figure and axes
fi1 = figure(...
	'Name', 'Truss', ...
	'Visible', 'off', ... 
	'Color', [1, 1, 1], ...
	'PaperUnits', 'centimeters', ...
	'PaperSize', paperSize, ...
	'PaperPositionMode', 'auto', ...
	'PaperPosition', paperPosition);
ax1 = axes(...
	'FontSize', 8, ...
	'FontUnits', 'points', ...
	'XLim', plotXLimits, ...
	'YLim', plotYLimits, ...
	'Position', [0.1, 0.065, 0.84, 0.88], ...	
	'Box', 'on', ...
	'DataAspectRatioMode', 'manual', ...
	'DataAspectRatio', [1, 1, 1], ...
	'TitleFontSizeMultiplier', 1.5);
set(get(ax1, 'Title'), 'String', [fileName, ': Stress']);
set(get(ax1, 'XLabel'), 'String', 'x [m]');
set(get(ax1, 'YLabel'), 'String', 'y [m]');
hold(ax1, 'on');

% Roller constrains
for numRol = 1 : numberRoller
	rNode = rollerNodes(numRol);
	rDirection = rollerDirections(numRol);
	rAngle = rollerAngles(numRol);
	C = cos(rAngle * pi / 180);
	S = sin(rAngle * pi / 180);
	if (rDirection == 1)
		rDirVec = [C; S];
	else
		rDirVec = [-S; C];
	end
	[drawSeg] = getRollerLines(nodeCoordinates(:, rNode), rDirVec, plotScale);
	for seg = 1 : 2
		plot(drawSeg(2*seg-1, :), drawSeg(2*seg, :), ...
		'LineStyle', '-', ...
		'LineWidth', 1, ...
		'Marker', 'none', ...
		'Color', [0.0, 0.0, 0.0]);	
	end
end

% Elements
posStress = elementStress(elementStress >= 0);
negStress = elementStress(elementStress <= 0);
maxPosStress = max(posStress);
maxNegStress = min(negStress);
for numEle = 1 : numberElements
	node1 = elementConnectivity(1, numEle);
	node2 = elementConnectivity(2, numEle);
	X1Coord = nodeCoordinates(1, node1);
	Y1Coord = nodeCoordinates(2, node1);
	X2Coord = nodeCoordinates(1, node2);
	Y2Coord = nodeCoordinates(2, node2);
	[elementColor] = getColors(elementStress(numEle), maxPosStress, maxNegStress);
	plot([X1Coord, X2Coord], [Y1Coord, Y2Coord], ...
		'LineStyle', '-', ...
		'LineWidth', 3, ...
		'Color', elementColor);
end

% Forces vectors
for numFor = 1 : numberForces
	fNode = forceNodes(numFor);
	fCompXiYi = forceComponents(:, numFor);
	fAngle = forceAngles(numFor);
	C = cos(fAngle * pi / 180);
	S = sin(fAngle * pi / 180);
	T = [C, S; -S, C];
	fCompXY = T' * fCompXiYi;
	fDirVec = fCompXY / norm(fCompXY);
	[drawSeg] = getForceArrow(nodeCoordinates(:, fNode), fDirVec, 14, plotScale);
	for seg = 1 : 3
	plot(drawSeg(2*seg-1, :), drawSeg(2*seg, :), ...
		'LineStyle', '-', ...
		'LineWidth', 1, ...
		'Marker', 'none', ...
		'Color', [0.0, 0.0, 0.0]);
	end
end

% Reaction vectors
sNode = 1;
for numPin = 1 : numberPin
	pNode = pinNodes(numPin);
	pReaction = globalReactions(:, sNode);
	% x component
	xReact = pReaction(1);
	fDirVec = [xReact; 0] / abs(xReact);
	[drawSeg] = getForceArrow(nodeCoordinates(:, pNode), fDirVec, 8, plotScale);
	for seg = 1 : 3
	plot(drawSeg(2*seg-1, :), drawSeg(2*seg, :), ...
		'LineStyle', '-', ...
		'LineWidth', 1, ...
		'Marker', 'none', ...
		'Color', [0.5, 0.5, 0.5]);
	end
	% y component
	yReact = pReaction(2);
	fDirVec = [0; yReact] / abs(yReact);
	[drawSeg] = getForceArrow(nodeCoordinates(:, pNode), fDirVec, 8, plotScale);
	for seg = 1 : 3
	plot(drawSeg(2*seg-1, :), drawSeg(2*seg, :), ...
		'LineStyle', '-', ...
		'LineWidth', 1, ...
		'Marker', 'none', ...
		'Color', [0.5, 0.5, 0.5]);
	end
	sNode = sNode + 1;
end
for numRol = 1 : numberRoller
	rNode = rollerNodes(numRol);
	rReaction = globalReactions(:, sNode);
	fDirVec = rReaction / norm(rReaction);
	[drawSeg] = getForceArrow(nodeCoordinates(:, rNode), fDirVec, 8, plotScale);
	for seg = 1 : 3
	plot(drawSeg(2*seg-1, :), drawSeg(2*seg, :), ...
		'LineStyle', '-', ...
		'LineWidth', 1, ...
		'Marker', 'none', ...
		'Color', [0.5, 0.5, 0.5]);
	end	
	sNode = sNode + 1;
end

% Nodes
nodeXCoord = nodeCoordinates(1, :);
nodeYCoord = nodeCoordinates(2, :);
plot(nodeXCoord, nodeYCoord, ...
	'LineStyle', 'none', ...
	'LineWidth', 1, ...
	'Marker', 'o', ...
	'MarkerSize', 4, ...
	'MarkerEdgeColor', [0.0, 0.0, 0.0], ...
	'MarkerFaceColor', [1.0, 1.0, 1.0]);

% Pin nodes
pinXCoord = nodeCoordinates(1, pinNodes);
pinYCoord = nodeCoordinates(2, pinNodes);
plot(pinXCoord, pinYCoord, ...
	'LineStyle', 'none', ...
	'LineWidth', 1.5, ...
	'Marker', 'o', ...
	'MarkerSize', 5, ...
	'MarkerEdgeColor', [0.0, 0.0, 0.0], ...
	'MarkerFaceColor', [0.0, 0.0, 0.0]);

% Roller nodes
rollerXCoord = nodeCoordinates(1, rollerNodes);
rollerYCoord = nodeCoordinates(2, rollerNodes);
plot(rollerXCoord, rollerYCoord, ...
	'LineStyle', 'none', ...
	'LineWidth', 1.5, ...
	'Marker', 'o', ...
	'MarkerSize', 5, ...
	'MarkerEdgeColor', [0.0, 0.0, 0.0], ...
	'MarkerFaceColor', [1.0, 1.0, 1.0]);

% Element numbers
for numEle = 1 : numberElements
	node1 = elementConnectivity(1, numEle); 
	node2 = elementConnectivity(2, numEle); 
	midPoint = (nodeCoordinates(:, node1) + nodeCoordinates(:, node2)) / 2;
	text(midPoint(1), midPoint(2), num2str(numEle, '%d'), ...
		'FontSize', 6, ...
		'HorizontalAlignment', 'center', ...
		'VerticalAlignment', 'middle', ...
		'BackgroundColor', [1.0, 1.0, 1.0], ...
		'Margin', 0.1);
end

% Create pdf file
print(fi1, filePath, '-dpdf');
