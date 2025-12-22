/*
 * Purpose: Comprehensive test file for Java coding rules - demonstrates all 20 rules
 * Author: Harsh Patil
 * Date: 2025-12-18
 * Modified By: N/A
 */

import java.io.*;
import java.sql.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.logging.Logger;

public class JavaRulesTest {

    private static final Logger logger = Logger.getLogger(JavaRulesTest.class.getName());

    // ==========================================
    // RULE 1: Use .equals() for String Comparison
    // Why: == compares object references, not values
    // ==========================================

    // BAD: Using == for strings
    public void badStringComparison(String username) {
        if (username == "admin") { // BAD
            grantAccess();
        }
    }

    // GOOD: Using .equals()
    public void goodStringComparison(String username) {
        if (username.equals("admin")) {
            grantAccess();
        }
    }

    // ==========================================
    // RULE 2: Avoid System.out.println in Production
    // Why: Proper logging provides levels and configurability
    // ==========================================

    // BAD: Using System.out
    public void badLogging() {
        System.out.println("User logged in");
        System.err.println("Error occurred");
    }

    // GOOD: Using logger
    public void goodLogging() {
        logger.info("User logged in successfully");
        logger.severe("Error occurred");
    }

    // ==========================================
    // RULE 3: Always Handle Exceptions Properly
    // Why: Unhandled exceptions hide failures
    // ==========================================

    // BAD: Poor exception handling
    public void badExceptionHandling() {
        try {
            processFile();
        } catch (IOException e) {
            System.out.println(e); // BAD
        }
    }

    // GOOD: Proper exception handling
    public void goodExceptionHandling() {
        try {
            processFile();
        } catch (IOException e) {
            logger.severe("File processing failed: " + e.getMessage());
            throw new RuntimeException("Processing failed", e);
        }
    }

    // ==========================================
    // RULE 4: Do Not Leave Empty Catch Blocks
    // Why: Silently ignoring exceptions makes debugging impossible
    // ==========================================

    // BAD: Empty catch block
    public void badEmptyCatch() {
        try {
            connectDatabase();
        } catch (SQLException e) {
            // Empty catch - BAD
        }
    }

    // GOOD: Handling exception
    public void goodCatchHandling() {
        try {
            connectDatabase();
        } catch (SQLException e) {
            logger.severe("Database connection failed: " + e.getMessage());
        }
    }

    // ==========================================
    // RULE 5: Use Try-With-Resources
    // Why: Ensures resources are closed automatically
    // ==========================================

    // BAD: Manual resource management
    public void badResourceManagement() throws IOException {
        FileInputStream fis = new FileInputStream("data.txt");
        // Missing try-with-resources
        fis.close();
    }

    // GOOD: Try-with-resources
    public void goodResourceManagement() throws IOException {
        try (FileInputStream fis = new FileInputStream("data.txt")) {
            readData(fis);
        }
    }

    // ==========================================
    // RULE 6: Prefer Interfaces Over Implementations
    // Why: Improves flexibility and testability
    // ==========================================

    // BAD: Using concrete types
    public void badConcreteTypes() {
        ArrayList<String> names = new ArrayList<>();
        HashMap<String, Integer> ages = new HashMap<>();
        HashSet<String> tags = new HashSet<>();
    }

    // GOOD: Using interfaces
    public void goodInterfaceTypes() {
        List<String> names = new ArrayList<>();
        Map<String, Integer> ages = new HashMap<>();
        Set<String> tags = new HashSet<>();
    }

    // ==========================================
    // RULE 7: Keep Fields Private
    // Why: Encapsulation protects object integrity
    // ==========================================

    // BAD: Public fields
    public class BadUser {
        public String email;
        public int age;
    }

    // GOOD: Private fields with getters/setters
    public class GoodUser {
        private String email;
        private int age;

        public String getEmail() {
            return email;
        }

        public void setEmail(String email) {
            this.email = email;
        }
    }

    // ==========================================
    // RULE 8: Use Constants for Fixed Values
    // Why: Improves readability and maintainability
    // ==========================================

    // BAD: Magic numbers
    public void badMagicNumbers(int retryCount) {
        if (retryCount > 3) {
            stopRetry();
        }
        if (age < 18) {
            denyAccess();
        }
    }

    // GOOD: Using constants
    public static final int MAX_RETRIES = 3;
    public static final int MINIMUM_AGE = 18;

    public void goodConstants(int retryCount) {
        if (retryCount > MAX_RETRIES) {
            stopRetry();
        }
        if (age < MINIMUM_AGE) {
            denyAccess();
        }
    }

    // ==========================================
    // RULE 9: Avoid Hard-Coded Credentials
    // Why: Hard-coded secrets are a security risk
    // ==========================================

    // BAD: Hard-coded credentials
    public void badHardcodedSecrets() {
        String password = "admin123";
        String apiKey = "sk_live_1234567890";
        String dbSecret = "secretPassword";
    }

    // GOOD: Using environment variables
    public void goodEnvSecrets() {
        String password = System.getenv("DB_PASSWORD");
        String apiKey = System.getenv("API_KEY");
        String dbSecret = System.getenv("DB_SECRET");
    }

    // ==========================================
    // RULE 10: Use .equals() for Object Comparison
    // Why: Ensures correct logical comparison
    // ==========================================

    // BAD: Using == for objects
    public void badObjectComparison(User user, User adminUser) {
        if (user == adminUser) { // BAD
            allow();
        }
    }

    // GOOD: Using .equals()
    public void goodObjectComparison(User user, User adminUser) {
        if (user.equals(adminUser)) {
            allow();
        }
    }

    // ==========================================
    // RULE 11: Avoid Catching Generic Exception
    // Why: Catching specific exceptions improves clarity
    // ==========================================

    // BAD: Catching generic Exception
    public void badGenericCatch() {
        try {
            readFile();
        } catch (Exception e) { // Too generic
            logger.severe("Error: " + e.getMessage());
        }
    }

    // GOOD: Catching specific exceptions
    public void goodSpecificCatch() {
        try {
            readFile();
        } catch (FileNotFoundException e) {
            logger.severe("File not found: " + e.getMessage());
        } catch (IOException e) {
            logger.severe("IO error: " + e.getMessage());
        }
    }

    // ==========================================
    // RULE 12: Avoid Null Pointer Exceptions
    // Why: Null checks prevent runtime crashes
    // ==========================================

    // BAD: No null check
    public void badNoNullCheck(User user) {
        user.process(); // May throw NullPointerException
    }

    // GOOD: With null check
    public void goodNullCheck(User user) {
        if (user != null) {
            user.process();
        }
    }

    // ==========================================
    // RULE 13: Use Optional to Handle Absence
    // Why: Makes null handling explicit and safer
    // ==========================================

    // BAD: Returning null
    public User badReturnNull(int id) {
        if (id == 0) {
            return null;
        }
        return new User();
    }

    // GOOD: Using Optional
    public Optional<User> goodReturnOptional(int id) {
        if (id == 0) {
            return Optional.empty();
        }
        return Optional.of(new User());
    }

    // ==========================================
    // RULE 14: Avoid String Concatenation in Loops
    // Why: Improves performance and memory usage
    // ==========================================

    // BAD: String concatenation in loop
    public String badStringConcat(List<String> items) {
        String result = "";
        for (String item : items) {
            result = result + item; // BAD
        }
        return result;
    }

    // GOOD: Using StringBuilder
    public String goodStringBuilder(List<String> items) {
        StringBuilder builder = new StringBuilder();
        for (String item : items) {
            builder.append(item);
        }
        return builder.toString();
    }

    // ==========================================
    // RULE 15: Use PreparedStatement for SQL
    // Why: Prevents SQL injection attacks
    // ==========================================

    // BAD: SQL injection vulnerability
    public void badSQLInjection(Connection conn, String userId) throws SQLException {
        Statement stmt = conn.createStatement();
        stmt.execute("SELECT * FROM users WHERE id = " + userId); // BAD
    }

    // GOOD: Using PreparedStatement
    public void goodPreparedStatement(Connection conn, String userId) throws SQLException {
        PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
        stmt.setString(1, userId);
        stmt.executeQuery();
    }

    // ==========================================
    // RULE 16: Avoid Public Fields
    // Why: Preserves encapsulation and control
    // ==========================================

    // BAD: Public fields in class
    public class BadConfig {
        public String url;
        public int timeout;
    }

    // GOOD: Private fields
    public class GoodConfig {
        private String url;
        private int timeout;

        public String getUrl() {
            return url;
        }

        public int getTimeout() {
            return timeout;
        }
    }

    // ==========================================
    // RULE 17: Make Methods Small and Focused
    // Why: Improves readability and testability
    // ==========================================

    // BAD: Long method doing too much
    public void badLongMethod() {
        validateInput();
        checkPermissions();
        loadConfiguration();
        connectToDatabase();
        processData();
        saveResults();
        sendNotification();
        logActivity();
        updateMetrics();
        cleanupResources();
        archiveOldData();
        generateReport();
    }

    // GOOD: Small focused method
    public void goodSmallMethod(User user) {
        if (user == null || user.getId() == 0) {
            throw new IllegalArgumentException("Invalid user");
        }
    }

    // ==========================================
    // RULE 18: Use Immutable Objects Where Possible
    // Why: Reduces bugs and improves thread safety
    // ==========================================

    // BAD: Mutable class
    public class BadMutableConfig {
        private String url;

        public void setUrl(String url) {
            this.url = url;
        }
    }

    // GOOD: Immutable class
    public final class GoodImmutableConfig {
        private final String url;

        public GoodImmutableConfig(String url) {
            this.url = url;
        }

        public String getUrl() {
            return url;
        }
    }

    // ==========================================
    // RULE 19: Avoid Thread.sleep() in Loops
    // Why: Leads to inefficient scheduling
    // ==========================================

    // BAD: Thread.sleep in loop
    public void badSleepInLoop() throws InterruptedException {
        while (true) {
            Thread.sleep(1000); // BAD
            process();
        }
    }

    // GOOD: Using ScheduledExecutorService
    public void goodScheduledExecutor() {
        ScheduledExecutorService scheduler = Executors.newSingleThreadScheduledExecutor();
        scheduler.scheduleAtFixedRate(this::process, 0, 1, TimeUnit.SECONDS);
    }

    // ==========================================
    // RULE 20: Follow Java Naming Conventions
    // Why: Ensures consistency and readability
    // ==========================================

    // GOOD: Proper naming conventions
    public class UserService { // PascalCase for classes
        private static final int MAX_SIZE = 100; // UPPER_CASE for constants
        private String userName; // camelCase for fields

        public void processUser() { // camelCase for methods
            // Implementation
        }
    }

    // Helper methods and classes
    private void grantAccess() {
    }

    private void denyAccess() {
    }

    private void processFile() throws IOException {
    }

    private void connectDatabase() throws SQLException {
    }

    private void readData(InputStream is) {
    }

    private void stopRetry() {
    }

    private void allow() {
    }

    private void readFile() throws IOException {
    }

    private void validateInput() {
    }

    private void checkPermissions() {
    }

    private void loadConfiguration() {
    }

    private void connectToDatabase() {
    }

    private void processData() {
    }

    private void saveResults() {
    }

    private void sendNotification() {
    }

    private void logActivity() {
    }

    private void updateMetrics() {
    }

    private void cleanupResources() {
    }

    private void archiveOldData() {
    }

    private void generateReport() {
    }

    private void process() {
    }

    private int age = 20;

    // Mock User class
    static class User {
        private int id;

        public int getId() {
            return id;
        }

        public void process() {
        }
    }
}
