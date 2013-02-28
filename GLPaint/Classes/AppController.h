/*
     File: AppController.h
 Abstract: The UIApplication delegate class, which is the central controller of
 the application.
  Version: 1.11

*/

//CLASS INTERFACES:

@class PaintingWindow;
@class PaintingView;
@class SoundEffect;

@interface AppController : NSObject <UIApplicationDelegate>
{
	PaintingWindow		*window;
	PaintingView		*drawingView;

	SoundEffect			*erasingSound;
	SoundEffect			*selectSound;
	CFTimeInterval		lastTime;
}

@property (nonatomic, retain) IBOutlet PaintingWindow *window;
@property (nonatomic, retain) IBOutlet PaintingView *drawingView;
- (IBAction)toggleGrid:(id)sender;

@end
