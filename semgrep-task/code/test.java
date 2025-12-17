
/**
 * Purpose: Test file to demonstrate Java coding rule violations
 * Author: Test User
 * Date: 2025-12-17
 * Modified By: N/A
 */

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class test {

    // Rule Violation: Public fields (should be private)
    public String username;
    public int age;

    // Hard-coded password - SECURITY ISSUE
    private String password = "admin123";

    // Using implementation instead of interface
    public void badCollectionUsage() {
        ArrayList list = new ArrayList(); // Should use List interface
        HashMap map = new HashMap(); // Should use Map interface

        list.add("item1");
        map.put("key", "value");
    }

    // Empty catch block - ERROR
    public void poorErrorHandling() {
        
        try {
            int result = 10 / 0;
        } catch (Exception e) {
            // Empty catch block - ignoring exception
        }
    }

    // Using System.out.println instead of logger
    public void debugWithPrint() {
        System.out.println("Debug message");
        System.out.println("This should use a logging framework");
    }

    // Generic exception handling with System.out
    public void genericExceptionHandling() {
        try {
            String data = null;
            data.length();
        } catch (Exception e) {
            System.out.println(e); // Poor error handling
        }
    }

    // Function that's too long and does multiple things
    public void doEverything() {
        System.out.println("Starting process");

        ArrayList items = new ArrayList();
        items.add("item1");
        items.add("item2");

        for (int i = 0; i < items.size(); i++) {
            System.out.println(items.get(i));
        }

        try {
            Thread.sleep(1000);
        } catch (Exception e) {
            // Empty catch
        }

        HashMap config = new HashMap();
        config.put("setting1", "value1");
        config.put("setting2", "value2");

        System.out.println("Process complete");
    }

    // Duplicate code example
    public void processUserData(String userId) {
        if (userId != null) {
            System.out.println("Processing user: " + userId);
        }
    }

    public void processAdminData(String adminId) {
        if (adminId != null) {
            System.out.println("Processing user: " + adminId);
        }
    }

    // Good example - proper error handling
    public void goodErrorHandling() {
        try {
            int result = performCalculation();
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            // Proper exception handling with specific exception type
            System.err.println("Calculation error: " + e.getMessage());
            throw e;
        }
    }

    private int performCalculation() {
        return 42;
    }
}
