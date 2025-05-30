<?php
$conn = new mysqli("156.67.64.3", "u332392237_wedding", "Temporal2025**", "u332392237_cecijaviaccess");
$conn->set_charset("utf8");
$conn->query("SET time_zone = '-06:00'");

$codigo = $_GET['codigo'] ?? '';

if (!$codigo) {
    echo json_encode(["exito" => false, "error" => "Código no proporcionado"]);
    exit;
}

$verificar = $conn->prepare("SELECT acceso_confirmado FROM boletos WHERE codigo_qr = ?");
$verificar->bind_param("s", $codigo);
$verificar->execute();
$res = $verificar->get_result();

if ($res->num_rows === 0) {
    echo json_encode(["exito" => false, "error" => "Código no encontrado"]);
    exit;
}

$row = $res->fetch_assoc();
if ($row['acceso_confirmado']) {
    echo json_encode(["exito" => false, "mensaje" => "El boleto ya fue escaneado previamente"]);
    exit;
}

$stmt = $conn->prepare("UPDATE boletos SET acceso_confirmado = 1, fecha_entrada = NOW() WHERE codigo_qr = ?");
$stmt->bind_param("s", $codigo);
$stmt->execute();

echo json_encode(["exito" => true, "mensaje" => "Acceso registrado"]);
?>