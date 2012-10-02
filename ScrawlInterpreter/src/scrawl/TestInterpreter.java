package scrawl;

import static org.junit.Assert.*;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;

import javax.imageio.ImageIO;

import org.junit.After;
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
		URL location = TestInterpreter.class.getProtectionDomain().getCodeSource().getLocation();
        System.out.println(location.getFile());
		try {
			image = ImageIO.read(new File(
					"/Users/steve/Dev/scrawl/ScrawlInterpreter/test_content/9_sections/2_4_6_8_.png"));
		} catch (IOException e) {
			System.out.println("Failed to load test image. " +
					"Check the relative path.");
			e.printStackTrace();
			assertTrue(false);
		}
		ImageInterpreter interp = new ImageInterpreter(image, 9);
	}

}
