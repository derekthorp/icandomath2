import java.util.*;
import java.io.*;

public class Display {
    public static final String r = "🏃";
    public static final String t = "⛳️";
    public static final String c = "🟩";
    public static final String e = "🏁";
    public static final int NUM_BLOCKS = 100;
    public static final int DISTANCE = 1000;

    public static void main (String[] args) throws FileNotFoundException {
        Scanner s = new Scanner(new File("runs.txt"));
        double totalDec;
        int truncatedDec;

        // from the runs.txt file, add up the distance in every row and capture it in totalDec
        totalDec = makeTotal(s);
        System.out.println("Total Mileage: " + totalDec + " out of " + DISTANCE);

        // cast as an int
        truncatedDec = (int) totalDec;

        // prints out the visual display as a percentage of the whole
        printProgress(truncatedDec);
    }

    // Scanner input adds up total distance of doubles in runs.txt
    public static double makeTotal(Scanner s) {
        double total = 0;

        while (s.hasNextDouble()) {
            total += s.nextDouble();
        }

        return total;
    }

    // Print the visual to make it look nice
    public static void printProgress(int truncatedDec) {
        if (truncatedDec >= DISTANCE) {
            System.out.println("DONE!" + " " + e + r + e);
        } else {
            int blockSize = DISTANCE / NUM_BLOCKS;
            int blocksCompleted = truncatedDec / blockSize;

            System.out.print(e);
            
            for (int i = 0; i < NUM_BLOCKS - blocksCompleted; i++) {
                System.out.print(t);
            }

            System.out.print(r);

            for (int i = 0; i < blocksCompleted; i++) {
                System.out.print(c);
            }
        }
        return;
    }
}
