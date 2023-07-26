import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

public class words_2 {
    private static final ArrayList<String> cities = new ArrayList<>();
    private static final Scanner scanner = new Scanner(System.in);
    public static void main(String [] args) {
        fillCities();
        gameLoop();
    }

    private static void gameLoop() {
        String lastCompCity = null;

        while (true) {

            String input = scanner.nextLine();

            if (input.equals("exit")) {
                System.out.println("Дякую за гру!\nТепер ви краще знаєте міста України.");
                System.exit(0);
            }
// Check if a user-entered city is in the list
            boolean isCorrectCity = false;
            for (String city: cities) {
                if(city.equalsIgnoreCase(input)) {
                    isCorrectCity = true;
                    break;
                }
            }
            if (!isCorrectCity) {
                System.out.println("Такого міста немає в базі даних. Введіть інше.");
                continue;
            }

// Checking whether the city name is entered from the correct letter
            if (lastCompCity != null) {
                char lastCompCityChar = lastCompCity.charAt(lastCompCity.length() - 1);
                char firstInputChar = input.charAt(0);

                if (Character.toLowerCase(firstInputChar) != Character.toLowerCase(lastCompCityChar)) {
                    System.out.println("Назва міста повинна починатися з літери “"
                            + Character.toUpperCase(lastCompCityChar) + "”");
                    continue;
                }
            }
            char lastChar = input.charAt(input.length() - 1);
            lastCompCity = getRandomCity(lastChar);
            System.out.println("Моє місто: " + lastCompCity);
        }
    }

    private static String getRandomCity(char firstChar) {
        List<String> properCities = new ArrayList<>();
        for (String city: cities) {
            if (Character.toLowerCase(city.charAt(0)) == Character.toLowerCase(firstChar)) {
                properCities.add(city);
            }
        }
        Random random = new Random();
        int index = random.nextInt(properCities.size());
        return properCities.get(index);
    }

    private static void fillCities() {
        try (BufferedReader br = new BufferedReader(new FileReader("cities.dat"))) {
            String line;
            while ((line = br.readLine()) != null) {
                cities.add(line.trim());
            }
        }
        catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
