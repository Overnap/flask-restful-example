import android.os.AsyncTask;
import android.util.Pair;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

/** 
 * AsyncTask that communicates with the server.
 * Returns json string and status code as Pair.
 *
 * Usage 
 * JSONObject body = new JSONObject(); // then build the body you want
 * ServerRequest request = new ServerRequest("/posts", "POST")
 * request.execute(body.tostring);
 * Pair<String, Integer> response = request.get();
 * if (response.second == 200) {
 * ...
 */

public class ServerRequest extends AsyncTask<String, Void, Pair<String, Integer>> {
    String path, method;

    public ServerRequest(String path, String method)
    {
        this.path = path;
        this.method = method;
    }

    @Override
    protected Pair<String, Integer> doInBackground(String... json) {
        int retCode = 0;
        String result = "";

        try {
            String query;
            if (!method.equals("POST"))
                query = "?json=" + URLEncoder.encode(json[0], "UTF-8");
            else
                query = "";
            URL url = new URL("http://HOST:PORT/" + path + query);
            HttpURLConnection conn = (HttpURLConnection)url.openConnection();
            conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
            conn.setRequestProperty("Accept", "application/json");
            conn.setRequestMethod(method);
            conn.setDoInput(true);

            if (method.equals("POST")) {
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);
                OutputStream os = conn.getOutputStream();
                os.write(json[0].getBytes(StandardCharsets.UTF_8));
                os.flush();
                os.close();
            }

            retCode = conn.getResponseCode();

            InputStream is = retCode == 200 ? conn.getInputStream() : conn.getErrorStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(is));
            StringBuffer response = new StringBuffer();
            String line;
            while((line = br.readLine()) != null) {
                response.append(line);
            }
            br.close();

            result = response.toString();

        } catch (IOException e) {
            e.printStackTrace();
        }

        return new Pair<>(result, retCode);
    }
}