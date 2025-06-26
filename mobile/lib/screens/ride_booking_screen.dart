import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import '../services/ride_service.dart';
import '../models/location.dart';

class RideBookingScreen extends StatefulWidget {
  @override
  _RideBookingScreenState createState() => _RideBookingScreenState();
}

class _RideBookingScreenState extends State<RideBookingScreen> {
  final _pickupController = TextEditingController();
  final _dropoffController = TextEditingController();
  String _selectedService = 'taxi';
  double _estimatedFare = 0.0;
  LatLng? _pickupLatLng;
  LatLng? _dropoffLatLng;
  GoogleMapController? _mapController;

  final List<String> _services = [
    'taxi',
    'carpool',
    'parcel_delivery',
    'food_delivery',
    'supermarket_delivery',
    'custom_order',
  ];

  void _onMapCreated(GoogleMapController controller) {
    _mapController = controller;
  }

  void _estimateFare() {
    // Placeholder: estimate fare based on distance between pickup and dropoff
    if (_pickupLatLng != null && _dropoffLatLng != null) {
      final distance = _calculateDistance(_pickupLatLng!, _dropoffLatLng!);
      setState(() {
        _estimatedFare = 50 + 150 * distance; // base + per km
      });
    }
  }

  double _calculateDistance(LatLng start, LatLng end) {
    // Simple haversine formula or placeholder
    const double R = 6371; // Earth radius in km
    final dLat = _deg2rad(end.latitude - start.latitude);
    final dLon = _deg2rad(end.longitude - start.longitude);
    final a = 
      (sin(dLat/2) * sin(dLat/2)) +
      cos(_deg2rad(start.latitude)) * cos(_deg2rad(end.latitude)) *
      (sin(dLon/2) * sin(dLon/2));
    final c = 2 * atan2(sqrt(a), sqrt(1-a));
    final distance = R * c;
    return distance;
  }

  double _deg2rad(double deg) {
    return deg * (3.141592653589793 / 180);
  }

  void _requestRide() async {
    if (_pickupLatLng == null || _dropoffLatLng == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Please select pickup and dropoff locations')));
      return;
    }
    final success = await RideService.requestRide(
      pickup: Location(lat: _pickupLatLng!.latitude, lng: _pickupLatLng!.longitude, address: _pickupController.text),
      dropoff: Location(lat: _dropoffLatLng!.latitude, lng: _dropoffLatLng!.longitude, address: _dropoffController.text),
      serviceType: _selectedService,
    );
    if (success) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Ride requested successfully')));
      Navigator.pop(context);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to request ride')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Réserver une course'),
      ),
      body: Column(
        children: [
          TextField(
            controller: _pickupController,
            decoration: InputDecoration(labelText: 'Lieu de prise en charge'),
            onChanged: (value) {
              // TODO: Geocode address to LatLng
            },
          ),
          TextField(
            controller: _dropoffController,
            decoration: InputDecoration(labelText: 'Destination'),
            onChanged: (value) {
              // TODO: Geocode address to LatLng
            },
          ),
          DropdownButton<String>(
            value: _selectedService,
            items: _services.map((service) {
              return DropdownMenuItem(
                value: service,
                child: Text(service),
              );
            }).toList(),
            onChanged: (value) {
              setState(() {
                _selectedService = value!;
                _estimateFare();
              });
            },
          ),
          Text('Tarif estimé: $_estimatedFare DJF'),
          ElevatedButton(
            onPressed: _requestRide,
            child: Text('Demander la course'),
          ),
          Expanded(
            child: GoogleMap(
              onMapCreated: _onMapCreated,
              initialCameraPosition: CameraPosition(
                target: LatLng(11.5721, 43.1456), // Djibouti city center
                zoom: 12,
              ),
              markers: {
                if (_pickupLatLng != null) Marker(markerId: MarkerId('pickup'), position: _pickupLatLng!),
                if (_dropoffLatLng != null) Marker(markerId: MarkerId('dropoff'), position: _dropoffLatLng!),
              },
            ),
          ),
        ],
      ),
    );
  }
}
