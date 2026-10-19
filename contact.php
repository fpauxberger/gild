<?php
// Stores contact-form submissions in contacts.txt (CSV). Works on any web host with PHP:
// nothing has to be started manually. Upload the whole site folder and make it writable.
header('Content-Type: application/json');
header('Cache-Control: no-store');

function fail($code) { http_response_code($code); echo '{"ok":false}'; exit; }
function clean($v, $n) {
    $v = mb_substr(trim((string)($v ?? '')), 0, $n);
    // Neutralise spreadsheet formula injection
    return ($v !== '' && strpos('=+-@', $v[0]) !== false) ? "'" . $v : $v;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') fail(405);
$raw = file_get_contents('php://input', false, null, 0, 10001);
if ($raw === false || strlen($raw) > 10000) fail(400);
$d = json_decode($raw, true);
if (!is_array($d)) fail(400);

$limits = ['name' => 100, 'email' => 150, 'phone' => 40, 'company' => 120, 'product' => 120, 'message' => 2000];
$row = [];
foreach ($limits as $k => $n) $row[$k] = clean($d[$k] ?? '', $n);
if ($row['name'] === '' || strpos($row['email'], '@') === false || $row['message'] === '') fail(400);

$file = __DIR__ . '/contacts.txt';
$isNew = !file_exists($file);
$fh = @fopen($file, 'a');
if (!$fh) fail(500);
flock($fh, LOCK_EX);
if ($isNew) fputcsv($fh, ['timestamp_utc', 'name', 'email', 'phone', 'company', 'product_interest', 'message'], ',', '"', '');
fputcsv($fh, [gmdate('Y-m-d\TH:i:sP'), $row['name'], $row['email'], $row['phone'], $row['company'], $row['product'], $row['message']], ',', '"', '');
flock($fh, LOCK_UN);
fclose($fh);
echo '{"ok":true}';
