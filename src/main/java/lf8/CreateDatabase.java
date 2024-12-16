package lf8;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class CreateDatabase {
    private static final Logger logger = LoggerFactory.getLogger(CreateDatabase.class);
    
    public static void main(String[] args) {
	try (Connection conn = DatabaseUtils.getConnection();
	     Statement stmt = conn.createStatement()) {
	    
	    String sql = "CREATE DATABASE IF NOT EXISTS school";
	    stmt.executeUpdate(sql);
	    logger.info("Database created successfully!");
	    
	} catch (Exception e) {
	    logger.error("Error while creating database: ", e);
	}
    }

    // New method to create the database and return a result string
    public static String create() {
	String result = "";

	try (Connection conn = DatabaseUtils.getConnection();
	     Statement stmt = conn.createStatement()) {

	    String sql = "CREATE DATABASE IF NOT EXISTS school";
	    stmt.executeUpdate(sql);
	    result = "Database created successfully!";
	    logger.info(result);

	} catch (Exception e) {
	    result = "Error while creating database: " + e.getMessage();
	    logger.error(result, e);
	}

	return result;
    }
}

/*
public class DatabaseCreator {
    public static void main(String[] args) {
	// Database connection details
	String url = "jdbc:mariadb://localhost:9450/"; // Adjust host and port as needed
	String user = "root"; // Replace with your DB username
	String password = "newEnm898Zy@"; // Replace with your DB password

	// SQL to create a new database
	String sql = "CREATE DATABASE school";

	try (Connection conn = DriverManager.getConnection(url, user, password);
	     Statement stmt = conn.createStatement()) {

	    // Execute the SQL statement
	    stmt.executeUpdate(sql);
	    System.out.println("Database created successfully!");

	} catch (Exception e) {
	    e.printStackTrace();
	}
    }
}
*/
