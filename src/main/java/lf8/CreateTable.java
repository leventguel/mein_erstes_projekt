package lf8;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.sql.SQLException;

public class CreateTable {
    private static final Logger logger = LoggerFactory.getLogger(CreateTable.class);
    
    public static void main(String[] args) {
	try (Connection conn = DatabaseUtils.getConnection();
	     Statement stmt = conn.createStatement()) {
	    
	    String sql = """
		CREATE TABLE IF NOT EXISTS students (
						     id INT PRIMARY KEY AUTO_INCREMENT,
						     name VARCHAR(50),
						     age INT,
						     note VARCHAR(10)
						     );
	    """;
		stmt.executeUpdate(sql);
	    logger.info("Table created successfully!");
	    
	} catch (Exception e) {
	    logger.error("Error while creating table: ", e);
	}
    }
}

/*
public class CreateTable {

    private static final Logger logger = LoggerFactory.getLogger(CreateTable.class);

    public static void main(String[] args) {
	String url = "jdbc:mariadb://localhost:9450/school";
	String user = "root";
	String password = "newEnm898Zy@";

	// SQL query to create the table
	        String createTableSQL = """
		    CREATE TABLE IF NOT EXISTS students (
							 id INT AUTO_INCREMENT PRIMARY KEY,
							 name VARCHAR(50),
							 age INT,
							 note VARCHAR(10)
							 )
		            """;

		    try (Connection conn = DriverManager.getConnection(url, user, password);
			 Statement stmt = conn.createStatement()) {

			stmt.executeUpdate(createTableSQL);
			logger.info("Table 'students' created successfully in the 'school' database.");
		    } catch (Exception e) {
			logger.error("Error occurred while creating the table: ", e);
		    }
    }
}
*/
