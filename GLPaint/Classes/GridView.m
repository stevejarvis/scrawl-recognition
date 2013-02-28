//
//  GridView.m
//  GLPaint
//
//  Created by Steve Jarvis on 2/12/13.
//
//

#import "GridView.h"

@implementation GridView

@synthesize sections;
@synthesize gridIsVisible;

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    [self setBackgroundColor:[UIColor colorWithWhite:50 alpha:0.1]];
    [self setGridIsVisible: true];
    return self;
}

- (void)drawRect:(CGRect)rect
{
    /*
     This is where the view is actually drawn. So overriding it allows me to add
     a grid to it.
     */
    if (self.gridIsVisible)
    {
        CGContextRef context = UIGraphicsGetCurrentContext();
        CGContextSetStrokeColorWithColor(context, [UIColor lightGrayColor].CGColor);
        CGContextSetLineWidth(context, 2.0);
        
        int dimension = [self frame].size.width;
        int edges[2] = {0, dimension};
        int step = dimension / sqrt(self.sections);
        // Do vertical grid lines
        CGContextMoveToPoint(context, 0.0, 0.0);
        int count = 1;
        for (int x = 0; x <= dimension; x += step)
        {
            CGContextAddLineToPoint(context, x, edges[count % 2]);
            CGContextAddLineToPoint(context, x + step, edges[count % 2]);
            count ++;
        }
        // Horizontal grid lines
        CGContextMoveToPoint(context, 0.0, 0.0);
        count = 1;
        for (int y = 0; y <= dimension; y += step)
        {
            CGContextAddLineToPoint(context, edges[count % 2], y);
            CGContextAddLineToPoint(context, edges[count % 2], y + step);
            count ++;
        }
        CGContextStrokePath(context);
    }
}

- (BOOL)pointInside:(CGPoint)point withEvent:(UIEvent *)event
{
    // Says we don't want the touch, let painting view handle it.
    return NO;
}

-(void) dealloc
{
    [super dealloc];
}

@end
