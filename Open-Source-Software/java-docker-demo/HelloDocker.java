public class HelloDocker {
    public static void main(String[] args) {

        System.out.println("================================");
        System.out.println(" Java Application Using Docker ");
        System.out.println("================================");

        System.out.println("Hello from Ubuntu Docker Container!");

        int a = 20;
        int b = 10;

        System.out.println("First Number: " + a);
        System.out.println("Second Number: " + b);

        System.out.println("Addition: " + (a + b));
        System.out.println("Subtraction: " + (a - b));
        System.out.println("Multiplication: " + (a * b));
        System.out.println("Division: " + (a / b));

        System.out.println("Java application executed successfully.");
    }
}
