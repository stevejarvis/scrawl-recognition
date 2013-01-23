/*
 This just makes a request to the site where the network is hosted
 and returns the output of the page. Scrapes it.
 
 */

#import "WebGet.h"

@implementation WebGet

// Given a url, return the text produced by that page.
-(id)initWithUrl:(NSString *)urlString callMeMaybe:(NSObject *)list
{
    self = [super init];
    
    if(self != nil) {
        listener = list;
        NSURL *url = [NSURL URLWithString:urlString];
        NSURLRequest *mRequest = [NSURLRequest requestWithURL:url
                                                  cachePolicy:NSURLRequestUseProtocolCachePolicy
                                              timeoutInterval:30.0];
        // Use the request to make a connection and start loading data.
        NSURLConnection *mConnection = [[NSURLConnection alloc] initWithRequest:mRequest
                                                                      delegate:self];
        if (mConnection) {
            // Create the NSMutableData to hold the received data.
            receivedData = [[NSMutableData data] retain];
        } else {
            NSLog(@"Connection failed!");
            // Inform the user that the connection failed.
        }
    }
    return self;
}

// Call back each time a header is loaded, so could happen multiple times per
// request. Although my site should have no redirects.
- (void)connection:(NSURLConnection *)connection didReceiveResponse:(NSURLResponse *)response
{
    NSLog(@"Connection recieved a response.");
    // Just reset the datasize, since we're loading a new page.
    [receivedData setLength:0];
}

// Periodically sent new data, remember it.
- (void)connection:(NSURLConnection *)connection didReceiveData:(NSData *)data
{
    NSLog(@"Received more data");
    // Append the new data to receivedData.
    [receivedData appendData:data];
}

// Bad news.
- (void)connection:(NSURLConnection *)connection didFailWithError:(NSError *)error
{
    // release the connection, and the data object
    [connection release];
    [receivedData release];
    
    // inform the user
    NSLog(@"Connection failed! Error - %@ %@",
          [error localizedDescription],
          [[error userInfo] objectForKey:NSURLErrorFailingURLStringErrorKey]);
}

// When download is finished, this method is called.
- (void)connectionDidFinishLoading:(NSURLConnection *)connection
{
    NSLog(@"Succeeded! Received %d bytes of data",[receivedData length]);
    dataString = [[NSString alloc] initWithData:receivedData
                                       encoding:NSASCIIStringEncoding];
    [listener receiveData:dataString];
    // release the connection, and the data object
    [connection release];
    [receivedData release];
    [dataString release];
}

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
