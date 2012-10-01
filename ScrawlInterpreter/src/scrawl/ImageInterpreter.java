package scrawl;

import java.awt.image.BufferedImage;

public class ImageInterpreter {
	
	int numSections;
	BufferedImage image;
	
	public ImageInterpreter(BufferedImage image, int sections) {
		this.image = image;
		this.numSections = sections;
	}
}
