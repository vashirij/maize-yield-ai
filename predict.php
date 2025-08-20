<?php
// Enable error reporting
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Sanitize and validate inputs
$district = isset($_GET['district']) ? escapeshellarg(trim($_GET['district'])) : '';
$crop = isset($_GET['crop']) ? escapeshellarg(trim($_GET['crop'])) : '';
$soil = isset($_GET['soil']) ? escapeshellarg(trim($_GET['soil'])) : '';
$area = isset($_GET['area']) ? trim($_GET['area']) : '';

if (!$district || !$crop || !$soil || !$area || !is_numeric($area)) {
    echo "<div class='alert alert-danger'>❌ Invalid input. Ensure all fields are correctly filled and area is a number.</div>";
    exit;
}

$area = floatval($area);
$escaped_area = escapeshellarg($area);

// Command to run Python script
$command = "python3 RF_predict.py $district $crop $soil $escaped_area 2>&1";

// Execute command and capture output
$output = shell_exec($command);

// Display output
if ($output) {
    echo "<div class='alert alert-success'><strong>Prediction Result:</strong><br>" . nl2br(htmlspecialchars($output)) . "</div>";
} else {
    echo "<div class='alert alert-danger'>❌ Failed to execute prediction model. Check server logs.</div>";
}
?>
