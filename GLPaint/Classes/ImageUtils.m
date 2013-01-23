//
//  ImageUtils.m
//  GLPaint
//
//  Created by Steve Jarvis on 1/23/13.
//
//

#import "ImageUtils.h"

@implementation ImageUtils

// Passed a mutable array of 2-number arrays. The x and y touches. They are set
// so 0,0 is the bottom left corner of the image. Size is how mig the thing is.
+(NSString *)generateUrl:(NSMutableArray *)xyTouches dimension:(NSInteger)size
{
    NSLog(@"Generating URL!");
    // Need to make a 2d array representing the image. Remember the count we're
    // given has 0,0 bottom left, but network assumes 0,0 is at top left.
    NSMutableString *pixelRep = [NSMutableString stringWithCapacity:196];
    for (int y=size; y>0; y--)
    {
        for (int x=0; x<size; x++)
        {
            NSArray *obj = [NSArray arrayWithObjects:[NSNumber numberWithInt:x],[NSNumber numberWithInt:y], nil];
            if ([xyTouches containsObject:obj]) {
                [pixelRep appendString:@"1"];
            } else {
                [pixelRep appendString:@"0"];
            }
        }
    }
    
    NSString *prefix = @"http://cs.nmu.edu/~sjarvis/interpret.py?sec=";
    // todo generate this...
    NSString *suffix = @"&t=3.0357142857142856&n=0.7270408163265306&s=0.7908163265306123&w=0.7397959183673469&e=0.778061224489796";
    
    return [NSString stringWithFormat:@"%@%@%@", prefix ,pixelRep, suffix];
    
    /*return @"http://cs.nmu.edu/~sjarvis/interpret.py?sec=0000000000000000000000000000000000010000000000111110000000001111100000000011011000000000000110000000000011000000000001110000000000111000000000001111111100000001111100000000000000000000000000000000&t=3.0357142857142856&n=0.7270408163265306&s=0.7908163265306123&w=0.7397959183673469&e=0.778061224489796";
     */
}

@end
