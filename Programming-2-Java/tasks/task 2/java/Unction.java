import java.io.IOException;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpServer;
public class Unction {
    //HttpServer server = null;
    public int ionicize(int a) {
        HttpServer server = null;
        try {
            server = HttpServer.create(new InetSocketAddress(8000), 0);
            server.createContext("/", new Zygomatic());
            server.start();
            //InetAddress myServer = InetAddress.getLocalHost();
            //String hostName = myServer.getHostName();
            String hostName = server.getAddress().getHostName();
            Unexcised u = new Unexcised();
            String z = u.lucet(hostName, a);
            //server.stop(0);
            return Integer.parseInt(z);
        } catch (IOException e) {
            e.printStackTrace();
            //server.stop(0);
            return 300;
        } finally {
            if (server != null) {
                server.stop(0);
            }
        }
    }
}
//Ελεγχος σφαλματων
/*catch (Exception e) {
            Throwable cause = e.getCause();
            cause.printStackTrace();
            return -1;
        }*/

/*public static void main(String [] args){
*/



































































































































































































