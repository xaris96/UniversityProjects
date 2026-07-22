package t21;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Optional;
public class GPT3Integration {
    //public static void main(String[] args) {
    private static final String apiKey = Optional.ofNullable(System.getenv("OPENAI_API_KEY"))
            .filter(key -> !key.isBlank())
            .orElse("YOUR_OPENAI_API_KEY_HERE");
            
    public String getResponse(String prompt) {
        
        try {
            //String prompt = "Once upon a time,";

            URL url = new URL("https://api.openai.com/v1/engines/text-davinci-003/completions");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Authorization", "Bearer " + apiKey);
            connection.setRequestProperty("Content-Type", "application/json");
            connection.setDoOutput(true);

            String requestData = "{\"prompt\": \"" + prompt + "\", \"max_tokens\": 50}";

            OutputStream os = connection.getOutputStream();
            os.write(requestData.getBytes(StandardCharsets.UTF_8));
            os.flush();
            os.close();

            int responseCode = connection.getResponseCode();

            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader in = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                String inputLine;
                StringBuilder response = new StringBuilder();

                while ((inputLine = in.readLine()) != null) {
                    response.append(inputLine);
                }
                in.close();
                return response.toString();
                // Handle the response JSON here
                //System.out.println("Response: " + response.toString());
            } else if (connection.getResponseCode() == 429) {
                // Handle Too Many Requests error
                Thread.sleep(1000); // Wait for 1 second before retrying
                return ("Received HTTP 429 Too Many Requests error. Retrying after a delay...");
                
                // Retry the request
            } else {
                //System.out.println("Request failed with response code: " + responseCode);
                return "Request failed with response code: " + responseCode;
            }
            //connection.disconnect();
        } catch (Exception e) {
            //e.printStackTrace();
            return "An error occurred: " + e.getMessage();

        }
    }
}
