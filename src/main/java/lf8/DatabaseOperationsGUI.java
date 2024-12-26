package lf8;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.table.DefaultTableModel;
import java.util.List;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class DatabaseOperationsGUI {

    // The main frame of the GUI
    private JFrame frame;
    private JTable table;

    // Flag to check if we are in GUI mode or CLI mode
    private static boolean useGui = true;  // Set this flag depending on your needs

    public static void main(String[] args) {
	// Check if running in GUI or CLI mode
	useGui = !System.getProperty("os.name").toLowerCase().contains("headless");

	if (useGui) {
	    // Run GUI version if GUI is available
	    SwingUtilities.invokeLater(() -> {
		    try {
			DatabaseOperationsGUI window = new DatabaseOperationsGUI();
			window.frame.setVisible(true);
		    } catch (Exception e) {
			e.printStackTrace();
		    }
		});
	} else {
	    // Fallback to CLI version if GUI is unavailable
	    Object[] result = RetrieveStudents.retrieve();
	    String cliOutput = (String) result[0];
	    System.out.println(cliOutput); // Print to the CLI
	}
    }

    public DatabaseOperationsGUI() {
	initialize();
    }

    private void initialize() {
	if (useGui) {
	    // Initialize the frame
	    frame = new JFrame();
	    frame.setBounds(100, 100, 600, 400);
	    frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
	    frame.getContentPane().setLayout(new BorderLayout());

	    // Create buttons for operations
	    JPanel panel = new JPanel(new GridLayout(1,5)); // 5 Buttons in a row
	    frame.getContentPane().add(panel, BorderLayout.NORTH);

	    JButton btnCreateDatabase = new JButton("Create Database");
	    JButton btnInsertData = new JButton("Insert Test Data");
	    JButton btnRetrieveData = new JButton("Retrieve Data");
	    // Add the "New Entry" button in the GUI
	    JButton btnNewEntry = new JButton("New Entry");
	    JButton btnDeleteEntries = new JButton("Delete Entries");
	    
	    panel.add(btnCreateDatabase);
	    panel.add(btnInsertData);
	    panel.add(btnRetrieveData);
	    panel.add(btnNewEntry);
	    panel.add(btnDeleteEntries);

	    // Create a DefaultTableModel to hold the table data
	    DefaultTableModel model = new DefaultTableModel();
	    model.addColumn("ID");
	    model.addColumn("Name");
	    model.addColumn("Age");
	    model.addColumn("Note");

	    // Create a JTable with the model
	    table = new JTable(model);
	    JScrollPane scrollPane = new JScrollPane(table);
	    frame.getContentPane().add(scrollPane, BorderLayout.CENTER);  // Add table to the center

	    // Action listeners for buttons
	    btnCreateDatabase.addActionListener(new ActionListener() {
		    public void actionPerformed(ActionEvent e) {
			String output = CreateDatabase.create();
			JOptionPane.showMessageDialog(frame, output);
		    }
		});

	    btnInsertData.addActionListener(new ActionListener() {
		    public void actionPerformed(ActionEvent e) {
			String output = InsertTestData.insert();
			JOptionPane.showMessageDialog(frame, output);
		    }
		});

	    btnRetrieveData.addActionListener(new ActionListener() {
		    public void actionPerformed(ActionEvent e) {
			// Retrieve data
			Object[] result = RetrieveStudents.retrieve();
			String cliOutput = (String) result[0];  // Get formatted CLI output
			List<Object[]> retrievedData = (List<Object[]>) result[1];
			String[] columns = (String[]) result[2];

			// Update JTable with retrieved data
			DefaultTableModel model = (DefaultTableModel) table.getModel();
			model.setColumnIdentifiers(columns);
			model.setRowCount(0);  // Clear previous data
			retrievedData.forEach(model::addRow);

			// Display CLI output in a dialog
			JTextArea textArea = new JTextArea(cliOutput);
			textArea.setEditable(false);
			textArea.setFont(new Font("Monospaced", Font.PLAIN, 12)); // Monospaced font for alignment
			JScrollPane scrollPane = new JScrollPane(textArea);
			JOptionPane.showMessageDialog(frame, scrollPane, "Retrieved Data (CLI Format)", JOptionPane.INFORMATION_MESSAGE);
		    }
		});
	    
	    // Action listener for the "New Entry" button
	    btnNewEntry.addActionListener(new ActionListener() {
		    public void actionPerformed(ActionEvent e) {
			// Prompt the user for input
			JTextField nameField = new JTextField();
			JTextField ageField = new JTextField();
			JTextField noteField = new JTextField();
			JComboBox<String> columnDropdown = new JComboBox<>(new String[]{"id", "name", "age", "note"});

			// Create a panel for input fields
			JPanel inputPanel = new JPanel(new GridLayout(3, 2));
			inputPanel.add(new JLabel("Name:"));
			inputPanel.add(nameField);
			inputPanel.add(new JLabel("Age:"));
			inputPanel.add(ageField);
			inputPanel.add(new JLabel("Note:"));
			inputPanel.add(noteField);
			inputPanel.add(new JLabel("Column Name:"));
			inputPanel.add(columnDropdown);

			int result = JOptionPane.showConfirmDialog(frame, inputPanel,
								   "Enter New Student Data", JOptionPane.OK_CANCEL_OPTION);

			if (result == JOptionPane.OK_OPTION) {
			    String name = nameField.getText().trim();
			    String ageText = ageField.getText().trim();
			    String note = noteField.getText().trim();

			    // Validate inputs
			    if (name.isEmpty() || ageText.isEmpty()) {
				JOptionPane.showMessageDialog(frame, "Name and Age are required.",
							      "Input Error", JOptionPane.ERROR_MESSAGE);
				return;
			    }

			    try {
				int age = Integer.parseInt(ageText);  // Validate age as an integer

				// Call the insert method
				String output = InsertData.insert(name, age, note);
				JOptionPane.showMessageDialog(frame, output);
			    } catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(frame, "Age must be a valid number.",
							      "Input Error", JOptionPane.ERROR_MESSAGE);
			    }
			}
		    }
		});

	    // Action listener for the "Delete Entries" button
	    btnDeleteEntries.addActionListener(new ActionListener() {
		    public void actionPerformed(ActionEvent e) {
			// Prompt the user to choose delete method
			Object[] options = {"Delete By Column", "Delete All Entries"};
			int choice = JOptionPane.showOptionDialog(frame,
								  "Select delete method:",
								  "Delete Entries",
								  JOptionPane.DEFAULT_OPTION,
								  JOptionPane.QUESTION_MESSAGE,
								  null,
								  options,
								  options[0]);

			if (choice == 0) {
			    // Delete by column
			    deleteByColumn();
			    refreshTable();
			} else if (choice == 1) {
			    // Delete all entries
			    int confirm = JOptionPane.showConfirmDialog(frame,
									"Are you sure you want to delete all entries?",
									"Confirm Delete",
									JOptionPane.YES_NO_OPTION);

			    if (confirm == JOptionPane.YES_OPTION) {
				deleteAll();
				refreshTable();
			    }
			}
		    }
		});
	}
    }

    private void deleteByColumn() {
	// Define input fields
	JTextField columnField = new JTextField();
	JTextField valueField = new JTextField();

	JPanel inputPanel = new JPanel(new GridLayout(2, 2));
	inputPanel.add(new JLabel("Column Name (id, name, age, note):"));
	inputPanel.add(columnField);
	inputPanel.add(new JLabel("Value:"));
	inputPanel.add(valueField);

	int result = JOptionPane.showConfirmDialog(frame, inputPanel,
						   "Delete by Column", JOptionPane.OK_CANCEL_OPTION);

	if (result == JOptionPane.OK_OPTION) {
	    String columnName = columnField.getText().trim();
	    String value = valueField.getText().trim();

	    // Validate column name
	    String[] validColumns = {"id", "name", "age", "note"};
	    boolean isValidColumn = false;
	    for (String validColumn : validColumns) {
		if (validColumn.equalsIgnoreCase(columnName)) {
		    columnName = validColumn; // Ensure exact match
		    isValidColumn = true;
		    break;
		}
	    }

	    if (!isValidColumn) {
		JOptionPane.showMessageDialog(frame, "Invalid column name. Operation aborted.",
					      "Input Error", JOptionPane.ERROR_MESSAGE);
		return;
	    }

	    // Perform deletion
	    String sql = "DELETE FROM students WHERE " + columnName + " = ?";

	    try (Connection conn = DatabaseUtils.getConnection();
		 PreparedStatement pstmt = conn.prepareStatement(sql)) {

		pstmt.setString(1, value);
		int affectedRows = pstmt.executeUpdate();

		JOptionPane.showMessageDialog(frame,
					      affectedRows + " entries deleted where " + columnName + " = " + value,
					      "Success", JOptionPane.INFORMATION_MESSAGE);

	    } catch (Exception ex) {
		JOptionPane.showMessageDialog(frame,
					      "Error occurred while deleting entries: " + ex.getMessage(),
					      "Error", JOptionPane.ERROR_MESSAGE);
	    }
	}
    }

    private void deleteAll() {
	String sql = "DELETE FROM students";

	try (Connection conn = DatabaseUtils.getConnection();
	     PreparedStatement pstmt = conn.prepareStatement(sql)) {

	    int affectedRows = pstmt.executeUpdate();

	    JOptionPane.showMessageDialog(frame,
					  "Successfully deleted all " + affectedRows + " entries from the database.",
					  "Success", JOptionPane.INFORMATION_MESSAGE);

	} catch (Exception ex) {
	    JOptionPane.showMessageDialog(frame,
					  "Error occurred while deleting all entries: " + ex.getMessage(),
					  "Error", JOptionPane.ERROR_MESSAGE);
	}
    }

    private void refreshTable() {
	Object[] result = RetrieveStudents.retrieve();
	String[] columns = (String[]) result[2];
	List<Object[]> retrievedData = (List<Object[]>) result[1];
	DefaultTableModel model = (DefaultTableModel) table.getModel();
	model.setColumnIdentifiers(columns);
	model.setRowCount(0);  // Clear previous data
	retrievedData.forEach(model::addRow);
    }
    
}
