package lf8;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

public class CombinedDatabaseOperations {

    private static final Logger logger = LoggerFactory.getLogger(CombinedDatabaseOperations.class);

    public static void main(String[] args) {
	if (args.length == 0) {
	    System.out.println("Usage: java -Dexec.mainClass=lf8.CombinedDatabaseOperations -Dexec.args=\"<operation>\"");
	    System.out.println("Available operations: createDatabase, createTable, insertTestData, retrieveData");
	    return;
	}

	String operation = args[0];
	String url = "jdbc:mariadb://localhost:9450/";
	String user = "root";
	String password = "newEnm898Zy@";

	try (Connection conn = DatabaseUtils.getConnection()) {
	    logger.info("Connected to MariaDB successfully!");

	    switch (operation) {
	    case "createDatabase" -> createDatabase(conn);
	    case "createTable" -> createTable(conn);
	    case "insertTestData" -> insertTestData(conn);
	    case "retrieveData" -> fetchAndDisplayData(conn);
	    default -> System.out.println("Invalid operation. Available operations: createDatabase, createTable, insertTestData, retrieveData");
	    }
	} catch (Exception e) {
	    logger.error("Error in database operations: ", e);
	}
    }

    private static void createDatabase(Connection conn) {
	try (Statement stmt = conn.createStatement()) {
	    stmt.executeUpdate("CREATE DATABASE IF NOT EXISTS school;");
	    logger.info("Database 'school' created or already exists.");
	} catch (Exception e) {
	    logger.error("Error creating database: ", e);
	}
    }

    private static void createTable(Connection conn) {
	try (Statement stmt = conn.createStatement()) {
	    stmt.executeUpdate("USE school;");
	    stmt.executeUpdate("""
			       CREATE TABLE IF NOT EXISTS students (
								    id INT PRIMARY KEY AUTO_INCREMENT,
								    name VARCHAR(50),
								    age INT,
								    note VARCHAR(10)
								    );
			       """);
			       logger.info("Table 'students' created or already exists.");
			       } catch (Exception e) {
		logger.error("Error creating table: ", e);
	    }
	}

	private static void insertTestData(Connection conn) {
	    String insertSQL = "INSERT INTO students (name, age, note) VALUES (?, ?, ?);";

	    try (PreparedStatement pstmt = conn.prepareStatement(insertSQL)) {
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

	private static void fetchAndDisplayData(Connection conn) {
	    String selectSQL = "SELECT id, name, age, note FROM students;";

	    try (Statement stmt = conn.createStatement();
		 ResultSet rs = stmt.executeQuery(selectSQL)) {

		// Print the header with aligned columns
		System.out.printf("%-5s%-20s%-5s%-5s%n", "ID", "Name", "Age", "Note");
		System.out.println("---------------------------------------------");

		// Fetch and print each row with aligned columns
		while (rs.next()) {
		    int id = rs.getInt("id");
		    String name = rs.getString("name");
		    int age = rs.getInt("age");
		    String note = rs.getString("note");

		    // %-5s means left-align and reserve 5 characters for each field, adjust as needed
		    System.out.printf("%-5d%-20s%-5d%-5s%n", id, name, age, note);
		}

		logger.info("Data fetched and displayed successfully!");

	    } catch (Exception e) {
		logger.error("Error fetching data: ", e);
	    }
	}
}
