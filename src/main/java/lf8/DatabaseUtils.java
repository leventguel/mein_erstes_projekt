package lf8;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;

public class DatabaseUtils {

    private static final String URL = "jdbc:mariadb://localhost:9450/school";
    private static final String USER = "root";
    private static final String PASSWORD = "newEnm898Zy@";

    public static Connection getConnection() throws Exception {
	return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}
