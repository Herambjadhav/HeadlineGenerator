import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;

import java.io.FileWriter;
import java.util.HashSet;
import java.util.List;
import java.util.HashMap;

public class App
{
//    private final static String crawlStorageFolder = "/Users/garethdsouza/Documents/MS/CSCI572InformationRetrieval/Assignment2/NYTimes";
//    private final static String crawlStorageFolder = "/Users/garethdsouza/Documents/MS/CSCI572InformationRetrieval/Assignment2/BBCNews";
	private final static String crawlStorageFolder = "/Users/garethdsouza/Git/csci544/DailyTrojan";
	
//    private final static String crawlSeed = "http://www.nytimes.com/";
//    private final static String crawlSeed = "http://www.bbc.com/news";
	private final static String crawlSeed = "http://dailytrojan.com";
    
    private final static int maxPageToFetch = 1000;
    private final static int maxDepthOfCrawling = 16;
    private final static int numberOfCrawlers = 7;
    private final static int maxDownloadedSize = 1024 * 1024 * 10;
    private final static String name = "Gareth Dsouza";
    private final static String id = "9965641748";
//    private final static String newssite = "NY News";
    private final static String newssite = "Daily Trojan";

    public static void main(String[] args) throws Exception {
    	System.out.println("Starting runCrawler");
        CrawlController crawlController = runCrawler();

        // get sum
        CrawlerState sumState = new CrawlerState();
        List<Object> crawlersLocalData = crawlController.getCrawlersLocalData();
        System.out.println("Reading local data");
        
        for (Object localData : crawlersLocalData) {
        	CrawlerState state = (CrawlerState) localData;
            sumState.attemptUrls.addAll(state.attemptUrls);
            sumState.visitedUrls.addAll(state.visitedUrls);
            sumState.discoveredUrls.addAll(state.discoveredUrls);
        }

        System.out.println("Writing Files");
        
        saveFetchCsv(sumState);
        saveVisitCsv(sumState);
        saveUrlsCsv(sumState);
        savePageRankCsv(sumState);
        saveStatistics(sumState);
        
        System.out.println("Crawl Completed");
    }

    public static void saveFetchCsv(CrawlerState sumState) throws Exception {
        String fileName = crawlStorageFolder + "/fetch.csv";
        FileWriter writer = new FileWriter(fileName);
        writer.append("URL,HTTPStatusCode\n");
        for (UrlInfo info : sumState.attemptUrls) {
            writer.append(info.url + "," + info.statusCode + "\n");
        }
        writer.flush();
        writer.close();
    }

    public static void saveVisitCsv(CrawlerState sumState) throws Exception {
        String fileName = crawlStorageFolder + "/visit.csv";
        FileWriter writer = new FileWriter(fileName);
        writer.append("URL,Size,#OfOutLinks,ContentType\n");
        for (UrlInfo info : sumState.visitedUrls) {
            if (info.type != "unknown") {
                writer.append(info.url + "," + info.size + "," + info.outgoingUrls.size() + "," + info.type + "\n");
            }
        }
        writer.flush();
        writer.close();
    }

    public static void saveUrlsCsv(CrawlerState sumState) throws Exception {
        String fileName = crawlStorageFolder + "/urls.csv";
        FileWriter writer = new FileWriter(fileName);
        writer.append("URL,Type\n");
        for (UrlInfo info : sumState.discoveredUrls) {
            writer.append(info.url + "," + info.type + "\n");
        }
        writer.flush();
        writer.close();
    }

    public static void savePageRankCsv(CrawlerState sumState) throws Exception {
        String fileName = crawlStorageFolder + "/pagerank.csv";
        String mapFileName = crawlStorageFolder + "/mapping.csv";
        FileWriter writer = new FileWriter(fileName);
        FileWriter mapWriter = new FileWriter(mapFileName);
        String fileId;

        for (UrlInfo info : sumState.visitedUrls) {
            if (info.extension.equals("")) {
                continue;
            }
            fileId = App.crawlStorageFolder + "/files/" + info.hash + info.extension;
            mapWriter.append(fileId + "," + info.url + "\n");
            writer.append(fileId + ",");
            for (String outgoingUrl : info.outgoingUrls) {
                // generate outgoing url
                String[] segment = outgoingUrl.split(".");
                if (segment.length > 1 && segment[segment.length - 1].length() != 0) {
                    fileId = App.crawlStorageFolder + "/files/" + UrlInfo.hashString(outgoingUrl) + "." + segment[segment.length - 1];
                    mapWriter.append(fileId + "," + outgoingUrl + "\n");
                    writer.append(fileId + ",");
                } else {
                    fileId = App.crawlStorageFolder + "/files/" + UrlInfo.hashString(outgoingUrl) + ".html";
                    mapWriter.append(fileId + "," + outgoingUrl + "\n");
                    writer.append(fileId + ",");
                }
            }
            writer.append("\n");
        }

        writer.flush();
        writer.close();
    }

    public static void saveStatistics(CrawlerState sumState) throws Exception {
        String fileName = crawlStorageFolder + "/CrawlReport.txt";
        FileWriter writer = new FileWriter(fileName);

        // Personal Info
        writer.append("Name: " + name + "\n");
        writer.append("USC ID: " + id + "\n");
        writer.append("NewsSite crawled: " + newssite + "\n");
        writer.append("\n");

        // Fetch Statistics
        writer.append("Fetch Statistics\n================\n");
        writer.append("fetches attempted: " + sumState.attemptUrls.size() + "\n");
        writer.append("fetched succeeded: " + sumState.visitedUrls.size() + "\n");

        // get failed url and aborted urls
        int failedUrlsCount = 0;
        int abortedUrlsCount = 0;
        for (UrlInfo info : sumState.attemptUrls) {
            if (info.statusCode >= 300 && info.statusCode < 400) {
                abortedUrlsCount++;
            } else if (info.statusCode != 200) {
                failedUrlsCount++;
            }
        }

        writer.append("fetched aborted: " + abortedUrlsCount + "\n");
        writer.append("fetched failed: " + failedUrlsCount + "\n");
        writer.append("\n");

        // Outgoing URLS
        HashSet<String> hashSet = new HashSet<String>();
        int uniqueUrls = 0;
        int newsUrls = 0;
        int uscUrls = 0;
        int outUrls = 0;
        writer.append("Outgoing URLs:\n==============\n");
        writer.append("Total URLS extracted: " + sumState.discoveredUrls.size() + "\n");
        for (UrlInfo info : sumState.discoveredUrls) {
            if (!hashSet.contains(info.url)) {
                hashSet.add(info.url);
                uniqueUrls++;
                if (info.type.equals("OK")) {
                	newsUrls++;
                } 
//                    else if (info.type.equals("USC")) {
//                    uscUrls++;
//                } 
                else{
                    outUrls++;
                }
            }
        }
        writer.append("# unique URLs extracted: " + uniqueUrls + "\n");
        writer.append("# unique URLs within News Site: " + newsUrls + "\n");
//        writer.append("# unique USC URLs outside School: " + uscUrls + "\n");
        writer.append("# unique USC outside News Site: " + outUrls + "\n");
        writer.append("\n");

        // Status Code
        writer.append("Status Codes\n=============\n");
        HashMap<Integer, Integer> hashMap = new HashMap<Integer, Integer>();
        for (UrlInfo info : sumState.attemptUrls) {
            if (hashMap.containsKey(info.statusCode)) {
                hashMap.put(info.statusCode, hashMap.get(info.statusCode) + 1);
            } else {
                hashMap.put(info.statusCode, 1);
            }
        }
        HashMap<Integer, String> statusCodeMapping = new HashMap<Integer, String>();
        statusCodeMapping.put(200, "OK");
        statusCodeMapping.put(301, "Moved Permanently");
        statusCodeMapping.put(302, "Found");
        statusCodeMapping.put(401, "Unauthorized");
        statusCodeMapping.put(403, "Forbidden");
        statusCodeMapping.put(404, "Not Found");
        statusCodeMapping.put(405, "Method Not Allowed");
        statusCodeMapping.put(500, "Internal Server Error");

        for (Integer key : hashMap.keySet()) {
            writer.append("" + key + " " + statusCodeMapping.get(key) + ": " + hashMap.get(key) + "\n");
        }
        writer.append("\n");

        // File Size
        writer.append("File Size\n===========\n");
        int oneK = 0;
        int tenK = 0;
        int hundredK = 0;
        int oneM = 0;
        int other = 0;
        for (UrlInfo info : sumState.visitedUrls) {
            if (info.size < 1024) {
                oneK++;
            } else if (info.size < 10240) {
                tenK++;
            } else if (info.size < 102400) {
                hundredK++;
            } else if (info.size < 1024 * 1024) {
                oneM++;
            } else {
                other++;
            }
        }
        writer.append("< 1KB: " + oneK + "\n");
        writer.append("1KB ~ <10KB: " + tenK + "\n");
        writer.append("10KB ~ <100KB: " + hundredK + "\n");
        writer.append("100KB ~ <1MB: " + oneM + "\n");
        writer.append(">= 1MB: " + other + "\n");
        writer.append("\n");

        // Content Types
        HashMap<String, Integer> hashMap1 = new HashMap<String, Integer>();
        writer.append("Content Types\n==============\n");
        for (UrlInfo info : sumState.visitedUrls) {
            if (info.type.equals("unknown")) {
                continue;
            }
            if (hashMap1.containsKey(info.type)) {
                hashMap1.put(info.type, hashMap1.get(info.type) + 1);
            } else {
                hashMap1.put(info.type, 1);
            }
        }
        for (String key : hashMap1.keySet()) {
            writer.append("" + key + ": " + hashMap1.get(key) + "\n");
        }
        writer.append("\n");

        writer.flush();
        writer.close();
    }

    public static CrawlController runCrawler() throws Exception {
        CrawlConfig config = new CrawlConfig();
        config.setCrawlStorageFolder(crawlStorageFolder);
        config.setMaxDepthOfCrawling(maxDepthOfCrawling);
        config.setMaxPagesToFetch(maxPageToFetch);
        config.setMaxDownloadSize(maxDownloadedSize);
        config.setIncludeBinaryContentInCrawling(true);

        // initialize
        PageFetcher pageFetcher = new PageFetcher(config);
        RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
        RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig, pageFetcher);

        // add seed
        CrawlController crawlController = new CrawlController(config, pageFetcher, robotstxtServer);
        crawlController.addSeed(crawlSeed);

        // start crawling
        MyCrawler.configure(crawlStorageFolder + "/files");
        MyCrawler.setSideToConsider(crawlSeed);
        crawlController.start(MyCrawler.class, numberOfCrawlers);

        return crawlController;
    }
}