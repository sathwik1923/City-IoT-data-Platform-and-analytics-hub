<?php
ini_set('log_errors', 1);
ini_set('error_log', '/tmp/php-error.log');
error_reporting(E_ALL);


$host = 'projectdb19.cjmiqqig0kbt.us-east-1.rds.amazonaws.com';
$dbname = 'projectdb';
$username = 'admin';
$password = 'saisindhu2005';


$conn = new mysqli($host, $username, $password, $dbname);

if ($conn->connect_error) {
    error_log("Connection failed: " . $conn->connect_error);
    header('Content-Type: application/json');
    echo json_encode(['error' => 'Database connection failed']);
    http_response_code(500);
    exit;
}


function handleRequest() {
    global $conn;

    
    $passkey = isset($_GET['passkey']) ? $_GET['passkey'] : '';
    $table = isset($_GET['table']) ? $_GET['table'] : '';

    
    if ($passkey !== 'sathwik23') {
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Invalid passkey']);
        http_response_code(403);
        return;
    }

    
    if (empty($table)) {
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Table name is required']);
        http_response_code(400);
        return;
    }

    
    $validTables = ['air_quality', 'traffic_flow','energy_consumption','waste management']; 
    if (!in_array($table, $validTables)) {
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Invalid table name']);
        http_response_code(400);
        return;
    }

    
    $table = $conn->real_escape_string($table);

    
    $result = $conn->query("SHOW TABLES LIKE '$table'");
    if ($result->num_rows == 0) {
        header('Content-Type: application/json');
        echo json_encode(['error' => 'Table does not exist']);
        http_response_code(400);
        return;
    }

   
    $sql = "SELECT * FROM $table";
    $result = $conn->query($sql);

    if ($result === FALSE) {
        error_log("SQL error: " . $conn->error);
        header('Content-Type: application/json');
        echo json_encode(['error' => 'SQL error occurred']);
        http_response_code(500);
        return;
    }

    $output = [];
    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $output[] = $row;
        }
    }

    
    header('Content-Type: application/json');
    echo json_encode($output);
}
handleRequest();


$conn->close();
?>
