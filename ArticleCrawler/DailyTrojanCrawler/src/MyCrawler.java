import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Set;
import java.util.regex.Pattern;

import com.google.common.io.Files;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;

public class MyCrawler extends WebCrawler{
	
//	private final static Pattern FILTERS = Pattern.compile(".*(\\.(css|js|gif|jpg|png|mp3|mp3|zip|gz))$");
	private final static Pattern FILTERS = Pattern.compile(".*(\\.(css|js|mp3|mp3|zip|gz|ico|xml))$");
	private static File storageFolder;
	private static String siteToConsider;
	private static int crawlCounter;
	
	CrawlerState crawlerState;
	
	public MyCrawler(){
		crawlerState = new CrawlerState();
		crawlCounter = 0;
	}
	
	public static void configure(String storageFolderName){
		storageFolder = new File(storageFolderName);
		if(!storageFolder.exists()){
			storageFolder.mkdirs();
		}
	}
	
	public static void setSideToConsider(String siteURL){
		siteToConsider = siteURL;
	}
	
	@Override
	public boolean shouldVisit(Page page, WebURL url) {
        String href = url.getURL().toLowerCase();
        String type = "N_OK";
        if (href.contains(siteToConsider)) {
            type = "OK";
        }
        crawlerState.discoveredUrls.add(new UrlInfo(href, type));
        return !FILTERS.matcher(href).matches() && type.equals("OK");
    }
	
	@Override
	public void visit(Page page){
		
		//Get the URL of the page
		String url = page.getWebURL().getURL();
		
		//Extract the contentType and not Encoding from the content type 
		//e.g. text/html; charset=UTF-8
		String contentType = page.getContentType().split(";")[0];
		
		//Create List for outgoing Urls for counting.
		ArrayList<String> outgoingUrls = new ArrayList<String>();
		
		UrlInfo urlInfo;
		//If file type is .html we will extract the links on the page.

		if(contentType.equals("text/html")){
			if(page.getParseData() instanceof HtmlParseData){
				
				HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
				//getOutgoingUrls() function from HtmlParseData is used. It returns a set of WebURL
				
				Set<WebURL> links =   htmlParseData.getOutgoingUrls();
				//Enumerate through the set and save the URLs of the outgoing links to the list
				
				for(WebURL link : links){
					outgoingUrls.add(link.getURL());
				}
				
				//Create the urlInfo object and add it to the list of visited URLs
				urlInfo = new UrlInfo(url,page.getContentData().length,outgoingUrls,"text/html",".html");
				crawlerState.visitedUrls.add(urlInfo);
			} 
			//Handle case if a static page has no outgoing urls or HTML Data cannot get parsed
			else {
				urlInfo = new UrlInfo(url,page.getContentData().length,outgoingUrls,"text/html",".html");
				crawlerState.visitedUrls.add(urlInfo);
			}
			
		//Do the same for 	
		} else if (contentType.equals("application/msword")) { // doc
            urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "application/msword", ".doc");
            crawlerState.visitedUrls.add(urlInfo);
        } else if (contentType.equals("application/pdf")) { // pdf
            urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "application/pdf", ".pdf");
            crawlerState.visitedUrls.add(urlInfo);
        } else if (contentType.equals("application/vnd.openxmlformats-officedocument.wordprocessingml.document")) {
            urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", ".docx");
            crawlerState.visitedUrls.add(urlInfo);
        } else if(contentType.equals("image/gif")){
        	urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "image/gif", ".gif");
            crawlerState.visitedUrls.add(urlInfo);
        }else if(contentType.equals("image/png")){
        	urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "image/png", ".png");
            crawlerState.visitedUrls.add(urlInfo);
        }else if(contentType.equals("image/jpg")){
        	urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "image/jpg", ".jpg");
            crawlerState.visitedUrls.add(urlInfo);
        }else if(contentType.equals("image/tif")){
        	urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "image/tif", ".tif");
            crawlerState.visitedUrls.add(urlInfo);
        }
        
        
        else {
            urlInfo = new UrlInfo(url, page.getContentData().length, outgoingUrls, "unknown", "");
            crawlerState.visitedUrls.add(urlInfo);
        }

		
		//Code to download the files to local server
		//Check if the file extension exists
		if (!urlInfo.extension.equals("")) {
			
			//Save file path and name as absolute path of folder/hash value of file name.extension
			//eg test/files/0d753a9b0d62a8def58df957007b12f6.html
			String filename = storageFolder.getAbsolutePath() + "/" + urlInfo.hash + urlInfo.extension;
            
			try {
				//Write page content data to new file with above filename
                Files.write(page.getContentData(), new File(filename));
            } catch (IOException iox) {
                System.out.println("Failed to write file: " + filename);
            }
        }
        System.out.println("Crawl Counter - "+crawlCounter);
        crawlCounter++;
		
		
	}
	
	@Override
    protected void handlePageStatusCode(WebURL webUrl, int statusCode, String statusDescription) {
        crawlerState.attemptUrls.add(new UrlInfo(webUrl.getURL(), statusCode));
    }

    @Override
    public Object getMyLocalData() {
        return crawlerState;
    }
	
	
	
}
