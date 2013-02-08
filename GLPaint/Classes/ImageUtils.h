//
//  ImageUtils.h
//  GLPaint
//
//  Created by Steve Jarvis on 1/23/13.
//
//

#import <Foundation/Foundation.h>

@interface ImageUtils : NSObject
{
    int dimension;
}

@property(retain) NSMutableString *pixelRep;

-(NSString *)generateUrl:(NSMutableString *)xyTouches dimension:(int)size;
-(NSString *)sectionsAsInk;
-(BOOL)sectionNumberContainsInk:(int)sectionNum;
-(NSString *)getDensities;
-(char)getValueAtX:(int)xCoordinate y:(int)yCoordinate;

@end
