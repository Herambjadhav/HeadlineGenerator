import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;

public class UrlInfo {
	public int statusCode;
	public String url;
	public String type;
	public int size;
	public ArrayList<String> outgoingUrls;
	public String extension;
	public String hash;
	
	
	public UrlInfo(String url,int statusCode){
		this.statusCode = statusCode;
		this.url = url;
	}
	
	public UrlInfo(String url, String type) {
	        this.url = url;
	        this.type = type;
	}
	public UrlInfo(String url, int size, ArrayList<String> outgoingUrls, String type, String extenstion) {
        this.url = url;
        this.size = size;
        this.outgoingUrls = outgoingUrls;
        this.type = type;
        this.extension = extenstion;
        this.hash = hashString(url);
        
    }
	public static String hashString(String s) {
        byte[] hash = null;
        try {
            MessageDigest md = MessageDigest.getInstance("MD5");
            hash = md.digest(s.getBytes());

        } catch (NoSuchAlgorithmException e) { e.printStackTrace(); }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < hash.length; ++i) {
            String hex = Integer.toHexString(hash[i]);
            if (hex.length() == 1) {
                sb.append(0);
                sb.append(hex.charAt(hex.length() - 1));
            } else {
                sb.append(hex.substring(hex.length() - 2));
            }
        }
        return sb.toString();
    }
}
