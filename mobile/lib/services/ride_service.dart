import 'dart:convert';
import 'package:http/http.dart' as http;
import 'auth_service.dart';
import '../models/location.dart';

class RideService {
  static const _baseUrl = 'http://localhost:8000'; // Change to your backend URL

  static Future<bool> requestRide({
    required Location pickup,
    required Location dropoff,
    required String serviceType,
  }) async {
    final token = await AuthService.getToken();
    if (token == null) return false;

    final response = await http.post(
      Uri.parse('$_baseUrl/rides/'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({
        'pickup_location': {
          'lat': pickup.lat,
          'lng': pickup.lng,
          'address': pickup.address,
        },
        'dropoff_location': {
          'lat': dropoff.lat,
          'lng': dropoff.lng,
          'address': dropoff.address,
        },
        'service_type': serviceType,
      }),
    );

    return response.statusCode == 200;
  }
}
