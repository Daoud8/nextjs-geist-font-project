import 'package:flutter/material.dart';
import '../services/driver_service.dart';

class DriverRegistrationScreen extends StatefulWidget {
  @override
  _DriverRegistrationScreenState createState() => _DriverRegistrationScreenState();
}

class _DriverRegistrationScreenState extends State<DriverRegistrationScreen> {
  final _formKey = GlobalKey<FormState>();
  String? _cin;
  String? _license;
  String? _vehicleRegistration;
  String? _vehiclePhotoUrl;
  String? _insurance;

  bool _loading = false;
  String? _error;

  void _submit() async {
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      bool success = await DriverService.registerDriver(
        cin: _cin!,
        license: _license!,
        vehicleRegistration: _vehicleRegistration!,
        vehiclePhotoUrl: _vehiclePhotoUrl!,
        insurance: _insurance!,
      );
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Inscription réussie')));
        Navigator.pop(context);
      } else {
        setState(() {
          _error = 'Échec de l\'inscription';
        });
      }
    } catch (e) {
      setState(() {
        _error = 'Erreur: $e';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Inscription Chauffeur'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              if (_error != null)
                Text(_error!, style: TextStyle(color: Colors.red)),
              TextFormField(
                decoration: InputDecoration(labelText: 'CIN'),
                onSaved: (value) => _cin = value,
                validator: (value) => value == null || value.isEmpty ? 'Champ requis' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Permis'),
                onSaved: (value) => _license = value,
                validator: (value) => value == null || value.isEmpty ? 'Champ requis' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Immatriculation véhicule'),
                onSaved: (value) => _vehicleRegistration = value,
                validator: (value) => value == null || value.isEmpty ? 'Champ requis' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Photo véhicule URL'),
                onSaved: (value) => _vehiclePhotoUrl = value,
                validator: (value) => value == null || value.isEmpty ? 'Champ requis' : null,
              ),
              TextFormField(
                decoration: InputDecoration(labelText: 'Assurance'),
                onSaved: (value) => _insurance = value,
                validator: (value) => value == null || value.isEmpty ? 'Champ requis' : null,
              ),
              SizedBox(height: 20),
              _loading
                  ? Center(child: CircularProgressIndicator())
                  : ElevatedButton(
                      onPressed: _submit,
                      child: Text('S\'inscrire'),
                    ),
            ],
          ),
        ),
      ),
    );
  }
}
