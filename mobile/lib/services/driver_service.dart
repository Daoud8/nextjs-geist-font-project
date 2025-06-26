import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auth_service.dart';

class DriverService {
  static const _baseUrl = 'http://localhost:8000'; // Change to your backend URL

  static Future<bool> registerDriver({
    required String cin,
    required String license,
    required String vehicleRegistration,
    required String vehiclePhotoUrl,
    required String insurance,
  }) async {
    final token = await AuthService.getToken();
    if (token == null) return false;

    final response = await http.post(
      Uri.parse('$_baseUrl/driver/register'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({
        'cin': cin,
        'license': license,
        'vehicle_registration': vehicleRegistration,
        'vehicle_photo': vehiclePhotoUrl,
        'insurance': insurance,
      }),
    );

    return response.statusCode == 200;
  }

  static Future<bool> setOnlineStatus(bool isOnline) async {
    final token = await AuthService.getToken();
    if (token == null) return false;

    final response = await http.post(
      Uri.parse('$_baseUrl/driver/status'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({'is_online': isOnline}),
    );

    return response.statusCode == 200;
  }
}
