package lf8;

import java.sql.Connection;
import java.sql.PreparedStatement;

public class InsertData {
    public static String insert(String name, int age, String note) {
	String sql = "INSERT INTO students (name, age, note) VALUES (?, ?, ?)";

	try (Connection conn = DatabaseUtils.getConnection();
	     PreparedStatement pstmt = conn.prepareStatement(sql)) {

	    pstmt.setString(1, name);
	    pstmt.setInt(2, age);
	    pstmt.setString(3, note);

	    int rowsInserted = pstmt.executeUpdate();
	    if (rowsInserted > 0) {
		return "New student entry added successfully.";
	    } else {
		return "Failed to add new student entry.";
	    }

	} catch (Exception e) {
	    e.printStackTrace();
	    return "Error occurred while adding new entry.";
	}
    }
}
