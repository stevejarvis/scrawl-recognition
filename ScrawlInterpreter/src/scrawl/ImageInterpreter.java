package scrawl;

import java.awt.image.BufferedImage;

public class ImageInterpreter {
	/*
	 * Class will interpret an image as a grid and return an array of 1s
	 * and 0s representing whether each section of the grid contains ink.
	 * 
	 * Instantiate with an image and number of sections to evaluate. Number
	 * of sections must be a perfect square, and safest if the root of that
	 * square is a divisor of the length/width of the image. Because of the
	 * controlled environment in which this class is meant to operate, edge 
	 * cases, such as that, are not necessarily handled gracefully.
	 */
	
	boolean debug = false;
	int numSections;
	BufferedImage image;
	
	public ImageInterpreter(BufferedImage image, int sections) 
			throws IllegalArgumentException, NullPointerException {
		if (Math.sqrt(sections) % 1 != 0) {
			throw new IllegalArgumentException(
					"Number of sections must be a perfect square.");
		}
		if (image == null) { 
			throw new NullPointerException("Image must not be null.");
		}
		this.image = image;
		this.numSections = sections;
	}
	
	public int[] getInterpretationAsArray() {
		/*
		 * May be a long-running method.
		 * 
		 * Divide the image into the appropriate number of sections. Analyze
		 * the image and return an array indicative of the image contents.
		 */
		int[] res = new int[this.numSections];
		int sides = (int) Math.sqrt(this.numSections);
		int sectionSize = this.image.getHeight() / sides;
		if (this.debug) { 
			System.out.println("Image is " + this.image.getHeight() + " X " + 
					this.image.getWidth() + "."); 
		}
		if (this.debug) { 
			System.out.println(sectionSize + " pixels per section."); 
		}
		for (int y=0; y<sides; y++) {
			for (int x=0; x<sides; x++) {
				res[sides*y + x] = sectionContainsInk(x * sectionSize, 
						y * sectionSize, sectionSize);
			}
		}
		return res;
	}
	
	private int sectionContainsInk(int startX, int startY, int range) {
		/*
		 * Passed coordinates and range to scan, returns a 1 if ink is found, 
		 * 0 if not.
		 */
		int endX = startX + range;
		int endY = startY + range;
		// The treshold of color to count as ink, on 256 scale.
		int threshold = 200;
		if (this.debug) { 
			System.out.println("Examining pixels ("+startX+","+startY+") -> (" +
					endX+","+endY+")"); 
		}
		int[] pixels = new int[range * range];
		this.image.getRGB(startX, startY, range, range, pixels, 0, range);
		for (int pixel : pixels) {
			int red = pixel >> 16 & 0xFF;
			int green = pixel >> 8 & 0xFF;
			int blue = pixel & 0xFF;
			if (red < threshold || green < threshold || blue < threshold) {
				return 1;
			}
		}
		return 0;
	}
}
