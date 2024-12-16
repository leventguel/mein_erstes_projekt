package lf8;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.util.Scanner;

public class DeleteEntries {

    private static final Logger logger = LoggerFactory.getLogger(DeleteEntries.class);

    public static void main(String[] args) {
	Scanner scanner = new Scanner(System.in);

	System.out.println("Choose an option:");
	System.out.println("1. Delete specific entry by column value");
	System.out.println("2. Delete all entries");
	int choice = scanner.nextInt();
	scanner.nextLine(); // Consume newline

	switch (choice) {
	case 1 -> { deleteByColumn(scanner); }
	case 2 -> { deleteAll(); }
	default -> System.out.println("Invalid choice.");
	}
	scanner.close();
    }

    private static void deleteByColumn(Scanner scanner) {
	// Define a whitelist of valid column names
	String[] validColumns = {"id", "name", "age", "note"};
	System.out.println("Enter column name (e.g., id, name, age, note):");
	String columnName = scanner.nextLine();

	// Validate the column name
	boolean isValidColumn = false;
	for (String validColumn : validColumns) {
	    if (validColumn.equalsIgnoreCase(columnName)) {
		columnName = validColumn; // Match to the exact case in the database schema
		isValidColumn = true;
		break;
	    }
	}

	if (!isValidColumn) {
	    System.out.println("Invalid column name. Operation aborted.");
	    logger.warn("Attempted to delete using an invalid column name: {}", columnName);
	    return;
	}

	System.out.println("Enter value to match:");
	String value = scanner.nextLine();

	String sql = "DELETE FROM students WHERE " + columnName + " = ?";

	try (Connection conn = DatabaseUtils.getConnection();
	     PreparedStatement pstmt = conn.prepareStatement(sql)) {

	    pstmt.setString(1, value);
	    int affectedRows = pstmt.executeUpdate();

	    if (affectedRows > 0) {
		logger.info("Successfully deleted {} entries where {} = {}", affectedRows, columnName, value);
	    } else {
		logger.info("No entries found matching {} = {}", columnName, value);
	    }

	} catch (Exception e) {
	    logger.error("Error while deleting entries by column: ", e);
	}
    }

    private static void deleteAll() {
	String sql = "DELETE FROM students";

	try (Connection conn = DatabaseUtils.getConnection();
	     PreparedStatement pstmt = conn.prepareStatement(sql)) {

	    int affectedRows = pstmt.executeUpdate();

	    logger.info("Successfully deleted all {} entries from the database.", affectedRows);

	} catch (Exception e) {
	    logger.error("Error while deleting all entries: ", e);
	}
    }

}
