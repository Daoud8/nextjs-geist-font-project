import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'screens/passenger_home.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(DjibRideApp());
}

class DjibRideApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DjibRide',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: PassengerHomeScreen(),
    );
  }
}
