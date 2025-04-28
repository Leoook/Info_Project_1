import java.util.Random;

public class Main {
    public static void main(String[] args) {
        int[] randomArray = generateRandomArray(10, 1, 100); // Array of size 10 with values between 1 and 100
        printArray(randomArray);
    }

    public static int[] generateRandomArray(int size, int min, int max) {
        Random random = new Random();
        int[] array = new int[size];
        for (int i = 0; i < size; i++) {
            array[i] = random.nextInt(max - min + 1) + min;
        }
        return array;
    }

    public static void printArray(int[] array) {
        System.out.print("Random Array: ");
        for (int num : array) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}