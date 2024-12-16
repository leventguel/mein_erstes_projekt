package lf8;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;
import java.sql.ResultSetMetaData;

import java.util.ArrayList;
import java.util.List;

public class RetrieveStudents {
    private static final Logger logger = LoggerFactory.getLogger(RetrieveStudents.class);
    
    // Method to retrieve student data, format it for CLI and return data for the GUI
    public static Object[] retrieve() {
	String query = "SELECT * FROM students";
	List<Object[]> data = new ArrayList<>();
	StringBuilder cliOutput = new StringBuilder();
	String[] columns = new String[0];
	int[] columnWidths;

	try (Connection conn = DatabaseUtils.getConnection();
	     Statement stmt = conn.createStatement();
	     ResultSet rs = stmt.executeQuery(query)) {

	    // Fetch column names and initialize widths
	    ResultSetMetaData metaData = rs.getMetaData();
	    int columnCount = metaData.getColumnCount();
	    columns = new String[columnCount];
	    columnWidths = new int[columnCount];

	    for (int i = 1; i <= columnCount; i++) {
		columns[i - 1] = metaData.getColumnName(i);
		columnWidths[i - 1] = columns[i - 1].length(); // Start with column name length
	    }

	    // Fetch data and adjust column widths
	    while (rs.next()) {
		Object[] row = new Object[columnCount];
		for (int i = 1; i <= columnCount; i++) {
		    Object value = rs.getObject(i);
		    row[i - 1] = value != null ? value.toString() : "NULL";
		    columnWidths[i - 1] = Math.max(columnWidths[i - 1], row[i - 1].toString().length());
		}
		data.add(row);
	    }

	    // Build CLI output header
	    for (int i = 0; i < columns.length; i++) {
		cliOutput.append(String.format("%-" + columnWidths[i] + "s ", columns[i]));
	    }
	    cliOutput.append("\n");
	    for (int width : columnWidths) {
		cliOutput.append("-".repeat(width)).append(" ");
	    }
	    cliOutput.append("\n");

	    // Build CLI output rows
	    for (Object[] row : data) {
		for (int i = 0; i < row.length; i++) {
		    cliOutput.append(String.format("%-" + columnWidths[i] + "s ", row[i]));
		}
		cliOutput.append("\n");
	    }

	} catch (Exception e) {
	    cliOutput.append("Error retrieving student data.\n");
	    e.printStackTrace();
	}

	return new Object[]{cliOutput.toString(), data, columns};
    }
    
}

/* former stuff
public class RetrieveStudents {
    private static final Logger logger = LoggerFactory.getLogger(RetrieveStudents.class);

    public static void main(String[] args) {
	String query = "SELECT * FROM students";

	try (Connection conn = DatabaseUtils.getConnection();
	     Statement stmt = conn.createStatement();
	     ResultSet rs = stmt.executeQuery(query)) {

	    System.out.printf("%-5s%-20s%-5s%-5s%n", "ID", "Name", "Age", "Note");
	    System.out.println("---------------------------------------------");
	    
	    while (rs.next()) {
		int id = rs.getInt("id");
		String name = rs.getString("name");
		int age = rs.getInt("age");
		String note = rs.getString("note");
		//System.out.printf("ID: %d, Name: %s, Age: %d, Note: %s%n", id, name, age, note);
		System.out.printf("%-5d%-20s%-5d%-5s%n", id, name, age, note);
	    }

	} catch (Exception e) {
	    logger.error("Error while retrieving students: ", e);
	}
    }
*/
    /*
    public static String retrieve() {
	String query = "SELECT * FROM students";
	StringBuilder output = new StringBuilder();

	try (Connection conn = DatabaseUtils.getConnection();
	     Statement stmt = conn.createStatement();
	     ResultSet rs = stmt.executeQuery(query)) {

	    output.append(String.format("%-5s%-20s%-5s%-5s%n", "ID", "Name", "Age", "Note"));
	    output.append("---------------------------------------------\n");

	    while (rs.next()) {
		int id = rs.getInt("id");
		String name = rs.getString("name");
		int age = rs.getInt("age");
		String note = rs.getString("note");
		output.append(String.format("%-5d%-20s%-5d%-5s%n", id, name, age, note));
	    }

	} catch (Exception e) {
	    logger.error("Error while retrieving students: ", e);
	    output.append("Error retrieving student data.\n");
	}

	return output.toString();
    }
    */
    /*
    public static String retrieve() {
	String query = "SELECT * FROM students";
	StringBuilder output = new StringBuilder();

	try (Connection conn = DatabaseUtils.getConnection();
	     Statement stmt = conn.createStatement();
	     ResultSet rs = stmt.executeQuery(query)) {

	    output.append(String.format("%-5s%-20s%-5s%-5s%n", "ID", "Name", "Age", "Note"));
	    output.append("---------------------------------------------\n");

	    while (rs.next()) {
		int id = rs.getInt("id");
		String name = rs.getString("name");
		int age = rs.getInt("age");
		String note = rs.getString("note");
		output.append(String.format("%-5d%-20s%-5d%-5s%n", id, name, age, note));
	    }

	} catch (Exception e) {
	    logger.error("Error while retrieving students: ", e);
	    output.append("Error retrieving student data.\n");
	}

	// System.out.println("Retrieved data:\n" + output.toString());  // Debug output
	return output.toString();
    }
}
    */
/*
public class RetrieveStudents {

    private static final Logger logger = LoggerFactory.getLogger(RetrieveStudents.class);

    public static void main(String[] args) {
	String url = "jdbc:mariadb://localhost:9450/school";
	String user = "root";
	String password = "newEnm898Zy@";

	String query = "SELECT id, name, age, note FROM students";

	try (Connection conn = DriverManager.getConnection(url, user, password);
	     Statement stmt = conn.createStatement();
	     ResultSet rs = stmt.executeQuery(query)) {

	    System.out.println("ID | Name            | Age | Note");
	    System.out.println("-----------------------------------");

	    while (rs.next()) {
		int id = rs.getInt("id");
		String name = rs.getString("name");
		int age = rs.getInt("age");
		String note = rs.getString("note");

		System.out.printf("%2d | %-15s | %3d | %4s\n", id, name, age, note);
	    }

	    logger.info("Data retrieved successfully!");

	} catch (Exception e) {
	    logger.error("Error while retrieving data: ", e);
	}
    }
}
*/
