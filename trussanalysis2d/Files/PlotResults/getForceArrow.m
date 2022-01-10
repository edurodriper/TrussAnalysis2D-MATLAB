function [drawSeg] = getForceArrow(appPoint, dirVector, vectorLength, plotScale)

arrowLPaper = 3; % mm
arrowWPaper = 2; % mm
vectorLPaper = vectorLength; % mm

arrowL = arrowLPaper / 10 / plotScale;
arrowW = arrowWPaper / 10 / plotScale;
vectorL = vectorLPaper / 10 / plotScale;

dDir = dirVector;
nDir = [0, -1; 1, 0] * dDir;

pointO = appPoint;
pointC = pointO + dDir * vectorL;
pointA = pointC - (dDir * arrowL) + (nDir * arrowW / 2);
pointB = pointC - (dDir * arrowL) - (nDir * arrowW / 2);

drawSeg = [...
	pointO, pointC; ...
	pointA, pointC; ...
	pointB, pointC];
