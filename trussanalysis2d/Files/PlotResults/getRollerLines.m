function [drawSeg] = getRollerLines(appPoint, dirVector, plotScale)

rollerLPaper = 16; % mm
rollerHPaper = 2.5; % mm

rollerL = rollerLPaper / 10 / plotScale;
rollerH = rollerHPaper / 10 / plotScale;

dDir = dirVector;
nDir = [0, -1; 1, 0] * dDir;

pointO = appPoint;
pointA1 = pointO + (nDir * rollerH / 2) - (dDir * rollerL / 2);
pointB1 = pointO + (nDir * rollerH / 2) + (dDir * rollerL / 2);
pointA2 = pointO - (nDir * rollerH / 2) - (dDir * rollerL / 2);
pointB2 = pointO - (nDir * rollerH / 2) + (dDir * rollerL / 2);

drawSeg = [...
	pointA1, pointB1; ...
	pointA2, pointB2];