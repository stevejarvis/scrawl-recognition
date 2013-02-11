//
//  Tests.m
//  Tests
//
//  Created by Steve Jarvis on 2/7/13.
//
//

#import "Tests.h"
#import "ImageUtils.h"

@implementation Tests

- (void)setUp
{
    [super setUp];
    
    // Set-up code here.
}

- (void)tearDown
{
    // Tear-down code here.
    
    [super tearDown];
}

- (void)testSectionsAsInk
{
    NSMutableString *pixels = [NSMutableString stringWithString:@"1000000000000000000000001"];
    ImageUtils *iutils = [[ImageUtils alloc] initWithSize:5
                                         numberOfSections:25
                                                pixelData:pixels];

}

@end
