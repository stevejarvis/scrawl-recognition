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

@end
