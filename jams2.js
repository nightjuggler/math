/* globals self */
(function() {
"use strict";
function convolve3x3(s, d, width, height)
{
	var yDelta = width * 4;
	var i0, i1, i2, i3, i5, i6, i7, i8;

	var k0 = 0, k1 = 1, k2 = 0;
	var k3 = 1, k4 = 2, k5 = 1;
	var k6 = 0, k7 = 1, k8 = 0;

	var sumOfWeights = k0 + k1 + k2 + k3 + k4 + k5 + k6 + k7 + k8;

	var i = 0;
	for (var y = 0; y < height; ++y)
	{
		var yUp = y === 0 ? 0 : -yDelta;
		var yDn = y === height - 1 ? 0 : yDelta;

		for (var x = 0; x < width; ++x)
		{
			var xLft = x === 0 ? 0 : -4;
			var xRgt = x === width - 1 ? 0 : 4;
/*
	"The values in the kernel matrix are applied such that the kernel matrix is rotated 180 degrees
	relative to the source and destination images in order to match convolution theory as described
	in many computer graphics textbooks."
	(https://www.w3.org/TR/filter-effects-1/#feConvolveMatrixElement)
*/
			// 8 7 6
			// 5 4 3
			// 2 1 0

			i7 = i + yUp;
			i8 = i7 + xLft;
			i6 = i7 + xRgt;
			i5 = i + xLft;
			i3 = i + xRgt;
			i1 = i + yDn;
			i2 = i1 + xLft;
			i0 = i1 + xRgt;

			var r = k8*s[i8] + k7*s[i7] + k6*s[i6] +
				k5*s[i5] + k4*s[i ] + k3*s[i3] +
				k2*s[i2] + k1*s[i1] + k0*s[i0];
			var g = k8*s[i8+1] + k7*s[i7+1] + k6*s[i6+1] +
				k5*s[i5+1] + k4*s[i +1] + k3*s[i3+1] +
				k2*s[i2+1] + k1*s[i1+1] + k0*s[i0+1];
			var b = k8*s[i8+2] + k7*s[i7+2] + k6*s[i6+2] +
				k5*s[i5+2] + k4*s[i +2] + k3*s[i3+2] +
				k2*s[i2+2] + k1*s[i1+2] + k0*s[i0+2];

			d[i  ] = r / sumOfWeights;
			d[i+1] = g / sumOfWeights;
			d[i+2] = b / sumOfWeights;
			d[i+3] = s[i+3];
			i += 4;
		}
	}
}
function setRGB(d, i, iterationCount)
{
	if (iterationCount === null) {
		d[i  ] = 0;
		d[i+1] = 0;
		d[i+2] = 0;
		d[i+3] = 255;
		return;
	}
	var h = (280 + iterationCount) % 360 / 60;
	if (h < 1) {
		// rgb(255,0,0) -> rgb(255,255,0) [Red -> Yellow]
		d[i  ] = 255;
		d[i+1] = 255 * h;
		d[i+2] = 0;
	} else if (h < 2) {
		// rgb(255,255,0) -> rgb(0,255,0) [Yellow -> Lime]
		d[i  ] = 255 * (2 - h);
		d[i+1] = 255;
		d[i+2] = 0;
	} else if (h < 3) {
		// rgb(0,255,0) -> rgb(0,255,255) [Lime -> Cyan]
		d[i  ] = 0;
		d[i+1] = 255;
		d[i+2] = 255 * (h - 2);
	} else if (h < 4) {
		// rgb(0,255,255) -> rgb(0,0,255) [Cyan -> Blue]
		d[i  ] = 0;
		d[i+1] = 255 * (4 - h);
		d[i+2] = 255;
	} else if (h < 5) {
		// rgb(0,0,255) -> rgb(255,0,255) [Blue -> Magenta]
		d[i  ] = 255 * (h - 4);
		d[i+1] = 0;
		d[i+2] = 255;
	} else {
		// rgb(255,0,255) -> rgb(255,0,0) [Magenta -> Red]
		d[i  ] = 255;
		d[i+1] = 0;
		d[i+2] = 255 * (6 - h);
	}
	d[i+3] = 255;
}
function inSet(zx, zy, cx, cy, n)
{
	zx += cx;
	zy += cy;

	var i = 0;
	var zx2 = zx*zx;
	var zy2 = zy*zy;

	while (zx2 + zy2 <= 4)
	{
		if (++i === n)
			return null;

		zy = cy + 2*zx*zy;
		zx = cx + zx2 - zy2;

		zx2 = zx*zx;
		zy2 = zy*zy;
	}
	return i;
}
function computeJulia(d, w, h, config)
{
	const {maxIteration: n, minX, maxY, step, cx, cy} = config;

	for (var y = h, zy = maxY, i = 0; y !== 0; y -= 1, zy -= step)
		for (var x = w, zx = minX; x !== 0; x -= 1, zx += step, i += 4)
			setRGB(d, i, inSet(zx, zy, cx, cy, n));
}
function computeMandelbrot(d, w, h, config)
{
	const {maxIteration: n, minX, maxY, step} = config;

	for (var y = h, zy = maxY, i = 0; y !== 0; y -= 1, zy -= step)
		for (var x = w, zx = minX; x !== 0; x -= 1, zx += step, i += 4)
			setRGB(d, i, inSet(0, 0, zx, zy, n));
}
let data1 = null;
self.addEventListener("message", function({data: config}) {
	const {isJulia, width, height} = config;
	if (data1 === null)
		data1 = new Uint8ClampedArray(width * height * 4);

	(isJulia ? computeJulia : computeMandelbrot)(data1, width, height, config);

	const data2 = new Uint8ClampedArray(width * height * 4);
	convolve3x3(data1, data2, width, height);
	self.postMessage(data2, [data2.buffer]);
});
})();
