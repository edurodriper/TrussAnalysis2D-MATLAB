function [elementColor] = getColors(currentValue, positiveValue, negativeValue)

colorCompression = [0.7843, 0, 0.1569];
colorZero = [0.9020, 0.9020, 0.9020];
colorTension = [0.1569, 0, 0.7843];

if (currentValue < 0)
	ratio = currentValue / negativeValue;
	c1 = colorCompression;
	c2 = colorZero;
else
	ratio = currentValue / positiveValue;
	c1 = colorTension;
	c2 = colorZero;
end

elementColor = zeros(1, 3);
elementColor(2) = c2(2) + ratio * (c1(2) - c2(2));
elementColor(1) = c2(1) + ratio * (c1(1) - c2(1));
elementColor(3) = c2(3) + ratio * (c1(3) - c2(3));
