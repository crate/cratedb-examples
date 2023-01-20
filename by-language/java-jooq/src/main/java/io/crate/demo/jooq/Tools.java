package io.crate.demo.jooq;

import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Properties;

public class Tools {

    /**
     * Open file from resource folder as stream.
     *
     * https://mkyong.com/java/java-read-a-file-from-resources-folder/
     */
    public static InputStream openResourceStream(String fileName) {
        //
        //
        ClassLoader classLoader = Application.class.getClassLoader();
        return classLoader.getResourceAsStream(fileName);
    }

    /**
     * Read text file from application resources.
     */
    public static String readTextFile(String fileName) throws IOException {
        InputStream inputStream = Tools.openResourceStream(fileName);
        String text = new String(inputStream.readAllBytes(), StandardCharsets.UTF_8);
        return text;
    }

    /**
     * Read settings from properties file.
     */
    public static Properties readSettingsFile(String fileName) {
        InputStream is = Tools.openResourceStream(fileName);
        Properties properties = new Properties();
        try {
            properties.load(is);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return properties;
    }

    /**
     * Some pretty printing.
     */
    public static void title(String title) {
        String dashes = "=".repeat(title.length());
        System.out.println();
        System.out.println(dashes);
        System.out.println(title);
        System.out.println(dashes);
        System.out.println();
    }

    public static void print(Object o) {
        System.out.println(o);
    }

}
