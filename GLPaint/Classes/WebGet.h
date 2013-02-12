//
//  WebGet.h
//  GLPaint
//
//  Created by Steve Jarvis on 1/15/13.
//
//

#import <Foundation/Foundation.h>

@interface WebGet : NSObject {
    NSMutableData *receivedData;
    NSObject *listener;
}

-(id)initWithUrl:(NSString *)urlString callMeMaybe:(NSObject *)list;

@end
