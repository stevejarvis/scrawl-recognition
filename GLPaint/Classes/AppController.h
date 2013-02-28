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
@class Reachability;

@interface AppController : NSObject <UIApplicationDelegate>
{
	PaintingWindow		*window;
	PaintingView		*drawingView;

	SoundEffect			*erasingSound;
	SoundEffect			*selectSound;
	CFTimeInterval		lastTime;
    
    Reachability* reachability;
}

@property (nonatomic, retain) IBOutlet PaintingWindow *window;
@property (nonatomic, retain) IBOutlet PaintingView *drawingView;
@property (retain, nonatomic) IBOutlet UIView *networkStatusIndicator;
- (IBAction)toggleGrid:(id)sender;
-(void) networkStatusChanged:(NSNotification *)noti;
-(void) updateNetworkStatus;


@end
