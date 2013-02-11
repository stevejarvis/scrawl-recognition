//
//  ImageUtils.m
//  GLPaint
//
//  Created by Steve Jarvis on 1/23/13.
//
//

#import "ImageUtils.h"

@implementation ImageUtils

@synthesize pixelRep;

-(id)initWithSize:(int)size numberOfSections:(int)numSections pixelData:(NSMutableString *)pixelData
{
    self = [super init];
    pixelRep = pixelData;
    dimension = size;
    numOfSections = numSections;
    return self;
}

// Passed a mutable string of 1's and 0's representing a touch per pixel. Size is
// the number of pixels in one dimension.
-(NSString *)generateUrl
{
    self = [super init];
    
    NSLog(@"Generating URL!");
    
    NSString *inkRep = [self sectionsAsInk];
    NSString *densities = [self getDensities];
    NSString *url = [NSString stringWithFormat:@"http://cs.nmu.edu/~sjarvis/interpret.py?sec=%@&%@", inkRep, densities];
    [pixelRep release];
    return url;
}

-(char)getValueAtX:(int)xCoordinate y:(int)yCoordinate
{
    return [pixelRep characterAtIndex:(yCoordinate * dimension + xCoordinate)];
}

-(NSString *)sectionsAsInk
{
    NSMutableString *retVal = [NSMutableString stringWithCapacity:numOfSections];
    for (int i=0; i<numOfSections; i++) {
        if ([self sectionNumberContainsInk:i]) {
            [retVal appendString:@"1"];
        } else {
            [retVal appendString:@"0"];
        }
    }
    NSAssert([retVal length] == numOfSections, @"The sections as ink section is not %d.", numOfSections);
    NSLog(@"sectionsAsInk: %@", retVal);
    return retVal;
}

-(BOOL)sectionNumberContainsInk:(int)sectionNum
{
    int sectionsPerSide = sqrt(numOfSections);
    int sectionDimension = floor(dimension / sectionsPerSide);
    int startRow = floor((sectionNum / sectionsPerSide) * sectionDimension);
    int startColumn = floor((sectionNum % sectionsPerSide) * sectionDimension);
    for (int y = startRow; y < (startRow + sectionDimension); y++)
    {
        for (int x = startColumn; x < (startColumn + sectionDimension); x++)
        {
            if ([self getValueAtX:x y:y] == '1'){
                return true;
            }
        }
    }
    return false;
}

-(NSString *)getDensities
{
    float north = 0.0;
    for (int y = 0; y < (dimension / 2); y++)
    {
        for (int x = 0; x < dimension; x++)
        {
            if ([self getValueAtX:x y:y] == '1'){
                north ++;
            }
        }
    }
    
    float south = 0.0;
    for (int y = (dimension / 2); y < dimension; y++)
    {
        for (int x = 0; x < dimension; x++)
        {
            if ([self getValueAtX:x y:y] == '1'){
                south ++;
            }
        }
    }

    float west = 0.0;
    for (int y = 0; y < dimension; y++)
    {
        for (int x = 0; x < (dimension / 2); x++)
        {
            if ([self getValueAtX:x y:y] == '1'){
                west ++;
            }
        }
    }
    
    float east = 0.0;
    for (int y = 0; y < dimension; y++)
    {
        for (int x = (dimension / 2); x < dimension; x++)
        {
            if ([self getValueAtX:x y:y] == '1'){
                east ++;
            }
        }
    }
    
    float total = north + south + west + east;

    // The factor of 10 is introduced by the network to exaggerate the density differences.
    // Now that seems silly.
    total = total / (dimension * dimension / 10);
    north = north / (dimension * dimension / 10);
    south = south / (dimension * dimension / 10);
    west = west / (dimension * dimension / 10);
    east = east / (dimension * dimension / 10);
    
    NSString *ret = [NSString stringWithFormat:@"t=%1.9f&n=%1.9f&s=%1.9f&w=%1.9f&e=%1.9f", total, north, south, west, east];
    NSLog(@"Dimensions: %@", ret);
    return ret;
}

- (void) dealloc
{
    [super dealloc];
}

@end
