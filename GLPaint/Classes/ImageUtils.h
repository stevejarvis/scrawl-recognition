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
    int numOfSections;
}

@property(retain) NSMutableString *pixelRep;

-(id)initWithSize:(int)size numberOfSections:(int)numSections pixelData:(NSMutableString *)pixelData;
-(NSString *)generateUrl;
-(NSString *)sectionsAsInk;
-(BOOL)sectionNumberContainsInk:(int)sectionNum;
-(NSString *)getDensities;
-(char)getValueAtX:(int)xCoordinate y:(int)yCoordinate;

@end
