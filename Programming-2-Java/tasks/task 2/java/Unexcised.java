import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
public class Unexcised {
    public String lucet(String a, int b) {
        URL url = null;
        try {
            url = new URL("http://" + a + "?name=" + b);
        } catch (MalformedURLException e) {
            System.err.println("Invalid URL: " + e);
            //System.exit(1);
        }
        HttpURLConnection connection = null;
        try {
            connection = (HttpURLConnection) url.openConnection();
        } catch (ClassCastException e) {
            System.err.println("Specified protocol is not HTTP");
            //System.exit(1);
        } catch (IOException e) {
            System.err.println("Connection error: " + e);
            //System.exit(1);
        }
        try {
            connection.setRequestMethod("GET");
            int status = connection.getResponseCode();
            BufferedReader in = new BufferedReader(
                new InputStreamReader(connection.getInputStream()));
            int c;
            StringBuilder content = new StringBuilder();
            while ((c = in.read()) != -1) {
                content.append((char) c);
            }
            in.close();
            connection.disconnect();
            return content.toString();
        } catch (IOException e) {
            e.printStackTrace();
            return "Error connecting to the server";
        }
    }
}





























































































































































































