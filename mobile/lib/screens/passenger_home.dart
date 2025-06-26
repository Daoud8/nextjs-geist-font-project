import 'package:flutter/material.dart';

class PassengerHomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('DjibRide - Passager'),
      ),
      body: Center(
        child: Text(
          'Bienvenue sur DjibRide Passager',
          style: TextStyle(fontSize: 24),
        ),
      ),
    );
  }
}
