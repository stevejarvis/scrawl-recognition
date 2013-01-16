/*
     File: AppController.m
 Abstract: The UIApplication delegate class, which is the central controller of
 the application.
  Version: 1.11
 
 */

#import "AppController.h"
#import "PaintingView.h"
#import "SoundEffect.h"

//CONSTANTS:

#define kMinEraseInterval		0.5


@implementation AppController

@synthesize window;
@synthesize drawingView;

- (void) applicationDidFinishLaunching:(UIApplication*)application
{
	CGRect					rect = [[UIScreen mainScreen] applicationFrame];
	
    // Defer to the OpenGL view to set the brush color
	[drawingView setBrushColorWithRed:200 green:200 blue:200];
	
	// Look in the Info.plist file and you'll see the status bar is hidden
	// Set the style to black so it matches the background of the application
	[application setStatusBarStyle:UIStatusBarStyleBlackTranslucent animated:NO];
	// Now show the status bar, but animate to the style.
	[application setStatusBarHidden:NO withAnimation:YES];
	
	// Load the sounds
	NSBundle *mainBundle = [NSBundle mainBundle];	
	erasingSound = [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"Erase" ofType:@"caf"]];
	selectSound =  [[SoundEffect alloc] initWithContentsOfFile:[mainBundle pathForResource:@"Select" ofType:@"caf"]];

	// Erase the view when recieving a notification named "shake" from the NSNotificationCenter object
	// The "shake" nofification is posted by the PaintingWindow object when user shakes the device
	[[NSNotificationCenter defaultCenter] addObserver:self selector:@selector(eraseView) name:@"shake" object:nil];
}

// Release resources when they are no longer needed,
- (void) dealloc
{
	[selectSound release];
	[erasingSound release];
	[drawingView release];
	[window release];
	
	[super dealloc];
}

// Called when receiving the "shake" notification; plays the erase sound and redraws the view
-(void) eraseView
{
	if(CFAbsoluteTimeGetCurrent() > lastTime + kMinEraseInterval) {
		[erasingSound play];
		[drawingView erase];
		lastTime = CFAbsoluteTimeGetCurrent();
	}
}

@end
