<?php
$conn = new mysqli("localhost", "TU_USUARIO", "TU_PASSWORD", "TU_BASE_DE_DATOS");
$conn->set_charset("utf8");

$codigo = $_GET['codigo'] ?? '';

if (!$codigo) {
    echo json_encode(["valido" => false, "error" => "Código no proporcionado"]);
    exit;
}

$sql = "SELECT nombre, mesa, personas, acceso_confirmado FROM boletos WHERE codigo_qr = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $codigo);
$stmt->execute();
$result = $stmt->get_result();

if ($row = $result->fetch_assoc()) {
    echo json_encode([
        "valido" => true,
        "nombre" => $row["nombre"],
        "mesa" => $row["mesa"],
        "personas" => $row["personas"],
        "usado" => (bool)$row["acceso_confirmado"]
    ]);
} else {
    echo json_encode(["valido" => false, "mensaje" => "Código no encontrado"]);
}
?>