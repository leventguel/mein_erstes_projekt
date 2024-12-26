package lf8;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.Statement;
import java.sql.SQLException;

public class InsertTestData {
    private static final Logger logger = LoggerFactory.getLogger(InsertTestData.class);

    public static void main(String[] args) {
	String insertSQL = "INSERT INTO students (name, age, note) VALUES (?, ?, ?);";

	try (Connection conn = DatabaseUtils.getConnection();
	     PreparedStatement pstmt = conn.prepareStatement(insertSQL)) {

	    pstmt.setString(1, "Max Mustermann");
	    pstmt.setInt(2, 18);
	    pstmt.setString(3, "1");
	    pstmt.executeUpdate();

	    pstmt.setString(1, "Maria Musterfrau");
	    pstmt.setInt(2, 19);
	    pstmt.setString(3, "2");
	    pstmt.executeUpdate();

	    pstmt.setString(1, "John Doe");
	    pstmt.setInt(2, 17);
	    pstmt.setString(3, "2");
	    pstmt.executeUpdate();

	    pstmt.setString(1, "Jane Doe");
	    pstmt.setInt(2, 20);
	    pstmt.setString(3, "5");
	    pstmt.executeUpdate();

	    logger.info("Test data inserted successfully!");

	} catch (Exception e) {
	    logger.error("Error while inserting test data: ", e);
	}
    }

    // New method to insert test data and return a result string
    public static String insert() {
	String result = "";

	String insertSQL = "INSERT INTO students (name, age, note) VALUES (?, ?, ?);";

	try (Connection conn = DatabaseUtils.getConnection();
	     PreparedStatement pstmt = conn.prepareStatement(insertSQL)) {

	    pstmt.setString(1, "Max Mustermann");
	    pstmt.setInt(2, 18);
	    pstmt.setString(3, "1");
	    pstmt.executeUpdate();

	    pstmt.setString(1, "Maria Musterfrau");
	    pstmt.setInt(2, 19);
	    pstmt.setString(3, "2");
	    pstmt.executeUpdate();

	    pstmt.setString(1, "John Doe");
	    pstmt.setInt(2, 17);
	    pstmt.setString(3, "2");
	    pstmt.executeUpdate();

	    pstmt.setString(1, "Jane Doe");
	    pstmt.setInt(2, 20);
	    pstmt.setString(3, "5");
	    pstmt.executeUpdate();

	    result = "Test data inserted successfully!";
	    logger.info(result);

	} catch (Exception e) {
	    result = "Error while inserting test data: " + e.getMessage();
	    logger.error(result, e);
	}

	return result;
    }
}

/*
public class InsertTestData {

    private static final Logger logger = LoggerFactory.getLogger(InsertTestData.class);

    public static void main(String[] args) {
	String url = "jdbc:mariadb://localhost:9450/school";
	String user = "root";
	String password = "newEnm898Zy@";

	String insertSQL = "INSERT INTO students (name, age, note) VALUES (?, ?, ?);";

	try (Connection conn = DriverManager.getConnection(url, user, password);
	     PreparedStatement pstmt = conn.prepareStatement(insertSQL)) {

	    // Insert Max Mustermann
	    pstmt.setString(1, "Max Mustermann");
	    pstmt.setInt(2, 18);
	    pstmt.setString(3, "1");
	    pstmt.executeUpdate();

	    // Insert Maria Musterfrau
	    pstmt.setString(1, "Maria Musterfrau");
	    pstmt.setInt(2, 19);
	    pstmt.setString(3, "2");
	    pstmt.executeUpdate();

	    // Insert John Doe
	    pstmt.setString(1, "John Doe");
	    pstmt.setInt(2, 17);
	    pstmt.setString(3, "2");
	    pstmt.executeUpdate();

	    // Insert Jane Doe
	    pstmt.setString(1, "Jane Doe");
	    pstmt.setInt(2, 20);
	    pstmt.setString(3, "5");
	    pstmt.executeUpdate();

	    logger.info("Test data inserted successfully!");

	} catch (Exception e) {
	    logger.error("Error while inserting test data: ", e);
	}
    }
}
*/
