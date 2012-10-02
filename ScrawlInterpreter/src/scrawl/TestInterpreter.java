package scrawl;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

import javax.imageio.ImageIO;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

public class TestInterpreter {

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}
	
	@Test
	public void testInstantiation() {
		BufferedImage image = null;		
		ImageInterpreter interp;
		
		try {
			image = ImageIO.read(new File("/Users/steve/Dev/scrawl/ScrawlInterpreter/test_content/9_sections/2_4_6_8_.png"));
		} catch (IOException e) {
			System.out.println("Failed to load test image. " +
					"Check the relative path.");
			e.printStackTrace();
			assertTrue(false);
		}
		
		try {
			interp = new ImageInterpreter(image, 9);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
			assertTrue(false);
		}
	}
	
	@Test
	public void testNineSection() {
		BufferedImage image = null;		
		ImageInterpreter interp = null;
		
		try {
			image = ImageIO.read(new File("/Users/steve/Dev/scrawl/ScrawlInterpreter/test_content/9_sections/2_4_6_8_.png"));
		} catch (IOException e) {
			System.out.println("Failed to load test image. " +
					"Check the relative path.");
			e.printStackTrace();
			assertTrue(false);
		}
		
		try {
			interp = new ImageInterpreter(image, 9);
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
			assertTrue(false);
		}
		
		if (interp == null) { assertTrue(false); }
		
		int[] expected = {0,0,1,0,1,0,1,0,1};
		int[] actual = interp.getInterpretationAsArray();
		
		Assert.assertArrayEquals("Wrong interpretation! ", expected, actual);
	}

}
