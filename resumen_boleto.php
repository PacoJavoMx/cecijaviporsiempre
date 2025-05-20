<?php
$mysqli = new mmysqli("156.67.64.3", "u332392237_wedding", "Temporal2025**", "u332392237_cecijaviaccess");
$mysqli->set_charset("utf8");

$query = "SELECT codigo_qr, nombre, mesa, personas, acceso_confirmado, fecha_entrada FROM boletos ORDER BY mesa, nombre";
$result = $mysqli->query($query);

$data = [];
while ($row = $result->fetch_assoc()) {
    $data[] = $row;
}
echo json_encode($data);
?>