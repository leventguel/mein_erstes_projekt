package lf8;

import java.sql.Connection;
import java.sql.DriverManager;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

//import org.apache.logging.log4j.LogManager;
//import org.apache.logging.log4j.Logger;

public class TestConnection {

    // Create a Logger instance for the class
    private static final Logger logger = LoggerFactory.getLogger(TestConnection.class); // Logback
    //private static final Logger logger = LogManager.getLogger(TestConnection.class); // log4j

    public static void main(String[] args) {

	try (Connection conn = DatabaseUtils.getConnection()) {
	    if (conn != null) {
		// Log success message at INFO level
		logger.info("Connected to MariaDB successfully!");
	    } else {
		// Log failure message at WARN level
		logger.warn("Failed to make connection!");
	    }
	} catch (Exception e) {
	    // Log the exception message at ERROR level
	    logger.error("Error while trying to connect to the database.", e);
	}
    }
}

/*
public class TestConnection {

    // Create a Logger instance for the class
    private static final Logger logger = LoggerFactory.getLogger(TestConnection.class); // Logback
    //private static final Logger logger = LogManager.getLogger(TestConnection.class); // log4j

    public static void main(String[] args) {
	String url = "jdbc:mariadb://localhost:9450/";
	String user = "root";
	String password = "newEnm898Zy@";

	try (Connection conn = DriverManager.getConnection(url, user, password)) {
	    if (conn != null) {
		// Log success message at INFO level
		logger.info("Connected to MariaDB successfully!");
	    } else {
		// Log failure message at WARN level
		logger.warn("Failed to make connection!");
	    }
	} catch (Exception e) {
	    // Log the exception message at ERROR level
	    logger.error("Error while trying to connect to the database.", e);
	}
    }
}
*/
