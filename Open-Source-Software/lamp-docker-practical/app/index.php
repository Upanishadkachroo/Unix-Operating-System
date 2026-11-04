
<?php
$host = getenv('DB_HOST') ?: 'db';
$db   = getenv('MYSQL_DATABASE') ?: 'studentdb';
$user = getenv('MYSQL_USER') ?: 'studentuser';
$pass = getenv('MYSQL_PASSWORD');

try {
    $pdo = new PDO(
        "mysql:host=$host;dbname=$db;charset=utf8mb4",
        $user,
        $pass,
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );

    // Create the table if it does not exist.
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS students (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) NOT NULL,
            course VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ");

    // Insert a new student.
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $name = trim($_POST['name'] ?? '');
        $email = trim($_POST['email'] ?? '');
        $course = trim($_POST['course'] ?? '');

        if ($name !== '' && filter_var($email, FILTER_VALIDATE_EMAIL)
            && $course !== '') {
            $stmt = $pdo->prepare(
                "INSERT INTO students (name, email, course)
                 VALUES (?, ?, ?)"
            );
            $stmt->execute([$name, $email, $course]);

            header("Location: index.php");
            exit;
        }
    }

    $students = $pdo->query(
        "SELECT * FROM students ORDER BY id DESC"
    )->fetchAll(PDO::FETCH_ASSOC);

} catch (PDOException $e) {
    die("Database connection failed: " .
        htmlspecialchars($e->getMessage()));
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Record Management</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f4f8;
            margin: 40px;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
        }
        input {
            padding: 10px;
            margin: 5px;
        }
        button {
            padding: 10px 18px;
            background: #1769aa;
            color: white;
            border: none;
            cursor: pointer;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 25px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background: #1769aa;
            color: white;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Student Record Management System</h1>
    <p>Powered by Docker, Apache, PHP and MySQL.</p>

    <h2>Add Student</h2>

    <form method="POST">
        <input type="text" name="name"
               placeholder="Student Name" required>

        <input type="email" name="email"
               placeholder="Email" required>

        <input type="text" name="course"
               placeholder="Course" required>

        <button type="submit">Add Student</button>
    </form>

    <h2>Student Records</h2>

    <table>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Course</th>
        </tr>

        <?php foreach ($students as $student): ?>
        <tr>
            <td><?= htmlspecialchars($student['id']) ?></td>
            <td><?= htmlspecialchars($student['name']) ?></td>
            <td><?= htmlspecialchars($student['email']) ?></td>
            <td><?= htmlspecialchars($student['course']) ?></td>
        </tr>
        <?php endforeach; ?>
    </table>
</div>
</body>
</html>
