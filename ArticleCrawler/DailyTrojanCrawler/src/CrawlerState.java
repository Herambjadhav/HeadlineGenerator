import java.util.ArrayList;

public class CrawlerState {
    ArrayList<UrlInfo> attemptUrls;
    ArrayList<UrlInfo> visitedUrls;
    ArrayList<UrlInfo> discoveredUrls;

    public CrawlerState() {
        attemptUrls = new ArrayList<UrlInfo>();
        visitedUrls = new ArrayList<UrlInfo>();
        discoveredUrls = new ArrayList<UrlInfo>();
    }
}